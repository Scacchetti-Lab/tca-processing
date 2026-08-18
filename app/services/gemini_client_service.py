from os import getenv as __getenv
from dotenv import load_dotenv as __load_dotenv
from google import genai as __genai
from google.genai.interactions import Interaction, InteractionSSEEvent
from app.constants.ai_context import TRANSCRIPT_CONTEXT as _TRANSCRIPT_CONTEXT, CHATBOT_CONTEXT as _CHATBOT_CONTEXT, CHATBOT_INITAL as _CHATBOT_INITAL 
from app.models.chats_models import ChatBotResponse as _ChatBotResponse
from app.models.transcripts_models import TranscriptAnalyse
from app.models.response_model import ResponseModel
from fastapi import status

__load_dotenv()

__GEMINI_API_KEY = __getenv("GEMINI_API_KEY")
__GEMINI_MODEL_NAME = __getenv("GEMINI_MODEL_NAME")

__client = __genai.Client(api_key=__GEMINI_API_KEY)

def analyse_transcript(transcript: str) -> ResponseModel:
    try:
        transcript_analysed = _create_transcript_interactor(transcript)

        return ResponseModel(
                status=status.HTTP_200_OK,
                content=transcript_analysed.model_dump(mode='json'),
                is_valid=True
            )
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

async def send_message(user_message: str, previous_interaction_id: str | None = None) -> ResponseModel:
    try:
        response = ''
        if previous_interaction_id is None:
            response = await _create_init_interactor(user_message, False)
        else:
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

async def get_feedback_by_meeting_id(id: str):
    '''Retorna o Feedback gerado na analíse da transcrição com base em um Id especificado'''
    pass

async def generate_client_prediction(client_id: str):
    '''Gera uma previsão sobre o cliente partindo do ID especificado e o que esperar de seu futuro com a empresa'''
    pass

async def generate_meeting_prediction(transcript_id: str):
    '''Gera uma previsão sobre a reunião a seguir partindo do ID especificado e o que esperar de seu futuro com a empresa'''
    pass

def _create_transcript_interactor(request: str) -> TranscriptAnalyse:
    '''Cria um interactor custom e próprio para analíse de transcrições, sendo necessário informar:\n
        @request: str = Transcricão pura
    '''
    prompt = f'Analise a seguinte transcrição de reunião e retorne o JSON estruturado conforme instruído:\n\n{request}'
    
    interaction = __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=prompt,
        generation_config={"thinking_level": "medium", "temperature": 0.2},
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": TranscriptAnalyse.model_json_schema()
        },
        system_instruction=_TRANSCRIPT_CONTEXT,
        store=False,
    )

    if not isinstance(interaction, Interaction):
        raise TypeError("Resposta inesperada da API: esperava Interaction, recebeu Stream.")

    if interaction.output_text is None:
        raise ValueError("A IA não retornou conteúdo de texto na análise da transcrição.")

    return TranscriptAnalyse.model_validate_json(interaction.output_text)


async def _create_init_interactor(prompt: str, stream: bool = True) -> _ChatBotResponse | None:
    ''' Cria um interactor que servirá para iniciar a conversa de um chatbot, com base em um request fornecido e seu contexto'''

    interaction = __client.interactions.create(
        model=__GEMINI_MODEL_NAME,
        input=prompt,
        generation_config={"thinking_level": "medium", "temperature": 0.2},
        response_format={
            "type": "text",
            "mime_type": "text/plain",
        },
        system_instruction=_CHATBOT_CONTEXT,
        store=True,
        stream=stream,
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


async def _create_response_interactor(prompt: str, interaction_id: str, stream: bool = True):
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
