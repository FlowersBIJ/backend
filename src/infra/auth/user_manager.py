from typing import Dict, Any

from casdoor import User

from src.application.auth.repos.user_repo import UIAuth


class CasdoorUser(UIAuth):
    async def modify_user(self, method: str, user: User, params: Any = None) -> Dict:
        """
        modify Casdoor user by some method
        :param method: "add-user" or "update-user" or "delete-user"
        :param user: Casdoor user
        :param params: params for modifying user

        :return: POST request result in dict format
        """
        data = {
            "method": method,
            "user": user
        }
        if params is not None:
            data["params"] = params
        return await self.sdk.modify_user(**data)
