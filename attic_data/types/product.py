from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from attic_data.core.utils import generate_id, get_timestamp


class ProductMediaImage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(...)
    alt_text: str = Field(...)


class ProductMediaVideo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str = Field(...)
    description: str = Field(...)


class ProductMedia(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    images: list[ProductMediaImage] = Field(...)
    videos: list[ProductMediaVideo] = Field(...)


class ProductSeo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    meta_title: str = Field(...)
    meta_description: str = Field(...)
    meta_keywords: str = Field(...)
    canonical_url: str = Field(...)


class ProductDescription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    short: str = Field(...)
    long: str = Field(...)


class ProductStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    availability: str = Field(...)
    lifecycle: str = Field(...)
    featured: bool = Field(...)
    on_sale: bool = Field(...)


class ProductAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(...)
    value: str = Field(...)


class ProductLegal(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    warranty_info: str = Field(...)
    return_policy: str = Field(...)


class ProductDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    brand: str = Field(...)
    model: str = Field(...)
    condition: str = Field(...)
    clearance: bool = Field(...)
    legal: ProductLegal = Field(...)
    attributes: list[ProductAttributes] = Field(...)


class ProductReviewsDistribution(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    five: int = Field(...)
    four: int = Field(...)
    three: int = Field(...)
    two: int = Field(...)
    one: int = Field(...)


class ProductReviews(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    total_count: int = Field(...)
    average_rating: float = Field(...)
    star_distribution: ProductReviewsDistribution = Field(...)


class ProductMetadata(BaseModel):
    model_config = ConfigDict(populate_by_name=False)

    created_at: int = Field(...)
    updated_at: int = Field(...)
    published_at: Optional[int] = Field(None)
    unpublished_at: Optional[int] = Field(None)
    reviewed_at: Optional[int] = Field(None)
    released_at: Optional[int] = Field(None)
    expiration_date: Optional[int] = Field(None)


class ProductListing(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sku: str = Field(...)
    seo: ProductSeo = Field(...)
    title: str = Field(...)
    description: ProductDescription = Field(...)
    categories: dict = Field(...)
    tags: list[str] = Field(...)
    status: ProductStatus = Field(...)


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., alias="_id", default_factory=generate_id)
    url: str = Field(...)
    metadata: ProductMetadata = Field(...)
    media: ProductMedia = Field(...)
    listing: ProductListing = Field(...)
    details: ProductDetails = Field(...)
    variants: list[int] = Field(...)
    reviews: ProductReviews = Field(...)

    @staticmethod
    def with_empty_values(id: str = "") -> "Product":
        return Product(
            _id=id or generate_id(),
            url="",
            metadata=ProductMetadata(
                created_at=get_timestamp(),
                updated_at=get_timestamp(),
                published_at=None,
                unpublished_at=None,
                reviewed_at=None,
                released_at=None,
                expiration_date=None,
            ),
            media=ProductMedia(images=[], videos=[]),
            listing=ProductListing(
                sku="",
                seo=ProductSeo(
                    meta_title="",
                    meta_description="",
                    meta_keywords="",
                    canonical_url="",
                ),
                title="",
                description=ProductDescription(short="", long=""),
                categories={},
                tags=[],
                status=ProductStatus(
                    availability="", lifecycle="", featured=False, on_sale=False
                ),
            ),
            details=ProductDetails(
                brand="",
                model="",
                condition="",
                clearance=False,
                legal=ProductLegal(warranty_info="", return_policy=""),
                attributes=[],
            ),
            variants=[],
            reviews=ProductReviews(
                total_count=0,
                average_rating=0.0,
                star_distribution=ProductReviewsDistribution(
                    five=0,
                    four=0,
                    three=0,
                    two=0,
                    one=0,
                ),
            ),
        )
