import os

print("os.getcwd() =", os.getcwd())
print("os.path.dirname(__file__) =", os.path.dirname(__file__))
print("os.path.abspath(__file__) =", os.path.abspath(__file__))
print("os.path.dirname(os.path.abspath(__file__)) =", os.path.dirname(os.path.abspath(__file__)))


