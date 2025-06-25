from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue
from typing import List, Dict
import uuid

client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "memory"

def create_collection(vector_size: int = 768):
    if client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"🧨 기존 컬렉션 '{COLLECTION_NAME}' 삭제")
        client.delete_collection(collection_name=COLLECTION_NAME)

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"✅ 컬렉션 '{COLLECTION_NAME}' 재생성 완료.")

def upload_memory(text: str, embedding: List[float], metadata: Dict):
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={**metadata, "text": text}
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_similar_memories(query_vector: List[float], top_k: int = 3) -> List[Dict]:
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return _format_results(results)

def search_similar_memories_with_emotion(query_vector: List[float], emotion: str, top_k: int = 3) -> List[Dict]:
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        query_filter=Filter(
            must=[
                FieldCondition(key="emotion", match=MatchValue(value=emotion))
            ]
        )
    )
    return _format_results(results)

def _format_results(results) -> List[Dict]:
    return [
        {
            "text": hit.payload.get("text", ""),
            "score": hit.score,
            "metadata": hit.payload
        }
        for hit in results
    ]
