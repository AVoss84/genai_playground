# from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
# from langchain.schema.runnable import Runnable
# from langchain.schema.runnable.config import RunnableConfig
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from typing import cast
import chainlit as cl
from utils import convert_to_base64, prompt_func
import pprint


# @cl.on_chat_start
# def on_chat_start():
#     print("A new chat session has started!")


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

    model = ChatOllama(model="llama3.2-vision", temperature=0)

    chain = prompt_func | model | StrOutputParser()

    #     question = "Give an example about the topic of section 3.1"

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

        # model = ChatOpenAI(streaming=True)
        # prompt = ChatPromptTemplate.from_messages(
        #     [
        #         (
        #             "system",
        #             "You're a very knowledgeable historian who provides accurate and eloquent answers to historical questions.",
        #         ),
        #         ("human", "{question}"),
        #     ]
        # )
        # runnable = prompt | model | StrOutputParser()
        # cl.user_session.set("runnable", runnable)



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
    if not msg.elements:
        await cl.Message(content="No file attached").send()
        return

    # Processing images exclusively
    images = [file for file in msg.elements if "image" in file.mime]

    # Read the first image
    with open(images[0].path, "r") as f:
        pass

    await cl.Message(content=f"Received {len(images)} image(s)").send()

