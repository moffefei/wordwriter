import re

with open('/Users/moffe/小贝智言/coding/wordwriter/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 修改第一个字体处理部分（黑色字体）
pattern1 = r'c.setFillColorRGB\(0, 0, 0\)\n\s+# 使用字体选择器来处理罕见汉字\n\s+# 检查字符是否为常见汉字范围.*?c.setFillColorRGB\(0, 0, 0, alpha=1\)'
replacement1 = r'''c.setFillColorRGB(0, 0, 0)
                                # 检查字符是否为常见汉字范围
                                is_common_char = '\u4e00' <= word <= '\u9fff'
                                is_rare_char = not is_common_char
                                
                                # 选择字体
                                if is_common_char:
                                    # 常见汉字使用楷体
                                    current_font = BOLD_FONT
                                else:
                                    # 罕见汉字使用备用字体
                                    current_font = RARE_CHAR_FONT
                                
                                # 设置字体并绘制汉字
                                c.setFont(current_font, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                                
                                # 如果是罕见字，添加拼音
                                if is_rare_char:
                                    # 获取拼音（带声调）
                                    pinyin_list = pypinyin.pinyin(word, style=pypinyin.Style.TONE)
                                    if pinyin_list and pinyin_list[0]:
                                        pinyin_text = pinyin_list[0][0]
                                        # 绘制拼音在字的右上角
                                        c.setFont('Helvetica', 10)
                                        c.drawString(grid_x + grid_size/2 + 5, grid_y + grid_size - 3, f"({pinyin_text})")
                                        # 恢复原来的字体
                                        c.setFont(current_font, 26)
                                
                                c.setFillColorRGB(0, 0, 0, alpha=1)'''

# 修改第二个字体处理部分（红色字体0.45透明度）
pattern2 = r'c.setFillColorRGB\(1, 0, 0\)\n\s+if hasattr\(c, "setFillAlpha"\):\n\s+c.setFillAlpha\(0.45\)\n\s+# 同样选择合适的字体.*?if hasattr\(c, "setFillAlpha"\):\n\s+c.setFillAlpha\(1\)'
replacement2 = r'''c.setFillColorRGB(1, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(0.45)
                                
                                # 检查字符是否为常见汉字范围
                                is_common_char = '\u4e00' <= word <= '\u9fff'
                                is_rare_char = not is_common_char
                                
                                # 选择字体
                                if is_common_char:
                                    # 常见汉字使用楷体
                                    current_font = BOLD_FONT
                                else:
                                    # 罕见汉字使用备用字体
                                    current_font = RARE_CHAR_FONT
                                
                                # 设置字体并绘制汉字
                                c.setFont(current_font, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                                
                                # 如果是罕见字，添加拼音
                                if is_rare_char:
                                    # 获取拼音（带声调）
                                    pinyin_list = pypinyin.pinyin(word, style=pypinyin.Style.TONE)
                                    if pinyin_list and pinyin_list[0]:
                                        pinyin_text = pinyin_list[0][0]
                                        # 绘制拼音在字的右上角
                                        c.setFont('Helvetica', 10)
                                        c.setFillColorRGB(0, 0, 0)
                                        c.drawString(grid_x + grid_size/2 + 5, grid_y + grid_size - 3, f"({pinyin_text})")
                                        # 恢复原来的字体和颜色
                                        c.setFont(current_font, 26)
                                        c.setFillColorRGB(1, 0, 0)
                                        if hasattr(c, "setFillAlpha"):
                                            c.setFillAlpha(0.45)
                                
                                c.setFillColorRGB(0, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(1)'''

# 修改第三个字体处理部分（红色字体0.3透明度）
pattern3 = r'c.setFillColorRGB\(1, 0, 0\)\n\s+if hasattr\(c, "setFillAlpha"\):\n\s+c.setFillAlpha\(0.3\)\n\s+# 同样选择合适的字体.*?if hasattr\(c, "setFillAlpha"\):\n\s+c.setFillAlpha\(1\)'
replacement3 = r'''c.setFillColorRGB(1, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(0.3)
                                
                                # 检查字符是否为常见汉字范围
                                is_common_char = '\u4e00' <= word <= '\u9fff'
                                is_rare_char = not is_common_char
                                
                                # 选择字体
                                if is_common_char:
                                    # 常见汉字使用楷体
                                    current_font = BOLD_FONT
                                else:
                                    # 罕见汉字使用备用字体
                                    current_font = RARE_CHAR_FONT
                                
                                # 设置字体并绘制汉字
                                c.setFont(current_font, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                                
                                # 如果是罕见字，添加拼音
                                if is_rare_char:
                                    # 获取拼音（带声调）
                                    pinyin_list = pypinyin.pinyin(word, style=pypinyin.Style.TONE)
                                    if pinyin_list and pinyin_list[0]:
                                        pinyin_text = pinyin_list[0][0]
                                        # 绘制拼音在字的右上角
                                        c.setFont('Helvetica', 10)
                                        c.setFillColorRGB(0, 0, 0)
                                        c.drawString(grid_x + grid_size/2 + 5, grid_y + grid_size - 3, f"({pinyin_text})")
                                        # 恢复原来的字体和颜色
                                        c.setFont(current_font, 26)
                                        c.setFillColorRGB(1, 0, 0)
                                        if hasattr(c, "setFillAlpha"):
                                            c.setFillAlpha(0.3)
                                
                                c.setFillColorRGB(0, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(1)'''

# 使用DOTALL模式以便匹配跨越多行的内容
modified_content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
modified_content = re.sub(pattern2, replacement2, modified_content, flags=re.DOTALL)
modified_content = re.sub(pattern3, replacement3, modified_content, flags=re.DOTALL)

with open('/Users/moffe/小贝智言/coding/wordwriter/app.py', 'w', encoding='utf-8') as f:
    f.write(modified_content)

print("已添加拼音显示功能")
