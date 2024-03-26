from typing import Any, Literal

from .base_class import BaseSchema, BaseSchemaFromDB


class DefaultFieldOut(BaseSchema):
    key: str
    label: str
    type: Literal["text", "number", "time"]
    required: bool


class SelectFieldOut(BaseSchema):
    key: str
    label: str
    type: Literal["select"]
    options: list[str]
    required: bool


class InfoFieldOut(BaseSchema):
    label: str
    type: Literal["info"]
    value: str


class GroupFieldsOut(BaseSchema):
    label: str
    fields: list[DefaultFieldOut | SelectFieldOut | InfoFieldOut]


class GroupsFieldOut(BaseSchema):
    label: str
    type: Literal["groups"]
    groups: list[GroupFieldsOut]


class TeamSurveysOut(BaseSchemaFromDB):
    main_fields: list[DefaultFieldOut | SelectFieldOut | GroupsFieldOut]
    add_fields: list[DefaultFieldOut | SelectFieldOut | GroupsFieldOut]


class TeamSurveysAddFieldsUpdateIn(BaseSchema):
    add_fields: list[DefaultFieldOut | SelectFieldOut | GroupsFieldOut]


class SportsmanAnswerOut(BaseSchema):
    key: str
    value: Any


class SportsmanSurveysOut(BaseSchemaFromDB):
    answers: list[SportsmanAnswerOut]
    survey: TeamSurveysOut
