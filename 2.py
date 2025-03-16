import csv, re
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
ALLOWED_TAGS = {"u", "ud", "c", "br", "god", "sl"}
def validate_tags(filename):
    errors, tag_pattern = [], re.compile(r"</?([a-zA-Z]+)>")
    total_rows, updated_rows = 0, 0
    date_counts = Counter()
    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, 1):
            total_rows += 1
            content = row.get("content", "").strip()
            updated_at = row.get("updated_at", "").strip()
            if updated_at:
                updated_rows += 1
                date_counts[updated_at] += 1
            found_tags = tag_pattern.findall(content)
            invalid_tags = [tag for tag in found_tags if tag not in ALLOWED_TAGS]
            if invalid_tags:
                errors.append(f"第 {i} 行：发现不允许的标签 {set(invalid_tags)}")
    updated_ratio = (updated_rows / total_rows) * 100 if total_rows else 0
    return errors, updated_ratio, date_counts
def plot_date_frequencies(date_counts):
    if not date_counts:
        print("没有可用的日期数据。")
        return
    dates, frequencies = zip(*sorted(date_counts.items()))
    plt.figure(figsize=(10, 5), dpi=150)
    plt.bar(dates, frequencies, color='skyblue')
    plt.xlabel("日期")
    plt.ylabel("频数")
    plt.title("日期频数图")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    errors, updated_ratio, date_counts = validate_tags("CUVNanjing.csv")
    if errors:
        print("标签格式错误：")
        print("\n".join(errors))
    else:
        print("所有标签格式正确！")
    print(f"更新的行比例：{updated_ratio:.2f}%")
    plot_date_frequencies(date_counts)
