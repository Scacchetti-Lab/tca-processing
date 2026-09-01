from time import sleep
from os import getenv as __getenv
from traceback import format_exc
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from google.genai.interactions import Interaction
from google.genai.errors import ClientError
from app.constants.ai_context import CHATBOT_CONTEXT as _CHATBOT_CONTEXT, CHATBOT_INITAL as _CHATBOT_INITAL 
from app.types.chats_models import ChatBotResponse as _ChatBotResponse
from app.types.transcripts_models import TranscriptAnalyse, TranscriptPayload
from app.types.response_model import ResponseModel
from fastapi import status

from app.helpers.create_context import build_extraction_system_instruction

__load_dotenv() 

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)

def analyse_transcript(payload: TranscriptPayload | str, tries: int = 3) -> ResponseModel:
    if isinstance(payload, str):
        payload = TranscriptPayload(transcript=payload)

    for i in range(tries):
        try:
            transcript_analysed = _create_transcript_interactor(payload)
            return ResponseModel(
                status=status.HTTP_200_OK,
                content=transcript_analysed.model_dump(mode='json'),
                is_valid=True
            )

        except ClientError as ex:
            if ex.code == 429 and i < tries - 1:
                sleep(15 * (2 ** i))   # 15s, 30s
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

async def send_message(user_message: str, previous_interaction_id: str | None = None) -> ResponseModel:
    try:
        response = await _create_response_interactor(user_message, previous_interaction_id, False)

        if not response:
            return ResponseModel(
                status=status.HTTP_404_NOT_FOUND,
                message='AI não enviou uma resposta, ocorreu algum problema inesperado.',
                is_valid=True
            )

        return ResponseModel(
            status=status.HTTP_200_OK,
            content=_ChatBotResponse(
                    user_input=user_message,
                    answer=response.answer,
                    previous_interaction_id=response.previous_interaction_id
                ).model_dump(mode='json'),
            is_valid=True
        )
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

async def generate_client_prediction(client_id: str):
    '''Gera uma previsão sobre o cliente partindo do ID especificado e o que esperar de seu futuro com a empresa'''
    return ResponseModel(
        status=status.HTTP_201_CREATED,
        content={'result': 'teste'},
        is_valid=True
    )

async def generate_meeting_prediction(meeting_id: str):
    '''Gera uma previsão sobre a reunião a seguir partindo do ID especificado e o que esperar de seu futuro com a empresa'''
    return ResponseModel(
        status=status.HTTP_201_CREATED,
        content={'result': 'teste'},
        is_valid=True
    )

def _create_transcript_interactor(payload: TranscriptPayload) -> TranscriptAnalyse:
    '''Cria um interactor custom e próprio para analíse de transcrições, sendo necessário informar:\n
        @request: str = Transcricão pura
    '''
    prompt = f'Analise a seguinte transcrição de reunião e retorne o JSON estruturado conforme instruído:\n\n{payload.transcript}'
    context = build_extraction_system_instruction(payload.score_type)
    
    interaction = __client.interactions.create(
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
        raise TypeError("Resposta inesperada da API: esperava Interaction, recebeu Stream.")

    if interaction.output_text is None:
        raise ValueError("A IA não retornou conteúdo de texto na análise da transcrição.")

    return TranscriptAnalyse.model_validate_json(interaction.output_text)

async def _create_response_interactor(prompt: str, interaction_id: str | None, stream: bool = True):
    ''' Cria um interactor que servirá para continuar a conversa anteriormente começada, com base no Id do estado fornecido no model, um request (mensagem do usuário) e se será assíncrono ou não a resposta'''
    interaction = __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=prompt,
        previous_interaction_id=interaction_id,
        generation_config={
            "thinking-level": "medium",
            "temperature": 0.5
        },
        store=True,
        system_instruction=_CHATBOT_CONTEXT,
        stream=stream
    )

    ai_response = _ChatBotResponse(user_input=prompt, answer='', previous_interaction_id='')
    
    if isinstance(interaction, Interaction):
        if interaction.output_text is None:
            raise ValueError("A IA não retornou conteúdo de texto na análise da transcrição.")
        ai_response.answer = interaction.output_text
        ai_response.previous_interaction_id = interaction.id
    else:
        for event in interaction:
            if event.event_type == "step.delta":
                if event.delta.type == "text":
                    ai_response.answer = event.delta.text
            elif event.event_type == "response.completed":
                ai_response.previous_interaction_id = event.interaction.id
            elif event.event_type == "error":
                raise ValueError(f"Erro no streaming: {event}")

    if (not ai_response.answer):
        return None

    return ai_response
