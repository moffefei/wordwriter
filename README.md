# 汉字田字格练习生成器 (Chinese Character Grid Practice Generator)

一个自动生成汉字田字格练习PDF的Web应用，适合小学生（1 到 6 年级一类和二类字）及汉字学习者使用。可根据需要生成不同数量的汉字练习，支持随机选择汉字并配以《史记》名句作为练习素材。

## pdf效果

<img width="695" height="896" alt="image" src="https://github.com/user-attachments/assets/dfcdcfc0-d8a5-45c2-85cd-cb79cc9b3aba" />
<img width="695" height="528" alt="image" src="https://github.com/user-attachments/assets/f1496f66-0cda-49a1-ba7f-a6e27e43370e" />

## 功能特点

- 自动生成田字格练习PDF，方便打印
- 支持自定义练习字数和标题
- 支持批量生成多天的练习内容
- 随机选择汉字用于练习
- 自动添加《史记》名句作为练习素材
- 适合小学生和汉字学习者使用

## 安装使用

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/username/wordwriter.git
cd wordwriter

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 运行应用

```bash
python app.py
```

应用将在 http://127.0.0.1:5001 运行，使用浏览器访问即可。

### 使用说明

1. 在首页设置标题、日期范围和汉字数量
2. 点击"生成字帖"按钮生成PDF文件
3. 下载生成的PDF文件并打印

## 项目结构

```
wordwriter/
├── app.py              # 主应用程序
├── data/               # 汉字数据文件
├── fonts/              # 字体文件
│   └── kaitiGBK.ttf    # 楷体字体文件
├── scripts/            # 工具脚本
│   ├── __init__.py
│   └── random_quote.py # 随机名句脚本
├── static/             # 静态资源
│   └── logo_simple.svg # 应用logo
├── templates/          # HTML模板
│   ├── index.html      # 首页模板
│   └── error.html      # 错误页模板
└── requirements.txt    # 依赖列表
```

## 技术栈

- Flask: Web框架
- ReportLab: PDF生成
- Markdown: 文本处理
- PyPinyin: 拼音处理

## 常见问题解答

**Q: 如何修改默认字体?**  
A: 在 `fonts` 目录下替换 `kaitiGBK.ttf` 文件，或修改 `app.py` 中的 `FONT_PATH` 变量。

**Q: 为什么使用田字格?**  
A: 田字格是中国传统的汉字书写练习格式，有助于练习者掌握汉字的结构和笔画位置。

**Q: 汉字字库是怎么获得的，是最新的吗**  
A:1～6年级一类字二类字是从小学语文最新课标（人教版）课本里的，另外会随机从《史记》里抽取部分字生成。


## 贡献指南

欢迎提交Pull Request或Issues！如需贡献代码，请:

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

本项目采用MIT许可证 - 详情见[LICENSE](LICENSE)文件

## 鸣谢

- 感谢[ReportLab](https://www.reportlab.com/)提供PDF生成支持
- 感谢[hunterhug](https://github.com/hunterhug/china-history)提供的《史记》古文和现代文资料，另有中国历史书籍可前往查看获取
- 感谢所有开源字体项目和贡献者
