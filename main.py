import json
import msal
import requests
from pathlib import Path


class GraphClient:
    def __init__(self, config_path: str = "auth_config.json"):
        """
        Initialize GraphClient using client-credential authentication.
        """
        config_file = Path(__file__).parent / config_path
        with open(config_file, "r") as f:
            config = json.load(f)

        self.tenant_id = config["tenant_id"]
        self.client_id = config["client_id"]
        self.client_secret = config["client_secret"]
        self.scope = config["scope"]

        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.base_url = "https://graph.microsoft.com/v1.0"

        self.token = self._get_access_token()

    # -------------------------------------------------------
    # Authentication
    # -------------------------------------------------------
    def _get_access_token(self) -> str:
        """Acquire token using MSAL client credentials flow."""
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority,
        )

        token_result = app.acquire_token_for_client(scopes=self.scope)

        if "access_token" not in token_result:
            raise Exception(f"Token error: {token_result.get('error_description')}")

        return token_result["access_token"]

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"}

    # -------------------------------------------------------
    # Generic Request Method
    # -------------------------------------------------------
    def _request(self, method: str, endpoint: str, data=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            json=data
        )
        if response.status_code >= 400:
            raise Exception(f"Graph API Error {response.status_code}: {response.text}")
        if response.text:
            return response.json()
        return None  # DELETE operations return no content

    # -------------------------------------------------------
    # User Operations
    # -------------------------------------------------------

    def search_user(self, search_query: str):
        """
        Search for users by displayName or userPrincipalName.
        Example: search_user("john")
        """
        endpoint = f"/users?$filter=startswith(displayName,'{search_query}') or startswith(userPrincipalName,'{search_query}')"
        return self._request("GET", endpoint)

    def create_user(self, display_name: str, username: str, password: str):
        """
        Create a new Entra ID user.
        username should be full UPN: e.g., newuser@contoso.com
        password must meet tenant password policy requirements.
        """

        user_data = {
            "accountEnabled": True,
            "displayName": display_name,
            "mailNickname": username.split("@")[0],
            "userPrincipalName": username,
            "passwordProfile": {
                "forceChangePasswordNextSignIn": False,
                "password": password
            }
        }

        return self._request("POST", "/users", user_data)

    def delete_user(self, user_id: str):
        """
        Delete a user by object ID or userPrincipalName.
        """
        endpoint = f"/users/{user_id}"
        return self._request("DELETE", endpoint)


# -------------------------------------------------------
# Example usage
# -------------------------------------------------------
if __name__ == "__main__":
    graph = GraphClient()

    print("\n🔎 Searching for users containing 'john'...\n")
    results = graph.search_user("john")
    print(json.dumps(results, indent=2))

    # Example create user (SAFE for GitHub — user must provide real values)
    # print("\n👤 Creating a new user...\n")
    # new_user = graph.create_user(
    #     display_name="Demo User",
    #     username="demo.user@YOURDOMAIN.com",
    #     password="TempPassword123!"
    # )
    # print(json.dumps(new_user, indent=2))

    # Example delete user
    # print("\n🗑️ Deleting a user...\n")
    # graph.delete_user("OBJECT-ID-OR-UPN")
    # print("✔ User deleted")
