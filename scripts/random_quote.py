import os
import random
import re
from bs4 import BeautifulSoup
import pypinyin
import unicodedata
import opencc
import logging

# 加载简繁转换器
cc = opencc.OpenCC('t2s')

def is_chinese_char(char):
    """判断是否为汉字（不含标点、引号等）"""
    return '\u4e00' <= char <= '\u9fff'

def is_chinese_punctuation(char):
    """判断是否为中文标点，包括全角引号、括号等"""
    punctuations = '，。！？；：""''（）《》【】、—…·'
    return char in punctuations

def is_common_char(char):
    """判断是否为常用字（含常用汉字和常用标点，支持繁体）"""
    # 常用汉字Unicode范围
    common_ranges = [
        (0x4E00, 0x9FFF),  # CJK统一汉字
        (0x3000, 0x303F),  # CJK标点符号
        (0xFF00, 0xFFEF),  # 全角ASCII、全角标点
    ]
    code = ord(char)
    # 简体和繁体都判断
    char_s = cc.convert(char)
    return any(start <= ord(char_s) <= end for start, end in common_ranges)

def get_pinyin(char):
    """获取汉字的拼音"""
    return pypinyin.lazy_pinyin(char)[0]

def add_pinyin_to_rare_chars(text):
    """为生僻字添加拼音标注，格式为字[拼音]，不对标点和引号加拼音"""
    result = []
    for char in text:
        # 只对汉字且不是常用字的加拼音
        if is_chinese_char(char) and not is_common_char(char):
            pinyin = get_pinyin(char)
            result.append(f"{char}[{pinyin}]")
        else:
            result.append(char)
    return ''.join(result)

def normalize_quotes(text):
    if not text:
        return text
    # 替换异常全角引号和括号
    text = text.replace('（（', '（').replace('））', '）')
    # 替换半角引号为全角
    text = text.replace('"', '“').replace("'", "‘")
    # 替换英文括号为中文括号
    text = text.replace('(', '（').replace(')', '）')
    # 替换英文引号为中文引号
    text = text.replace('"', '“').replace("'", "‘")
    # 规范化所有全角引号
    text = text.replace('""', '""').replace('""', '"')
    # 去除多余的嵌套引号
    text = re.sub(r'([""])\1+', r'\1', text)
    return text

def get_random_quote(max_try=20, min_len=20, max_len=120):
    """随机获取史记中的一句话及其译文，严格控制长度，保证原文和译文配对"""
    try:
        shiji_dir = "data/史记"
        duanyi_files = []
        for root, dirs, files in os.walk(shiji_dir):
            for file in files:
                if file.endswith("-段译.html"):
                    duanyi_files.append(os.path.join(root, file))
        if not duanyi_files:
            return None
        for _ in range(max_try):
            file_path = random.choice(duanyi_files)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            paragraphs = soup.find_all('p')
            valid_pairs = []
            for idx, p in enumerate(paragraphs):
                if (p.find('a') or p.get('id') or p.get('class') or 
                    (p.get('style') and 'color:#967d63' in p.get('style'))):
                    continue
                text = p.get_text().strip()
                # 找下一个译文段落
                next_p = p.find_next('p')
                if next_p and next_p.get('style') and 'color:#967d63' in next_p.get('style'):
                    trans_text = next_p.get_text().strip()
                    if min_len <= len(text) <= max_len and min_len <= len(trans_text) <= max_len:
                        valid_pairs.append((p, next_p))
            if not valid_pairs:
                continue
            paragraph, trans_p = random.choice(valid_pairs)
            text = paragraph.get_text().strip()
            translation = trans_p.get_text().strip()
            # 提取出处（章节名）
            rel_path = os.path.relpath(file_path, shiji_dir)
            parts = rel_path.split(os.sep)
            if len(parts) >= 2:
                chapter = parts[-1].replace('-段译.html', '')
                section = parts[-2]
                source = f"{section}·{chapter}"
            else:
                source = rel_path.replace('-段译.html', '')
            text_with_pinyin = add_pinyin_to_rare_chars(text)
            text_with_pinyin = normalize_quotes(text_with_pinyin)
            translation = normalize_quotes(translation)
            # print("调试输出：", repr(text_with_pinyin))  # 调试输出
            return {
                'original': text_with_pinyin,
                'translation': translation,
                'source': source
            }
    except Exception as e:
        logging.error(f"Error in get_random_quote: {str(e)}")
        return None
    return None

if __name__ == "__main__":
    quote = get_random_quote()
    if quote:
        print("原文：", quote['original'])
        print("译文：", quote['translation'])
        print("出处：", quote['source'])
    else:
        print("未能获取到合适的句子")
