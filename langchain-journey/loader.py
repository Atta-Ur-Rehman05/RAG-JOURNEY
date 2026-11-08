#this file contain how we can load the pdf 


from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("ATTA UR REHMAN cv.pdf")

documents = loader.load()

print(f"Loaded {len(documents)} documents from the PDF.")
print(documents[0].page_content)