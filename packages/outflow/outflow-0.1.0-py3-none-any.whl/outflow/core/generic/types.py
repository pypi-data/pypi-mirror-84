# -*- coding: utf-8 -*-
from typing import Dict, NewType, Union

from typing_extensions import TypedDict

TargetOutputs = NewType("TargetOutputs", Union[Dict, None])


class TypedTargetOutputs(TypedDict):
    pass


def outputs_type_factory(type_dict=None, name="TypedTargetOutputs", *args, **kwargs):
    if type_dict is None:
        return TargetOutputs
    else:
        return TypedDict(name, type_dict)
