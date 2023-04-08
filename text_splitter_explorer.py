from langchain.document_loaders import PDFMinerLoader
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from splitters.splitters import ArticleSplitter
from constants import ARTICLE_PATTERNS, ARTICLE_PATTERN_A, ARTICLE_PATTERN_B, ARTICLE_PATTERN_C, ARTICLE_PATTERN_D, ARTICLE_PATTERN_E, INFORME_OFICIAL_HOMOLOGADO

# load the text

loader = PDFMinerLoader('docs/leydetransito.pdf')
# load custom splitter
text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_A)
# split the text
texts, articles = text_splitter.split_text(loader.load()[0].page_content)

print(len(texts))

print("First \n", texts[0], articles[0])
print('\n\n')
print("Last \n",texts[-1], articles[-1])

print(articles)

longest = max(articles, key=len)
print(longest)