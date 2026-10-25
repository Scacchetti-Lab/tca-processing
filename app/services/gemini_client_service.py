import asyncio
from time import sleep
from os import getenv as __getenv
from traceback import format_exc
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from google.genai.interactions import Interaction
from google.genai.errors import ClientError
from app.helpers.contexts.predict_client import build_client_prediction_instruction
from app.helpers.contexts.predict_meeting import build_meeting_prediction_instruction
from app.types.chats_models import ChatBotResponse as _ChatBotResponse, ChatBotFirstResponse as _ChatBotFirstResponse
from app.types.transcripts_models import TranscriptAnalyse, TranscriptPayload
from app.types.response_model import ResponseModel
from fastapi import status

from app.helpers.contexts.transcript_context import build_extraction_system_instruction

__load_dotenv()

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)


async def analyse_transcript(payload: TranscriptPayload | str, tries: int = 3) -> ResponseModel:
    if isinstance(payload, str):
        payload = TranscriptPayload(transcript=payload, scope="EXTERNAL")

    for i in range(tries):
        try:
            transcript_analysed = await _create_transcript_interactor(payload)
            return ResponseModel(
                status=status.HTTP_200_OK,
                content=transcript_analysed.model_dump(mode='json'),
                is_valid=True
            )

        except ClientError as ex:
            if ex.code == 429 and i < tries - 1:
                sleep(15 * (2 ** i))
                continue

            if ex.code == 429:
                return ResponseModel(
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                    message="Limite de requisições da IA atingido. Tente novamente em alguns instantes."
                )
            raise

        except Exception as ex:
            print(format_exc())
            return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

    return ResponseModel(
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
        message="Não foi possível gerar a análise após múltiplas tentativas."
    )


async def send_message(user_message: str, context: str, previous_interaction_id: str | None = None) -> ResponseModel:
    try:
        response = await _create_response_interactor(user_message, context, previous_interaction_id)
        return ResponseModel(
            status=status.HTTP_200_OK,
            content=response.model_dump(mode='json'),
            is_valid=True,
        )
    except ClientError as ex:
        if ex.code == 429:
            return ResponseModel(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                message="Limite de requisições da IA atingido. Tente novamente em instantes.",
                is_valid=False,
            )
        raise
    except (RuntimeError, ValueError) as ex:
        return ResponseModel(
            status=status.HTTP_502_BAD_GATEWAY,
            message=f"A IA não retornou uma resposta válida: {ex}",
            is_valid=False,
        )


async def generate_client_prediction(context: str):
    interaction = await __client.aio.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=context,
        system_instruction=build_client_prediction_instruction(),
        generation_config={"thinking_level": "low", "temperature": 0.4},
        store=False,
    )

    if not isinstance(interaction, Interaction):
        raise TypeError(f"Resposta inesperada da API: esperava Interaction, recebeu {type(interaction).__name__}.")

    if not interaction.output_text:
        raise ValueError("A IA não retornou uma previsão.")

    return interaction.output_text.strip()


async def generate_meeting_prediction(context: str):
    interaction = await __client.aio.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=context,
        system_instruction=build_meeting_prediction_instruction(),
        generation_config={"thinking_level": "low", "temperature": 0.4},
        store=False,
    )

    if not isinstance(interaction, Interaction):
        raise TypeError(f"Resposta inesperada da API: esperava Interaction, recebeu {type(interaction).__name__}.")

    if not interaction.output_text:
        raise ValueError("A IA não retornou uma previsão.")
    return interaction.output_text.strip()


async def _create_transcript_interactor(payload: TranscriptPayload) -> TranscriptAnalyse:
    '''Cria um interactor custom e próprio para analíse de transcrições, sendo necessário informar:\n
        @request: str = Transcricão pura
    '''
    prompt = f'Analise a seguinte transcrição de reunião e retorne o JSON estruturado conforme instruído:\n\n{payload.transcript}'
    context = build_extraction_system_instruction(payload.scope, payload.profile, payload.client)

    interaction = await __client.aio.interactions.create(
            model=__GEMINI_MODEL_NAME,
            input=prompt,
            generation_config={"thinking_level": "medium", "temperature": 0.2},
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": TranscriptAnalyse.model_json_schema()
            },
            system_instruction=context,
            store=False,
        )

    if not isinstance(interaction, Interaction):
        raise TypeError(f"Resposta inesperada da API: esperava Interaction, recebeu {type(interaction).__name__}.")

    if interaction.output_text is None:
        raise ValueError("A IA não retornou conteúdo de texto na análise da transcrição.")

    return TranscriptAnalyse.model_validate_json(interaction.output_text)


async def _create_response_interactor(
    prompt: str, context: str, interaction_id: str | None
) -> "_ChatBotResponse | _ChatBotFirstResponse":
    is_first_message = interaction_id is None
    generation_config = {"thinking_level": "low", "temperature": 0.5}

    if is_first_message:
        interaction, title = await asyncio.gather(
            __client.aio.interactions.create(
                model=__GEMINI_MODEL_NAME,
                input=prompt,
                previous_interaction_id=interaction_id,
                generation_config=generation_config,
                store=True,
                system_instruction=context,
                stream=False,
            ),
            generate_session_title(prompt),
        )
    else:
        interaction = await __client.aio.interactions.create(
            model=__GEMINI_MODEL_NAME,
            input=prompt,
            previous_interaction_id=interaction_id,
            generation_config=generation_config,
            store=True,
            system_instruction=context,
            stream=False,
        )
        title = None

    if not isinstance(interaction, Interaction):
        raise RuntimeError("Tipo retornado pela IA é inválido.")
    if not interaction.output_text:
        raise ValueError("A IA não retornou conteúdo de texto na resposta do chat.")

    tokens = (
        interaction.usage.total_output_tokens
        if interaction.usage and interaction.usage.total_output_tokens
        else 0
    )

    if is_first_message:
        return _ChatBotFirstResponse(
            title=title,
            reply=interaction.output_text,
            previous_interaction_id=interaction.id,
            tokens_used=tokens,
        )

    return _ChatBotResponse(
        reply=interaction.output_text,
        previous_interaction_id=interaction.id,
        tokens_used=tokens,
    )


async def generate_session_title(first_user_msg: str) -> str:
    """
    Gera o título com base só na mensagem do usuário -- permite rodar em
    paralelo com a resposta principal na primeira mensagem da sessão.
    Nunca deixa a criação da sessão falhar por causa do título: em caso de
    erro, devolve um título genérico em vez de propagar a exceção.
    """
    try:
        interaction = await __client.aio.interactions.create(
            model=__GEMINI_MODEL_NAME,
            input=first_user_msg,
            system_instruction=(
                "Gere um título curto (até 6 palavras) que identifique o assunto "
                "da conversa que está prestes a começar, com base na primeira "
                "mensagem do usuário. Responda APENAS com o título, sem aspas, "
                "sem pontuação final."
            ),
            generation_config={"thinking_level": "low", "temperature": 0.3},
            store=False,
        )
        if isinstance(interaction, Interaction) and interaction.output_text:
            return interaction.output_text.strip()
    except Exception:
        pass
    return "Nova conversa"