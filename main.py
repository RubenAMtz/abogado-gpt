from constants import ARTICLE_PATTERN_A, ARTICLE_PATTERN_B, ARTICLE_PATTERN_C, ARTICLE_PATTERN_D, ARTICLE_PATTERN_E, \
	INFORME_OFICIAL_HOMOLOGADO
from keys import openai_key
import os
import openai
from langchain.llms import AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PDFMinerLoader
from langchain.vectorstores import Chroma
from splitters.splitters import ArticleSplitter
from langchain.chains import RetrievalQA
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent

import os
import openai
openai.api_type = "azure"
openai.api_base = "https://openai-acs.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = openai_key

response = openai.Completion.create(
  engine="ChatGPT",
  prompt="Confirm that this is a test",
  temperature=1,
  max_tokens=100,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  best_of=1,
  stop=None)

print(response)

os.environ['OPENAI_API_TYPE'] = "azure"
os.environ['OPENAI_API_KEY'] = openai_key
os.environ['OPENAI_API_BASE'] = "https://openai-acs.openai.azure.com/"
os.environ['OPENAI_API_VERSION'] = "2022-12-01"

# os.environ['OPENAI_API_VERSION'] = "2023-03-15-preview"
# deployment_name = 'text-davinci-003'
deployment_name = 'GPT_351'
# deployment_name = 'gpt-35-turbo'
# model_name = 'gpt-35-turbo'


# load Chroma
embeddings = OpenAIEmbeddings(model='embeddings', chunk_size=1)
chroma_db = 'chromadb'
if os.path.exists(chroma_db):
	print('loading Chroma db')
	db = Chroma(persist_directory=chroma_db, embedding_function=embeddings, collection_name='abodago_gpt')
else:
	print('creating Chroma db')
	# load the text
	loader = PDFMinerLoader('docs/leydetransito.pdf')
	# load custom splitter
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_A)
	# split the text
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db = Chroma.from_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": 'ley de transito'} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/leyseguridadpublica.pdf')
	# load custom splitter
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_B)
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "ley de seguridad publica"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/codigo_penal_del_estado_de_sonora.pdf')
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_A)
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "codigo penal"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/LEY NACIONAL DE EJECUCIÓN PENAL.pdf')
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_D)
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "ley nacional de ejecución penal"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/Ley de Control Vehicular para el Estado de Sonora.pdf')
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_B)
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "ley de control vehicular"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/Bando de Policía y Gobierno para el Municipio de Hermosillo.pdf')
	# load custom splitter
	text_splitter = ArticleSplitter(pattern=ARTICLE_PATTERN_E)
	# split the text
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "bando de policia y gobierno"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')
	# add texts to the db
	loader = PDFMinerLoader('docs/LINEAMIENTOS_INFORME_POLICIAL_HOMOLOGADO__IPH_.pdf')
	# load custom splitter
	text_splitter = ArticleSplitter(pattern=INFORME_OFICIAL_HOMOLOGADO)
	# split the text
	texts, articles = text_splitter.split_text(loader.load()[0].page_content)
	db.add_texts(texts, embedding=embeddings, metadatas=[{"article": art, "source": "informe oficial homologado"} for art in articles], persist_directory=chroma_db, collection_name='abodago_gpt')


llm = AzureOpenAI(temperature=0, deployment_name=deployment_name, streaming=False, max_tokens=500, verbose=True)
retriever = RetrievalQA.from_chain_type(
	llm=llm, 
	chain_type="stuff",
	verbose=False,
	retriever=db.as_retriever(search_kwargs={"k": 5}, search_type="mmr")
)

# tool_description = "Usa esta herramienta para responder preguntas usando las leyes de Sonora. Si el usuario dice 'preguntale a la ley' usa esta herramienta para obtener la respuesta. Esta herramienta también puede ser usada para responder preguntas de seguimiento."
tool_description = "Use this tool to answer questions about the laws and corresponding articles of Sonora. If the user says 'ask the law' use this tool to get the answer. This tool can also be used to answer follow up questions."
tools = [Tool(
	func=retriever.run,
	description=tool_description,
	name='Laws of Sonora',
)]

memory = ConversationBufferWindowMemory(
	memory_key="chat_history", # import to align with agent prompt
	human_prefix="User: ",
	ai_prefix="Agent: ",
	k=5,
	return_messages=True
)

conversational_agent = initialize_agent(
	agent='chat-conversational-react-description',
	tools=tools,
	llm=llm,
	verbose=False,
	max_iterations=3,
	early_stopping_method='generate',
	memory=memory,
	streaming=True,
)

# create a loop to interact with the agent
while True:
	# user_input = input("User: ")
	# same as above but input should be printed in green
	user_input = input("\033[92mUser: \033[0m")
	if user_input == "exit":
		break
	response = conversational_agent.run(user_input)
	# print("Agent: ", response)
	# same as above but response should be printed in blue
	print("\033[94mAgent: \033[0m", response)