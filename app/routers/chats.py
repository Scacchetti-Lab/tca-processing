'''
--- Chats ---
POST   /chats/{id}/messages              # envia mensagem
POST   /chats/meetings/{id}/feedback     # Gera um feedback de uma reunião especicada pelo seu ID
POST   /chats/user/{id}/feedback         # Gera um feedback para um usuário especicada pelo seu ID
POST   /chats/meetings/{id}/predict      # Gera uma previsão com base na transcrição da última reunião   
'''

from fastapi import APIRouter

router = APIRouter()

