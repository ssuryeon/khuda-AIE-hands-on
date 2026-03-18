"""
3주차: 요약 결과를 DB에 저장하고 다시 꺼냅니다.

실습: TODO [1]~[5]를 순서대로 채운 뒤 서버 실행 → /docs 또는 scripts/week3.sh 로 확인.
"""

import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import database, models, schemas


def _created_at_to_iso(created_at: str) -> str:
    """SQLite 저장 시각을 API용 ISO 8601 형식으로 변환."""
    return created_at.replace(" ", "T", 1) + "Z" if created_at and " " in created_at else (created_at or "")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO [1] 앱 기동 시 테이블 생성. 힌트: models.Base.metadata.create_all(bind=...)
    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(
    title="AIE_hands-on",
    description="테크 블로그 요약 서버 - 5주 커리큘럼",
    version="0.1.0",
    lifespan=lifespan,
)


# TODO [2] SessionLocal()로 세션 생성 → yield db → finally: db.close()
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}


def _build_dummy_response() -> schemas.SummaryResponse:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return schemas.SummaryResponse(
        main_points=["스키마 적용됨", "3주차 DB 저장"],
        core_summary="더미 요약 (3주차에서 DB에 저장 후 반환)",
        structure_summary="요청→검증→저장→응답",
        practical_insights=["content_text 필수", "output_format은 json만"],
        meta=schemas.SummaryMeta(prompt_version="v1.0", generated_at=now),
    )


@app.post("/summarize", response_model=schemas.SummaryResponseWithId)
def summarize(body: schemas.SummaryRequest, db: Session = Depends(get_db)) -> schemas.SummaryResponseWithId:
    # TODO [3] response 생성 → Summary 행 만들어 db.add/commit/refresh → SummaryResponseWithId(id=row.id, ...) 반환
    response = _build_dummy_response()
    raise NotImplementedError("TODO [3]")


@app.get("/summaries", response_model=list[schemas.SummaryListItem])
def list_summaries(db: Session = Depends(get_db)) -> list[schemas.SummaryListItem]:
    # TODO [4] 전체 조회 후 최신순 정렬, SummaryListItem 리스트로 반환 (created_at은 _created_at_to_iso 사용)
    raise NotImplementedError("TODO [4]")


@app.get("/summaries/{id}", response_model=schemas.SummaryDetail)
def get_summary(id: int, db: Session = Depends(get_db)) -> schemas.SummaryDetail:
    # TODO [5] id로 조회 → 없으면 404 / 있으면 output_json 파싱해 SummaryDetail 반환
    row = db.query(models.Summary).filter(models.Summary.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Summary not found")
    raise NotImplementedError("TODO [5]")
