# ⚠️ Vault Bulk Delete - Multiple Tables

> **WARNING**:  
> 🚫 **THIS SCRIPT IS FOR TEST USE ONLY.**  
> ❌ **DO NOT RUN THIS AGAINST A PRODUCTION VAULT UNDER ANY CIRCUMSTANCE.**  
> This script irreversibly deletes data from multiple tables in a Skyflow Vault.

---

## 📋 Overview

This Python script performs a **bulk deletion** of records from a list of Skyflow Vault tables. It is designed for test or development environments where vault data needs to be programmatically wiped during automated testing or setup resets.

---

## ⚙️ Configuration

Before running the script, replace the following **placeholder values** in the code:

| Variable         | Description                                  | Example Format                                  |
| ---------------- | -------------------------------------------- | ----------------------------------------------- |
| `VAULT_ID`       | Your Skyflow Vault ID                        | `"your-vault-id"`                               |
| `BASE_VAULT_URL` | Base URL for your Vault API                  | `"https://your-vault-id.vault.skyflowapis.com"` |
| `AUTH_TOKEN`     | A valid **Bearer** authorization token       | `"Bearer eyJhbGciOi..."`                        |
| `TABLE_NAMES`    | A list of table names to delete records from | `["table1", "table2", "table3"]`                |

---

## 🚀 Usage

1. **Install Python Requirements (if not already available)**  
   This script uses the `requests` and `concurrent.futures` modules (both part of the standard library for Python ≥ 3.2):

   ```bash
   pip install requests
   ```
