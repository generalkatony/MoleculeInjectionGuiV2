import requests
import json
import os
import pandas as pd
from openpyxl import load_workbook

trade_id = 149198

url = "https://ct-eu.molecule.io/api/v2/legs/sublegs?trade_id=" + str(trade_id)

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "ccheong_nx@qsol.co.uk",
    "x-token": "T-TyVnTYsoyaQtL9nRst",
}


response = requests.get(url, headers=headers)
# Parse the JSON response
response_data = response.json()
# print response for checking
print(json.dumps(response_data, separators=(",", ":"), indent=4))


# Extract data from the JSON response
res_data = response_data["data"]


# Create an empty list to store the flattened data
flattened_data = []

# Iterate through the data and flatten the attributes
for item in res_data:
    record = {"id": item["id"], "type": item["type"], **item["attributes"]}
    flattened_data.append(record)

# Create a Pandas DataFrame from the flattened data
df = pd.DataFrame(flattened_data)


print(df)

#############################################################################

# log_loc = "response_data.xlsx"

# Create a new Excel writer
# writer = pd.ExcelWriter(log_loc, engine="openpyxl")

# Write the DataFrame to the Excel file
# df.to_excel(writer, sheet_name="Data", index=False)

# Save the Excel file using writer.book.save()
# writer.book.save(log_loc)

#############################################################################

# Specify the CSV file path
csv_file_path = "response_data.csv"

# Write the DataFrame to a CSV file
df.to_csv(csv_file_path, index=False)

#############################################################################


df = pd.read_csv(
    r"response_data.csv",
    header=0,
)

first_value = int(df["id"].iloc[0])
# Test Payload
payload = {
    "fulfillment_date": "2023-10-11",
    "commodity": "Aromatic",
    "volume": 1,
    "price": "",
    "asset": "",
    "status": "estimate",
    "fill": True,
    "final_delivery": False,
    "subleg_id": str(first_value),
    "external _id": "",
    "external_source": "",
    "dedupe_external_id": "True",
    "custom_field_name": "",
}

# remove n/a data from package
filtered_payload = {
    key: value for key, value in payload.items() if value is not None and value != ""
}

########check if 'status' condition is valid##################
# Define the allowed statuses
allowed_statuses = ["adjustment", "estimate", "in_transit", "delivered/received"]

if "status" in filtered_payload and filtered_payload["status"] not in allowed_statuses:
    del filtered_payload["status"]


ticket_url = "https://ct-eu.molecule.io/api/v2/inventory/tickets"

# Send the JSON data in the request
response = requests.post(ticket_url, data=json.dumps(filtered_payload), headers=headers)
print("\n sent package looks like " + json.dumps(filtered_payload))

# print(f"\n Request failed with status code: {response.status_code}")
print(json.dumps(response.json(), separators=(",", ":"), indent=4))
