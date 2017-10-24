import numpy as np

print('''
An example''')
a = np.arange(15).reshape(3, 5)
print(a)
print(a.shape)
print(a.ndim)
print(a.dtype.name)
print(a.itemsize)
print(a.size)
print(type(a))
b = np.array([6, 7, 8])
print(b)
print(type(b))

print('''
Array Creation''')
a = np.array([2, 3, 4])
print(a)
print(a.dtype)
b = np.array([1.2, 3.5, 5.1])
print(b.dtype)

print()
b = np.array([(1.5, 2, 3), (4, 5, 6)])
print(b)

print()
c = np.array([[1, 2], [3, 4]], dtype=complex)
print(c)

print()
print(np.zeros((3, 4)))
print(np.ones((2, 3, 4), dtype=np.int16))
print(np.empty((2, 3)))

print()
print(np.arange(10, 30, 5))
print(np.arange(0, 2, 0.3))

print()
from numpy import pi

print(np.linspace(0, 2, 9))
x = np.linspace(0, 2 * pi, 100)
f = np.sin(x)

print('''
Printing Arrays''')
a = np.arange(6)
print(a)
b = np.arange(12).reshape(4, 3)
print(b)
c = np.arange(24).reshape(2, 3, 4)
print(c)

print()
print(np.arange(10000))
print(np.arange(10000).reshape(100, 100))
# np.set_printoptions(threshold='nan')

print('''
Basic Operations''')
a = np.array([20, 30, 40, 50])
b = np.arange(4)
print(b)
c = a - b
print(c)
print(b ** 2)
print(10 * np.sin(a))
print(a < 35)

print()
A = np.array([[1, 1],
              [0, 1]])
B = np.array([[2, 0],
              [3, 4]])
print(A * B)
print(A.dot(B))
print(np.dot(A, B))

print()
a = np.ones((2, 3), dtype=int)
b = np.random.random((2, 3))
a *= 3
print(a)
b += a
print(b)
# a += b
a = np.ones(3, dtype=np.int32)
b = np.linspace(0, pi, 3)
print(b.dtype.name)
c = a + b
print(c)
print(c.dtype.name)
d = np.exp(c * 1j)
print(d)
print(d.dtype.name)

print()
a = np.random.random((2, 3))
print(a)
print(a.sum())
print(a.min())
print(a.max())

print('''
Universal Functions''')
B = np.arange(3)
print(B)
np.exp(B)
np.sqrt(B)
C = np.array([2., -1., 4.])
np.add(B, C)

print('''
Indexing, Slicing and Iterating''')
a = np.arange(10) ** 3
print(a)
print(a[2])
print(a[2:5])
a[:6:2] = -1000
print(a)
print(a[::-1])
for i in a:
    print(i ** (1 / 3.0))

print('''
shape Manipulation''')
a = np.floor(10 * np.random.random((3, 4)))
print(a)
print(a.shape)

print()
print(a.ravel())
print(a.reshape(6, 2))
print(a.T)
print(a.T.shape)
print(a.shape)

print()
a.resize(2, 6)
print(a)
print(a.reshape(3, -1))

print('''
Stacking together different arrays''')
a = np.floor(10 * np.random.random((2, 2)))
print(a)
b = np.floor(10 * np.random.random((2, 2)))
print(b)
print(np.vstack((a, b)))
print(np.hstack((a, b)))

print()
from numpy import newaxis

#print(np.column_stack(a, b))
a = np.array([4., 2.])
b = np.array([2., 8.])
print(a[:,newaxis])
print(np.column_stack((a[:,newaxis],b[:,newaxis])))
print(np.vstack((a[:,newaxis],b[:,newaxis])))