#!/bin/bash

# 创建图标文件的脚本
# 需要先安装 imagemagick: brew install imagemagick
# 对于 Windows .ico 文件，需要安装 png2ico: brew install png2ico

# 确保 static 目录存在
mkdir -p static/icons

# 使用 SVG 文件生成 PNG 格式
convert -background none static/logo_simple.svg static/icons/logo_128.png
convert -background none -resize 16x16 static/logo_simple.svg static/icons/logo_16.png
convert -background none -resize 32x32 static/logo_simple.svg static/icons/logo_32.png
convert -background none -resize 48x48 static/logo_simple.svg static/icons/logo_48.png
convert -background none -resize 64x64 static/logo_simple.svg static/icons/logo_64.png
convert -background none -resize 128x128 static/logo_simple.svg static/icons/logo_128.png
convert -background none -resize 256x256 static/logo_simple.svg static/icons/logo_256.png
convert -background none -resize 512x512 static/logo_simple.svg static/icons/logo_512.png

# 创建 Windows ICO 文件
png2ico static/logo_simple.ico static/icons/logo_16.png static/icons/logo_32.png static/icons/logo_48.png static/icons/logo_64.png static/icons/logo_128.png static/icons/logo_256.png

# 创建 macOS ICNS 文件
mkdir -p static/logo.iconset
cp static/icons/logo_16.png static/logo.iconset/icon_16x16.png
cp static/icons/logo_32.png static/logo.iconset/icon_16x16@2x.png
cp static/icons/logo_32.png static/logo.iconset/icon_32x32.png
cp static/icons/logo_64.png static/logo.iconset/icon_32x32@2x.png
cp static/icons/logo_128.png static/logo.iconset/icon_128x128.png
cp static/icons/logo_256.png static/logo.iconset/icon_128x128@2x.png
cp static/icons/logo_256.png static/logo.iconset/icon_256x256.png
cp static/icons/logo_512.png static/logo.iconset/icon_256x256@2x.png
cp static/icons/logo_512.png static/logo.iconset/icon_512x512.png

# 转换为 ICNS 文件
iconutil -c icns static/logo.iconset -o static/logo_simple.icns

# 清理临时文件
rm -rf static/logo.iconset

echo "Icon files have been created in the static directory:"
echo "- static/logo_simple.ico (Windows)"
echo "- static/logo_simple.icns (macOS)"