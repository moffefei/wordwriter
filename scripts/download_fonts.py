import os
import shutil
import urllib.request
import logging

# 配置下载字体
FONT_URLS = {
    'SourceHanSansSC-Regular.ttf': 'https://github.com/adobe-fonts/source-han-sans/raw/release/OTF/SimplifiedChinese/SourceHanSansSC-Regular.otf',
    'SourceHanSerifSC-Regular.ttf': 'https://github.com/adobe-fonts/source-han-serif/raw/release/OTF/SimplifiedChinese/SourceHanSerifSC-Regular.otf'
}

def download_fonts():
    """下载开源字体到项目中"""
    embedded_fonts_dir = os.path.join('fonts', 'embedded')
    os.makedirs(embedded_fonts_dir, exist_ok=True)
    
    for font_name, font_url in FONT_URLS.items():
        font_path = os.path.join(embedded_fonts_dir, font_name)
        
        # 如果字体已存在，跳过下载
        if os.path.exists(font_path):
            print(f"字体 {font_name} 已存在，跳过下载")
            continue
            
        try:
            print(f"开始下载字体 {font_name}...")
            # 使用urllib下载文件
            urllib.request.urlretrieve(font_url, font_path)
            print(f"字体 {font_name} 下载成功")
        except Exception as e:
            print(f"下载字体 {font_name} 失败: {str(e)}")
            logging.error(f"下载字体 {font_name} 失败: {str(e)}")

if __name__ == "__main__":
    download_fonts()