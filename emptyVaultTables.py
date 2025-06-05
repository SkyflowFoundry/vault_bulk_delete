# *** Vault Bulk Delete - Multiple Tables ***
# *** NB: THIS CODE IS ONLY INTENDED FOR TEST USE!!! ***
# *** UNDER +- NO -+ CIRCUMSTANCE RUN THIS AGAINST A PRODUCTION VAULT ***

import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration
VAULT_ID = "<your-vault-id>"
VAULT_URL = "<your-vault-url>"
# Static list of tables to delete from:
TABLE_NAMES = ["table1", "table2", "table3", "table4", "table5"]
BASE_VAULT_URL = f"{VAULT_URL}/v1/vaults/{VAULT_ID}"
AUTH_TOKEN = "Bearer eyJhbGciOi... ... ....."
HEADERS = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}
LIMIT = 25   #default batch size

def fetch_records(table_name, offset):
    #Go and Fetch records from a given table using the right API
    url = f"{BASE_VAULT_URL}/{table_name}?offset={offset}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 401:
        print(f"[ERROR] Unauthorized request to {url}. Token may be expired.")
        return []
    if response.status_code == 404:
        print(f"[INFO] Table {table_name} not found.")
        return []
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch records from {table_name}: {response.status_code} - {response.text}")
        return []

    records = response.json().get("records", [])
    return [
        record["fields"]["skyflow_id"]
        for record in records
        if "fields" in record and "skyflow_id" in record["fields"]
    ]

def delete_records(table_name, batch):
    # Go and Delete a batch of records from table using skyflow_ids
    url = f"{BASE_VAULT_URL}/{table_name}"
    payload = {"skyflow_ids": batch}
    response = requests.delete(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"[ERROR] Failed to delete from {table_name}: {response.status_code} - {response.text}")
    return response.status_code

def get_record_count(table_name):
    """Get the total number of records in a table."""
    url = f"{BASE_VAULT_URL}/{table_name}?limit=1&offset=0"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"[WARN] Could not get record count for {table_name}: {response.status_code} - {response.text}")
        return 0
    return len(response.json().get("records", []))

def verify_table_empty(table_name, max_retries=3):
    """Verify that a table has been emptied."""
    for attempt in range(max_retries):
        count = get_record_count(table_name)
        if count == 0:
            return True
        print(f"[INFO] {table_name} not empty yet (Attempt {attempt+1}): {count} remaining")
        time.sleep(1)
    return False

def delete_table_data(table_name):
    """Delete all data from a single table and verify completion."""
    print(f"\n--- Processing table: {table_name} ---")
    
    # Fetch records
    offset = 0
    skyflow_ids = []

    while True:
        records = fetch_records(table_name, offset)
        if not records:
            break
        skyflow_ids.extend(records)
        offset += LIMIT

    print(f"Total skyflow_ids fetched from {table_name}: {len(skyflow_ids)}")

    # Delete in batches
    if skyflow_ids:
        batches = [skyflow_ids[i:i + LIMIT] for i in range(0, len(skyflow_ids), LIMIT)]
        failed_batches = 0
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(delete_records, table_name, batch) for batch in batches]
            for i, future in enumerate(futures):
                status_code = future.result()
                if status_code == 200:
                    print(f"Batch {i+1}/{len(batches)} deleted from {table_name}")
                else:
                    print(f"❌ Batch {i+1}/{len(batches)} failed in {table_name}")
                    failed_batches += 1

        if failed_batches > 0:
            print(f"[WARNING] {failed_batches} batches failed in {table_name}")
            return False

    # Verify deletion
    print(f"Verifying table {table_name} is empty...")
    if verify_table_empty(table_name):
        print(f"✓ Table {table_name} successfully emptied")
        return True
    else:
        print(f"✗ Table {table_name} still contains records")
        return False

def main():
    """Main entry point to delete data from multiple tables."""
    print("Starting multi-table bulk delete operation...")
    print(f"Tables to process: {TABLE_NAMES}")
    
    success_count = 0
    failed_tables = []

    for table_name in TABLE_NAMES:
        try:
            if delete_table_data(table_name):
                success_count += 1
            else:
                failed_tables.append(table_name)
        except Exception as e:
            print(f"[EXCEPTION] Error processing {table_name}: {str(e)}")
            failed_tables.append(table_name)

    # Summary
    print(f"\n{'='*50}")
    print("DELETION OPERATION COMPLETE")
    print(f"{'='*50}")
    print(f"Tables processed: {len(TABLE_NAMES)}")
    print(f"Successes: {success_count}")
    print(f"Failures: {len(failed_tables)}")
    if failed_tables:
        print("Failed tables:", ", ".join(failed_tables))
        print("❌ Operation completed with errors")
    else:
        print("✅ All tables successfully emptied!")

if __name__ == "__main__":
    main()
