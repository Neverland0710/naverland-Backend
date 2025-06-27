from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from typing import List, Dict
import uuid


# ✅ Qdrant 설정
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "memory"

# ✅ 벡터 컬렉션 생성 (차원: 1536 for text-embedding-3-small)
def create_collection(vector_size: int = 1536):
    if client.collection_exists(collection_name=COLLECTION_NAME):
        print(f"🧨 기존 컬렉션 '{COLLECTION_NAME}' 삭제")
        client.delete_collection(collection_name=COLLECTION_NAME)

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"✅ 컬렉션 '{COLLECTION_NAME}' 재생성 완료.")

# ✅ 벡터 업로드
def upload_memory(text: str, embedding: List[float], metadata: Dict):
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={**metadata, "text": text}
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

# ✅ 유사 메시지 검색
def search_similar_memories(
    query_vector: List[float],
    user_id: str,
    top_k: int = 3
) -> List[Dict]:
    filter = {
        "must": [
            {"key": "user_id", "match": {"value": user_id}}
        ]
    }

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        query_filter=filter
    )
    return _format_results(results)



# ✅ 결과 포맷
def _format_results(results) -> List[Dict]:
    return [
        {
            "text": hit.payload.get("text", ""),
            "score": hit.score,
            "metadata": hit.payload
        }
        for hit in results
    ]
