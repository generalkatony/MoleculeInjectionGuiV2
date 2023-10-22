import tkinter as tk
from tkinter import ttk, filedialog
import json


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
########### UNIVERSAL DATA DICT ############################
entry_widgets = {}
entered_value = []  # list for entered values
############################################################
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


for i, var_name in enumerate(variables):
    label = ttk.Label(fields_frame, text=var_name.capitalize() + ":")
    label.grid(row=i, column=0, sticky="ew")

    # Create a regular Entry widget for other variables
    entry = ttk.Entry(fields_frame)

    entry.grid(row=i, column=1)
    entry_widgets[var_name] = entry


def get_values():
    for var_name, entry_widget in entry_widgets.items():
        value = entry_widget.get()
        if value is not None and value != "":
            entered_value.append({var_name, value})

    ########## PRINT WITH FORMAT ##################################

    formatted_value = []
    # Format the values and append to the formatted_values list
    for var_name, value in entered_value:
        formatted_value.append(f"{var_name.capitalize()}: {value}")

    # Now, you can print the formatted values
    print("Formatted Entered Values:")
    for formatted_value in formatted_value:
        print(formatted_value)


###############################################################

get_values_button = ttk.Button(fields_frame, text="Get Values", command=get_values)
get_values_button.grid(row=len(variables), columnspan=2)

############################################################
# add dark/light mode toggle
mode_switch = ttk.Checkbutton(frame, text="Mode", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

############################################################

cusfields_frame = ttk.LabelFrame(frame, text="Custom Fields")
cusfields_frame.grid(row=1, column=1, padx=10, pady=10)

# Create a dictionary to store the mapping between labels and Entry widgets
cus_entry_widgets = {}


def add_entry():
    label_text = f"Custom Field {len(cus_entry_widgets) + 1}"
    custom_label = ttk.Entry(cusfields_frame)
    custom_label.grid(row=len(cus_entry_widgets), column=0)
    custom_value = ttk.Entry(cusfields_frame)
    custom_value.grid(row=len(cus_entry_widgets), column=1)
    # Store the new entry widgets with descriptive keys
    cus_entry_widgets[label_text] = (custom_label, custom_value)

    # Print the values of each entry box, if not empty
    print("Values of Custom Fields:")
    for label, (entry1, entry2) in cus_entry_widgets.items():
        value1 = entry1.get()
        value2 = entry2.get()


# Iterate and print each key-value pair in the cus_entry_widgets dictionary
for label, (entry1, entry2) in cus_entry_widgets.items():
    print(f"{label}: Label - {entry1.get()}, Value - {entry2.get()}")


add_button = ttk.Button(cusfields_frame, text="Add Entry", command=add_entry)
add_button.grid(row=15, column=0)

#############################################################


#############################################################

window.mainloop()
