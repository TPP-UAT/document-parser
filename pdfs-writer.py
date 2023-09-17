from __future__ import print_function

import fitz
import re
import sys
import html
from bs4 import BeautifulSoup
from fitz import Rect

def show_pdf_divided_by_page_number_and_blocks(file_path, page_number, amount_of_block):
    doc = fitz.open(file_path)
    page = doc[page_number]
    page_text = page.get_text()

    for block_number in range(amount_of_block):
        print("Bloque # " + str(block_number) +": \n")

        line_number = 0
        for line in page_text[block_number]["lines"]:
            print("Line # " + str(line_number) +":" )
            line_number += 1

            span_number = 0
            for span in line["spans"]:
                print("Spans # " + str(span_number) + ": " + span["text"])
                span_number += 1
                # print("Font type: " + span["font"])
                # print("Font size: " + str(span["size"]))
        print("\n\n\n")
    
    # text_blocks_dict = page.get_text("dict")["blocks"]
    # unified_tsaurus_text = ""
    # for line in text_blocks_dict[6]["lines"]:
    #     for span in line["spans"]:
    #         unified_tsaurus_text = unified_tsaurus_text + span["text"]
            
    # print("unified_tsaurus_text", unified_tsaurus_text)

def union(rect1, rect2):
    """
    Combine two rectangles.
    """

    xmin = min(rect1.x0, rect2.x0)
    xmax = max(rect1.x1, rect2.x1)
    ymin = min(rect1.y0, rect2.y0)
    ymax = max(rect1.y1, rect2.y1)

    return Rect(xmin, ymin, xmax, ymax)

def modify_scientific_paper(file_path):
    doc = fitz.open(file_path)

    page = doc[0]
    text = page.get_text()

    regex = r'Uniﬁed Astronomy Thesaurus concepts:\s*((?:[^;)]+\(\d+\);\s*)+[^;)]+\(\d+\))'
    key_words_paragraph = re.findall(regex, text)
    key_to_replace = 'Uniﬁed Astronomy Thesaurus concepts: ' + key_words_paragraph[0]

    text_to_replace = page.search_for(key_to_replace)
    print("text_to_replace", text_to_replace)
     # Concatena los rectángulos en una sola entidad.
    combined_rect = union(text_to_replace[0], text_to_replace[1])

    new_text = 'Lionel Messi es un reconocido futbolista argentino que es ampliamente considerado como uno de los mejores jugadores de fútbol de todos los tiempos. Nació el 24 de junio de 1987 en Rosario, Argentina. '

    # Agrega la anotación de censura.
    page.add_redact_annot(combined_rect, new_text, fontsize=10, fontname="Times-Roman")

    page.apply_redactions()

    doc.save("test2.pdf")

def modify_scientific_paper2(file_path):
    doc = fitz.open(file_path)

    page = doc[0]
    text = page.get_text()

    regex = r'Uniﬁed Astronomy Thesaurus concepts:\s*((?:[^;)]+\(\d+\);\s*)+[^;)]+\(\d+\))'
    key_words_paragraph = re.findall(regex, text)
    key_to_replace = 'Uniﬁed Astronomy Thesaurus concepts: ' + key_words_paragraph[0]

    text_to_replace = page.search_for(key_to_replace)
     # Concatena los rectángulos en una sola entidad.
    combined_rect = union(text_to_replace[0], text_to_replace[1])

    # Creo el texto que va a ir en italica y el normal
    new_text = [
        {"text": "Unified Astronomy Thesaurus concepts:", "font": "Times-Italic", "fontsize": 10},
        {"text": "A esto es un link muy largo largo", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo1.com"},
        {"text": "B esto es un link muy largo largo", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo2.com"},
        {"text": "C esto es un link muy largo largo", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo3.com"},
        {"text": "D esto es un link muy largo largo", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo4.com"},
        {"text": "E esto es un link muy largo largo", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo5.com"},
    ]

    page.add_redact_annot(combined_rect, "")
    page.apply_redactions()

    # Make a rectangle on the available space
    # page.draw_rect(fitz.Rect(combined_rect.x0, combined_rect.y0, combined_rect.x1, combined_rect.y1), color=(0, 1, 0), width=2)  # (1, 0, 0) representa el color rojo y 2 es el ancho del borde

    # Get the position of the new combined rectangle
    text_height = 7
    x, y = combined_rect.x0, combined_rect.y0 + text_height
    x0, y0, x1, y1 = combined_rect.x0, combined_rect.y0, combined_rect.x1, combined_rect.y1

    # Iterate through text_parts and insert them with the specified styles
    count_parts = 0
    for part in new_text:
        count_parts += 1

        # Text size
        text_x = fitz.get_text_length(part["text"], fontname=part["font"], fontsize=part["fontsize"])

        # Check if the text needs to be moved to the line below
        if (x1 - (x + text_x) < 1):
            x = x0
            y += 12

        if "link" in part:
            # page.draw_rect(fitz.Rect(x, y - text_height, x + text_x, y), color=(1, 0, 0), width=2)  # (1, 0, 0) representa el color rojo y 2 es el ancho del borde
            # If a link is defined in the part, create a link annotation
            page.insert_text((x, y), part["text"], fontname=part["font"], fontsize=part["fontsize"], color=(0, 0, 1))
            link = {"kind": 2, "uri": part["link"], "from": fitz.Rect(x, y - text_height, x + text_x, y)}
            page.insert_link(link)

            # Add a semicolon after the link if not the last link
            if count_parts < len(new_text):
                page.insert_text((x + text_x + 0.5, y), ";", fontname=part["font"], fontsize=part["fontsize"])
                x += 5
        else:
            # Insert regular text
            page.insert_text((x, y), part["text"], fontname=part["font"], fontsize=part["fontsize"])
    
        # Update the position for the next part of the text
        x += text_x + 2    

    # Agrega y aplica la anotacion

    doc.save("test2.pdf")

if __name__ == "__main__":
    test_file_name = "paper.pdf"

    modify_scientific_paper2(test_file_name)
