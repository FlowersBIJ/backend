from abc import ABC, abstractmethod
from typing import Dict, Any

from casdoor import AsyncCasdoorSDK, User  # type: ignore


class UIAuth(ABC):
    def __init__(self, sdk: AsyncCasdoorSDK):
        self.sdk = sdk

    @abstractmethod
    async def modify_user(
            self,
            method: str,
            user: User,
            params: Dict | None = None
    ) -> Dict:
        raise NotImplementedError
