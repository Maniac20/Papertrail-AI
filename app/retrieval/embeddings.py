from sentence_transformers import SentenceTransformer
class EmbeddingService:
    def __init__(self, model_name):
        self.model_name, self._model = model_name, None
    @property
    def model(self):
        if self._model is None: self._model = SentenceTransformer(self.model_name)
        return self._model
    def embed_documents(self, texts):
        vectors = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
        return vectors.tolist()
    def embed_query(self, text):
        return self.embed_documents([text])[0]
