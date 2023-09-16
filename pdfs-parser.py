import fitz  # PyMuPDF
import re
import json
import os

# Directory containing the PDF files
pdf_directory = "PDFs/"

# Define a regex pattern to find URLs
regex = r'Uniﬁed Astronomy Thesaurus concepts:\s*((?:[^;)]+\(\d+\);\s*)+[^;)]+\(\d+\))'

concepts_dict = {}  # Dictionary to store IDs and associated files

# Loop through all files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_file = os.path.join(pdf_directory, filename)

        # Open the PDF file
        pdf_document = fitz.open(pdf_file)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            text = page.get_text()

            # Find all URLs using the regex pattern
            urls = re.findall(regex, text)

            if len(urls) > 0:
                concepts = urls[0]  # Assuming there's only one match per page

                # Utilizamos una expresión regular para encontrar todos los números entre paréntesis
                ids = re.findall(r'\((\d+)\)', concepts)

                for id in ids:
                    id_str = str(id)

                    if id_str not in concepts_dict:
                        concepts_dict[id_str] = {
                            'id': id_str,
                            'files': []
                        }

                    if pdf_file not in concepts_dict[id_str]['files']:
                        concepts_dict[id_str]['files'].append(pdf_file)

        # Close the PDF document
        pdf_document.close()

# Specify the output file path
output_file = "pdfs.json"

# Write the JSON data to the output file
with open(output_file, 'w') as json_file:
    json.dump(list(concepts_dict.values()), json_file, indent=4)

print(f"JSON data saved to {output_file}")
