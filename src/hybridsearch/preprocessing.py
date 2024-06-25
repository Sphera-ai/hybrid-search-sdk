from __future__ import annotations

import fitz  # PyMuPDF
import pypdf as pypdf


def preprocess_text(
    pdf_path: str, chunk_size: int = 1000, overlap_size=200
) -> list[str]:
    """
    This function preprocesses the pdf file and returns a list of strings
    containing the text of each page, split in chunks

    :param pdf_path: str, required -> Path to the pdf file
    :param chunk_size: int, optional -> Size of the chunks
    :param overlap_size: int, optional -> Size of the overlap between chunks
    :return: list[str]
    """

    pdf = pypdf.PdfReader(pdf_path)
    text = [page.extract_text() for page in pdf.pages]
    # TODO: should clean the text from special characters

    # chunk the text of each page with overlap
    chunks = [
        page[i : i + chunk_size]
        for page in text
        for i in range(0, len(page), chunk_size - overlap_size)
    ]

    return chunks


def preprocess_image(image_path: str):
    """
    This function preprocesses extract iamges from a pdf file
    and returns a list of images

    :param image_path: str, required -> Path to the image file
    :return: list[image]

    """
    pass


def extract_text_with_metadata(pdf_path):
    """
    Extract text from a PDF file along with page and line information.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        list: A list of dictionaries containing page number, line number, and text.
    """
    doc = fitz.open(pdf_path)
    data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if line.strip():  # Ignore empty lines
                data.append(
                    {
                        "page": page_num + 1,
                        "line_num": line_num + 1,
                        "text": line.strip(),
                    }
                )

    return data


def create_chunks_by_words(data, chunk_size, overlap_size):
    """
    Create chunks of text ensuring each chunk starts and ends with a complete word, with overlapping.

    Args:
        data (list): A list of dictionaries containing page number, line number, and text.
        chunk_size (int): Desired chunk size in terms of number of words.
        overlap_size (int): Desired overlap size in terms of number of words.

    Returns:
        list: A list of dictionaries containing page number, start line, end line, and text chunk.
    """
    chunks = []
    current_chunk = []
    current_page = data[0]["page"]
    start_line = data[0]["line_num"]
    word_count = 0

    for i, entry in enumerate(data):
        words = entry["text"].split()
        current_chunk.extend(words)
        word_count += len(words)

        if word_count >= chunk_size:
            chunk_text = " ".join(current_chunk[:chunk_size])
            end_line = entry["line_num"]
            chunks.append(
                {
                    "page": current_page,
                    "start_line": start_line,
                    "end_line": end_line,
                    "text": chunk_text,
                }
            )
            current_chunk = current_chunk[chunk_size - overlap_size :]
            word_count = len(current_chunk)
            current_page = entry["page"]
            start_line = entry["line_num"]

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append(
            {
                "page": current_page,
                "start_line": start_line,
                "end_line": data[-1]["line_num"],
                "text": chunk_text,
            }
        )

    return chunks


def create_chunks_by_characters(data, chunk_size, overlap_size):
    """
    Create chunks of text ensuring each chunk starts and ends with a complete word, with overlapping.

    Args:
        data (list): A list of dictionaries containing page number, line number, and text.
        chunk_size (int): Desired chunk size in terms of number of characters.
        overlap_size (int): Desired overlap size in terms of number of characters.

    Returns:
        list: A list of dictionaries containing page number, start line, end line, and text chunk.
    """
    chunks = []
    current_chunk = ""
    current_page = data[0]["page"]
    start_line = data[0]["line_num"]
    char_count = 0

    for i, entry in enumerate(data):
        text = entry["text"]
        current_chunk += text + " "
        char_count += len(text) + 1  # Include space

        if char_count >= chunk_size:
            chunk_text = current_chunk[:chunk_size].rsplit(" ", 1)[0]
            end_line = entry["line_num"]
            chunks.append(
                {
                    "page": current_page,
                    "start_line": start_line,
                    "end_line": end_line,
                    "text": chunk_text,
                }
            )
            current_chunk = current_chunk[len(chunk_text) - overlap_size :].lstrip()
            char_count = len(current_chunk)
            current_page = entry["page"]
            start_line = entry["line_num"]

    if current_chunk.strip():
        chunks.append(
            {
                "page": current_page,
                "start_line": start_line,
                "end_line": data[-1]["line_num"],
                "text": current_chunk.strip(),
            }
        )

    return chunks


def process_pdf_to_chunks(pdf_path, chunk_size, overlap_size, mode="words"):
    """
    Process a PDF file to create chunks of text with page and line metadata, and overlapping.

    Args:
        pdf_path (str): Path to the PDF file.
        chunk_size (int): Desired chunk size in terms of number of words or characters.
        overlap_size (int): Desired overlap size in terms of number of words or characters.
        mode (str): Mode of chunking ('words' or 'characters').

    Returns:
        list: A list of dictionaries containing page number, start line, end line, and text chunk.
    """
    data = extract_text_with_metadata(pdf_path)

    if mode == "words":
        chunks = create_chunks_by_words(data, chunk_size, overlap_size)
    elif mode == "characters":
        chunks = create_chunks_by_characters(data, chunk_size, overlap_size)
    else:
        raise ValueError("Mode must be 'words' or 'characters'")

    return chunks


# # Example usage
# pdf_path = "/home/prasanna/Documents/hybrid-search-sdk/tests/test.pdf"
# chunk_size = 100  # Set the desired chunk size
# overlap_size = 20  # Set the desired overlap size
# mode = "words"  # or 'characters'

# chunks = process_pdf_to_chunks(pdf_path, chunk_size, overlap_size, mode)

# for chunk in chunks:
#     print(
#         f"Page: {chunk['page']}, Start Line: {chunk['start_line']}, End Line: {chunk['end_line']}\n{chunk['text']}\n"
#     )

#     if chunk["page"] == 10:
#         break
