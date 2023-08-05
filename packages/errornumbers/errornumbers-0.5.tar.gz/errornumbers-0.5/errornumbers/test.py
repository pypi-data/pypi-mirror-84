from errornumbers import ErrorNumber
from errornumbers.ErrorNumberFunctions import sin
import math

m_1 = ErrorNumber(49.91, 0.05)
m_2 = ErrorNumber(55.42, 0.06)
x_1 = ErrorNumber(9.7, 0.005)
x_2 = ErrorNumber(11.7, 0.005)
m_kg = m_2.minus(m_1).divided_byc(1000)
x_meter = x_2.minus(x_1).divided_byc(100)

k = m_kg.timesc(9.81).divided_by(x_meter)

print(k)

one = ErrorNumber(13.31, 0.02)
print(one.divided_byc(20).inverse())
