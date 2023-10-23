import tkinter as tk
from tkinter import ttk, filedialog
import json
from icecream import ic

############## GENERAL FUNCTIONS ############################


#############################################################

window = tk.Tk()
window.title("Data Entry Form")

style = ttk.Style(window)
window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")


def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")


frame = ttk.Frame(window)
frame.pack()

##########################################################
# Info LabelFrame
info_frame = ttk.LabelFrame(frame, text="Info")
info_frame.grid(row=0, column=0)

url_label = ttk.Label(info_frame, text="URL")
url_label.grid(row=0, column=0)
url_entry = ttk.Entry(info_frame)
url_entry.grid(row=0, column=1)

email_label = ttk.Label(info_frame, text="Email")
email_label.grid(row=1, column=0)
email_entry = ttk.Entry(info_frame)
email_entry.grid(row=1, column=1)

token_label = ttk.Label(info_frame, text="Token")
token_label.grid(row=2, column=0)
token_entry = ttk.Entry(info_frame)
token_entry.grid(row=2, column=1)


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

###### INFO DICT ####################################

info_value = {}

###### GET N STORE VALUES ###########################


########### UNIVERSAL FIELD DATA DICT ######################

entry_widgets = {}
entered_value = []  # list for entered values

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
    "fill",
    "final_delivery",
    "subleg_id",
    "external _id",
    "external_source",
    "dedupe_external_id",
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
mode_switch = ttk.Checkbutton(frame, text="Mode", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

############################################################

cusfields_frame = ttk.LabelFrame(frame, text="Custom Fields")
cusfields_frame.grid(row=1, column=1, padx=10, pady=10)

# Create a dictionary to store the mapping between labels and Entry widgets
cus_entry_widgets = {}


def add_entry():
    custom_label = ttk.Entry(cusfields_frame)
    custom_label.grid(row=len(cus_entry_widgets), column=0)
    custom_value = ttk.Entry(cusfields_frame)
    custom_value.grid(row=len(cus_entry_widgets), column=1)
    # Store the new entry widgets with descriptive keys
    cus_entry_widgets.update({custom_label: custom_value})
    # ic(cus_entry_widgets)


add_button = ttk.Button(cusfields_frame, text="Add Entry", command=add_entry)
add_button.grid(row=15, column=0)


####### GET VALUES FROM BUTTON ###################
def get_values(w, entered_values):
    for var_name, entry_widget in w.items():
        value = entry_widget.get()
        if value is not None and value != "":
            entered_values.append({var_name: value})

    formatted_values = []  # Define the list for formatted values

    # Format the values and append to the formatted_values list
    for entry in entered_values:
        for var_name, value in entry.items():
            formatted_values.append(f"{var_name.capitalize()}: {value}")

    # Now, you can print the formatted values
    print("Formatted Entered Values:")
    for formatted_value in formatted_values:
        ic(formatted_value)


def get_custom_values(w, entered_values):
    for cus_label, cus_value in w.items():
        label = cus_label.get()
        value = cus_value.get()

        if label is not None and label != "":
            if value is not None and value != "":
                ic(entered_values.append({label: value}))

    formatted_values = []  # Define the list for formatted values

    # Format the values and append to the formatted_values list
    for entry in entered_values:
        for cus_text, label in entry.items():
            formatted_values.append(f"{cus_text.capitalize()}: {label}")

    # Now, you can print the formatted values
    print("Formatted Entered Values:")
    for formatted_value in formatted_values:
        print(formatted_value)


############### CREATE GET VALUE BUTTON ####################


def get_all_values():
    get_values(entry_widgets, entered_values=entered_value)
    get_custom_values(cus_entry_widgets, entered_values=entered_value)


get_values_button = ttk.Button(
    fields_frame,
    text="Get Values",
    command=lambda: get_all_values(),
)
get_values_button.grid(row=len(variables), columnspan=2)

#############################################################


#############################################################

window.mainloop()
