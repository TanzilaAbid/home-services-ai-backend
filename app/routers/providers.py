from fastapi import APIRouter, Query
from pydantic import BaseModel
from app.database import SessionLocal
from sqlalchemy import text

router = APIRouter()


class ProviderOut(BaseModel):
    provider_id: str
    name: str
    category: str
    rating: float
    hourly_rate: float
    is_available: bool


class ProviderListResponse(BaseModel):
    providers: list[ProviderOut]
    count: int
    page: int
    limit: int
    total_pages: int


@router.get("/providers", response_model=ProviderListResponse)
def list_providers(
    category: str | None = Query(default=None, description="Filter by category e.g. 'Painter'"),
    max_price: float | None = Query(default=None, description="Max hourly rate"),
    min_rating: float | None = Query(default=None, description="Minimum rating"),
    page: int = Query(default=1, ge=1, description="Page number, starting at 1"),
    limit: int = Query(default=10, ge=1, le=50, description="Results per page (max 50)"),
):
    db = SessionLocal()
    try:
        filters = ["pp.is_available = TRUE"]
        params = {}

        if category:
            filters.append("sc.name = :category")
            params["category"] = category
        if max_price is not None:
            filters.append("pp.hourly_rate <= :max_price")
            params["max_price"] = max_price
        if min_rating is not None:
            filters.append("pp.rating_avg >= :min_rating")
            params["min_rating"] = min_rating

        where_clause = " AND ".join(filters)

        # total count for pagination metadata
        count_query = text(f"""
            SELECT COUNT(*) FROM provider_profiles pp
            JOIN users u ON pp.user_id = u.id
            JOIN service_categories sc ON pp.category_id = sc.id
            WHERE {where_clause}
        """)
        total_count = db.execute(count_query, params).scalar()

        offset = (page - 1) * limit
        params["limit"] = limit
        params["offset"] = offset

        data_query = text(f"""
            SELECT pp.id, u.full_name, sc.name, pp.rating_avg, pp.hourly_rate, pp.is_available
            FROM provider_profiles pp
            JOIN users u ON pp.user_id = u.id
            JOIN service_categories sc ON pp.category_id = sc.id
            WHERE {where_clause}
            ORDER BY pp.rating_avg DESC
            LIMIT :limit OFFSET :offset
        """)
        rows = db.execute(data_query, params).fetchall()

        providers = [
            ProviderOut(
                provider_id=str(row[0]),
                name=row[1],
                category=row[2],
                rating=float(row[3]) if row[3] else 0.0,
                hourly_rate=float(row[4]) if row[4] else 0.0,
                is_available=row[5],
            )
            for row in rows
        ]

        total_pages = (total_count + limit - 1) // limit if total_count else 0

        return ProviderListResponse(
            providers=providers,
            count=total_count,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )
    finally:
        db.close()
