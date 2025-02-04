import json
import os

from dotenv import load_dotenv
import chainlit as cl
from chainlit.input_widget import Select, Slider
from langchain_chroma import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


from setting import metadata_field_info
from prompts import PROMPT


load_dotenv()
GEMENI_CHAT_MODEL = "gemini-1.5-flash-latest"
GEMENI_API_KEY = os.environ.get("GEMENI_API_KEY")
GEMENI_EMBEDDING_MODEL = "models/embedding-001"


def get_metadata(document, col):
    try:
        return document.metadata[col]

    except:
        return " "


def texted_metadata(document):
    metadata = f"""
    [Metadata]
    WMS Layer: {get_metadata(document,'title')}
    Data Source: {get_metadata(document,'source_url')}
    """
    return metadata


def get_source_documents(query):
    embeddings = GoogleGenerativeAIEmbeddings(
        google_api_key=GEMENI_API_KEY, model=GEMENI_EMBEDDING_MODEL
    )

    persist_directory = "./chroma_db"
    vectorstore = Chroma(
        persist_directory=persist_directory, embedding_function=embeddings
    )
    doc_contents = "Geospatial dataset in the Netherlands"

    llm = ChatGoogleGenerativeAI(google_api_key=GEMENI_API_KEY, model=GEMENI_CHAT_MODEL)
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectorstore,
        doc_contents,
        metadata_field_info,
        search_kwargs={"k": 5},
    )

    documents = retriever.invoke(query)

    total_documents = ""
    for idx, document in enumerate(documents):
        total_documents += f"""
        ---------------------------------------------
        ### Data {idx+1}
        {texted_metadata(document)}
        Outline: {document.page_content}
        """
    return documents, total_documents


def make_final_answers(documents):
    text_elements = []
    answer = ""
    if documents:
        for document in documents:
            source_name = document.metadata["title"]
            text_elements.append(
                cl.Text(
                    content=document.page_content + texted_metadata(document),
                    name=str(source_name),
                    display="side",
                )
            )
        source_names = [text_el.name for text_el in text_elements]

        if source_names:
            answer += f"\nWMS Layers: {', '.join(source_names)}"
        else:
            answer += "\nNo sources found"

    return cl.Message(content=answer, elements=text_elements)


@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Gemini",
            markdown_description="The underlying LLM model is **Gemini**.",
            icon="https://cdn-icons-png.flaticon.com/512/8649/8649595.png",
        )
    ]


@cl.on_chat_start
async def start_chat():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Gemini - Model",
                values=[
                    "gemini-1.5-flash-latest",
                    "gemini-1.5-pro-latest",
                ],
                initial_index=0,
            ),
            Slider(
                id="Temperature",
                label="Gemini - Temperature",
                initial=0.9,
                min=0,
                max=1,
                step=0.1,
            ),
        ]
    ).send()

    cl.user_session.set("gemini_model", settings["Model"])
    cl.user_session.set("temperature", float(settings["Temperature"]))
    actions = [
        cl.Action(
            name="analysis1",
            value="Suggest a geospatial analysis for land use data in the Netherlands.",
            label="Analyze land use data",
            payload={"value": "land_use_data"},
        ),
        cl.Action(
            name="analysis2",
            value="Can you analyze the population distribution changes across administrative districts in the Netherlands?",
            label="Analyze population distribution",
            payload={"value": "population_distribution"},
        ),
        cl.Action(
            name="analysis3",
            value="How can I analyze flood risk using geospatial data in the Netherlands?",
            label="Analyze flood risk data",
            payload={"value": "flood_risk_data"},
        ),
    ]

    await cl.Message(
        content="Please read `Readme` first for instructions!",
        actions=actions,
    ).send()

    system_content = "You are a helpful assistant."

    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": system_content}],
    )


@cl.on_settings_update
async def setup_agent(settings):
    cl.user_session.set("gemini_model", settings["Model"])
    cl.user_session.set("temperature", float(settings["Temperature"]))


async def process_query(content: str):
    message_history = cl.user_session.get("message_history", [])
    if message_history is None:
        message_history = []

    msg = cl.Message(content="")
    await msg.send()

    documents, total_documents = get_source_documents(content)
    prompt_content = PROMPT.format(document=total_documents, question=content)

    message_history.append({"role": "user", "content": prompt_content})

    model = cl.user_session.get("gemini_model", "gemini-1.5-flash-latest")
    temperature = cl.user_session.get("temperature", 0.9)

    llm = ChatGoogleGenerativeAI(
        google_api_key=GEMENI_API_KEY,
        model=model,
        temperature=temperature,
        streaming=True,
    )

    async for chunk in llm.astream(prompt_content):
        await msg.stream_token(chunk.content)

    message_history.append({"role": "assistant", "content": msg.content})
    cl.user_session.set("message_history", message_history)

    await make_final_answers(documents).send()


@cl.action_callback("analysis1")
async def on_action(action: cl.Action):
    await process_query(action.payload)


@cl.action_callback("analysis2")
async def on_action(action: cl.Action):
    await process_query(action.payload)


@cl.action_callback("analysis3")
async def on_action(action: cl.Action):
    await process_query(action.payload)


@cl.on_message
async def on_message(message: cl.Message):
    await process_query(message.content)
