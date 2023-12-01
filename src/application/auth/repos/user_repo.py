from abc import ABC, abstractmethod
from typing import Dict

from casdoor import AsyncCasdoorSDK, User


class UIAuth(ABC):
    def __init__(self, sdk: AsyncCasdoorSDK):
        self.sdk = sdk

    @abstractmethod
    async def modify_user(self, method: str, user: User, params=None) -> Dict:
        raise NotImplementedError
