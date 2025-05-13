# 小学生字帖生成器 (WordWriter)

一个基于Flask的Web应用，用于生成小学生练字字帖。支持自定义字数、自动分页，并包含描红功能。

## 功能特点

- 🎯 支持自定义生成字数
- 📝 每个汉字配有5个练习格
- 🖌️ 智能描红功能（40%和70%透明度）
- 📄 自动分页（每页最多17行）
- 🎨 美观的田字格布局
- 📱 响应式Web界面

## 技术栈

- Python 3.8+
- Flask 3.0.2
- ReportLab 4.0.4
- Bootstrap 5.1.3

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/wordwriter.git
cd wordwriter
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 即可使用。

## 项目结构


## 使用说明

1. 在网页界面输入字帖标题
2. 设置需要生成的汉字数量
3. 点击"生成字帖"按钮
4. 下载生成的PDF文件
5. 打印即可使用

## 字帖格式

- 每行2个汉字
- 每个汉字5个练习格
- 第1格：黑色示范字
- 第2格：40%透明度描红
- 第3格：70%透明度描红
- 第4-5格：空白练习格

## 注意事项

- 确保系统已安装楷体字体
- 建议使用A4纸张打印
- 生成的PDF文件会在24小时后自动清理

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。

## 致谢

- 感谢所有贡献者的付出
- 特别感谢开源社区提供的优秀工具和库
