import tkinter as tk
from tkinter import ttk, filedialog
import json
import os
from icecream import ic
import bulk_upload_ticket.py

############## GENERAL FUNCTIONS ############################


#############################################################

window = tk.Tk()
window.title("Automata Alpha Release 1.0.2")

style = ttk.Style(window)
window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

######### LOAD SAVED DATA FROM .JSON ########################
# Check if the JSON file exists and create it if it doesn't

filename = "data.json"

if not os.path.exists(filename):
    print(f"Creating {filename}")
    with open(filename, "w") as json_file:
        json.dump({}, json_file)

# Load data from JSON
with open(filename, "r") as json_file:
    saved_data = json.load(json_file)
    print(f"Loaded data from {filename}: {saved_data}")


########### TO CLEAR .JSON FILE #############################
def clear_json_file(file_path):
    try:
        # Open the JSON file in write mode, which clears its contents
        with open(file_path, "w") as json_file:
            # Write an empty JSON structure (an empty dictionary)
            json.dump({}, json_file)
        print(f"Contents of {file_path} cleared successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


############################################################


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")


frame = ttk.Frame(window)
frame.pack()

########### UNIVERSAL FIELD DATA DICT ######################

info_value = {}
entry_widgets = {}
entered_value = {}  # list for entered values
cus_entry_widgets = {}
cus_saved_entry_widgets = {}

##########################################################

info_value = saved_data.get(
    "info_value", {}
)  # Get info_value or an empty dictionary if it doesn't exist
entered_value = saved_data.get(
    "entered_value", {}
)  # Get entered_value or an empty dictionary if it doesn't exist

ic(info_value)
ic(entered_value)
##########################################################
# Info LabelFrame
info_frame = ttk.LabelFrame(frame, text="Info")
info_frame.grid(row=0, column=0)

info_fields = [
    "URL",
    "Email",
    "Token",
]

info_widgets = {}

for i, var_name in enumerate(info_fields):
    label = ttk.Label(info_frame, text=var_name.capitalize() + ":")
    label.grid(row=i, column=0, sticky="ew")

    # Create a regular Entry widget for other variables
    entry = ttk.Entry(info_frame)

    entry.grid(row=i, column=1)
    info_widgets[var_name] = entry


##############################
def set_path(entry_field):
    path = filedialog.askopenfilename()
    entry_field.delete(0, tk.END)
    entry_field.insert(0, path)


csv_label = ttk.Label(info_frame, text="CSV File")
csv_label.grid(row=0, column=3)
csv_entry = ttk.Entry(info_frame)
csv_entry.grid(row=0, column=4)

btn_get_path = ttk.Button(
    info_frame, text="Select File", command=lambda: set_path(csv_entry)
)
btn_get_path.grid(row=1, column=4)


############# DEFAULT FIELD FRAME ##########################

# Fields LabelFrame
fields_frame = ttk.LabelFrame(frame, text="Default Fields")
fields_frame.grid(row=1, column=0, padx=10, pady=10)

variables = [
    "fulfillment_date",
    "commodity",
    "volume",
    "price",
    "asset",
    "status",
    "final_delivery",
    "subleg_id",
    "external _id",
    "external_source",
    "custom_field_name",
]

####### CREATE VALUE INPUT FRAME #####################

for i, var_name in enumerate(variables):
    label = ttk.Label(fields_frame, text=var_name.capitalize() + ":")
    label.grid(row=i, column=0, sticky="ew")

    # Create a regular Entry widget for other variables
    entry = ttk.Entry(fields_frame)

    entry.grid(row=i, column=1)
    entry_widgets[var_name] = entry

################# dark/ light mode #########################

# add dark/light mode toggle
mode_switch = ttk.Checkbutton(frame, text="Theme", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

############################################################

cusfields_frame = ttk.LabelFrame(frame, text="Custom Fields")
cusfields_frame.grid(row=1, column=1, padx=10, pady=10)


def add_entry(frame, widget, key=None, value=None):
    custom_label = ttk.Entry(frame)
    custom_label.grid(row=len(widget), column=0)
    custom_value = ttk.Entry(frame)
    custom_value.grid(row=len(widget), column=1)

    if key is not None and key != "":
        custom_label.insert(0, key)
    if value is not None and value != "":
        custom_value.insert(0, value)

    # Store the new entry widgets with descriptive keys (use label text as key)
    widget[custom_label] = custom_value
    # ic(cus_entry_widgets)


add_button = ttk.Button(
    cusfields_frame,
    text="Add Entry",
    command=lambda: add_entry(cusfields_frame, cus_entry_widgets),
)
add_button.grid(row=15, column=0)


####### GET VALUES FROM BUTTON ###################


def get_values(widget, entered_values):
    for var_name, entry_widget in widget.items():
        value = entry_widget.get()
        if value is not None and value != "":
            entered_values[var_name] = value

    # Now, you can print the formatted values
    print("Formatted Entered Values:")
    ic(entered_values)


def get_custom_values(w, entered_values):
    for cus_label, cus_value in w.items():
        label = cus_label.get()
        value = cus_value.get()

        if label is not None and label != "":
            if value is not None and value != "":
                entered_values[label] = value

    # ic(entered_values)


def get_all_values():
    get_values(info_widgets, entered_values=info_value)
    get_values(entry_widgets, entered_values=entered_value)
    get_custom_values(cus_entry_widgets, entered_values=entered_value)


get_values_button = ttk.Button(
    fields_frame,
    text="Get Values",
    command=lambda: get_all_values(),
)
get_values_button.grid(row=len(variables), column=0)

############# CLEAR ALL BUTTON #############################


def clear_fields(widget, database=None):
    for key, value in widget.items():
        if isinstance(key, ttk.Entry):
            key.delete(0, "end")
        if isinstance(value, ttk.Entry):
            value.delete(0, "end")

    if database is not None:
        database.clear()


def clear_all_fields():
    clear_fields(entry_widgets, entered_value)
    clear_fields(cus_entry_widgets, entered_value)
    clear_json_file(filename)


clear_fields_button = ttk.Button(
    fields_frame, text="Clear Fields", command=clear_all_fields
)
clear_fields_button.grid(row=len(variables), column=1)

########### STORE ENTERED VALUES DATA #######################


# Function to save the data as JSON
def save_data_as_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file)


# Function to load data from JSON and populate tkinter Entry widgets
def load_data_from_json(filename):
    with open(filename, "r") as json_file:
        loaded_data = json.load(json_file)
        for key, value in loaded_data.items():
            if key in entry_widgets:
                entry_widgets[key].delete(0, "end")
                entry_widgets[key].insert(0, value)


def load_data_from_saved(loaded_data, widget):
    for key, value in loaded_data.items():
        if key in widget:
            widget[key].delete(0, "end")
            widget[key].insert(0, value)


def load_custom_data_from_saved(loaded_data, filter_variables, widget):
    filtered_data = {}
    for key, value in loaded_data.items():
        if key not in filter_variables:
            filtered_data[key] = value

    for idx, (key, value) in enumerate(filtered_data.items()):
        add_entry(cusfields_frame, cus_entry_widgets, key, value)

    ic(filtered_data)


# Example usage to save data as JSON (you can call this when the script exits)
window.protocol("WM_DELETE_WINDOW", lambda: on_closing())


# Define the on_closing function
def on_closing():
    # Saved all data in the same load
    all_data = {"info_value": info_value, "entered_value": entered_value}
    save_data_as_json(all_data, filename)
    # save_data_as_json(cus_entry_widgets, filename)
    window.destroy()


# Example usage to load data from JSON into Entry widgets (you can call this at the script's start)
load_data_from_saved(info_value, info_widgets)
load_data_from_saved(entered_value, entry_widgets)
load_custom_data_from_saved(entered_value, variables, cus_entry_widgets)

#############################################################

window.mainloop()
