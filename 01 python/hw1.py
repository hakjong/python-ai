line_count = 0
word_count = 0
word_dic = {}
highest_line = None
highest_line_num = 0

with open("a.txt") as f:
    while True:
        s = f.readline()
        if not s: break
        s = s.strip("\n")
        lst = s.split(" ")

        line_count += 1
        word_count += len(lst)

        # 단어가 가장 많은 줄 검출
        if highest_line_num < len(lst):
            highest_line = line_count
            highest_line_num = len(lst)

        # 단어 빈도 세기
        for word in lst:
            if word in word_dic:
                word_dic[word] += 1
            else:
                word_dic[word] = 0


print("단어수: %d" % word_count)
print("줄수: %d" % line_count)
print("가장 많이 쓰인 단어: %s" % max(word_dic, key=word_dic.get))
print("단어가 가장 많이 포함된 라인: %d" % highest_line)
print("단어가 가장 많이 포함된 라인에서의 단어 수: %d" % highest_line_num)