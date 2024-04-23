def find_first_difference(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.read()
        content2 = f2.read()
    min_length = min(len(content1), len(content2))
    for i in range(min_length):
        if content1[i] != content2[i]:
            return i, content1[max(0, i - 20):i], content1[i:min(i + 20, len(content1))], content2[max(0, i - 20):i], content2[i:min(i + 20, len(content2))]
    if len(content1) != len(content2):
        return min_length, None, None, None, None
    return -1, None, None, None, None

if __name__ == "__main__":
    file1 = "1.txt"
    file2 = "bible_wordsonly.txt"
    position, context1_before, context1_after, context2_before, context2_after = find_first_difference(file1, file2)
    if position == -1:
        print("文件内容完全相同")
    else:
        print(f"第一处不同的位置在第 {position + 1} 个字符处")
        print("第一个文件中不同位置的上下文：")
        print(context1_before, context1_after)
        print("第二个文件中不同位置的上下文：")
        print(context2_before, context2_after)
