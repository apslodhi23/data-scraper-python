from pydantic import BaseModel, Field
from typing import Optional

class Settings(BaseModel):
    limit: Optional[int] = Field(None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Field(None, description="Proxy string to use for scraping")

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str
