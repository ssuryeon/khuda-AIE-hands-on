"""3주차 정답: 요약 생성 후 DB 저장, 목록/단건 조회."""

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
    models.Base.metadata.create_all(bind=database.engine)
    yield


app = FastAPI(
    title="AIE_hands-on",
    description="테크 블로그 요약 서버 - 5주 커리큘럼",
    version="0.1.0",
    lifespan=lifespan,
)


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
        main_points=["스키마 적용됨", "DB에 저장됨"],
        core_summary="더미 요약 (DB에 저장 후 반환)",
        structure_summary="요청→검증→저장→응답",
        practical_insights=["content_text 필수", "output_format은 json만"],
        meta=schemas.SummaryMeta(prompt_version="v1.0", generated_at=now),
    )


@app.post("/summarize", response_model=schemas.SummaryResponseWithId)
def summarize(body: schemas.SummaryRequest, db: Session = Depends(get_db)) -> schemas.SummaryResponseWithId:
    response = _build_dummy_response()
    output_json = json.dumps(response.model_dump())
    row = models.Summary(
        title=body.title,
        content_text=body.content_text,
        output_json=output_json,
        prompt_version=response.meta.prompt_version,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return schemas.SummaryResponseWithId(
        id=row.id,
        **response.model_dump(),
    )


@app.get("/summaries", response_model=list[schemas.SummaryListItem])
def list_summaries(db: Session = Depends(get_db)) -> list[schemas.SummaryListItem]:
    rows = (
        db.query(models.Summary)
        .order_by(models.Summary.created_at.desc())
        .all()
    )
    return [
        schemas.SummaryListItem(
            id=r.id,
            title=r.title,
            created_at=_created_at_to_iso(r.created_at),
        )
        for r in rows
    ]


@app.get("/summaries/{id}", response_model=schemas.SummaryDetail)
def get_summary(id: int, db: Session = Depends(get_db)) -> schemas.SummaryDetail:
    row = db.query(models.Summary).filter(models.Summary.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Summary not found")
    data = json.loads(row.output_json)
    return schemas.SummaryDetail(
        id=row.id,
        title=row.title,
        content_text=row.content_text,
        main_points=data["main_points"],
        core_summary=data["core_summary"],
        structure_summary=data["structure_summary"],
        practical_insights=data["practical_insights"],
        meta=schemas.SummaryMeta(**data["meta"]),
        created_at=_created_at_to_iso(row.created_at),
    )
