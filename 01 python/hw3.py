import numpy as np
import scipy as sp
import string

print("안녕하세요...")
print("다항방정식을 풀어드릴게요........")
hang = int(input("항이 몇개인가요......? "))

arr_a = []
arr_b = []

for sick_num in range(1, hang + 1):
    print("%d : " % sick_num, end='')
    for hang_num in range(0, hang):
        print("□x%d" % hang_num, end='')
        if hang_num != hang - 1:
            print(" + ", end='')
        else:
            print(" = □")
    input_str = input()
    input_list = input_str.split()
    arr_a.append([int(x) for x in input_list[:-1]])
    arr_b.append([int(x) for x in input_list[-1:]])

a = np.array(arr_a)
b = np.array(arr_b)
arr_ans = np.linalg.solve(a, b)

print("답입니다.....")
for n in range(1, len(arr_ans) + 1):
    print("x%d = %f" % (n, arr_ans[n - 1]))