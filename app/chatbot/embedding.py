from typing import List, Tuple
from dotenv import load_dotenv
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
from sentence_transformers import SentenceTransformer

# ✅ 환경변수 로드
load_dotenv()

# ✅ 문장 임베딩 모델
EMBEDDING_MODEL_NAME = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# ✅ 감정 분류 모델
EMOTION_MODEL_NAME = "taeminlee/klue-roberta-base-emotion"
emotion_tokenizer = AutoTokenizer.from_pretrained(EMOTION_MODEL_NAME)
emotion_model = AutoModelForSequenceClassification.from_pretrained(EMOTION_MODEL_NAME)
emotion_model.eval()

# ✅ 감정 라벨 자동 매핑
emotion_config = AutoConfig.from_pretrained(EMOTION_MODEL_NAME)
EMOTION_LABELS = [emotion_config.id2label[i] for i in range(len(emotion_config.id2label))]

# ✅ 통합 함수
def get_embedding_and_emotion(text: str) -> Tuple[List[float], str]:
    try:
        # 1. 문장 임베딩
        embedding = embedding_model.encode(text).tolist()
        if len(embedding) != 768:
            raise ValueError(f"❌ 잘못된 임베딩 벡터 차원 수: {len(embedding)}")

        # 2. 감정 분류
        inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True)
        with torch.no_grad():
            outputs = emotion_model(**inputs)
            predicted_class = torch.argmax(outputs.logits, dim=1).item()
        emotion = EMOTION_LABELS[predicted_class]

        return embedding, emotion

    except Exception as e:
        print(f"❌ 임베딩/감정 추론 실패: {e}")
        return [], ""
