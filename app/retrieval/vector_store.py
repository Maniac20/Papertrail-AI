from uuid import uuid5, NAMESPACE_URL
from qdrant_client import QdrantClient, models

class QdrantVectorStore:
    def __init__(self, path, collection, vector_size):
        self.collection = collection
        self.client = QdrantClient(path=path)
        if not self.client.collection_exists(collection):
            self.client.create_collection(collection_name=collection,
                vectors_config=models.VectorParams(size=vector_size,distance=models.Distance.COSINE))
    def upsert_chunks(self, document_id, user_id, filename, chunks, vectors):
        points = []
        for i,(chunk,vector) in enumerate(zip(chunks,vectors)):
            chunk_id = f"{document_id}:{i}"
            points.append(models.PointStruct(
                id=str(uuid5(NAMESPACE_URL,chunk_id)), vector=vector,
                payload={"chunk_id":chunk_id,"document_id":document_id,"user_id":user_id,
                         "filename":filename,"page":chunk["page"],"text":chunk["text"],"chunk_index":i}))
        if points: self.client.upsert(collection_name=self.collection,points=points)
    def search(self, vector, user_id, limit, document_ids=None):
        must=[models.FieldCondition(key="user_id",match=models.MatchValue(value=user_id))]
        if document_ids:
            must.append(models.FieldCondition(key="document_id",match=models.MatchAny(any=document_ids)))
        result=self.client.query_points(collection_name=self.collection,query=vector,
            query_filter=models.Filter(must=must),limit=limit,with_payload=True)
        return [{"score":p.score,**(p.payload or {})} for p in result.points]
    def delete_document(self, document_id, user_id):
        self.client.delete(collection_name=self.collection,points_selector=models.FilterSelector(
            filter=models.Filter(must=[
                models.FieldCondition(key="document_id",match=models.MatchValue(value=document_id)),
                models.FieldCondition(key="user_id",match=models.MatchValue(value=user_id))])))
