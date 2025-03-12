import csv
import sys
import re
import pyperclip
def load_csv_to_dict(filename, key_field, value_field, value_transform=int):
    result = {}
    with open(filename, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[row[key_field]] = value_transform(row[value_field])
    return result
def load_book_map(filename):
    book_map = load_csv_to_dict(filename, 'en_abbr', 'id')
    book_map_cn = load_csv_to_dict(filename, 'en_abbr', 'cuv_full', str)
    return book_map, book_map_cn
def load_bible(filename):
    verses = []
    env_vars = {}
    with open(filename, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if re.match(r'<.*?>', row['id']):
                env_vars[row['id']] = row['content']
            verses.append(row)
    return verses, env_vars
def replace_env_vars(content, env_vars):
    for env_var, value in env_vars.items():
        content = content.replace(env_var, value)
    return content
def clean_content(content, env_vars, comment_lookup, no_comments):
    if not content: return ""
    content = replace_env_vars(content, env_vars).replace("<br>", "\n")
    if no_comments:
        content = re.sub(r'<c id=.*?>', '', content)
    else:
        content = re.sub(r'<c id=(.*?)>', lambda m: f" ({comment_lookup.get(m.group(1), 'N/A')})", content)
    content = re.sub(r'</c>', '', content)
    content = re.sub(r'<u>|</u>|<ud>|</ud>', '', content)
    return content
def get_verses(verses, start_book, start_chap, start_verse, end_book, end_chap, end_verse, include_section_numbers=False, no_comments=False):
    results = []
    comment_lookup = {v['id']: v['content'] for v in verses if v['type'] == '4'}
    first_verse_of_chap = True
    current_chap = start_chap
    actual_end_verse = end_verse
    actual_end_chap = end_chap
    for v in verses:
        if v['type'] not in ['1', '3']: continue
        if '、' in v['verse']:
            verse_range = v['verse'].split('、')
            try:
                start_verse_of_range = int(verse_range[0])
                end_verse_of_range = int(verse_range[-1])
            except ValueError:
                continue
        else:
            try:
                book, chap, verse = map(int, (v['book'], v['chapter'], v['verse']))
                start_verse_of_range = end_verse_of_range = verse
            except ValueError:
                continue
        book, chap = map(int, (v['book'], v['chapter']))
        if (start_book < book < end_book) or (start_book == book and start_chap <= chap <= end_chap and start_verse <= end_verse_of_range) or (end_book == book and start_chap <= chap <= end_chap and start_verse_of_range <= end_verse):
            if chap != current_chap:
                first_verse_of_chap = True
                current_chap = chap
            if chap == start_chap and end_verse_of_range >= start_verse:
                if chap == end_chap and start_verse_of_range > end_verse:
                    break
                content = clean_content(v['content'], env_vars, comment_lookup, no_comments)
                if include_section_numbers:
                    verse_display = v['verse']
                    content = f"{chap}.{verse_display} {content}" if first_verse_of_chap else f"{verse_display} {content}"
                    first_verse_of_chap = False
                results.append(content)
                actual_end_verse = end_verse_of_range
                actual_end_chap = chap
                if end_verse_of_range >= end_verse and chap == end_chap: break
    return "".join(results).rstrip("\r\n"), actual_end_chap, actual_end_verse
def parse_reference(ref, book_map, book_map_cn):
    if ref is None: return 0, "", "", 0, 0
    parts = ref.split('.')
    book = book_map.get(parts[0], 0)
    book_cn = book_map_cn.get(parts[0], "")
    return (book, book_cn, int(parts[1]) if len(parts) > 1 else 0, int(parts[2]) if len(parts) > 2 else 0)
if __name__ == "__main__":
    bible_file = "CUVNanjing.csv"
    map_file = "map.csv"
    book_map, book_map_cn = load_book_map(map_file)
    verses, env_vars = load_bible(bible_file)
    if len(sys.argv) < 2:
        print("Usage: python script.py [-v] [-w] [-nc] book [chapter [verse]] [end_book.chapter.verse]")
        sys.exit(1)
    include_section_numbers = "-v" in sys.argv
    include_verse_range = "-w" in sys.argv
    no_comments = "-nc" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ("-v", "-w", "-nc")]
    start_ref = args[0]
    end_ref = args[1] if len(args) > 1 else None
    start_book, start_book_cn, start_chap, start_verse = parse_reference(start_ref, book_map, book_map_cn)
    end_book, end_book_cn, end_chap, end_verse = parse_reference(end_ref, book_map, book_map_cn) if end_ref else (start_book, start_book_cn, start_chap, start_verse)
    if start_chap == 0:
        start_chap = 1
        end_chap = float('inf')
        start_verse = 1
        end_verse = float('inf')
    elif start_verse == 0:
        start_verse = 1
        end_verse = float('inf')
    output, actual_end_chap, actual_end_verse = get_verses(verses, start_book, start_chap, start_verse, end_book, end_chap, end_verse, include_section_numbers, no_comments)
    if include_verse_range:
        ref_range = f"【{start_book_cn}{start_chap}:{start_verse}-{(end_book_cn if end_book != start_book else '')}{actual_end_chap}:{actual_end_verse}】\n"
        output = ref_range + output
    print(output)
    pyperclip.copy(output)
