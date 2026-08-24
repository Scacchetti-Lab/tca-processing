from uuid import UUID
from sqlmodel import SQLModel, Field, Uuid, column, table

# necessario para ter o relacionamento das duas chaves primárias estrangeiras
user_profile_tbl = table(
    "user_profile",
    column("up_id", Uuid),
    column("up_user_id", Uuid),
    column("up_profile_id", Uuid),
)

class user_profile(SQLModel, table=True):
    up_user_id: UUID = Field(primary_key=True)
    up_profile_id: UUID = Field(primary_key=True)


