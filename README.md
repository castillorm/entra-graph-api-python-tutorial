# 👥 User Management (CRUD) with Microsoft Graph API in Python

This section explains how to **Search**, **Create**, and **Delete** users in **Azure Entra ID (Azure Active Directory)** using Python and the Microsoft Graph API.

All examples use the `GraphClient` class included in this repository.

> ✔ **Safe for public GitHub** — no secrets, no tenant-specific identifiers
> ✔ Works with **client credentials flow** (app-only authentication)
> ✔ Requires **admin consent** for user write/delete operations

---

# 📌 Prerequisites

Your Azure App Registration must include these **Application Permissions**:

| Operation    | Required Microsoft Graph Permission                   |
| ------------ | ----------------------------------------------------- |
| Search users | `User.Read.All`                                       |
| Create users | `User.ReadWrite.All` **or** `Directory.ReadWrite.All` |
| Delete users | `User.ReadWrite.All` **or** `Directory.ReadWrite.All` |

After adding them, click **Grant admin consent**.

---

# 🧱 Importing the Graph Client

```python
from graph_client import GraphClient

graph = GraphClient()
```

---

# 🔎 Search for Users

You can search by **displayName** or **userPrincipalName (UPN)** using substring matching.

### Example: Search for users containing `"john"`

```python
results = graph.search_user("john")
print(results)
```

### Example Output (sanitized)

```json
{
  "value": [
    {
      "id": "11111111-2222-3333-4444-555555555555",
      "displayName": "John Smith",
      "userPrincipalName": "john.smith@contoso.com"
    },
    {
      "id": "aaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
      "displayName": "Johnny Doe",
      "userPrincipalName": "johnny.doe@contoso.com"
    }
  ]
}
```

---

# 👤 Create a New User

Use the `create_user()` method to provision a new account in Azure Entra ID.

### Required Fields

| Field          | Description                                       |
| -------------- | ------------------------------------------------- |
| `display_name` | Friendly display name                             |
| `username`     | Full UPN (example: `alex.wilson@contoso.com`)     |
| `password`     | Temporary password meeting tenant security policy |

### Example — Create a User

```python
new_user = graph.create_user(
    display_name="Demo User",
    username="demo.user@YOURDOMAIN.com",
    password="TempPassword123!"
)

print(new_user)
```

### Example Response

```json
{
  "id": "c12345ab-678d-4f00-b765-d99999999999",
  "displayName": "Demo User",
  "userPrincipalName": "demo.user@YOURDOMAIN.com",
  "mailNickname": "demo.user",
  "accountEnabled": true
}
```

---

# 🗑️ Delete a User

You can delete a user using either:

* The **Object ID**
* The **UPN** (e.g., `demo.user@contoso.com`)

### Example — Delete a User

```python
graph.delete_user("demo.user@YOURDOMAIN.com")
print("User deleted!")
```

If successful, Microsoft Graph returns no content (`204 No Content`).

---

# ⚠️ Important Notes About User CRUD

* **Deletion is permanent** unless Soft Delete is enabled and recoverable within 30 days.
* Creating users may require licensing depending on your tenant settings.
* For production environments:

  * Store secrets in **Azure Key Vault**, not JSON files.
  * Log all CRUD operations.
  * Apply **Least Privilege** (avoid granting `Directory.ReadWrite.All` unless absolutely needed).
* The client credentials flow (app-only authentication) **cannot modify the signed-in user** (`/me`). Only delegated auth can.

---

# 🔐 Permissions & Admin Consent

| Action       | Permission                                        | Admin Consent Required? |
| ------------ | ------------------------------------------------- | ----------------------- |
| Search Users | `User.Read.All`                                   | ✔ Yes                   |
| Create Users | `User.ReadWrite.All` or `Directory.ReadWrite.All` | ✔ Yes                   |
| Delete Users | `User.ReadWrite.All` or `Directory.ReadWrite.All` | ✔ Yes                   |

You can verify permissions at:

```
Azure Portal → Microsoft Entra ID → App Registrations → Your App → API Permissions
```

---

# 📁 Recommended Repo Structure for User CRUD

```
/
├── src/
│   ├── graph_client.py
│   ├── auth_config_example.json
│   └── examples/
│       ├── search_user.py
│       ├── create_user.py
│       └── delete_user.py
├── .gitignore
└── README.md
```

---

# 🚀 Example CLI Scripts (Optional for Repo)

### `examples/search_user.py`

```python
from graph_client import GraphClient

graph = GraphClient()
print(graph.search_user("alex"))
```

### `examples/create_user.py`

```python
from graph_client import GraphClient

graph = GraphClient()
graph.create_user("Alex Wilson", "alex.wilson@YOURDOMAIN.com", "TempPassword123!")
```

### `examples/delete_user.py`

```python
from graph_client import GraphClient

graph = GraphClient()
graph.delete_user("alex.wilson@YOURDOMAIN.com")
```

---

# 🧪 Testing & Validation

You can verify user creation via:

* Azure Portal → Microsoft Entra ID → Users
* Microsoft Graph Explorer: [https://developer.microsoft.com/en-us/graph/graph-explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
* PowerShell:

```powershell
Get-MgUser -Search 'DisplayName:Demo'
```

---

# ✅ Summary

With the methods provided by `GraphClient`, you can:

| Operation    | Method                                  | Description              |
| ------------ | --------------------------------------- | ------------------------ |
| Search Users | `search_user(query)`                    | Finds users by name/UPN  |
| Create User  | `create_user(name, username, password)` | Provisions a new user    |
| Delete User  | `delete_user(id_or_upn)`                | Permanently removes user |

This allows you to build automated onboarding, offboarding, and identity lifecycle capabilities with clean, reusable Python code.
