from string import ascii_lowercase
import re
import operator

OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
}

def compare_with_operator(A,op,B):
    op_func = OPERATORS[op]
    result = op_func(A, B)
    return result
