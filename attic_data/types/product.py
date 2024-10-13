from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class ProductMediaImage(BaseModel):
    url: HttpUrl
    alt_text: Optional[str]


class ProductMediaVideo(BaseModel):
    url: HttpUrl
    description: Optional[str]


class ProductMedia(BaseModel):
    images: Optional[List[ProductMediaImage]]
    videos: Optional[List[ProductMediaVideo]]


class ProductSeo(BaseModel):
    meta_title: str
    meta_description: str
    meta_keywords: Optional[str]
    canonical_url: Optional[HttpUrl]


class ProductDescription(BaseModel):
    short: str
    long: str


class ProductStatus(BaseModel):
    availibility: str
    lifecycle: str
    featured: bool
    on_sale: bool


class ProductAttributes(BaseModel):
    name: str
    value: str


class ProductLegal(BaseModel):
    warranty_info: str
    return_policy: str


class ProductDetails(BaseModel):
    brand: str
    model: str
    condition: str
    clearance: bool
    legal: ProductLegal
    attributes: List[ProductAttributes]


class ProductReviewsDistribution(BaseModel):
    five: int
    four: int
    three: int
    two: int
    one: int


class ProductReviews(BaseModel):
    total_count: int
    average_rating: float
    star_distribution: ProductReviewsDistribution


class ProductMetadata(BaseModel):
    created_at: int
    updated_at: int
    published_at: Optional[int]
    unpublished_at: Optional[int]
    reviewed_at: Optional[int]
    released_at: Optional[int]
    expiration_date: Optional[int]


class ProductListing(BaseModel):
    sku: str
    seo: ProductSeo
    title: str
    description: ProductDescription
    categories: Optional[dict]
    tags: Optional[List[str]]
    status: ProductStatus


class Product(BaseModel):
    _id: int
    metadata: ProductMetadata
    media: Optional[ProductMedia]
    listing: ProductListing
    details: ProductDetails
    variants: Optional[List[int]]
    reviews: Optional[ProductReviews]
