"""
2주차: API 계약을 코드로 고정합니다

핵심 질문: 어떤 입력을 받고, 어떤 출력이 나가는지 코드로 강제할 수 있는가?

실습 순서:
  1. TODO [1]~[3]: 아래 스키마 클래스를 완성하세요.
  2. TODO [4]: /summarize 엔드포인트를 새 스키마로 교체하세요.
  3. 서버 실행 후 http://localhost:8000/docs 에서 직접 확인하세요.
     - content_text 없이 요청  → 422 자동 반환
     - output_format: "xml"    → 422 자동 반환
     - 올바른 요청             → 200 + SummaryResponse 구조
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


# TODO [1] -----------------------------------------------
# SummaryRequest 모델을 정의하세요.
#
# 필드:
#   content_text  : str             — 필수, 요약할 본문
#   title         : str | None      — 선택 (기본값 None)
#   output_format : Literal["json"] — 필수, "json" 이외 값은 422
# --------------------------------------------------------
class SummaryRequest(BaseModel):
    contest_text: str
    title: str | None = None
    output_format: Literal["json"]

# TODO [2] -----------------------------------------------
# SummaryMeta 모델을 정의하세요.
#
# 필드:
#   prompt_version : str — 예: "v1.0"
#   generated_at   : str — ISO 8601, 예: "2024-01-15T10:30:00Z"
# --------------------------------------------------------
class SummaryMeta(BaseModel):
    prompt_version: str
    generated_at: str

# TODO [3] -----------------------------------------------
# SummaryResponse 모델을 정의하세요.
#
# 필드:
#   main_points        : list[str]
#   core_summary       : str
#   structure_summary  : str
#   practical_insights : list[str]
#   meta               : SummaryMeta
# --------------------------------------------------------
class SummaryResponse(BaseModel):
    main_points        : list[str]
    core_summary       : str
    structure_summary  : str
    practical_insights : list[str]
    meta               : SummaryMeta


# TODO [4] -----------------------------------------------
# POST /summarize 엔드포인트를 2주차 스키마로 전환하세요.
#
# 시그니처:
#   @app.post("/summarize", response_model=SummaryResponse)
#   def summarize(body: SummaryRequest) -> SummaryResponse:
#
# 힌트:
#   - 현재 시각: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
#   - 실제 요약 로직 없이 더미 값으로 채워 반환해도 됩니다.
# --------------------------------------------------------
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
