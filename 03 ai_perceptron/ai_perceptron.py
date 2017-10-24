import random
import numpy as np

learn_rate = 0.1
result_true = 1
result_false = 0

# 테스트하고 교정하고 적중률출력
def tra_one(tra, tra_ans, per):
    # 평가 & 학습
    delta = np.zeros((10, 64), dtype=np.float64)
    output = np.dot(tra, per)
    current = 0
    for idx_case in range(len(output)):
        per_out = np.argmax(output[idx_case])
        if tra_ans[idx_case][per_out] == result_true:
            current += 1
        output_each = output[idx_case]
        ans_each = tra_ans[idx_case]
        tra_each = tra[idx_case]
        # 각각의 퍼셉트론에 대해
        for idx_num in range(10):
            # 하나의 퍼셉트론이 잘못된 판단을 했을 때
            if not (output_each[idx_num] >= 1000 and ans_each[idx_num] == result_true):
                # delta에 합산
                if output_each[idx_num] >= 1000:
                    output_each[idx_num] = 1
                else:
                    output_each[idx_num] = -1
                t_o = (learn_rate * (0 - output_each[idx_num]))
                delta_tmp = np.dot(t_o, tra_each.reshape(1, 64))
                delta[idx_num] += delta_tmp[0]
    per += np.transpose(delta)
    return current / len(output)

def test_per(tra, tra_ans, per):
    # 평가
    output = np.dot(tra, per)
    current = 0
    for idx_case in range(len(output)):
        per_out = np.argmax(output[idx_case])
        if tra_ans[idx_case][per_out] == result_true:
            current += 1
        output_each = output[idx_case]
        ans_each = tra_ans[idx_case]
        tra_each = tra[idx_case]
    return current / len(output)


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

    # 정답을 행렬로 바꾸기
    tmp = []
    for ans_now in tra_ans:
        tmp_line = []
        for t in range(ans_now):
            tmp_line.append(result_false)
        tmp_line.append(result_true)
        for t in range(9 - ans_now):
            tmp_line.append(result_false)
        tmp.append(tmp_line)
    tra_ans = tmp
    del tmp

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

    # 정답을 행렬로 바꾸기
    tmp = []
    for ans_now in tes_ans:
        tmp_line = []
        for t in range(ans_now):
            tmp_line.append(result_false)
        tmp_line.append(result_true)
        for t in range(9 - ans_now):
            tmp_line.append(result_false)
        tmp.append(tmp_line)
    tes_ans = tmp
    del tmp


    # 퍼셉트론 초기화
    per = []
    for p_t in range(10):
        per_line = []
        for w_t in range(64):
            per_line.append(random.random() - 0.5) # -0.5 ~ 0.5
        per.append(per_line)


    # 배열을 행렬로
    tra = np.array(tra)
    tra_ans = np.array(tra_ans)
    per = np.array(per).transpose() # 퍼셉트론은 계산을 위해 뒤집어야함

    tra_list = []
    tes_list = []
    for t in range(100):
        tra_now = tra_one(tra, tra_ans, per)
        tes_now = test_per(tes, tes_ans, per)
        tra_list.append(tra_now)
        tes_list.append(tes_now)
        print('%d : tra : %f%%  ' % (t, tra_now * 100), end='')
        print(', test : %f%%' % (tes_now * 100))
    print("MAX : tra : %f%%, test : %f%%" % (max(tra_list) * 100, max(tes_list) * 100))
