from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import create_retrieval_chain
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json

def pdf_extract(filepath) :

    try:

        api_key = ""

        llm = ChatOpenAI(api_key=api_key)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are world class technical documentation writer."),
            ("user", "{input}")
        ])


        output_parser = StrOutputParser()

        chain = prompt | llm | output_parser

        loader = PyPDFLoader(filepath)
        docs = loader.load_and_split()

        embeddings = OpenAIEmbeddings(api_key=api_key)



        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        vector = FAISS.from_documents(documents, embeddings)

        print("Vector loaded")


        prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}""")

        document_chain = create_stuff_documents_chain(llm, prompt)


        document_chain.invoke({
            "input": "how can langsmith help with testing?",
            "context": [Document(page_content="langsmith can let you visualize test results")]
        })

        print("Chain invoked")


        retriever = vector.as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)

        response = retrieval_chain.invoke({"input": "get all transactions data in json format"})

        print("Got response")


        transactions = json.loads(response["answer"])["transactions"]

        # print(transactions)

        responsedata = []

        for transaction in transactions :
            print(transaction)
            transdata = {}
            transdata["description"] = transaction["Description"]
            if transaction["Debit"]:
                transaction["Debit"] = transaction["Debit"].replace(",","")
            
            if transaction["Credit"]:
                transaction["Credit"] = transaction["Credit"].replace(",","")

            if transaction["Credit"] == "" :
                print("First")
                transdata["amount"] = int(float(transaction["Debit"]))
                transdata["transtype"] = "Expense" 
            elif int(float(transaction["Credit"])) == 0 :
                print("Second")
                transdata["amount"] = int(float(transaction["Debit"]))
                transdata["transtype"] = "Expense" 
            else :
                print("Third")
                transdata["amount"] = int(float(transaction["Credit"]))
                transdata["transtype"] = "Income" 

            responsedata.append(transdata)
        # print(responsedata)
        return responsedata
    except Exception as e :
        print(e)
        return e