from typing import Literal
from .base_class import BaseSchema


class DefaultFieldOut(BaseSchema):
    key: str
    label: str
    type: Literal["text", "number", "bool", "time"]
    required: bool


class SelectFieldOut(BaseSchema):
    key: str
    label: str
    type: Literal["select"]
    options: list[str]
    required: bool


class TableCellsDefaultFieldOut(BaseSchema):
    key: str
    row_index: int
    column_index: int
    type: Literal["text", "number", "bool", "time"]
    required: bool


class TableCellsSelectFieldOut(BaseSchema):
    key: str
    row_index: int
    column_index: int
    type: Literal["select"]
    options: list[str]
    required: bool


class TableCellsInfoFieldOut(BaseSchema):
    key: str
    row_index: int
    column_index: int
    type: Literal["info"]
    placeholder: str


class TableFieldOut(BaseSchema):
    label: str
    type: Literal["table"]
    rows_length: int
    rows: list[str]
    columns_length: int
    columns: list[str]
    cells: list[
        TableCellsDefaultFieldOut | TableCellsSelectFieldOut | TableCellsInfoFieldOut
    ]


class TeamSurveysOut(BaseSchema):
    main_fields: list[DefaultFieldOut | SelectFieldOut | TableFieldOut]
    add_fields: list[DefaultFieldOut | SelectFieldOut | TableFieldOut]


class TeamSurveysAddFieldsUpdateIn(BaseSchema):
    add_fields: list[DefaultFieldOut | SelectFieldOut | TableFieldOut]
