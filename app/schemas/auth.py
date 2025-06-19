from pydantic import BaseModel
from typing import Literal
# 구글 로그인 요청을 위한 스키마
class SocialLoginRequest(BaseModel):
    provider: Literal["google"]
    access_token: str

# 로그인 응답에 포함될 토큰 + 유저 정보
class SocialLoginResponse(BaseModel):
    id: str
    email: str
    name: str
    provider: str
    access_token: str