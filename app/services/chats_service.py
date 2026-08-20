from app.types.response_model import ResponseModel
from app.services.gemini_client_service import send_message
from app.types.chats_models import ChatBotResponse as _ChatBotResponse
from fastapi import status

async def init_ai_session(message: str) -> ResponseModel:
    try:
        return await send_message(message)
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )

async def make_ai_response(message: str, previous_id: str):
    try:
        response = await send_message(message, previous_id)
        return response
    except Exception as ex:
        print(ex)
        return ResponseModel(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                message=f"[ERRO]: Ocorreu um erro inesperado\n- {ex}"
            )