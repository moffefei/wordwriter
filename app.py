from flask import Flask, render_template, send_file, request
import os
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import markdown
from datetime import datetime, timedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import logging
from functools import wraps
import time

logging.basicConfig(
    filename='wordwriter.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 限制请求大小为1MB

# 注册楷体字体
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'kaiti_GB2312.ttf')
pdfmetrics.registerFont(TTFont('Kaiti', FONT_PATH))

class WordWriter:
    def __init__(self):
        self.words = set()
        self.load_words()
        
    def load_words(self):
        """从data目录下的所有markdown文件中加载汉字"""
        data_dir = 'data'
        for filename in os.listdir(data_dir):
            if filename.endswith('.md'):
                with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 提取所有汉字
                    for char in content:
                        if '\u4e00' <= char <= '\u9fff':
                            self.words.add(char)
    
    def generate_grid(self, c, x, y, size):
        # 外框实线
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(1)
        c.rect(x, y, size, size, stroke=1, fill=0)

        # 虚线辅助线
        c.setDash(2, 2)
        c.setStrokeColorRGB(1, 0, 0)
        if hasattr(c, "setStrokeAlpha"):
            c.setStrokeAlpha(0.2)
        # 水平、竖直、对角线
        c.line(x, y + size/2, x + size, y + size/2)
        c.line(x + size/2, y, x + size/2, y + size)
        c.line(x, y, x + size, y + size)
        c.line(x, y + size, x + size, y)
        # 恢复
        c.setDash()
        c.setStrokeColorRGB(0, 0, 0)
        if hasattr(c, "setStrokeAlpha"):
            c.setStrokeAlpha(1)
    
    def create_worksheet(self, output_file='worksheet.pdf', title="每日练字", word_count=30):
        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4

        # 选取指定数量的汉字
        selected_words = random.sample(list(self.words), word_count)

        grid_size = 1.5 * cm
        margin_x = 2 * cm
        margin_y = 3 * cm
        grids_per_row = 10  # 每行10格
        max_rows_per_page = 17

        total_rows = math.ceil(word_count / 2)
        total_pages = math.ceil(total_rows / max_rows_per_page)

        for page in range(total_pages):
            # 页标题
            c.setFont("Kaiti", 16)
            page_title = f"{title} - {datetime.now().strftime('%Y-%m-%d')}"
            if total_pages > 1:
                page_title += f" (第{page+1}页)"
            c.drawString(margin_x, height - 1*cm, page_title)
            c.setFont("Kaiti", 26)

            # 当前页的行数
            start_row = page * max_rows_per_page
            end_row = min(start_row + max_rows_per_page, total_rows)
            for row in range(start_row, end_row):
                for col in range(grids_per_row):
                    grid_x = margin_x + col * grid_size
                    grid_y = height - margin_y - (row - start_row) * grid_size

                    self.generate_grid(c, grid_x, grid_y, grid_size)

                    # 判断是否写字
                    if col % 5 == 0:
                        word_index = row * 2 + col // 5
                        if word_index < len(selected_words):
                            # 第一格：黑色
                            c.setFillColorRGB(0, 0, 0)
                            c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, selected_words[word_index])
                            c.setFillColorRGB(0, 0, 0, alpha=1)
                    elif col % 5 == 1:
                        word_index = row * 2 + col // 5
                        if word_index < len(selected_words):
                            # 第二格：40%透明度描红
                            c.setFillColorRGB(1, 0, 0)
                            if hasattr(c, "setFillAlpha"):
                                c.setFillAlpha(0.45)
                            c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, selected_words[word_index])
                            c.setFillColorRGB(0, 0, 0)
                            if hasattr(c, "setFillAlpha"):
                                c.setFillAlpha(1)
                    elif col % 5 == 2:
                        word_index = row * 2 + col // 5
                        if word_index < len(selected_words):
                            # 第三格：70%透明度描红
                            c.setFillColorRGB(1, 0, 0)
                            if hasattr(c, "setFillAlpha"):
                                c.setFillAlpha(0.3)
                            c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, selected_words[word_index])
                            c.setFillColorRGB(0, 0, 0)
                            if hasattr(c, "setFillAlpha"):
                                c.setFillAlpha(1)
                    # 第四、五格不写字
            if page < total_pages - 1:
                c.showPage()
        c.save()

# 创建WordWriter实例
writer = WordWriter()

# 限制访问频率装饰器
def limit_rate(seconds=1):
    def decorator(f):
        last_request = {}
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            ip = request.remote_addr
            if ip in last_request and now - last_request[ip] < seconds:
                return '请求过于频繁，请稍后再试', 429
            last_request[ip] = now
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
@limit_rate(1)  # 限制每秒最多一次请求
def generate():
    try:
        # 清理旧文件
        cleanup_old_files()
        
        # 获取并验证输入
        title = request.form.get('title', '每日练字')[:50]
        try:
            word_count = int(request.form.get('word_count', 30))
            word_count = max(1, min(word_count, 100))
        except ValueError:
            word_count = 30
        
        # 生成文件
        output_file = f'static/worksheet_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        writer.create_worksheet(output_file, title, word_count)
        
        # 记录日志
        logging.info(f'Generated worksheet: {output_file} with {word_count} words')
        
        return send_file(output_file, as_attachment=True)
    except Exception as e:
        logging.error(f'Error generating worksheet: {str(e)}')
        return render_template('error.html', error=str(e)), 500

def cleanup_old_files():
    try:
        static_dir = 'static'
        current_time = datetime.now()
        for filename in os.listdir(static_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(static_dir, filename)
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if (current_time - file_creation_time).days > 1:
                    os.remove(file_path)
                    logging.info(f'Cleaned up old file: {file_path}')
    except Exception as e:
        logging.error(f'Error cleaning up files: {str(e)}')

@app.errorhandler(Exception)
def handle_error(error):
    return render_template('error.html', error=str(error)), 500

if __name__ == '__main__':
    # 确保必要的目录存在
    os.makedirs('static', exist_ok=True)
    
    # 启动应用
    app.run(debug=True, host='127.0.0.1', port=5000) 