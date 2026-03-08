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


# TODO [2] -----------------------------------------------
# SummaryMeta 모델을 정의하세요.
#
# 필드:
#   prompt_version : str — 예: "v1.0"
#   generated_at   : str — ISO 8601, 예: "2024-01-15T10:30:00Z"
# --------------------------------------------------------


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


@app.get("/health")
def health():
    return {"status": "ok"}


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
    raise NotImplementedError
