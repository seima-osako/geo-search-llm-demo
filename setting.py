from langchain.chains.query_constructor.base import AttributeInfo


metadata_field_info = [
    AttributeInfo(
        name="title",
        description="The human-readable title of the WMS layer or service",
        type="string",
    ),
    AttributeInfo(
        name="authority",
        description="The organization or agency responsible for providing the data service",
        type="string",
    ),
]
