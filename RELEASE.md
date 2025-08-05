# 发布新版本指南

本文档介绍如何创建和发布WordWriter的新版本。

## 版本发布流程

我们使用GitHub Actions自动构建Windows和macOS的可执行文件，并将其发布到GitHub Releases。

### 步骤1: 更新版本号

在发布新版本前，需要更新项目中的版本号：

1. 在`build.sh`和`build_windows.bat`中更新`VERSION`变量
2. 如有其他地方显示版本号的，也需要更新

### 步骤2: 提交更改并创建标签

```bash
# 提交所有更改
git add .
git commit -m "准备发布版本 X.Y.Z"
git push

# 创建版本标签
git tag -a vX.Y.Z -m "版本 X.Y.Z"
git push origin vX.Y.Z
```

例如，对于版本1.0.0：

```bash
git tag -a v1.0.0 -m "版本 1.0.0"
git push origin v1.0.0
```

### 步骤3: 监控GitHub Actions

推送标签后，GitHub Actions会自动触发构建流程：

1. 登录GitHub，进入项目仓库
2. 点击"Actions"选项卡查看构建进度
3. 构建完成后，会自动创建新的Release，并上传Windows和macOS可执行文件

### 步骤4: 完善发布说明

GitHub自动创建的发布需要进一步完善：

1. 进入GitHub仓库的"Releases"页面
2. 点击刚创建的版本
3. 点击"Edit"按钮
4. 更新发布说明，包括新功能、修复的bug等
5. 点击"Update release"保存更改

## 本地构建可执行文件

如果需要在本地构建可执行文件进行测试，可以使用以下命令：

### macOS系统

```bash
# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 构建macOS应用
./build.sh
```

### Windows系统

```cmd
:: 安装依赖
pip install -r requirements.txt
pip install pyinstaller

:: 构建Windows应用
build_windows.bat
```

构建完成后，可执行文件将位于`dist`目录中。