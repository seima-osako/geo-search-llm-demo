from langchain.prompts import PromptTemplate

PROMPT = PromptTemplate(
    template="""
    You are a geospatial data analyst. Based on the following dataset information, please provide a concise suggestion on what kind of geospatial analysis can be performed using data below.
    Please provide a brief analysis suggestion in your response based on the dataset details.
    If available WMS layers exist, provide the **hyperlink** for relevant data sources (you don't need to use all datasets, and there may be duplicate sources, but with different WMS styles).
    If not, you can simply state that no relevant WMS layers were found.

    Question:
    {question}
    
    Dataset Details
    {document}

    [Output  Format]
    Analysis Suggestion:
    {{Analysis Suggestion}}

    Expected WMS Layers:
    1. {{[Layer Name](URL)}}
    2. {{[Layer Name](URL)}}
    """,
    input_variables=["document", "question"],
)
