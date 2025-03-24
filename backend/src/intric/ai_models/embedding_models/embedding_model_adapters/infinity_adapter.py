from tenacity import retry, stop_after_attempt, wait_random_exponential

from intric.ai_models.embedding_models.embedding_model_adapters.base import (
    EmbeddingModelAdapter,
)
from intric.files.chunk_embedding_list import ChunkEmbeddingList
from intric.info_blobs.info_blob import InfoBlobChunk
from intric.main.aiohttp_client import aiohttp_client
from intric.main.config import get_settings
from intric.main.logging import get_logger

logger = get_logger(__name__)


class InfinityAdapter(EmbeddingModelAdapter):
    async def get_embedding_for_query(self, query: str):
        truncated_query = query[: self.model.max_input]
        query_prepended = [f"query: {truncated_query}"]

        embeddings = await self._get_embeddings(query_prepended)
        return embeddings[0]

    # Copied from text_embedding
    # TODO: Refactor this later
    def _chunk_chunks(self, chunks: list[InfoBlobChunk]):
        cum_len = 0
        prev_i = 0
        for i, chunk in enumerate(chunks):
            cum_len += len(chunk.text)

            if cum_len > self.model.max_input:
                yield chunks[prev_i:i]
                prev_i = i
                cum_len = 0

        yield chunks[prev_i:]

    async def get_embeddings(self, chunks: list[InfoBlobChunk]):
        chunk_embedding_list = ChunkEmbeddingList()
        for chunked_chunks in self._chunk_chunks(chunks):
            texts_prepended = [f"passage: {chunk.text}" for chunk in chunked_chunks]

            logger.debug(f"Embedding a chunk of {len(chunked_chunks)} chunks")

            embeddings_for_chunks = await self._get_embeddings(texts_prepended)
            chunk_embedding_list.add(chunked_chunks, embeddings_for_chunks)

        return chunk_embedding_list

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    async def _get_embeddings(self, texts: list[str]) -> list[list[float]]:

        payload = {"input": texts, "model": self.model.name}

        url = f"{get_settings().infinity_url}/embeddings"
        async with aiohttp_client().post(url, json=payload) as resp:
            data = await resp.json()

        return [embedding["embedding"] for embedding in data["data"]]
