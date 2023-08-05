from errornumbers import ErrorNumber
import math

def sin(e_n):
    value = math.sin(e_n.value)
    abs_error = abs(math.cos(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)

def cos(e_n):
    value = math.cos(e_n.value)
    abs_error = abs(math.sin(e_n.value) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)

def tan(e_n):
    value = math.sin(e_n.value)/math.cos(e_n.value)
    abs_error = abs((1 / math.cos(e_n.value)) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)

def cot(e_n):
    value = math.cos(e_n.value)/math.sin(e_n.value)
    abs_error = abs((1 / math.sin(e_n.value)) * e_n.absolute_error)
    return ErrorNumber(value, abs_error)

def exp(e_n):
    value = math.e**e_n.value
    error = value * absolute_error
    return ErrorNumber(value, error)

def expbase(e_n, base):
    value = base**e_n.value
    error = value * absolute_error
    return ErrorNumber(value, error)
