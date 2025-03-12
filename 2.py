import csv, re

def validate_tags(filename):
    errors, tag_pattern = [], re.compile(r"<(u|ud)>.*?</\1>")
    with open(filename, "r", encoding="utf-8-sig") as file:
        for i, row in enumerate(csv.DictReader(file), 1):
            content = row.get("content", "")
            if not content or tag_pattern.findall(content) or not re.search(r"<(/?u|/?ud)>", content): continue
            errors.append(f"第 {i} 行：标签错误")
    return errors

if __name__ == "__main__":
    errors = validate_tags("CUVNanjing.csv")
    print("标签格式错误：" if errors else "所有标签格式正确！")
    print("\n".join(errors))
