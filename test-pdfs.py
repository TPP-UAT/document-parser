import fitz
import re

# Abrir el documento PDF
pdf_document = fitz.open('PDFs/Szabo_2020_ApJ_891_100.pdf')

# Inicializar una variable para almacenar el texto correspondiente a la regex
extracted_text = ''

# Expresión regular para el rango deseado, excluyendo las palabras clave
regex_pattern = r'Abstract([\s\S]*?)Uniﬁed Astronomy Thesaurus concepts:'

# Iterar a través de las páginas y buscar la regex
for page_number in range(len(pdf_document)):
    page = pdf_document[page_number]
    page_text = page.get_text()
    
    # Buscar la regex en el texto de la página actual
    match = re.search(regex_pattern, page_text)
    
    # Si se encuentra una coincidencia, agregarla a la variable de texto extraído
    if match:
        extracted_text += match.group(1)  # Usar group(1) para obtener solo el contenido entre "Abstract" y "Uniﬁed Astronomy Thesaurus concepts:"

# Imprimir o hacer lo que necesites con extracted_text
print(extracted_text)

# Cerrar el documento PDF
pdf_document.close()
