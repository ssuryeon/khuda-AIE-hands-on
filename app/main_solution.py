"""
2주차 정답 코드: API 계약을 코드로 고정합니다

핵심: Pydantic 모델을 FastAPI에 연결하면
  - 입력이 스키마에 맞지 않으면 FastAPI가 자동으로 422를 반환합니다.
  - 출력도 response_model에 맞는 구조임을 FastAPI가 보장합니다.
"""

from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AIE_hands-on",
    description="테크 블로그 요약 서버 - 5주 커리큘럼",
    version="0.1.0",
)


class SummaryRequest(BaseModel):
    content_text: str             # 필수 — 없으면 FastAPI가 자동으로 422 반환
    title: str | None = None      # 선택 — 기본값 None
    output_format: Literal["json"]  # "json" 이외 값이면 422 자동 반환


class SummaryMeta(BaseModel):
    prompt_version: str
    generated_at: str


class SummaryResponse(BaseModel):
    main_points: list[str]
    core_summary: str
    structure_summary: str
    practical_insights: list[str]
    meta: SummaryMeta


@app.get("/health")
def health():
    return {"status": "ok"}


# response_model 지정 → 반환값이 SummaryResponse 구조임을 FastAPI가 검증
@app.post("/summarize", response_model=SummaryResponse)
def summarize(body: SummaryRequest) -> SummaryResponse:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return SummaryResponse(
        main_points=[
            "2주차: 입력 스키마(SummaryRequest)가 적용되었습니다",
            "2주차: 출력 스키마(SummaryResponse)가 적용되었습니다",
        ],
        core_summary="Pydantic 스키마로 API 계약이 고정되었습니다. 규격 외 입력은 422로 차단됩니다.",
        structure_summary="요청 → 스키마 검증 → 더미 응답 반환 (3주차에서 실제 LLM 호출로 교체됩니다)",
        practical_insights=[
            "content_text 필드가 없으면 FastAPI가 자동으로 422를 반환합니다",
            "output_format은 'json'만 허용합니다. 다른 값은 422로 차단됩니다",
        ],
        meta=SummaryMeta(
            prompt_version="v1.0",
            generated_at=now,
        ),
    )
