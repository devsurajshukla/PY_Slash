from math_utils import add, subtract, divide, multiply

result1 = add(10, 5)
result2 = subtract(10, 5)
result3 = multiply(10, 5)
try:
    result4 = divide(10, 0)
except ValueError as e:
    result4 = str(e)

print("Addition:", result1)
print("Subtraction:", result2)
print("Multiplication:", result3)
print("Division:", result4)
