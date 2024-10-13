from typing import Optional
from pydantic import BaseModel


class ProductMediaImage(BaseModel):
    url: str
    alt_text: str


class ProductMediaVideo(BaseModel):
    url: str
    description: str


class ProductMedia(BaseModel):
    images: list[ProductMediaImage]
    videos: list[ProductMediaVideo]


class ProductSeo(BaseModel):
    meta_title: str
    meta_description: str
    meta_keywords: str
    canonical_url: str


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
    attributes: list[ProductAttributes]


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
    categories: dict
    tags: list[str]
    status: ProductStatus


class Product(BaseModel):
    _id: str
    metadata: ProductMetadata
    media: ProductMedia
    listing: ProductListing
    details: ProductDetails
    variants: list[int]
    reviews: ProductReviews
