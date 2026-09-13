from uuid import UUID
from app.helpers.contexts.predict_meeting import make_predict_meeting_context as __make_mt_ctx
from app.helpers.contexts.predict_client import make_predict_client_context as __make_cl_ctx
from app.repository.meeting import MeetingRepository as __MeetingRepository
from app.repository.client import ClientRepository as __ClientRepository
from app.db_connect import SessionDep as __SessionDep
from app.services.gemini_client_service import generate_meeting_prediction as __gen_mt_predict, generate_client_prediction as __gen_cl_predict

async def predict_meeting(meeting_id: UUID, session: __SessionDep) -> str:
    mt_repo = __MeetingRepository(session)
    client = mt_repo.find_meeting_client(meeting_id)
    performance_history = mt_repo.get_performance_history(client.id)
    strategic_history = mt_repo.get_strategic_history(client.id)

    context = __make_mt_ctx(client, performance_history, strategic_history)

    return await __gen_mt_predict(context)


async def predict_client_status(client_id: UUID, session: __SessionDep) -> str | None:
    cl_repo = __ClientRepository(session)
    mt_repo = __MeetingRepository(session)

    client = cl_repo.find_by_id(client_id)
    if client is None:
        __print_error("Cliente não encontrado")
        return None
    details = cl_repo.find_client_details(client_id)
    if details is None:
        __print_error("Falha ao obter detalhes")
        return None
    strategic_history = mt_repo.get_strategic_history(client_id)

    context = __make_cl_ctx(client, details, strategic_history)
    return await __gen_cl_predict(context)


def __print_error(msg: str):
    print(f"\033[1;31m{msg}\033[m")