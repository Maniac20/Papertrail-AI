from app.core.config import get_settings
class RAGService:
    def __init__(self,embeddings,vector_store):
        self.embeddings,self.vector_store=embeddings,vector_store
        self.settings=get_settings()
    def retrieve(self,question,user_id,document_ids=None):
        vector=self.embeddings.embed_query(question)
        hits=self.vector_store.search(vector,user_id,self.settings.retrieval_top_k,document_ids)
        return [h for h in hits if h.get("score",0)>=self.settings.retrieval_score_threshold]
    def build_context(self,chunks):
        parts=[]; total=0
        for c in chunks:
            part=f"[Source: {c['filename']}, page {c['page']}, chunk {c['chunk_id']}]\n{c['text']}"
            if total+len(part)>self.settings.max_context_chars: break
            parts.append(part); total+=len(part)
        return "\n\n---\n\n".join(parts)
