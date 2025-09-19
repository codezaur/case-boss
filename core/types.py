from enum import Enum


class CaseType(Enum):
    CAMEL = "camel"  # eg. youShallNotPass
    KEBAB = "kebab"  # eg. you-shall-not-pass
    PASCAL = "pascal"  # eg. YouShallNotPass
    SNAKE = "snake"  # eg. you_shall_not_pass
    SPACE = "space"  # eg. you shall not pass
    START = "start"  # eg. You Shall Not Pass
