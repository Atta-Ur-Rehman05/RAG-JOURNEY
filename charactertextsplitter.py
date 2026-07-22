# this is the charactertextsplitter pipeline

from langchain_text_splitters import CharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter

text = """
        microsoft is a compnay 


        they were established in 1900.


        they give alot of services and products to market and help and evolve the modren technologies 
"""


# text_splitter = CharacterTextSplitter(
#     separator="\n\n",
#     chunk_size=20,
#     chunk_overlap=5,
#     length_function=len,
#     is_separator_regex=False,
# )

# chunks = text_splitter.split_text(text)

# for i,chunk in enumerate(chunks):
#     print(len(chunk))
#     print("chunk no ",i+1)
#     print(chunk)
#     print("\n")


    # draw backs of charactertextsplitter
    # it does not support multiple separator 
    # 1. it split the text on the basis of characters
    # 2. it does not consider the meaning of the text
    # 3. it does not consider the context of the text
    # 4. it does not consider the structure of the text
    # 5. it does not consider the semantic meaning of the text
    # 6. it does not consider the syntactic meaning of the text
    # 7. it does not consider the pragmatic meaning of the text
    # 8. it does not consider the semantic meaning of the text
    # 9. it does not consider the syntactic meaning of the text
    # 10. it does not consider the pragmatic meaning of the text
    # 

text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " "],
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

    # advantages of recursive character text splitter
    # 1. it support multiple separator 
    # 2. it split the text on the basis of characters
    # 3. it does not consider the meaning of the text
    # 4. it does not consider the context of the text
    # 5. it does not consider the structure of the text
    # 6. it does not consider the semantic meaning of the text
    # 7. it does not consider the syntactic meaning of the text
    # 8. it does not consider the pragmatic meaning of the text
    # 9. it does not consider the semantic meaning of the text
    # 10. it does not consider the syntactic meaning of the text
    # 11. it does not consider the pragmatic meaning of the text