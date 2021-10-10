from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    code: str = None
    access_token: str = None
    refresh_token:  str = None
    user_id: str = None
    token_expiration_time: int = None