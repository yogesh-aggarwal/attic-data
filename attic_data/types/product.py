from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductMediaImage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(..., alias="url")
    alt_text: str = Field(..., alias="altText")


class ProductMediaVideo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(..., alias="url")
    description: str = Field(..., alias="description")


class ProductMedia(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    images: list[ProductMediaImage] = Field(..., alias="images")
    videos: list[ProductMediaVideo] = Field(..., alias="videos")


class ProductSeo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    meta_title: str = Field(..., alias="metaTitle")
    meta_description: str = Field(..., alias="metaDescription")
    meta_keywords: str = Field(..., alias="metaKeywords")
    canonical_url: str = Field(..., alias="canonicalUrl")


class ProductDescription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    short: str = Field(..., alias="short")
    long: str = Field(..., alias="long")


class ProductStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    availability: str = Field(..., alias="availability")
    lifecycle: str = Field(..., alias="lifecycle")
    featured: bool = Field(..., alias="featured")
    on_sale: bool = Field(..., alias="onSale")


class ProductAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., alias="name")
    value: str = Field(..., alias="value")


class ProductLegal(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    warranty_info: str = Field(..., alias="warrantyInfo")
    return_policy: str = Field(..., alias="returnPolicy")


class ProductDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    brand: str = Field(..., alias="brand")
    model: str = Field(..., alias="model")
    condition: str = Field(..., alias="condition")
    clearance: bool = Field(..., alias="clearance")
    legal: ProductLegal = Field(..., alias="legal")
    attributes: list[ProductAttributes] = Field(..., alias="attributes")


class ProductReviewsDistribution(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    five: int = Field(..., alias="five")
    four: int = Field(..., alias="four")
    three: int = Field(..., alias="three")
    two: int = Field(..., alias="two")
    one: int = Field(..., alias="one")


class ProductReviews(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_count: int = Field(..., alias="totalCount")
    average_rating: float = Field(..., alias="averageRating")
    star_distribution: ProductReviewsDistribution = Field(..., alias="starDistribution")


class ProductMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    created_at: int = Field(..., alias="createdAt")
    updated_at: int = Field(..., alias="updatedAt")
    published_at: Optional[int] = Field(None, alias="publishedAt")
    unpublished_at: Optional[int] = Field(None, alias="unpublishedAt")
    reviewed_at: Optional[int] = Field(None, alias="reviewedAt")
    released_at: Optional[int] = Field(None, alias="releasedAt")
    expiration_date: Optional[int] = Field(None, alias="expirationDate")


class ProductListing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sku: str = Field(..., alias="sku")
    seo: ProductSeo = Field(..., alias="seo")
    title: str = Field(..., alias="title")
    description: ProductDescription = Field(..., alias="description")
    categories: dict = Field(..., alias="categories")
    tags: list[str] = Field(..., alias="tags")
    status: ProductStatus = Field(..., alias="status")


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id")
    metadata: ProductMetadata = Field(..., alias="metadata")
    media: ProductMedia = Field(..., alias="media")
    listing: ProductListing = Field(..., alias="listing")
    details: ProductDetails = Field(..., alias="details")
    variants: list[int] = Field(..., alias="variants")
    reviews: ProductReviews = Field(..., alias="reviews")
