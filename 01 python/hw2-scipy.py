import numpy as np

A = np.mat('[1 2;3 4]')
print(A)
print(A.I)
b = np.mat('[5 6]')
print(b)
print(b.T)
print(A * b.T)

print()
from scipy import linalg

a = np.array([[1, 2], [3, 4]])
print(A)
b = np.array([[5],[6]])
print(b)
print(linalg.inv(A).dot(b))
print(A.dot(linalg.inv(A).dot(b)))
print(np.linalg.solve(A, b))
print(A.dot(np.linalg.solve(A,b)))