from flask import Flask, render_template, send_file, request
import os
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from datetime import datetime, timedelta
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import logging
from functools import wraps
import time
from scripts.random_quote import get_random_quote
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import blue, black

logging.basicConfig(
    filename='wordwriter.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 限制请求大小为1MB

# 注册汉字字体
# 使用项目内置字体目录
FONT_PATH = 'fonts/kaitiGBK.ttf'

try:
    # 注册楷体字体
    if os.path.exists(FONT_PATH):
        pdfmetrics.registerFont(TTFont('KaitiGBK', FONT_PATH))
        BOLD_FONT = 'KaitiGBK'
        RARE_CHAR_FONT = 'KaitiGBK'
        logging.info("成功注册楷体字体 kaitiGBK.ttf")
    else:
        logging.error(f"字体文件不存在: {FONT_PATH}")
        BOLD_FONT = 'Helvetica'
        RARE_CHAR_FONT = 'Helvetica'
except Exception as e:
    # 如果字体文件不存在，使用默认字体
    logging.error(f"注册字体失败：{str(e)}")
    BOLD_FONT = 'Helvetica'
    RARE_CHAR_FONT = 'Helvetica'

class WordWriter:
    """汉字田字格生成器类
    
    用于加载汉字并生成田字格练习笔记。支持自定义练习汉字数量、标题和日期。
    """
    def __init__(self):
        self.words = set()
        self.load_words()
        
    def load_words(self):
        """从 data 目录下的所有 markdown 文件中加载汉字
        
        遍历 data 目录下的所有 markdown 文件，提取其中的所有非 ASCII 字符添加到字符集中。
        """
        data_dir = 'data'
        for filename in os.listdir(data_dir):
            if filename.endswith('.md'):
                with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 提取所有汉字
                    for char in content:
                        if ord(char) > 128:  # 检测所有非ASCII字符，包括中文、日文、韩文等
                            self.words.add(char)
    
    def generate_grid(self, c, x, y, size):
        """绘制田字格
        
        在PDF画布上绘制一个带边框和辅助线的田字格。
        
        Args:
            c: ReportLab画布对象
            x: 田字格左上角x坐标
            y: 田字格左上角y坐标
            size: 田字格大小
        """
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
    
    def draw_wrapped_text(self, c, text, x, y, font_name, font_size, max_width, leading=1.2, dry_run=False, return_lines=False):
        """在PDF上自动换行绘制文本
        
        计算文本在指定宽度内如何换行，并在PDF上绘制。
        
        Args:
            c: ReportLab画布对象
            text: 要绘制的文本
            x: 起始x坐标
            y: 起始y坐标
            font_name: 字体名称
            font_size: 字体大小
            max_width: 最大宽度
            leading: 行间距系数
            dry_run: 如果为True，只计算不绘制
            return_lines: 如果为True，返回行数而非坐标
            
        Returns:
            如果return_lines=True，返回行数；否则返回绘制后的新y坐标
        """
        c.setFont(font_name, font_size)
        lines = []
        current_line = ''
        for char in text:
            if stringWidth(current_line + char, font_name, font_size) > max_width:
                lines.append(current_line)
                current_line = char
            else:
                current_line += char
        if current_line:
            lines.append(current_line)
        for i, line in enumerate(lines):
            if not dry_run:
                c.drawString(x, y - i * font_size * leading, line)
        if return_lines:
            return len(lines)
        return y - (len(lines)-1) * font_size * leading

    def draw_bold_title_and_text(self, c, title, text, x, y, bold_font, regular_font, font_size, max_width, return_lines=False):
        """首行标题加粗，标题为蓝色，正文为黑色，自动换行时与标题首行对齐"""
        # 简化字体选择，统一使用楷体
        title_font = bold_font
                
        title_width = stringWidth(title, title_font, font_size)
        # 手动分行
        words = list(text)
        lines = []
        # 首行剩余宽度
        first_line_width = max_width - title_width
        current_line = ''
        current_width = 0
        # 计算首行
        for i, char in enumerate(words):
            w = stringWidth(char, regular_font, font_size)
            if current_width + w > first_line_width:
                lines.append(current_line)
                break
            current_line += char
            current_width += w
        else:
            lines.append(current_line)
            i = len(words)
        # 后续行
        start = i
        while start < len(words):
            current_line = ''
            current_width = 0
            while start < len(words):
                w = stringWidth(words[start], regular_font, font_size)
                if current_width + w > max_width:
                    break
                current_line += words[start]
                current_width += w
                start += 1
            lines.append(current_line)
        # 绘制首行
        c.setFont(title_font, font_size)
        c.setFillColor(blue)
        c.drawString(x, y, title)
        c.setFont(regular_font, font_size)
        c.setFillColor(black)
        if lines and lines[0]:  # 确保有内容才绘制
            c.drawString(x + title_width, y, lines[0])
        # 绘制后续行
        line_height = font_size * 1.2  # 恢复为正常行高
        for idx, line in enumerate(lines[1:]):
            c.drawString(x, y - (idx + 1) * line_height, line)
        c.setFillColor(black)
        if return_lines:
            return lines
        return len(lines)
        
    def draw_underline(self, c, x, y, width):
        """绘制下划线
        
        在指定位置绘制一条水平下划线
        
        Args:
            c: ReportLab画布对象
            x: 左侧x坐标
            y: y坐标
            width: 线段宽度
        """
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.5)
        c.line(x, y, x + width, y)

    def create_worksheet(self, output_file='worksheet.pdf', title="每日练字", word_count=30, date_str=None):
        """创建汉字练习工作表PDF
        
        生成包含指定数量汉字的田字格练习PDF。可选择性地添加《史记》名句作为练习素材。
        
        Args:
            output_file: 输出文件路径
            title: 工作表标题
            word_count: 要包含的汉字数量
            date_str: 日期字符串，如果为 None 则使用当前日期
        """
        c = canvas.Canvas(output_file, pagesize=A4)
        width, height = A4
        
        # 底部预留空间
        bottom_margin = 2.0 * cm

        # 选取指定数量的汉字
        selected_words = random.sample(list(self.words), word_count)

        grid_size = 1.5 * cm
        grids_per_row = 10  # 每行10格
        max_rows_per_page = 12  # 减少每页行数以确保显示完整
        # 动态计算margin_x使田字格居中
        grid_total_width = grids_per_row * grid_size
        margin_x = (width - grid_total_width) / 2
        margin_y = 3 * cm

        total_rows = math.ceil(word_count / 2)
        
        # 重要修改：限制第一页最多显示10行田字格
        first_page_max_rows = 10
        second_page_start_row = 0
        
        if total_rows > first_page_max_rows:
            second_page_start_row = first_page_max_rows
            total_pages = 1 + math.ceil((total_rows - first_page_max_rows) / max_rows_per_page)
        else:
            total_pages = 1

        # 史记名句引用（普通文本显示，自动换行）
        quote = get_random_quote()
        y_quote = height - 2.2*cm
        max_text_width = width - 2 * margin_x
        grid_top_y = None
        if quote:
            # 史记节选：标题加粗+正文同段落自动换行
            title_text = f"【史记原文（{quote['source']}）】"
            font_size = 16
            lines1_list = self.draw_bold_title_and_text(
                c,
                title_text,
                quote['original'],
                margin_x, y_quote, BOLD_FONT, RARE_CHAR_FONT, font_size, max_text_width,
                return_lines=True)
            
            # 计算原文总高度
            lines1_count = len(lines1_list)
            original_height = lines1_count * font_size * 1.2
            
            # 在原文下方添加下划线
            line_height = font_size * 2.5  # 下划线行高
            # 所有下划线长度一致
            for i in range(lines1_count):
                underline_y = y_quote - original_height - (i * line_height) - font_size * 1.2
                self.draw_underline(c, margin_x, underline_y, max_text_width)
            # 添加一个额外的下划线行
            extra_underline_y = y_quote - original_height - (lines1_count * line_height) - font_size
            self.draw_underline(c, margin_x, extra_underline_y, max_text_width)
            
            y_quote_new = y_quote - original_height - (lines1_count + 1) * line_height
            lines2 = 0
            y_quote_new2 = y_quote_new
            if quote['translation']:
                # 译文保持原有格式
                y_translation = y_quote_new
                lines2 = self.draw_bold_title_and_text(
                    c,
                    "【译文】：",
                    quote['translation'],
                    margin_x, y_translation, BOLD_FONT, RARE_CHAR_FONT, font_size, max_text_width)
                y_quote_new2 = y_translation - lines2 * font_size * 1.2
            
            c.setFont(RARE_CHAR_FONT, 16)
            # 计算史记内容总高度
            total_height = original_height + (lines1_count + 1) * line_height + (lines2 * font_size * 1.2 if lines2 else 0) + (0.2*cm if lines2 else 0)
            # 估算田字格区域所需的高度
            grid_rows_needed = min(max_rows_per_page, total_rows)
            grid_height_needed = grid_rows_needed * grid_size
            
            # 计算可用的高度
            available_height = height - 1 * cm - margin_y - bottom_margin
            
            # 如果可用高度小于预计需要的高度，调整max_rows_per_page
            if available_height < total_height + grid_height_needed:
                # 根据可用高度重新计算每页可容纳的行数
                max_rows_per_page = int((available_height - total_height) / grid_size)
                max_rows_per_page = max(1, max_rows_per_page) # 确保至少有1行
            
            grid_top_y = y_quote - total_height - 0.7*cm  # 史记内容下方空0.7cm
            
            # 确保田字格底部不会超出页面底部的预留区域
            min_allowed_y = bottom_margin
            last_row_bottom_y = grid_top_y - (min(max_rows_per_page, total_rows) - 1) * grid_size - grid_size
            
            if last_row_bottom_y < min_allowed_y:
                # 如果计算出的田字格底部低于允许的底部边距，减少每页最大行数
                adjusted_rows = int((grid_top_y - min_allowed_y) / grid_size)
                max_rows_per_page = min(max_rows_per_page, max(1, adjusted_rows))
                # 重新计算总页数
                total_pages = math.ceil(total_rows / max_rows_per_page)
        else:
            grid_top_y = height - margin_y

        for page in range(total_pages):
            # 页标题
            c.setFont(RARE_CHAR_FONT, 16)
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            page_title = f"{title} - {date_str}"
            if total_pages > 1:
                page_title += f" (第{page+1}页)"
            c.drawString(margin_x, height - 1*cm, page_title)
            c.setFont(RARE_CHAR_FONT, 26)

            # 当前页的行数
            if page == 0:
                # 第一页在史记内容下方显示，最多显示first_page_max_rows行
                start_row = 0
                end_row = min(first_page_max_rows, total_rows)
            else:
                # 后续页从第一页显示的行数之后开始
                start_row = first_page_max_rows + (page-1) * max_rows_per_page
                end_row = min(start_row + max_rows_per_page, total_rows)
            for row in range(start_row, end_row):
                # 计算当前行在页面内的行号
                row_in_page = row - start_row
                
                for col in range(grids_per_row):
                    grid_x = margin_x + col * grid_size
                    
                    # 田字格y坐标计算
                    if page == 0:
                        # 在第一页，从史记内容下方开始排列
                        grid_y = grid_top_y - row_in_page * grid_size
                    else:
                        # 后续页面从顶部开始排列
                        grid_y = height - margin_y - row_in_page * grid_size
                    self.generate_grid(c, grid_x, grid_y, grid_size)

                    # 只填正文内容
                    word_index = row * 2 + col // 5
                    if col % 5 in [0, 1, 2]:
                        if word_index < len(selected_words):
                            word = selected_words[word_index]
                            if col % 5 == 0:
                                # 黑色汉字
                                c.setFillColorRGB(0, 0, 0)
                                c.setFont(BOLD_FONT, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                            elif col % 5 == 1:
                                # 红色半透明汉字
                                c.setFillColorRGB(1, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(0.45)
                                c.setFont(BOLD_FONT, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                                c.setFillColorRGB(0, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(1)
                            elif col % 5 == 2:
                                # 浅红色透明汉字
                                c.setFillColorRGB(1, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(0.3)
                                c.setFont(BOLD_FONT, 26)
                                c.drawCentredString(grid_x + grid_size/2, grid_y + grid_size/2 - 9, word)
                                c.setFillColorRGB(0, 0, 0)
                                if hasattr(c, "setFillAlpha"):
                                    c.setFillAlpha(1)
            if page < total_pages - 1:
                c.showPage()
        c.save()

# 创建WordWriter实例
writer = WordWriter()

# 限制访问频率装饰器
def limit_rate(seconds=1):
    """限制API访问频率的装饰器
    
    通过跟踪每个IP的上次请求时间，限制请求频率。
    
    Args:
        seconds: 最小请求间隔时间（秒）
    
    Returns:
        包装后的视图函数
    """
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
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', today=today)

@app.route('/generate', methods=['POST'])
@limit_rate(1)
def generate():
    try:
        cleanup_old_files()
        title = request.form.get('title', '每日练字')[:50]
        try:
            word_count = int(request.form.get('word_count', 30))
            word_count = max(1, min(word_count, 100))
        except ValueError:
            word_count = 30
        date_start = request.form.get('date_start') or datetime.now().strftime('%Y-%m-%d')
        date_end = request.form.get('date_end') or datetime.now().strftime('%Y-%m-%d')
        # 生成日期区间
        start_dt = datetime.strptime(date_start, '%Y-%m-%d')
        end_dt = datetime.strptime(date_end, '%Y-%m-%d')
        delta_days = (end_dt - start_dt).days + 1
        pdf_files = []
        for i in range(delta_days):
            cur_date = (start_dt + timedelta(days=i)).strftime('%Y-%m-%d')
            output_file = f'static/worksheet_{cur_date}_{random.randint(1000,9999)}.pdf'
            writer.create_worksheet(output_file, title, word_count, date_str=cur_date)
            pdf_files.append(output_file)
        if len(pdf_files) == 1:
            return send_file(pdf_files[0], as_attachment=True)
        # 多个PDF，打包为zip
        import zipfile
        zip_path = f'static/worksheets_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for pdf in pdf_files:
                zipf.write(pdf, os.path.basename(pdf))
        return send_file(zip_path, as_attachment=True)
    except Exception as e:
        logging.error(f'Error generating worksheet: {str(e)}')
        return render_template('error.html', error=str(e)), 500

def cleanup_old_files():
    """清理超过24小时的临时PDF和ZIP文件
    
    进行定期清理，删除static目录下超过24小时的临时生成文件，减少磁盘占用。
    """
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
    
    # 启动应用，使用5001端口避免与AirPlay冲突
    app.run(debug=True, host='127.0.0.1', port=5001)
