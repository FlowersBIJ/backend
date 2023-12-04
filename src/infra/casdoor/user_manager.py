from typing import Dict

from casdoor import User  # type: ignore

from src.application.auth.repos.user_repo import UIAuth


class CasdoorUser(UIAuth):
    async def modify_user(self, method: str, user: User, params: Dict | None = None) -> Dict:
        """
        modify Casdoor user by some method
        :param method: "add-user" or "update-user" or "delete-user"
        :param user: Casdoor user.
        :param params: New params for Casdoor User. Only for "update-user" method.
                       Choose params, that you need to update and write it in dictionary

        :return: POST request result in dict format
        """

        return await self.sdk.modify_user(method=method, user=user, params=params)
