from typing import Optional
from pydantic import BaseModel, Field


class ProductMediaImage(BaseModel):
    url: str = Field(..., alias="url")
    alt_text: str = Field(..., alias="altText")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductMediaVideo(BaseModel):
    url: str = Field(..., alias="url")
    description: str = Field(..., alias="description")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductMedia(BaseModel):
    images: list[ProductMediaImage] = Field(..., alias="images")
    videos: list[ProductMediaVideo] = Field(..., alias="videos")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductSeo(BaseModel):
    meta_title: str = Field(..., alias="metaTitle")
    meta_description: str = Field(..., alias="metaDescription")
    meta_keywords: str = Field(..., alias="metaKeywords")
    canonical_url: str = Field(..., alias="canonicalUrl")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductDescription(BaseModel):
    short: str = Field(..., alias="short")
    long: str = Field(..., alias="long")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductStatus(BaseModel):
    availability: str = Field(..., alias="availability")
    lifecycle: str = Field(..., alias="lifecycle")
    featured: bool = Field(..., alias="featured")
    on_sale: bool = Field(..., alias="onSale")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductAttributes(BaseModel):
    name: str = Field(..., alias="name")
    value: str = Field(..., alias="value")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductLegal(BaseModel):
    warranty_info: str = Field(..., alias="warrantyInfo")
    return_policy: str = Field(..., alias="returnPolicy")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductDetails(BaseModel):
    brand: str = Field(..., alias="brand")
    model: str = Field(..., alias="model")
    condition: str = Field(..., alias="condition")
    clearance: bool = Field(..., alias="clearance")
    legal: ProductLegal = Field(..., alias="legal")
    attributes: list[ProductAttributes] = Field(..., alias="attributes")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductReviewsDistribution(BaseModel):
    five: int = Field(..., alias="five")
    four: int = Field(..., alias="four")
    three: int = Field(..., alias="three")
    two: int = Field(..., alias="two")
    one: int = Field(..., alias="one")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductReviews(BaseModel):
    total_count: int = Field(..., alias="totalCount")
    average_rating: float = Field(..., alias="averageRating")
    star_distribution: ProductReviewsDistribution = Field(..., alias="starDistribution")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductMetadata(BaseModel):
    created_at: int = Field(..., alias="createdAt")
    updated_at: int = Field(..., alias="updatedAt")
    published_at: Optional[int] = Field(None, alias="publishedAt")
    unpublished_at: Optional[int] = Field(None, alias="unpublishedAt")
    reviewed_at: Optional[int] = Field(None, alias="reviewedAt")
    released_at: Optional[int] = Field(None, alias="releasedAt")
    expiration_date: Optional[int] = Field(None, alias="expirationDate")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class ProductListing(BaseModel):
    sku: str = Field(..., alias="sku")
    seo: ProductSeo = Field(..., alias="seo")
    title: str = Field(..., alias="title")
    description: ProductDescription = Field(..., alias="description")
    categories: dict = Field(..., alias="categories")
    tags: list[str] = Field(..., alias="tags")
    status: ProductStatus = Field(..., alias="status")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True


class Product(BaseModel):
    id: str = Field(..., alias="_id")
    metadata: ProductMetadata = Field(..., alias="metadata")
    media: ProductMedia = Field(..., alias="media")
    listing: ProductListing = Field(..., alias="listing")
    details: ProductDetails = Field(..., alias="details")
    variants: list[int] = Field(..., alias="variants")
    reviews: ProductReviews = Field(..., alias="reviews")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True
