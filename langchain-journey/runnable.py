# runnable : it standarize how components will be executed, and how they will be connected to each other. It is a wrapper for the components, and it will handle the input and output of the components. It will also handle the execution of the components, 
# and it will handle the connection between the components. 

# followin are the six important execution methods
# #1 invoke : it will execute the component and return the output of the component. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# #2 invoke_async : it will execute the component asynchronously and return the output of the component. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# # #3 stream : it will execute the component and return the output of the component as a stream. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# # #4 stream_async : it will execute the component asynchronously and return the output of the component as a stream. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# # #5 astream : it will execute the component asynchronously and return the output of the component as a stream. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# batch : it will execute the component and return the output of the component as a batch. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components.
# abatch : it will execute the component asynchronously and return the output of the component as a batch. It will also handle the input and output of the component. It will also handle the execution of the component, and it will handle the connection between the components. 




from langchain_core.runnables import (
    RunnableLambda,
    RunnableSequence
)

# def greet(name):
#     return f"Hello, {name}!"

# runnable = RunnableLambda(greet)

# result = runnable.invoke("atta")

# print(result)


def add_ten(x):
    return x + 10

def multiply_two(x):
    return x * 2

def subtract_five(x):
    return x - 5

step1 = RunnableLambda(add_ten)
step2 = RunnableLambda(multiply_two)
step3 = RunnableLambda(subtract_five)

chain = (       # LCEL langchain expression language
    step1
    | step2
    | step3
)

result = chain.invoke(5)

print(result)