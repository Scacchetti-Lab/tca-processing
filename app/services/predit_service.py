from uuid import UUID
from app.helpers.contexts.predict_meeting import __make_predict_meeting_context
from app.repository.meeting import MeetingRepository as __MeetingRepository
from app.db_connect import SessionDep as __SessionDep
from app.services.gemini_client_service import generate_meeting_prediction as __generate_meeting_prediction, generate_client_prediction as __generate_client_prediction

async def predict_meeting(meeting_id: UUID, session: __SessionDep) -> str:
    mt_repo = __MeetingRepository(session)
    client = mt_repo.find_meeting_client(meeting_id)
    performance_history = mt_repo.get_performance_history(client.id)
    strategic_history = mt_repo.get_strategic_history(client.id)

    context = __make_predict_meeting_context(client, performance_history, strategic_history)

    return await __generate_meeting_prediction(context)


async def predict_client_status(client_id: UUID, session: __SessionDep) -> str:
    return ''