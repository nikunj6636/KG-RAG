import os
import sys
import warnings
warnings.filterwarnings('ignore')

from langchain import hub
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-4o-mini")
prompt_text = """Answer the following question strictly based on the provided context. Do not use any external knowledge or make assumptions beyond the context provided. If the answer is not directly in the context, respond with 'The information is not available in the provided context.'"""


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main(dir_path):
    docs = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(dir_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                docs.append(Document(page_content=content))

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain


if __name__ == "__main__":
    n = len(sys.argv)
    if n < 2:
        print('Provide folder name!')
    else:
        dir_path = sys.argv[1]
        rag_chain = main(dir_path)

        try:
            while True:
                print("Enter question (press Ctrl+D to exit):")
                question = input()
                full_prompt = f"{prompt_text}\n\nQuestion: {question}"
                response = rag_chain.invoke(full_prompt)
                print(f'{response}\n')
        except EOFError:
            print("\nExiting. Goodbye!")
