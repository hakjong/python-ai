import nltk
import math


def load_file(filename):
    f = open(filename)
    arr = []
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split()
        arr.append(line)
    f.close()
    return arr


def remove_stopword(arr):
    f = open('stopword.txt')
    sword = []
    while True:
        word = f.readline()
        if not word:
            break
        sword.append(word.strip())
    for line in arr:
        for word in line[1:]:
            if word in sword:
                line.remove(word)
    f.close()


def stemming(arr):
    stemmer = nltk.PorterStemmer()
    for idx in range(len(arr)):
        line = arr[idx]
        singles = [stemmer.stem(plural) for plural in line[1:]]
        arr[idx] = line[0:1] + singles


def count_words(arr):
    cnt = {}
    cnt['_sum'] = 0
    for line in arr:
        subj = line[0]
        cnt['_sum'] += 1
        if not subj in cnt:
            cnt[subj] = {}
            cnt[subj]['_sum_word_num'] = 0
            cnt[subj]['_sum_word_all'] = 0
            cnt[subj]['_sum_subj'] = 0
        cnt[subj]['_sum_subj'] += 1
        for word in line[1:]:
            cnt[subj]['_sum_word_num'] += 1
            if not word in cnt[subj]:
                cnt[subj][word] = 1
                cnt[subj]['_sum_word_all'] += 1
            else:
                cnt[subj][word] += 1
    return cnt


def get_prob(word, subj, cnt):
    nu = 1
    if word in cnt[subj]:
        nu += cnt[subj][word]
    de = cnt[subj]['_sum_word_all'] + cnt[subj]['_sum_word_num']
    return nu / de

def naive(content, cnt):
    res = {}
    for subj in cnt:
        if subj[0] == '_':
            continue
        res[subj] = 0
        res[subj] += math.log2(cnt[subj]['_sum_subj'] / cnt['_sum'])
        for word in content:
            res[subj] += math.log2(get_prob(word, subj, cnt))

    return max(res, key=lambda  k: res[k])


if __name__ == '__main__':
    tra = load_file('r8-train-all-terms.txt')
    remove_stopword(tra)
    stemming(tra)
    cnt = count_words(tra)
    print('train completed.')

    tes = load_file('r8-test-all-terms.txt')
    remove_stopword(tes)
    stemming(tes)

    tes_pass = 0
    tes_count = 0
    for line in tes:
        tes_count += 1
        res = naive(line[1:], cnt)
        if res == line[0]:
            tes_pass += 1
        if tes_count % 1000 == 0:
            print('%f%% (%d / %d)' % (tes_pass / tes_count * 100, tes_pass, tes_count))

    print('%f%% (%d / %d)' % (tes_pass / tes_count * 100, tes_pass, tes_count))
