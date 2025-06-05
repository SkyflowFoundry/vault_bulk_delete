# ⚠️ Vault Bulk Delete - Multiple Tables

> **WARNING**:  
> 🚫 **THIS SCRIPT IS FOR TEST USE ONLY.**  
> ❌ **DO NOT RUN THIS AGAINST A PRODUCTION VAULT UNDER ANY CIRCUMSTANCE.**  
> This script irreversibly deletes data from multiple tables in a Skyflow Vault.

---

## 📋 Overview

This Python script performs a **bulk deletion** of records from a list of Skyflow Vault tables. It is designed exclusively for test or development environments where vault data must be routinely wiped, such as in automated test pipelines or pre-production refreshes.

---

## ⚙️ Configuration

Before running the script, replace the following **placeholder values** in the code:

| Variable      | Description                                          | Example Format                                   |
| ------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `VAULT_ID`    | Your Skyflow Vault ID                                | `"your-vault-id"`                                |
| `VAULT_URL`   | The base URL of your Skyflow vault service (no path) | `"https://your-tenant-id.vault.skyflowapis.com"` |
| `AUTH_TOKEN`  | A valid **Bearer** authorization token               | `"Bearer your-auth-token"`                       |
| `TABLE_NAMES` | A list of table names to delete records from         | `["table1", "table2", "table3"]`                 |

`The script constructs the full API base URL as follows:`

```python
BASE_VAULT_URL = f"{VAULT_URL}/v1/vaults/{VAULT_ID}"

```

## .

## 🚀 Usage

1. Install Python Requirements (if not already installed)

This script requires the requests library:

```pip install requests

```

2. Edit the Script

Update the configuration values (VAULT_ID, VAULT_URL, AUTH_TOKEN, and TABLE_NAMES) to match your test vault environment.

3. Run the Script

```python vault_bulk_delete.py

```

## 🧠 What the Script Does

Connects to your Skyflow Vault via its API.

Fetches all skyflow_ids in the specified tables using paginated requests.

Breaks the skyflow_ids into batches.

Deletes batches of records concurrently using a thread pool for performance.

Verifies that each table is fully emptied before moving on.

Provides a complete summary at the end including any failures.

## 🔐 Safety Notice

This script performs destructive operations with no user confirmation.

It assumes all data in the specified tables can be permanently deleted.

It is intended only for non-production/test environments where data loss is acceptable or intended.

If you accidentally run this against a production environment, data will be unrecoverable.
