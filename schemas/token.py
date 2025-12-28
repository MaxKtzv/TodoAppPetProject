from ..schemas.base import Base


class Token(Base):
    access_token: str
    token_type: str