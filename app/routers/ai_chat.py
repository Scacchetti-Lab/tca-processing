'''
--- Chats ---
GET    /chats                            # lista de chats do usuário autenticado (via token, não path)
GET    /chats/{id}                       # detalhe de um chat específico
GET    /chats/{id}/messages              # histórico de mensagens (com paginação: ?page=, ?limit=)
POST   /chats                            # cria novo chat
POST   /chats/{id}/messages              # envia mensagem (era "talk")
PATCH  /chats/{id}/messages/{messageId}  # edita mensagem específica
PATCH  /chats/{id}                       # edita metadados do chat (ex: título)
POST   /chats/{id}/share-link            # gera link de compartilhamento
DELETE /chats/{id}                       # soft-delete
'''

from fastapi import APIRouter

router = APIRouter()

