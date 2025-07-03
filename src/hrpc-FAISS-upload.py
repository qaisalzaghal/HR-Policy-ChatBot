from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

# https://www.hrhelpboard.com/hr-policies.html
# wget -r -A.html -P hr-policies https://www.hrhelpboard.com/hr-policies.html
def upload_htmls():
    """
    this function do ..
    1. reads recursively through the given folder hr-policies (without current folder)
    2. load the pages (Documents)
    3. loaded document are split into chuncks using splitter
    4. these chuncks are converted into language Embeddings and loaded as vectors into a local vector DataBase
    """

    # load all the HTML pages in the given folder structure using DirectoryLoader
    loader = DirectoryLoader(path="./hr-policies",glob="**/*.html")
    documents = loader.load()
    print(f"{len(documents)} pages loaded")

    # Split loaded document into Chuncks using CharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                    chunk_overlap=50,
                                                    separators=["\n\n", "\n", " ", ""]
                                                    )
    
    split_documents = text_splitter.split_documents(documents)
    print(f"Split into {len(split_documents)} Documrents...")

    print(split_documents[0].metadata)

    # Upload chuncks as vector embedding into FAISS
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(split_documents, embeddings)

    # Save the FAISS vector database to disk
    db.save_local("faiss_index")


def faiss_query():
    """
    this function dose the dolowing:
    1. load the local FAISS vector database
    2. Trigger a semantic search using a query
    3. this retrieves semantically matching vectors from the database
    """

    embeddings = OpenAIEmbeddings()
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    query = "Explain the Candidate Onboarding process"
    docs = new_db.similarity_search(query)

    # print all the extracted vectors from the above query

    for doc in docs:
        print("##---------page ------##")
        print(doc.metadata["source"])
        print("##---------content ------##")
        print(doc.page_content)


if __name__ == "__main__":
    # the below code 'upload_htmls()' is excecuted only once and then commented as the vector database is saved
    # experiments 
    #upload_htmls()
    # the below function is experimental to trigger a semantic search on the vector DB

    faiss_query() 