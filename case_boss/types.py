from enum import Enum


class CaseType(Enum):
    CAMEL = "camel"  # e.g., youShallNotPass
    KEBAB = "kebab"  # e.g., you-shall-not-pass
    PASCAL = "pascal"  # e.g., YouShallNotPass
    SNAKE = "snake"  # e.g., you_shall_not_pass
    SPACE = "space"  # e.g., you shall not pass
    START = "start"  # e.g., You Shall Not Pass
