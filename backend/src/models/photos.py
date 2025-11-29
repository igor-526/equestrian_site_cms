from sqlalchemy import Column, Date, ForeignKey, String, Table, Text, Integer

from utils.basemodel import metadata, timestamp_columns, uuid_pk

photos = Table(
    "photos",
    metadata,
    uuid_pk(),
    *timestamp_columns(),
    Column("name", String(63), nullable=False, index=True),
    Column("description", String(511), nullable=True),
    Column("path", String(511), nullable=False),
)