import pandas as pd
import re
import pdfx
import json

# Initialize an empty dictionary to store the JSON data
json_data = {}

def update_json_data(file_name, reference_id):
    if reference_id not in json_data:
        json_data[reference_id] = {
            "id": reference_id,
            "files": [file_name]
        }
    else:
        json_data[reference_id]["files"].append(file_name)

# List of PDF file names
pdf_files = [
    "PDFs/Czajka_2023_Planet._Sci._J._4_137.pdf",
    "PDFs/Jiang_2023_ApJL_945_L26.pdf"
]

for pdf_file in pdf_files:
    pdf = pdfx.PDFx(pdf_file)
    reference_dic = pdf.get_references_as_dict()

    for link in reference_dic['url']:
        regex = r"(https?://astrothesaurus.org/uat/\S+)"
        urls = re.findall(regex, link)
        for found in urls:
            reference_id = found.rsplit('/', 1)[-1]
            update_json_data(pdf_file, reference_id)

# Convert the dictionary to a list of JSON objects
json_list = list(json_data.values())

# Save the JSON data to a file
with open('output.json', 'w') as json_file:
    json.dump(json_list, json_file, indent=4)

# Print the JSON data
for entry in json_list:
    print(json.dumps(entry, indent=4))
