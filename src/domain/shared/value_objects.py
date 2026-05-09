# src/domain/shared/value_objects.py

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    
    def __eq__(self, value):
        if not isinstance(value, self.__class__):
            return False
        return self.__dict__ == value.__dict__
    
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    
    def __repr__(self):
        return self.__str__()
