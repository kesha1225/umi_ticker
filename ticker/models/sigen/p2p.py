import pydantic


class P2POffer(pydantic.BaseModel):
    id: int
    crypto_cur: str
    currency: str
    country: int
    min_order_sum: str
    max_order_sum: str | None
    price: str
    type: str
    status: str
    payment_types: str


class P2POffers(pydantic.BaseModel):
    success: bool
    offers: list[P2POffer] = pydantic.Field(alias="data")
    run_time: float
