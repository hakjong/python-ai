import random
import numpy as np

learning_rate = 0.001

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def calc(per, tra):
    result = []
    result.append(tra)
    for idx in range(len(per)):
        item = np.dot(result[idx], per[idx].T)
        item = sigmoid(item)
        result.append(item)
    return result

def evaluation(out_data, tra_ans):
    per_res = out_data.argmax(axis=1)
    current_set = np.equal(per_res, tra_ans)
    return np.sum(current_set) / current_set.size

def backpropagation(per, result, tra, target):
    out_o = result[-1]
    out_h = result[-2]
    ew_o = out_o - target
    oi_o = out_o * (1 - out_o)
    iw_o = out_h
    delta_o = np.zeros(per[-1].shape)
    for idx in range(len(tra)):
        a = (ew_o[idx] * oi_o[idx]).reshape((per[-1].shape[0], 1))
        b = iw_o[idx].reshape((1, per[-1].shape[1]))
        r = np.dot(a, b)
        delta_o += r
    delta_o *= learning_rate
    per[-1] -= delta_o
    before = ew_o * oi_o

    for idx in reversed(range(len(per) - 1)):
        out_h = result[idx + 1]
        ew_h = np.dot(before, per[idx + 1])
        oi_h = out_h * (1 - out_h)
        iw_h = None
        if idx == 0:
            iw_h = tra
        else:
            iw_h = result[idx]
        delta_h = np.zeros(per[idx].shape)
        for idx2 in range(len(ew_h)):
            a = (ew_h[idx2] * oi_h[idx2]).reshape((per[idx].shape[0], 1))
            b = iw_h[idx2].reshape((1, per[idx].shape[1]))
            r = np.dot(a, b)
            delta_h += r
        delta_h *= learning_rate
        per[idx] -= delta_h
        before = ew_h * oi_h

def make_per(in_num, out_num):
    per = []
    for t1 in range(out_num):
        item = []
        for t2 in range(in_num):
            item.append(random.random() - 0.5)
        per.append(item)
    per = np.array(per)
    return per

if __name__ == '__main__':
    # 트레이닝 데이터 읽어오기
    tra = []
    tra_ans = []
    with open('optdigits.tra', 'r') as f:
        while True:
            line_str = f.readline()
            if not line_str:
                break
            line_str = line_str.strip('\n')
            line_lst = [int(n) for n in line_str.split(',')]
            tra.append(line_lst[:-1])
            tra_ans.append(line_lst[-1])  # 정답은 따로저장
    tra = np.array(tra)

    # 정답을 타겟 행렬로
    tra_target = []
    for now_ans in tra_ans:
        item = []
        for t in range(now_ans):
            item.append(0)
        item.append(1)
        for t in range(9 - now_ans):
            item.append(0)
        tra_target.append(item)
    tra_target = np.array(tra_target)
    tra_ans = np.array(tra_ans)
    
    # 테스트 데이터 읽어오기
    tes = []
    tes_ans = []
    with open('optdigits.tes', 'r') as f:
        while True:
            line_str = f.readline()
            if not line_str:
                break
            line_str = line_str.strip('\n')
            line_lst = [int(n) for n in line_str.split(',')]
            tes.append(line_lst[:-1])
            tes_ans.append(line_lst[-1])  # 정답은 따로저장
    tes = np.array(tes)
    tes_ans = np.array(tes_ans)

    # 퍼셉트론 초기화
    per = []
    per.append(make_per(64, 30))
    per.append(make_per(30, 21))
    per.append(make_per(21, 15))
    per.append(make_per(15, 10))

    max = 0.0
    max_tes = 0.0
    for t in range(1000):
        result = calc(per, tra)
        suc = evaluation(result[-1], tra_ans)
        tes_suc = evaluation(calc(per, tes)[-1], tes_ans)
        print('%d: tra: %f%% / tes: %f%%' % (t, suc * 100, tes_suc * 100))
        if max < suc:
            max = suc
        if max_tes < tes_suc:
            max_tes = tes_suc
        backpropagation(per, result, tra, tra_target)
    print('--------------------------')
    print('MAX: tra: %f%% / tes: %f%%' % (max * 100, max_tes * 100))
