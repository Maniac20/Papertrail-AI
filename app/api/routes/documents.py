from fastapi import APIRouter,File,Form,HTTPException,UploadFile
from app.dependencies import get_document_service
from app.schemas.documents import DocumentUploadResponse,DocumentListResponse
router=APIRouter(prefix="/documents",tags=["documents"])

@router.post("/upload",response_model=DocumentUploadResponse)
async def upload_document(file:UploadFile=File(...),user_id:str=Form(default="demo-user")):
    if file.content_type not in {"application/pdf","application/octet-stream"}:
        raise HTTPException(415,"Only PDF files are supported.")
    content=await file.read(); service=get_document_service()
    if len(content)>service.max_upload_bytes:
        raise HTTPException(413,"PDF exceeds configured upload size limit.")
    try:
        result=service.ingest_pdf(content,file.filename or "uploaded.pdf",user_id)
        return DocumentUploadResponse(**result,message="PDF indexed successfully.")
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc

@router.get("",response_model=DocumentListResponse)
async def list_documents(user_id:str="demo-user"):
    return {"documents":get_document_service().list_documents(user_id)}

@router.delete("/{document_id}")
async def delete_document(document_id:str,user_id:str="demo-user"):
    if not get_document_service().delete_document(document_id,user_id):
        raise HTTPException(404,"Document not found.")
    return {"deleted":True,"document_id":document_id}
