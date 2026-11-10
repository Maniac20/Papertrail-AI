from fastapi import APIRouter,HTTPException
from app.dependencies import get_query_service
from app.schemas.chat import AskRequest,AskResponse
router=APIRouter(prefix="/ask",tags=["question answering"])

@router.post("",response_model=AskResponse)
async def ask_question(request:AskRequest):
    try:
        result=await get_query_service().ask(request.question,request.user_id,request.document_ids)
        return AskResponse(**result)
    except Exception as exc:
        raise HTTPException(502,"Question answering failed. Check server logs.") from exc
