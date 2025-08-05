# 小学生字帖生成器

这是一个专门为小学生设计的字帖生成工具，可以自动生成包含汉字练习和史记名句的PDF字帖。

## 功能特点

- 自动生成田字格练字模板
- 随机选择常用汉字进行练习
- 在字帖顶部添加史记名句及其译文
- 支持自定义字帖标题和汉字数量
- 支持生成单日或多日字帖
- 自动生成下划线供学生书写练习
- 使用楷体字体，适合小学生练字

## 项目结构

```
wordwriter/
├── app.py              # 主应用文件
├── requirements_app.txt # 应用依赖（精简版）
├── data/               # 汉字和古文数据
│   ├── characters.md   # 小学生必学汉字表
│   ├── classics.md     # 推荐古文
│   └── 史记/           # 史记原文、译文和段译
├── fonts/              # 字体文件
│   └── kaiti_GB2312.ttf # 楷体字体
├── scripts/            # 脚本文件
│   └── random_quote.py # 史记名句随机选择
├── static/             # 静态文件和生成的PDF
└── templates/          # HTML模板
    ├── index.html      # 主页面
    └── error.html      # 错误页面
```

## 安装依赖

```bash
pip install -r requirements_app.txt
```

## 使用方法

1. 确保字体文件存在：`fonts/kaiti_GB2312.ttf`
2. 运行应用：
   ```bash
   python app.py
   ```
3. 访问 http://localhost:5001
4. 设置字帖参数并生成PDF

## 自定义配置

- 修改 `data/characters.md` 添加更多汉字
- 修改 `data/史记/` 目录下的HTML文件添加更多史记内容
- 调整 `app.py` 中的字体大小和布局参数

## 注意事项

- 应用使用5001端口以避免与macOS AirPlay服务冲突
- 生成的PDF文件保存在 `static/` 目录下
- 旧的PDF文件会自动清理（超过1天的文件）
- 支持中文字符的拼音标注和繁简转换
