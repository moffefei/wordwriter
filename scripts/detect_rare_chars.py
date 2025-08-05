import os
import re
import sys
from pypinyin import pinyin, Style

def detect_rare_chars(file_path):
    """检测文件中的罕见汉字并输出带拼音版本"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    rare_chars = []
    for char in content:
        # 检查是否为汉字但不在常用Unicode范围
        if not ('\u4e00' <= char <= '\u9fff') and ord(char) > 128:
            rare_chars.append(char)
    
    # 去重并排序
    rare_chars = sorted(set(rare_chars))
    
    # 为每个罕见字生成拼音
    for char in rare_chars:
        py = pinyin(char, style=Style.TONE)
        pinyin_text = py[0][0] if py and py[0] else "?"
        print(f"{char} ({pinyin_text})")
    
    return rare_chars

if __name__ == "__main__":
    # 支持传入目录或文件
    path = sys.argv[1] if len(sys.argv) > 1 else 'data'
    
    if os.path.isdir(path):
        # 处理目录下的所有markdown文件
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.md')]
        for file_path in files:
            print(f"\n检查文件: {file_path}")
            rare_chars = detect_rare_chars(file_path)
            print(f"发现 {len(rare_chars)} 个罕见字符")
    else:
        # 处理单个文件
        print(f"\n检查文件: {path}")
        rare_chars = detect_rare_chars(path)
        print(f"发现 {len(rare_chars)} 个罕见字符")