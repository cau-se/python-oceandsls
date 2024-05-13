#  Copyright (c) 2024.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os

from chromadb.config import Settings

from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PythonLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, Language

from langchain_community.llms import GPT4All
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import StdOutCallbackHandler

#TODO check needed
from sentence_transformers import SentenceTransformer

root_dir = os.getcwd()

# TODO add pip install -U sentence-transformers chromadb langchain
# TODO downgraded pip install --upgrade chromadb==0.3.29

docs = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    for file in filenames:
        if file.endswith(".py") and "AssistantEnv" not in dirpath:
            try:
                loader = PythonLoader(os.path.join(dirpath, file))
                docs.extend(loader.load_and_split())
            except Exception as e:
                pass
print(f"{len(docs)} documents loaded.")
print("Creating vectorstore.")

text_splitter = RecursiveCharacterTextSplitter.from_language(
        chunk_size=60,
        chunk_overlap=2,
        language=Language.PYTHON,
)
texts = text_splitter.split_documents(docs)

##
# _legacy_config_values : {
#         'chromadb.api.local.LocalAPI',
#         'chromadb.db.clickhouse.Clickhouse',
#         'chromadb.db.duckdb.DuckDB',
#         'chromadb.db.duckdb.PersistentDuckDB',
#         'clickhouse',
#         'duckdb',
#         'duckdb+parquet',
#         'local',
#         'rest'
# }


CHROMA_SETTINGS = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="db",
        anonymized_telemetry=False,
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(
        documents = texts,
        embedding = embeddings,
        persist_directory="db",
        client_settings=CHROMA_SETTINGS,
)

db.persist()
db = None

print(f"Vectorstore created at {root_dir}\\db")

##

db_dir = os.getcwd() + "/db"

chroma = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings,
        client_settings=CHROMA_SETTINGS,
)

retriever = chroma.as_retriever(
        search_kwargs={
                "k": 6,
                # "fetch_k": 20, # TODO error unk
                # "maximal_marginal_relevance": True, # TODO error unk
        }
)

llm = GPT4All(
        model="orca-mini-3b-gguf2-q4_0.gguf", # /home/sgu/.cache/gpt4all/
        # n_ctx=1000, # TODO error unk
        backend="gptj",
        verbose=True,
        callbacks=[StdOutCallbackHandler()],
        n_threads=8,  # Change this according to your cpu threads
        temp=0.5,
)

qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
chat_history = []

while True:
    query = input("\nEnter a query: ")
    if query in ["quit", "q"]:
        break

    response = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, response["answer"]))