from dataclasses import dataclass


@dataclass(slots=True, kw_only=True, frozen=True)
class Permission:
    model: str
    action: str  # Literal["read", "modify", "admin"]


@dataclass(slots=True, kw_only=True)
class CachedUser:
    device_fingerprint: bytes
    user_id: str
    permissions: list[Permission]

    # ...more fields...
