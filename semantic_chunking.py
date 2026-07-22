# this file contain semanti chunking stuffs 

from langchain_text_splitters import SemanticChunker

from langchain_google_genai import GoogleGenerativeAIEmbeddings

import config

text = """
        microsoft is a compnay 


        they were established in 1900.


        they give alot of services and products to market and help and evolve the modren technologies 
"""


text_splitter = SemanticChunker(
    embeddings=GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL),
    breakpoint_threshold_type="standard",
)

chunks = text_splitter.split_text(text)

for i,chunk in enumerate(chunks):
    print(len(chunk))
    print("chunk no ",i+1)
    print(chunk)
    print("\n")
