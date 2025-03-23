from typing import List, Optional
from pydantic import BaseModel
from .product import ProductResponse

class SearchQuery(BaseModel):
    query: str
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    sort_by: Optional[str] = None
    sort_order: Optional[str] = "asc"
    page: int = 1
    limit: int = 10

class SearchResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    items: List[ProductResponse]

class SearchSuggestion(BaseModel):
    query: str
    suggestions: List[str] 