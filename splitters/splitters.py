from langchain.text_splitter import TextSplitter
import re
from typing import List, Tuple
import tiktoken


class ArticleSplitter(TextSplitter):
    """Implementation of splitting text that looks at characters."""
    def __init__(self, pattern=r'ARTICULO \d+.-'):
        """Initialize with separator."""
        self.pattern = pattern

    def split_text(self, text: str) -> Tuple[List[str], List[str]]:
        """Split text by separator."""
        text = self.clean_text(text)
        matches = re.finditer(rf'{self.pattern}', text)
        # get the start and end positions of each match
        groups, positions = zip(*[(m.group().split('.-')[0], (m.start(0), m.end(0))) for m in matches])
        # split the document by the positions
        articulos = [text[i:j] for i, j in zip([0]+[j for i, j in positions], [i for i, j in positions]+[None])]
        # remove the first element, which is non relevant
        articulos = articulos[1:]

        # get the matching string for each articulo using the start and end positions
        articulos_number = [text[i:j].split('.-')[0] for i, j in positions]
        # lower case and remove whitespaces and dots
        articulos_number = [articulo.lower().strip('. ') for articulo in articulos_number]

        # using tiktoken evaluate the number of tokens in each articulo
        gpt_encoding = tiktoken.get_encoding('p50k_base') # encoding for text-davinci-003
        for articulo, number in zip(articulos, articulos_number):
            lenght = len(gpt_encoding.encode(articulo))
            if lenght > 4095:
                print(lenght, number, articulo)

        # remove whitespaces from the beginning and end of each articulo
        articulos = [articulo.strip() for articulo in articulos]
        return articulos, articulos_number

    def clean_text(self, text: str) -> str:
        """Clean text by removing special characters."""
        # remove all \n
        text = text.replace('\n', ' ')
        text = re.sub(' +', ' ', text)
        # remove page number, we find it because it appears before '\x0c', use regex to find it
        text = re.sub(r'\d+ \x0c', '\x0c', text)
        # remove all '\x0c'
        text = text.replace('\x0c', ' ')
        return text