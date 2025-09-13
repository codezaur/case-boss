from enum import Enum


class CaseType(Enum):
    SNAKE = "snake"  # eg. you_shall_not_pass
    CAMEL = "camel"  # eg. youShallNotPass
    PASCAL = "pascal"  # eg. YouShallNotPass
    KEBAB = "kebab"  # eg. you-shall-not-pass
    SPACE = "space"  # eg. you shall not pass
