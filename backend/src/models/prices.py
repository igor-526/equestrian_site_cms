from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint

from utils.basemodel import metadata, timestamp_columns, uuid_pk

prices = Table(
    "prices",
    metadata,
    uuid_pk(),
    *timestamp_columns(),
    Column("name", String(63), nullable=False, index=True),
    Column("description", String(255), nullable=True),
    Column("group", String(31), nullable=True),
    Column("price", Integer(), nullable=False),
    Column("price_formatter", String(7), nullable=False),
    UniqueConstraint("name", "group", name="uq_name_group")
)

price_variants = Table(
    "price_variants",
    metadata,
    uuid_pk(),
    *timestamp_columns(),
    Column("price_id", ForeignKey("prices.id", ondelete="CASCADE"), nullable=False),
    Column("name", String(63), nullable=False),
    Column("description", String(255), nullable=True),
    Column("price", Integer(), nullable=False),
    Column("price_formatter", String(7), nullable=False),
    UniqueConstraint("name", "price_id", name="uq_name_price_id")
)
