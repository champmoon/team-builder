from typing import Any, Literal

ExampleKeys = Literal["example", "examples"]
ExampleValues = dict[str, Any] | list[dict[str, Any]]


ContentKeys = Literal["content"]
ContentType = Literal["application/json"]
ContentValues = dict[
    ContentType,
    dict[
        ExampleKeys,
        ExampleValues,
    ],
]


DescriptionKeys = Literal["description"]
DescriptionValues = str


ResponsesKeys = Literal["responses"]
ResponsesValues = dict[
    int,
    dict[
        ContentKeys | DescriptionKeys,
        ContentValues | DescriptionValues,
    ],
]


SummaryKeys = Literal["summary"]
SummaryValues = str


DocsKeys = SummaryKeys | DescriptionKeys | ResponsesKeys
DocsValues = SummaryValues | DescriptionValues | ResponsesValues

Docs = dict[DocsKeys, DocsValues]
