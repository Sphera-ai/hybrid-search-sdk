from __future__ import annotations

import os
import re

import fitz  # PyMuPDF
import numpy as np

# import pypdf as pypdf
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TESSDATA_PREFIX"] = os.getenv("TESSDATA_PREFIX")
TESSDATA_PREFIX = os.getenv("TESSDATA_PREFIX")


class Chunking:
    """
    This class provides methods for preprocessing documents.
    """

    def document_reader(self, pdf_path):
        """
        Reads a document(PDF or txt) and extracts the content.

        Args:
            pdf_path (str): The path to the PDF document.

        Returns:
            list: A list of dictionaries containing the extracted content.
            Each dictionary has the following keys:
                - "page" (int): The page number.
                - "line_num" (int): The line number.
                - "sentence" (str): The extracted sentence.
        """

        # check if the file is a pdf
        if pdf_path.endswith(".pdf"):
            doc = fitz.open(pdf_path)
        if pdf_path.endswith(".txt"):
            with open(pdf_path) as file:
                doc = file.read()

        data = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")

            if text == "":
                text = (
                    doc[page_num]
                    .get_textpage_ocr(
                        flags=3,
                        language="ita",
                        dpi=72,
                        full=False,
                        tessdata=TESSDATA_PREFIX,
                    )
                    .extractTEXT()
                )
            lines = re.split(r"(?<=[.?!])\s+", text)

            for line_num, line in enumerate(lines):
                if line.strip():  # Ignore empty lines
                    data.append(
                        {
                            "page": page_num + 1,
                            "line_num": line_num + 1,
                            "sentence": line.strip(),
                        }
                    )

        return data


class NaiveChunking(Chunking):
    """
    A class that provides methods to create chunks of text from PDF files with overlapping.

    Args:
        pdf_path (str): Path to the PDF file.

    Attributes:
        pdf_path (str): Path to the PDF file.

    Methods:
        create_chunks_by_words(data, chunk_size, overlap_size):
            Create chunks of text ensuring each chunk starts and ends with a complete word, with overlapping.
        create_chunks_by_characters(data, chunk_size, overlap_size):
            Create chunks of text ensuring each chunk starts and ends with a complete word, with overlapping.
        create_chunks(pdf_path, chunk_size, overlap_size, mode='words'):
            Process a PDF file to create chunks of text with page and line metadata, and overlapping.
    """

    def __init__(
        self, pdf_path: str, chunk_size: int, overlap_size: int, mode: str = "words"
    ):
        """
        Initialize the Preprocessing object.

        Args:
            pdf_path (str): The path to the PDF file.
            chunk_size (int): The size of each chunk in number of words.
            overlap_size (int): The size of the overlap between chunks in number of words.
            mode (str, optional): The mode of preprocessing. Defaults to "words", ["words" or "characters"].
        """
        self.pdf_path = pdf_path
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.mode = mode

    def create_chunks_by_words(self, data, chunk_size, overlap_size):
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
            words = entry["sentence"].split()
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

    def create_chunks_by_characters(self, data, chunk_size, overlap_size):
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
            text = entry["sentence"]
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

    def create_chunks(
        self,
    ):
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
        data = self.document_reader(self.pdf_path)

        if self.mode == "words":
            chunks = self.create_chunks_by_words(
                data, self.chunk_size, self.overlap_size
            )
        elif self.mode == "characters":
            chunks = self.create_chunks_by_characters(
                data, self.chunk_size, self.overlap_size
            )
        else:
            raise ValueError("Mode must be 'words' or 'characters'")

        return chunks


class SemanticChunking(Chunking):
    def __init__(
        self,
        pdf_path: str,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        """
        Initialize the Preprocessing class.

        Args:
            pdf_path (str): The path to the PDF file.
            model_name (str, optional): The name of the sentence transformer model to use.
                Defaults to "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2".
        """
        self.pdf_path = pdf_path
        self.model = SentenceTransformer(model_name)

    def create_chunks(self):
        """
        Initializes the preprocessing module.

        This function extracts text from a PDF file, combines sentences, calculates cosine distances,
        groups sentences based on distance thresholds, and returns the grouped chunks and the original sentences.

        Returns:
            chunks (list): A list of dictionaries representing the grouped chunks of sentences.
                Each dictionary contains the following keys:
                - page (int): The page number where the chunk starts.
                - start_line (int): The line number where the chunk starts.
                - end_line (int): The line number where the chunk ends.
                - text (str): The combined text of the chunk.

            sentences (list): A list of dictionaries representing the original sentences.
                Each dictionary contains the following keys:
                - combined_sentence_embedding: The embedding of the combined sentence.
                - combined_sentence: The combined sentence text.
                - line_num: The line number of the sentence.
                - page: The page number of the sentence.
        """
        text = self.document_reader(self.pdf_path)

        sentences = self.combine_sentences(text)

        for sen in sentences:
            sen["combined_sentence_embedding"] = self.model.encode(
                sen["combined_sentence"]
            )

        distances, sentences = self.calculate_cosine_distances(sentences)

        breakpoint_distance_threshold = np.std(distances) + np.mean(distances)
        indices_above_thresh = [
            i for i, x in enumerate(distances) if x > breakpoint_distance_threshold
        ]

        # Initialize the start index
        start_index = 0

        # Create a list to hold the grouped sentences
        chunks = []

        # Iterate through the breakpoints to slice the sentences
        for index in indices_above_thresh:
            # The end index is the current breakpoint
            end_index = index

            # Slice the sentence_dicts from the current start index to the end index
            group = sentences[start_index : end_index + 1]
            combined_text = " ".join([d["sentence"] for d in group])
            start_line = group[0]["line_num"]
            end_line = group[-1]["line_num"]
            page = group[0]["page"]

            c = {
                "page": page,
                "start_line": start_line,
                "end_line": end_line,
                "text": combined_text,
            }

            chunks.append(c)

            # Update the start index for the next group
            start_index = index + 1

        # The last group, if any sentences remain
        if start_index < len(sentences):
            combined_text = " ".join([d["sentence"] for d in sentences[start_index:]])
            start_line = group[0]["line_num"]
            end_line = group[-1]["line_num"]
            page = group[0]["page"]

            c = {
                "page": page,
                "start_line": start_line,
                "end_line": end_line,
                "text": combined_text,
            }

            chunks.append(c)
            # chunks.append(combined_text)

        return chunks, sentences

    def calculate_cosine_distances(self, sentences):
        """
        Calculates the cosine distances between consecutive sentences in a list.

        Args:
            sentences (list): A list of sentences, where each sentence is represented as a dictionary.

        Returns:
            tuple: A tuple containing two elements:
                - distances (list): A list of cosine distances between consecutive sentences.
                - sentences (list): The input list of sentences with the 'distance_to_next' key added to each sentence dictionary.
        """
        distances = []
        for i in range(len(sentences) - 1):
            embedding_current = sentences[i]["combined_sentence_embedding"]
            embedding_next = sentences[i + 1]["combined_sentence_embedding"]

            # Calculate cosine similarity
            similarity = cosine_similarity([embedding_current], [embedding_next])[0][0]

            # Convert to cosine distance
            distance = 1 - similarity

            # Append cosine distance to the list
            distances.append(distance)

            # Store distance in the dictionary
            sentences[i]["distance_to_next"] = distance

        return distances, sentences

    def combine_sentences(self, sentences, buffer_size=1):
        # Go through each sentence dict
        for i in range(len(sentences)):
            # Create a string that will hold the sentences which are joined
            combined_sentence = ""

            # Add sentences before the current one, based on the buffer size.
            for j in range(i - buffer_size, i):
                # Check if the index j is not negative (to avoid index out of range like on the first one)
                if j >= 0:
                    # Add the sentence at index j to the combined_sentence string
                    combined_sentence += sentences[j]["sentence"] + " "

            # Add the current sentence
            combined_sentence += sentences[i]["sentence"]

            # Add sentences after the current one, based on the buffer size
            for j in range(i + 1, i + 1 + buffer_size):
                # Check if the index j is within the range of the sentences list
                if j < len(sentences):
                    # Add the sentence at index j to the combined_sentence string
                    combined_sentence += " " + sentences[j]["sentence"]

            # Then add the whole thing to your dict
            # Store the combined sentence in the current sentence dict
            sentences[i]["combined_sentence"] = combined_sentence

        return sentences
