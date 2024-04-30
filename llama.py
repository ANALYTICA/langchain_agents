from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain import hub
from langchain.chains import LLMChain, RetrievalQA
from langchain.globals import set_debug
from langchain.prompts import PromptTemplate
import langchain
import os 
langchain.verbose = True

def load_model():
    for model in os.listdir("./persist/model"):
        model_file = model
    print("using model ", model_file)
    model = LlamaCpp(
        model_path="./persist/model/" + model,
        n_ctx=2048,
        temperature=0.0,
        max_tokens=2000,
        top_p=1,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
        verbose=True,  # Verbose is required to pass to the callback manager
    )

    return model

def get_retriever():
    txt = []
    pdf = []
    for f in os.listdir("./persist/documents"):
        if os.path.splitext(f)[1] == ".txt":
            txt.append(f)
        if os.path.splitext(f)[1] == ".pdf":
            pdf.append(f)
    if len(txt) > 0 or len(pdf) > 0:
        print("Documents found, vectorizing . . .")
        directory = "./persist/documents/"
        loaders = []
        for f in txt:
            loaders.append(TextLoader(directory + f,autodetect_encoding=True))
        for f in pdf:
            loaders.append(PyPDFLoader(directory + f))    

        # notice the splitting order
        r_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=50,
            separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )

        # run splitting
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        splits = r_splitter.split_documents(docs)
        print("Total Splits: ", len(splits), "\n")

        vectorstore = Chroma.from_documents(documents=splits, embedding=HuggingFaceEmbeddings(), persist_directory="./persist/vectorstore/")
        vectorstore.persist()
        print("Documents stored to database.")
    else:
        print("No documents found, looking for database . . .")
        vectorstore = Chroma(embedding_function=HuggingFaceEmbeddings(), persist_directory="./persist/vectorstore/")
        print("Database loaded.")

    print("vector store collections count: ", vectorstore._collection.count())
    retriever = vectorstore.as_retriever()
    return retriever

def raq_question(question,model,retriever):
    llm = model
    qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=retriever,
    return_source_documents=True
    )
    result = qa_chain({"query": question,"max_tokens": 1024})
    return {"result":result}

#https://stackoverflow.com/questions/76650513/dynamically-add-more-embedding-of-new-document-in-chroma-db-langchain
