# 打包说明

为了将项目打包成可执行文件，我们已经准备了以下文件：

1. **PyInstaller 规范文件**
   - `wordwriter_win.spec` - Windows平台的PyInstaller规范文件
   - `wordwriter_mac.spec` - macOS平台的PyInstaller规范文件

2. **构建脚本**
   - `build.sh` - Linux/macOS平台的通用构建脚本
   - `build_windows.bat` - Windows平台专用构建脚本
   - `create_icons.sh` - 用于创建应用图标的脚本（需要ImageMagick和png2ico）

3. **GitHub Actions工作流**
   - `.github/workflows/build-release.yml` - 用于自动构建和发布的GitHub Actions工作流配置

4. **发布指南**
   - `RELEASE.md` - 如何发布新版本的详细说明

## 构建步骤

### 在本地构建

#### macOS用户
1. 安装依赖: `pip install -r requirements.txt pyinstaller`
2. 创建图标(需要ImageMagick): `./create_icons.sh`
3. 运行构建脚本: `./build.sh`
4. 构建结果位于`dist`目录中

#### Windows用户
1. 安装依赖: `pip install -r requirements.txt pyinstaller`
2. 创建图标(使用相应工具)或复制已有图标
3. 运行构建脚本: `build_windows.bat`
4. 构建结果位于`dist`目录中

### 通过GitHub Actions自动构建

1. 在本地提交更改并推送
2. 创建版本标签: `git tag -a vX.Y.Z -m "版本 X.Y.Z"`
3. 推送标签: `git push origin vX.Y.Z`
4. GitHub Actions会自动构建并创建Release