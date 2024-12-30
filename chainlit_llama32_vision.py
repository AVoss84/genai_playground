from typing import cast
import chainlit as cl
from utils import convert_base64, prompt_func, MyOutputParser
from pprint import PrettyPrinter
# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable
# from langchain.schema.runnable.config import RunnableConfig
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.agents import Tool, initialize_agent


@cl.on_chat_start
async def start():

    # files = await cl.AskFileMessage(
    #     content="Please upload an image file",
    #     accept=["image/png", "image/jpeg"],
    #     max_size_mb=5,
    #     timeout=180
    # ).send()

    # if files:
    #     image_file = files[0]
    #     print(type(image_file))
    #     await cl.Message(content=f"Received image: {image_file.name}").send()

    #     # Convert the image to base64
    #     # image_b64 = convert_to_base64(image_file)
    #     # print(image_b64)
  
    # template = """
    #     You are an A.I. agent to answer questions based on the text and image provided.\n{output_format}
    #     Question: {context}
    # """
    
    # parser_node = JsonOutputParser(pydantic_object=MyOutputParser)
    
    # prompt = PromptTemplate(
    #     template=template,
    #     input_variables=["context"],
    #     partial_variables={"output_format": parser_node.get_format_instructions()},
    # )

    model = ChatOllama(model="llama3.2-vision", temperature=0)
    # model = ChatOllama(model="llama3", temperature=0.2)

    chain = prompt_func | model | StrOutputParser()
    # chain = prompt | model | parser_node

    # Store the chain in the user session for later use
    cl.user_session.set("chain", chain)

    #     text = f"""
    #         You will be provided with an image of a document. 
    #         Your task is to answer the user question. 
    #         If you are unable to answer the question, please do not come up with a random answer.     
    #     Question: {question}
    #     """

        # query_chain = chain.invoke(
        #     {
        #     "text": text, 
        #     "image": image_file
        #     }
        # )

        # pprint.pprint(query_chain)



# @cl.on_chat_start
# async def on_chat_start():

#     model = ChatOllama(model="llama3.2-vision", temperature=0)
#     # model = ChatOpenAI(streaming=True)
#     # prompt = ChatPromptTemplate.from_messages(
#     #     [
#     #         (
#     #             "system",
#     #             "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
#     #         ),
#     #         ("human", "{question}"),
#     #     ]
#     # )
#     runnable = prompt | model | StrOutputParser()
#     cl.user_session.set("runnable", runnable)


# @cl.on_message
# async def on_message(message: cl.Message):
#     runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

#     msg = cl.Message(content="")

#     async for chunk in runnable.astream(
#         {"question": message.content},
#         config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
#     ):
#         await msg.stream_token(chunk)

#     await msg.send()


@cl.on_message
async def on_message(msg: cl.Message):

    # Retrieve the stored chain from the user session
    chain = cl.user_session.get("chain")

    if chain is None:
        await cl.Message(content="Error: Chain not initialized. Please restart the chat session.").send()
        return

    print("User sent:", msg.content)

    # Check if the user sent any file attachments
    images = [file for file in (msg.elements or []) if "image" in file.mime]

    try:
        # Prepare query input
        query_input = {}
        if msg.content:
            query_input["text"] = f"Question: {msg.content}"
        if images:
            with open(images[0].path, "rb") as f:
                query_input["image"] = convert_base64(f.read())

        # Call the chain
        response = chain.invoke(query_input)
        
        print("\nResponse:")
        PrettyPrinter(indent=2).pprint(response)

        # parsed_response = StrOutputParser().parse(response)
        # print(f"Parsed response: {parsed_response}")

        # Process the response
        if isinstance(response, dict) and "answer" in response:
            await cl.Message(content=f"Answer: {response['answer']}").send()
        elif isinstance(response, str):
            await cl.Message(content=f"Answer: {response}").send()
        else:
            await cl.Message(content="Unexpected response format from the chain.").send()

    except Exception as e:
        print(f"Error processing message: {e}")
        await cl.Message(content="An error occurred while processing your request. Please try again.").send()
