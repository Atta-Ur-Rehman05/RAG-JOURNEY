# this is the charactertextsplitter pipeline

from langchain_text_splitters import CharacterTextSplitter

text = """
        microsoft is a compnay 

        
        they were established in 1900.


        they give alot of services and products to market and help and evolve the modren technologies 
"""


text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=20,
    chunk_overlap=5,
    length_function=len,
    is_separator_regex=False,
)

chunks = text_splitter.split_text(text)

for i,chunk in enumerate(chunks):
    print(len(chunk))
    print("chunk no ",i+1)
    print(chunk)
    print("\n")