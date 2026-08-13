'''
--- Chats ---
POST   /chats/{id}/messages              # envia mensagem
POST   /chats/meetings/{id}/feedback     # Gera um feedback de uma reunião especicada pelo seu ID
POST   /chats/user/{id}/feedback         # Gera um feedback para um usuário especicada pelo seu ID  
'''

from fastapi import APIRouter

router = APIRouter()

