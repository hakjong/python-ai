
# coding: utf-8

# 컴퓨터학부 2012105056 손학종

# In[1]:

# 한자 처리를 위한 라이브러리 사용
import hanja


# In[2]:

# 사용하지 않음
part = ['/NNG', '/NNP', '/NNB', '/NP', '/NR', '/VV', '/VA', '/VX', '/VCP', '/VCN',        '/MM', '/MAG', '/MAJ', '/IC', '/JKS', '/JKC', '/JKG', '/JKO', '/JKB', '/JKV',        '/JKQ', '/JX', '/JC', '/EP', '/EF', '/EC', '/ETN', '/ETM', '/XPN', '/XSN',         '/XSV', '/XSA', '/XR', '/SF', '/SP', '/SS', '/SE', '/SO', '/SL', '/SH',        '/SW', '/NF', '/NV', '/XN', '/NA']


# In[3]:

# 한 글자 짜리 특수문자
part_special = ['/SF', '/SP', '/SS', '/SE', '/SO', '/SW']


# 트레이닝 셋에서 데이터를 수집합니다.  
# 좌변, 우변 내용을 그대로 집어넣고,  
# 특수문자는 따로 수집합니다.

# In[4]:

# 데이터 수집
dic = {}
dic_special = {}

print('start')
count = 0
with open('train.txt') as f:
    while True:
        line = f.readline()
        # EOF
        if not line:
            break
        line = line.split()
        # 빈줄 처리
        if len(line) < 2:
            continue
        if not line[0] in dic:
            dic[line[0]] = line[1]
        # 특문 찾기
        for s in part_special:
            idx = line[1].find(s)
            if idx != -1:
                ch = line[1][idx-1]
                if not ch in dic_special:
                    dic_special[ch] = ch + s
                break
        # 진행상황 출력
        count += 1
        if count % 500000 == 0:
            print(count)
print('done')


# 특수문자가 제거된 사전(dic2)을 만듭니다.  
# 위에서 수집한 특수문자가 포함 된 항목을  
# 특수문자 기준 좌, 우로 분해 재귀하여 사전에 추가합니다.

# In[5]:

# 특문 제거해서 추가
print('start')
dic2 = {} # 특수문자 제거된 사전
def special_proc(left, right):
    for s in dic_special:
        idx = left.find(s)
        if idx != -1:
            ridx = right.find(s)
            new_left = left[:idx]
            new_right = right[:ridx - 1]
            if len(new_left) != 0:
                special_proc(new_left, new_right)
            new_left = left[idx + 1:]
            new_right = right[ridx + 5:]
            if len(new_left) != 0:
                special_proc(new_left, new_right)
            return
            
    if not left in dic2:
        dic2[left] = right
    
for d in dic:
    special_proc(d, dic[d])


print('done')


# 예측을 처리하는 함수의 정의입니다.  
# 사전에 있는 항목은 그대로 출력하고,  
# 없는 경우 특수문자를 찾아 분해하여 재귀합니다.
#   
# 사전에 없는 경우 9글자부터 1글자까지 다시 쪼개어 탐색하고  
# 그래도 못 찾은 경우 한자어인지 확인한 후  
# 마지막으로 남은 단어를 NA로 태깅합니다.

# In[6]:

def predict(line, dic):
    # 사전에 동일한 것이 있으면 그대로 출력
    if line in dic:
        return dic[line]
    else:
        # 특문 찾기
        for s in dic_special:
            idx = line.find(s)
            if idx != -1:
                result = ''
                if len(line[:idx]) != 0:
                    result += predict(line[:idx], dic2) + '+'
                result += dic_special[line[idx]]
                if len(line[idx + 1:]) != 0:
                    result += '+' + predict(line[idx + 1:], dic2)
                return result
            
        # 분할하여 탐색
        for charlen in reversed(range(1, 10)):
            for idx in range(len(line) - charlen + 1):
                s = line[idx:idx + charlen]
                if s in dic2:
                    result = ''
                    if len(line[:idx]) != 0:
                        result += predict(line[:idx], dic2) + '+'
                    result += dic2[s]
                    if len(line[idx + charlen:]) != 0:
                        result += '+' + predict(line[idx + charlen:], dic2)
                    return result
        # 한자어?
        if hanja.is_hanja(line[0]):
            return line + '/SH'
        
        return line + '/NA'


# 임의로 평가 시 84.3769% 의 정확도가 나왔습니다.  
# (dictionary 의 iteration 이 있기 때문에 매번 실행 시 다소 차이가 있습니다.)

# In[7]:

# 평가
print('start')
count = 0
correct = 0
with open('test.txt') as f:
    while True:
        line = f.readline()
        # EOF
        if not line:
            break
        line = line.split()
        # 빈 줄 처리
        if len(line) < 2:
            continue
        count += 1
        if line[1] == predict(line[0], dic):
            correct += 1
        else:
            # 틀린거 확인
            # print(line[1] + '\n' + predict(line[0], dic) + '\n')
            None
        # 진행상황 출력
        if count % 100000 == 0:
            print(count)
            
print(correct/count * 100)

