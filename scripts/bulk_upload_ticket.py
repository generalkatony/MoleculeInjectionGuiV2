import requests
import json
import pandas as pd
from openpyxl import load_workbook
from icecream import ic

###################################################
# url and dummy_test_input here


def create_headers(email, token):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-email": email,
        "x-token": token,
    }
    return headers


def bulk_ticket_upload(upload_file, headers, match_field, url):
    df_data = pd.read_csv(
        f"{upload_file}",
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

    for idx, data in df_data.iterrows():
        ################ SUBMIT API REQUEST TO FETCH SUBLEG ID ###################################

        trade_id = []
        subleg_id = []

        if data["trade_id"] is not None and data["trade_id"] != "":
            trade_id = data["trade_id"]

            get_subleg_url = f"https://{url}/api/v2/legs/sublegs?trade_id=" + str(
                trade_id
            )
            ic(get_subleg_url)
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

            ############ for writing the subleg_id data to csv format#############################################

            # Write the DataFrame to a CSV file
            df.to_csv(subleg_file_path, index=True)

            ############## THIS is the READ SUBLEG_ID N UPLOAD section##############################

            # Read the saved response
            df = pd.read_csv(
                f"{subleg_file_path}",
                header=0,
            )

            # Select which subleg to write to [molecule returns as 'ID']
            selected_subleg = 0
            subleg_id = int(df["id"].iloc[selected_subleg])

        else:
            trade_id = ""
            subleg_id = ""

        # Load n Populate the Payload Draft
        payload = {}

        for key, value in match_field.items():
            payload[key] = data[value]
        if str(subleg_id) is not None and str(subleg_id) != "":
            payload["fill"] = "true"
            payload["dedupe_external_id"] = "true"
            payload["subleg_id"] = str(subleg_id)

        else:
            payload["fill"] = "false"
            payload["dedupe_external_id"] = "false"

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

        ticket_url = f"https://{url}/api/v2/inventory/tickets"

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


####################################################
#     "x-email": "ccheong_nx@qsol.co.uk",
#     "x-token": "T-TyVnTYsoyaQtL9nRst",
match_field = {
    "fulfillment_date": "fulfillment_date",
    "commodity": "commodity",
    "volume": "volume",
    "price": "price",
    "asset": "asset",
    "status": "status",
    "final_delivery": "final_delivery",
    "external_id": "external_id",
    "external_source": "external_source",
    "custom_field_name": "custom_field_name",
}
test_url = "ct-eu.molecule.io"
file = "Test Data\Example_data.csv"
####################################################


headers = create_headers(email="ccheong_nx@qsol.co.uk", token="T-TyVnTYsoyaQtL9nRst")

bulk_ticket_upload(file, headers, match_field, test_url)
