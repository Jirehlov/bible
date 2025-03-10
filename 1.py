import csv
import sys
import re
import pyperclip
book_map = {
    'gen': 1, 'exo': 2, 'lev': 3, 'num': 4, 'deu': 5, 'jos': 6, 'jdg': 7, 'rut': 8, '1sa': 9, '2sa': 10,
    '1ki': 11, '2ki': 12, '1ch': 13, '2ch': 14, 'ezr': 15, 'neh': 16, 'est': 17, 'job': 18, 'psa': 19,
    'pro': 20, 'ecc': 21, 'sng': 22, 'isa': 23, 'jer': 24, 'lam': 25, 'ezk': 26, 'dan': 27, 'hos': 28,
    'jol': 29, 'amo': 30, 'oba': 31, 'jon': 32, 'mic': 33, 'nam': 34, 'hab': 35, 'zep': 36, 'hag': 37,
    'zec': 38, 'mal': 39, 'mat': 40, 'mrk': 41, 'luk': 42, 'jhn': 43, 'act': 44, 'rom': 45, '1co': 46,
    '2co': 47, 'gal': 48, 'eph': 49, 'php': 50, 'col': 51, '1th': 52, '2th': 53, '1ti': 54, '2ti': 55,
    'tit': 56, 'phm': 57, 'heb': 58, 'jas': 59, '1pe': 60, '2pe': 61, '1jn': 62, '2jn': 63, 
    '3jn': 64, 'jud': 65, 'rev': 66
    }
book_map_cn = {
    'gen': '创', 'exo': '出', 'lev': '利', 'num': '民', 'deu': '申', 'jos': '书', 'jdg': '士', 'rut': '得', '1sa': '撒上', '2sa': '撒下',
    '1ki': '王上', '2ki': '王下', '1ch': '代上', '2ch': '代下', 'ezr': '拉', 'neh': '尼', 'est': '斯', 'job': '伯', 'psa': '诗', 'pro': '箴',
    'ecc': '传', 'sng': '歌', 'isa': '赛', 'jer': '耶', 'lam': '哀', 'ezk': '结', 'dan': '但', 'hos': '何', 'jol': '珥', 'amo': '摩', 
    'oba': '俄', 'jon': '拿', 'mic': '弥', 'nam': '鸿', 'hab': '哈', 'zep': '番', 'hag': '该', 'zec': '亚', 'mal': '玛', 'mat': '太', 
    'mrk': '可', 'luk': '路', 'jhn': '约', 'act': '徒', 'rom': '罗', '1co': '林前', '2co': '林后', 'gal': '加', 'eph': '弗', 'php': '腓',
    'col': '西', '1th': '帖前', '2th': '帖后', '1ti': '提前', '2ti': '提后', 'tit': '多', 'phm': '门', 'heb': '来', 'jas': '雅', '1pe': '彼前',
    '2pe': '彼后', '1jn': '约一', '2jn': '约二', '3jn': '约三', 'jud': '犹', 'rev': '启'
    }
book_map_full_cn = {
    'gen': '创世记', 'exo': '出埃及记', 'lev': '利未记', 'num': '民数记', 'deu': '申命记', 'jos': '约书亚记', 'jdg': '士师记', 'rut': '路得记', 
    '1sa': '撒母耳记上', '2sa': '撒母耳记下', '1ki': '列王记上', '2ki': '列王记下', '1ch': '历代志上', '2ch': '历代志下', 'ezr': '以斯拉记', 
    'neh': '尼希米记', 'est': '以斯帖记', 'job': '约伯记', 'psa': '诗篇', 'pro': '箴言', 'ecc': '传道书', 'sng': '雅歌', 'isa': '以赛亚书', 
    'jer': '耶利米书', 'lam': '耶利米哀歌', 'ezk': '以西结书', 'dan': '但以理书', 'hos': '何西阿书', 'jol': '约珥书', 'amo': '阿摩司书', 
    'oba': '俄巴底亚书', 'jon': '约拿书', 'mic': '弥迦书', 'nam': '那鸿书', 'hab': '哈巴谷书', 'zep': '西番雅书', 'hag': '哈该书', 
    'zec': '撒迦利亚书', 'mal': '玛拉基书', 'mat': '马太福音', 'mrk': '马可福音', 'luk': '路加福音', 'jhn': '约翰福音', 'act': '使徒行传', 
    'rom': '罗马书', '1co': '哥林多前书', '2co': '哥林多后书', 'gal': '加拉太书', 'eph': '以弗所书', 'php': '腓立比书', 'col': '歌罗西书', 
    '1th': '帖撒罗尼迦前书', '2th': '帖撒罗尼迦后书', '1ti': '提摩太前书', '2ti': '提摩太后书', 'tit': '提多书', 'phm': '腓利门书', 
    'heb': '希伯来书', 'jas': '雅各书', '1pe': '彼得前书', '2pe': '彼得后书', '1jn': '约翰一书', '2jn': '约翰二书', '3jn': '约翰三书', 
    'jud': '犹大书', 'rev': '启示录'
    }
def load_bible(filename):
    verses = []
    god_name = ""
    with open(filename, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['id'] == '<god>':
                god_name = row['content']
            verses.append(row)
    return verses, god_name
def clean_content(content, god_name, comment_lookup, no_comments):
    if not content: return ""
    content = content.replace("<god>", god_name)
    content = content.replace("<br>", "\n")
    if no_comments:
        content = re.sub(r'<c id=.*?>', '', content)
    else:
        content = re.sub(r'<c id=(.*?)>', lambda m: f" ({comment_lookup.get(m.group(1), 'N/A')})", content)
    content = re.sub(r'</c>', '', content)
    content = re.sub(r'<u>|</u>|<ud>|</ud>', '', content)
    return content
def get_verses(verses, start_ref, end_ref=None, include_section_numbers=False, no_comments=False):
    start_book, start_book_cn, start_book_full_cn, start_chap, start_verse, start_is_whole_chap = parse_reference(start_ref)
    end_book, end_book_cn, end_book_full_cn, end_chap, end_verse, end_is_whole_chap = parse_reference(end_ref) if end_ref else (start_book, start_book_cn, start_book_full_cn, start_chap, start_verse, start_is_whole_chap)
    results = []
    comment_lookup = {v['id']: v['content'] for v in verses if v['type'] == '4'}
    multi_verse_map = {}
    verse_content_map = {}
    for v in verses:
        try:
            book = int(v['book']) if v['book'].isdigit() else 0
            chap = int(v['chapter']) if v['chapter'].isdigit() else 0
            verse_parts = v['verse'].split('、')
            verses_list = tuple(int(verse) for verse in verse_parts if verse.isdigit())
        except ValueError:
            continue
        if not verses_list or v['type'] not in ['1', '3']:
            continue
        content = clean_content(v['content'], god_name, comment_lookup, no_comments)
        if len(verses_list) > 1:
            multi_verse_map[(book, chap, verses_list)] = content
        else:
            verse_content_map[(book, chap, verses_list[0])] = content
    for (book, chap, verse_tuple), content in multi_verse_map.items():
        if start_book == book and start_chap == chap and start_verse in verse_tuple and end_verse in verse_tuple:
            if include_section_numbers:
                content = f"{chap}.{verse_tuple[0]}-{verse_tuple[-1]} {content}"
            results.append(content)
            result_text = "\n".join(results)
            return result_text.rstrip("\r\n")
    for (book, chap, verse), content in verse_content_map.items():
        if start_book == book and start_chap == chap and start_verse <= verse <= end_verse:
            if include_section_numbers:
                content = f"{chap}.{verse} {content}"
            results.append(content)
    result_text = "\n".join(results)
    return result_text.rstrip("\r\n")
def parse_reference(ref):
    if ref is None:
        return 0, "", "", float('inf'), float('inf'), False
    parts = ref.split('.')
    book = book_map.get(parts[0], 0)
    book_cn = book_map_cn.get(parts[0], "")
    book_full_cn = book_map_full_cn.get(parts[0], "")
    if len(parts) == 1:
        return book, book_cn, book_full_cn, float('inf'), float('inf'), True
    elif len(parts) == 2:
        return book, book_cn, book_full_cn, int(parts[1]), float('inf'), True
    elif len(parts) == 3:
        return book, book_cn, book_full_cn, int(parts[1]), int(parts[2]), False
    return 0, "", "", 0, 0, False
if __name__ == "__main__":
    bible_file = "CUVNanjing.csv"
    verses, god_name = load_bible(bible_file)
    if len(sys.argv) < 2:
        print("Usage: python script.py [-v] [-w] [-nc] book [chapter [verse]] [end_book.chapter.verse]")
        sys.exit(1)
    include_section_numbers = "-v" in sys.argv
    include_verse_range = "-w" in sys.argv
    no_comments = "-nc" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg not in ("-v", "-w", "-nc")]
    start_ref = args[0]
    end_ref = args[1] if len(args) > 1 else None
    start_book, start_book_cn, start_book_full_cn, start_chap, start_verse, start_is_whole_chap = parse_reference(start_ref)
    end_book, end_book_cn, end_book_full_cn, end_chap, end_verse, end_is_whole_chap = parse_reference(end_ref) if end_ref else (start_book, start_book_cn, start_book_full_cn, start_chap, float('inf'), start_is_whole_chap)
    if start_is_whole_chap or end_is_whole_chap:
        start_verse = 1
        end_verse = float('inf')
    output = get_verses(verses, start_ref, end_ref, include_section_numbers, no_comments)
    if include_verse_range:
        if start_book == end_book:
            ref_range = f"【{start_book_full_cn}{start_chap}:{start_verse}-{end_chap}:{end_verse}】\n" if end_ref else f"【{start_book_full_cn}{start_chap}:{start_verse}】\n"
        else:
            ref_range = f"【{start_book_full_cn}{start_chap}:{start_verse}-{end_book_full_cn}{end_chap}:{end_verse}】\n"
        output = ref_range + output
    print(output)
    pyperclip.copy(output)
