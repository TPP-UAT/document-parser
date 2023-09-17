import fitz
import re
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

def union_rectangles(rectangles):
    """
    Combine multiple rectangles into one.
    """

    xmin = min([r.x0 for r in rectangles])
    xmax = max([r.x1 for r in rectangles])
    ymin = min([r.y0 for r in rectangles])
    ymax = max([r.y1 for r in rectangles])

    return Rect(xmin, ymin, xmax, ymax)

def get_text_length(text):
    return fitz.get_text_length(text["text"], fontname=text["font"], fontsize=text["fontsize"])

def match_text_for_replacing(text):
    # Change the regex to match documents
    regex = r'Uniﬁed Astronomy Thesaurus concepts:\s*((?:[^;)]+\(\d+\);\s*)+[^;)]+\(\d+\))'
    keys_words_paragraph = re.findall(regex, text)
    keys_to_replace = 'Uniﬁed Astronomy Thesaurus concepts: ' + keys_words_paragraph[0]
    return keys_to_replace

def create_text(page, text_to_add, combined_rect):
    # Get the position of the new combined rectangle, adding an extra line
    text_height = 7
    x, y = combined_rect.x0, combined_rect.y0 + text_height
    x0, y0, x1, y1 = combined_rect.x0, combined_rect.y0, combined_rect.x1, combined_rect.y1 + 11

    # Iterate through text_parts and insert them with the specified styles
    count_parts = 0
    for part in text_to_add:
        count_parts += 1
        is_last_one = False

        # Text size
        text_x = get_text_length(part)

        # Check if next part is the last one
        if (y1 - (y + 11) < 0.1 and x1 - (x + text_x + get_text_length(text_to_add[count_parts])) < 0.1):
            is_last_one = True
        
        # Check if the text needs to be moved to the line below
        if (x1 - (x + text_x) < 0.1):
            x = x0
            y += 11

        # Check if we exceeded the available space
        if (y1 - y < 0.1):
            break

        if "link" in part:
            # Make a rectangle on the available link space
            # page.draw_rect(fitz.Rect(x, y - text_height, x + text_x, y), color=(1, 0, 0), width=2)  # (1, 0, 0) representa el color rojo y 2 es el ancho del borde

            # If a link is defined in the part, create a link annotation
            page.insert_text((x, y), part["text"], fontname=part["font"], fontsize=part["fontsize"], color=(0, 0, 1))
            link = {"kind": 2, "uri": part["link"], "from": fitz.Rect(x, y - text_height, x + text_x, y)}
            page.insert_link(link)

            # Add a semicolon after the link if not the last link
            if count_parts < len(text_to_add) and not is_last_one:
                page.insert_text((x + text_x + 0.5, y), ";", fontname=part["font"], fontsize=part["fontsize"])
                x += 5
        else:
            # Insert regular text
            page.insert_text((x, y), part["text"], fontname=part["font"], fontsize=part["fontsize"])
    
        # Update the position for the next part of the text
        x += text_x + 2    

def modify_scientific_paper(file_path, text_to_add):
    doc = fitz.open(file_path)

    page = doc[0]
    text = page.get_text()

    keys_to_replace = match_text_for_replacing(text)
    text_to_replace = page.search_for(keys_to_replace)

    # Merge all the rectangles into one
    combined_rect = union_rectangles(text_to_replace)

    # Create a rectangle replacing the previous text
    page.add_redact_annot(combined_rect, "")
    page.apply_redactions()

    # Make a rectangle on the available space
    # page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=(0, 1, 0), width=2)  # (1, 0, 0) representa el color rojo y 2 es el ancho del borde

    create_text(page, text_to_add, combined_rect)

    # Save the document
    doc.save("test.pdf")

if __name__ == "__main__":
    test_file_name = "paper3.pdf"

    new_text = [
        {"text": "Unified Astronomy Thesaurus concepts:", "font": "Times-Italic", "fontsize": 10},
        {"text": "A esto es un link", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo1.com"},
        {"text": "B esto es un link", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo2.com"},
        {"text": "C esto es un link", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo3.com"},
        {"text": "D esto es un link", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo4.com"},
        {"text": "E esto es un link", "font": "Times-Roman", "fontsize": 10, "link": "https://www.ejemplo5.com"},
    ]

    modify_scientific_paper(test_file_name, new_text)
