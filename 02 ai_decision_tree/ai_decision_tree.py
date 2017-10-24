import math
import collections as col
import numpy as np

result_idx = 0
names_file = 'mushroom.names'
data_file = 'mushroom.data'
test_file = 'mushroom.test'

names = []
dtree = {}
none_result = None


def trace(t, a):
    if t['name'] == 'end':
        return t['end']
    else:
        selected = a[t['name']]
        return trace(t[selected], a)


def make_dtree(t, d, n):
    # 탈출 조건
    if len(n) == 1 or entropy(d) == 0.0:
        t['name'] = 'end'
        # 가장 갯수많은걸로
        # 없으면 아무거나
        if len(d) == 0:
            t['end'] = none_result
            return
        c = col.Counter(d[:, result_idx])
        s = max(c, key=c.get)
        t['end'] = s
        return
    dic_tmp = {}
    for n_now in n:
        dic_tmp[n_now] = (gain_lst(d, n_now))
    m = max(dic_tmp, key=lambda d: dic_tmp[d][0])
    t['name'] = m

    nn = n.copy()
    nn.remove(m)

    for idx in range(0, len(names[m])):
        t[idx] = {}
        make_dtree(t[idx], dic_tmp[m][1][idx], nn)


def gain_lst(d, idx_att):
    g = entropy(d)
    dn = d.shape[0]  # 행 길이

    lst = []
    for i in range(0, len(names[idx_att])):
        lst.append(np.zeros((0, d.shape[1]), dtype='int'))
    for now in d:
        n = now[idx_att]
        lst[n] = np.vstack([lst[n], now])

    for now in lst:
        g -= (now.shape[0] / dn) * entropy(now)

    return (g, lst)


def entropy(d):
    c = col.Counter(d[:, result_idx])
    s = sum(c.values())
    e = 0
    for now in c.values():
        e -= (now / s) * math.log2(now / s)
    return e


if __name__ == '__main__':
    print('Making dtree...')
    with open(names_file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n').split(':')
            names.append(line[1].split(','))

    tra = []
    with open(data_file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n').split(',')
            item = []
            for idx in range(0, len(line)):
                item.append(names[idx].index(line[idx]))
            tra.append(item)

    tra = np.array(tra)

    # none_result 찾기
    c = col.Counter(tra[:, result_idx])
    none_result = max(c, key=lambda i: c[i])
    del c

    # 결과의 인덱스를 제외한 리스트가 세번째 인자로 들어감
    name_lst = list(range(0, len(names)))
    name_lst.remove(result_idx)
    make_dtree(dtree, tra, name_lst)
    print('Done\n')

    # 테스트
    print('Testing...')
    tst = []
    with open(test_file) as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip('\n').split(',')
            item = []
            for idx in range(0, len(line)):
                item.append(names[idx].index(line[idx]))
            tst.append(item)

    tst = np.array(tst)
    ok = 0
    cnt = tst.shape[0]

    for now in tst:
        if now[0] == trace(dtree, now):
            ok += 1

    print("%d/%d => %f%%" % (ok, cnt, ok / cnt * 100))
