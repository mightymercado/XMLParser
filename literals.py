from __future__ import annotations
from exceptions import CannotCastToBool, CannotCastToString, CannotCastToInteger

class String(str):
    # Don't cast to bool
    def __bool__(self):
        raise CannotCastToBool()
        
class Integer(int):
    # True div to integer div
    def __truediv__(self, other) -> Integer:
        if isinstance(other, Integer):
            return Integer(self // other)
        raise ValueError()

    # Don't cast to bool
    def __bool__(self):
        raise CannotCastToBool()