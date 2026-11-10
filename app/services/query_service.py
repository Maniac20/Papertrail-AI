class QueryService:
    def __init__(self,rag,answer_service):
        self.rag,self.answer_service=rag,answer_service
    async def ask(self,question,user_id,document_ids=None):
        chunks=self.rag.retrieve(question,user_id,document_ids)
        answer=await self.answer_service.answer(question,self.rag.build_context(chunks))
        citations=[]; seen=set()
        for c in chunks:
            key=(c["document_id"],c["page"],c["chunk_id"])
            if key in seen: continue
            seen.add(key)
            citations.append({"document_id":c["document_id"],"filename":c["filename"],
                "page":c["page"],"chunk_id":c["chunk_id"],"quote":c["text"][:240]})
        grounded=bool(chunks) and "do not provide enough information" not in answer.lower()
        return {"answer":answer,"citations":citations,"retrieved_chunks":len(chunks),"grounded":grounded}
