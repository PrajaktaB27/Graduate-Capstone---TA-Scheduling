from enum import Enum
from typing import List
from src.schemas.StudentResponse import Grade

def translate(data: List[dict]) -> List[dict]:
    """
    Util to translate enums to be represented as string names

    :param: data: a list of dictionaries
    """
    for dictionary in data:
        for k in dictionary:
            #translate if it is an enum, else move on.
            if isinstance(dictionary[k], Enum):
                dictionary[k] = dictionary[k].__str__()

    return data