import nltk
import collections


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

def make_out(filename, word_arr):
    tra = load_file(filename + '.txt')
    remove_stopword(tra)
    stemming(tra)

    fout = open(filename + '.dat', mode='w')
    cnt_line = 0
    for line in tra:
        cnt_line += 1
        if cnt_line % 100 == 0:
            print('line %d' % cnt_line)
        if line[0] == 'acq':
            fout.write('1 ')
        else:
            fout.write('-1 ')
        out_line = {}
        for word in line:
            if word not in word_arr:
                word_arr.append(word)
            word_idx = word_arr.index(word)
            if word_idx not in out_line:
                out_line[word_idx] = 0
            out_line[word_idx] += 1
        out_line = collections.OrderedDict(sorted(out_line.items()))
        for k, v in out_line.items():
            fout.write("%d:%d " % (k, v))
        fout.write('\n')
    print('line %d' % cnt_line)
    fout.close()


if __name__ == '__main__':
    word_arr = ['_none']
    make_out('r8-train-all-terms', word_arr)
    make_out('r8-test-all-terms', word_arr)