#!/bin/bash

# 设置版本号
VERSION="1.0.0"

# 创建输出目录
mkdir -p dist

# 输出信息函数
info() {
    echo -e "\033[1;34m[INFO]\033[0m $1"
}

error() {
    echo -e "\033[1;31m[ERROR]\033[0m $1"
    exit 1
}

# 检查系统类型
info "检测系统类型..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    info "检测到 macOS 系统，开始构建 macOS 应用..."
    
    # 检查icon文件
    if [ ! -f "static/logo_simple.icns" ]; then
        info "未找到 macOS 应用图标，将使用默认图标"
    fi
    
    # 构建 macOS 应用
    info "构建 macOS 应用..."
    pyinstaller --clean wordwriter_mac.spec || error "构建 macOS 应用失败"
    
    # 打包 DMG 或 ZIP
    info "正在打包 macOS 应用..."
    cd dist
    zip -r "WordWriter-macOS-${VERSION}.zip" WordWriter.app || error "打包 macOS 应用失败"
    cd ..
    
    info "macOS 应用构建完成: dist/WordWriter-macOS-${VERSION}.zip"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    info "检测到 Windows 系统，开始构建 Windows 应用..."
    
    # 检查icon文件
    if [ ! -f "static/logo_simple.ico" ]; then
        info "未找到 Windows 应用图标，将使用默认图标"
    fi
    
    # 构建 Windows 应用
    info "构建 Windows 应用..."
    pyinstaller --clean wordwriter_win.spec || error "构建 Windows 应用失败"
    
    # 打包 ZIP
    info "正在打包 Windows 应用..."
    cd dist
    zip -r "WordWriter-Windows-${VERSION}.zip" wordwriter || error "打包 Windows 应用失败"
    cd ..
    
    info "Windows 应用构建完成: dist/WordWriter-Windows-${VERSION}.zip"
    
else
    error "不支持的操作系统: $OSTYPE"
fi

info "构建完成!"