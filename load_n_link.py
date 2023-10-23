import requests
import json
import os
import pandas as pd
from openpyxl import load_workbook


###################################################
# url and dummy_test_input here


ticket_url = "https://ct-eu.molecule.io/api/v2/inventory/tickets"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "ccheong_nx@qsol.co.uk",
    "x-token": "T-TyVnTYsoyaQtL9nRst",
}

df_data = pd.read_csv(
    r"Example_data.csv",
    header=0,
)

# Specify the CSV file path for SUBLEG ID FETCH DATA
subleg_file_path = "response_data.csv"

df_data = df_data.fillna("")


# Convert TRADE_DATE column to desired format
date_format = "%Y-%m-%d %H:%M:%S"
df_data["fulfillment_date"] = pd.to_datetime(
    df_data["fulfillment_date"], dayfirst=True
).dt.strftime(date_format)

print(df_data)


input1 = "fulfillment_date"
input2 = "commodity"
input3 = "volume"
input4 = "price"
input5 = "asset"
input6 = "status"
# input7 = "fill"
input8 = "final_delivery"
# input9 = str(subleg_id)
input10 = "external_id"
input11 = "external_source"
input12 = "dedupe_external_id"
input13 = "custom_field_name"

for idx, data in df_data.iterrows():
    ################ SUBMIT API REQUEST TO FETCH SUBLEG ID ###################################

    trade_id = []
    subleg_id = []

    if data["trade_id"] is not None and data["trade_id"] != "":
        trade_id = data["trade_id"]

        get_subleg_url = (
            "https://ct-eu.molecule.io/api/v2/legs/sublegs?trade_id=" + str(trade_id)
        )

        # API requests for subleg ID of the given trade ID
        response = requests.get(get_subleg_url, headers=headers)

        # Parse the JSON response
        response_data = response.json()

        # print response for checking
        # print(json.dumps(response_data, separators=(",", ":"), indent=4))

        ############# filter n panda transform retrived subleg data ##################

        # Extract data from the JSON response
        res_data = response_data["data"]

        # Create an empty list to store the flattened data (unnest all the data inside atrributes)
        flattened_data = []

        # Iterate through the data and flatten the attributes
        for item in res_data:
            record = {"id": item["id"], "type": item["type"], **item["attributes"]}
            flattened_data.append(record)

        # Create a Pandas DataFrame from the flattened data
        df = pd.DataFrame(flattened_data)

        print(df)

        ########### for writing logs to excel file ##################################

        # log_loc = "response_data.xlsx"

        # Create a new Excel writer
        # writer = pd.ExcelWriter(log_loc, engine="openpyxl")

        # Write the DataFrame to the Excel file
        # df.to_excel(writer, sheet_name="Data", index=False)

        # Save the Excel file using writer.book.save()
        # writer.book.save(log_loc)

        ############ for writing the subleg_id data to csv format#############################################

        # Write the DataFrame to a CSV file
        df.to_csv(subleg_file_path, index=True)

        ############## THIS is the READ SUBLEG_ID N UPLOAD section##############################

        # Read the saved response
        df = pd.read_csv(
            r"response_data.csv",
            header=0,
        )

        # Select which subleg to write to [molecule returns as 'ID']
        selected_subleg = 0
        subleg_id = int(df["id"].iloc[selected_subleg])

    else:
        trade_id = ""
        subleg_id = ""

    # Load n Populate the Payload Draft

    if str(subleg_id) is not None and str(subleg_id) != "":
        payload = {
            "fulfillment_date": data[input1],
            "commodity": data[input2],
            "volume": data[input3],
            "price": data[input4],
            "asset": data[input5],
            "status": data[input6],
            "fill": "true",
            "final_delivery": data[input8],
            "subleg_id": str(subleg_id),
            "external _id": data[input10],
            "external_source": data[input11],
            "dedupe_external_id": data[input12],
            "custom_field_name": data[input13],
        }
    else:
        payload = {
            "fulfillment_date": data[input1],
            "commodity": data[input2],
            "volume": data[input3],
            "price": data[input4],
            "asset": data[input5],
            "status": data[input6],
            "fill": "false",
            "final_delivery": data[input8],
            "external _id": data[input10],
            "external_source": data[input11],
            "dedupe_external_id": data[input12],
            "custom_field_name": data[input13],
        }
    ####################### FILTER DATA SECTION ###########################################

    ######### remove n/a data from package ########################

    # Define values to remove
    values_to_remove = {"", "n/a", "N/a", "N/A", "n/A", "empty"}

    # filter the payload
    filtered_payload = {
        key: value
        for key, value in payload.items()
        if value is not None and value not in values_to_remove
    }

    ######## check if CHECKBOX condition is valid##################

    allowed_statuses = {
        "status": {"adjustment", "estimate", "in_transit", "delivered/received"},
        "fill": {"true", "false"},
        "final_delivery": {"true", "false"},
        "dedupe_external_id": {"true", "false"},
    }
    # Define the allowed statuses

    for key, value in allowed_statuses.items():
        if key in filtered_payload and filtered_payload[key] not in value:
            del filtered_payload[key]

    ############### UPLOAD DATA N PRINT RESPONSE ###########################################

    # Send the JSON data in the request
    response = requests.post(
        ticket_url, data=json.dumps(filtered_payload), headers=headers
    )
    print("\n sent package looks like " + json.dumps(filtered_payload))

    # print(f"\n Request failed with status code: {response.status_code}")
    print(f"\n Status code: {response.status_code} ( {response.reason} )\n")
    print(
        "Ticket loaded as: \n\n"
        + json.dumps(response.json(), separators=(",", ":"), indent=4)
    )
