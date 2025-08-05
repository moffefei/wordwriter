@echo off
:: 设置版本号
set VERSION=1.0.0

:: 创建输出目录
if not exist dist mkdir dist

echo [INFO] 开始构建 Windows 应用...

:: 检查icon文件
if not exist static\logo_simple.ico (
    echo [INFO] 未找到 Windows 应用图标，将使用默认图标
)

:: 构建 Windows 应用
echo [INFO] 构建 Windows 应用...
pyinstaller --clean wordwriter_win.spec
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 构建 Windows 应用失败
    exit /b 1
)

:: 打包 ZIP
echo [INFO] 正在打包 Windows 应用...
cd dist
powershell Compress-Archive -Path wordwriter -DestinationPath "WordWriter-Windows-%VERSION%.zip" -Force
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 打包 Windows 应用失败
    exit /b 1
)
cd ..

echo [INFO] Windows 应用构建完成: dist\WordWriter-Windows-%VERSION%.zip
echo [INFO] 构建完成!