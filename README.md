# HTML转EXE/Python工具

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

一个简单易用的工具，可以将HTML项目转换为独立的EXE可执行文件或Python脚本。支持API服务后台运行功能。

## 🌟 特性

- 🔄 **多种转换格式**：支持转换为EXE可执行文件或Python脚本
- 🎨 **现代化界面**：使用tkinter构建的美观用户界面
- ⚙️ **API服务支持**：可选的后台API服务运行功能
- 🖼️ **自定义图标**：为生成的EXE文件设置自定义图标
- 📱 **窗口配置**：可自定义应用程序窗口标题和大小
- 🎯 **一键转换**：简单直观的操作流程

## 📸 界面预览

![界面截图](screenshot.png) <!-- 如果有截图可以添加 -->

## 🚀 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/html-to-exe-converter.git
cd html-to-exe-converter

# 安装依赖
pip install -r requirements.txt
```

### 运行程序

```bash
python main.py
```

## 📋 使用方法

### 1. 基本转换
1. 选择HTML项目目录（包含所有HTML、CSS、JS等文件）
2. 选择输出目录
3. 设置窗口标题和主HTML文件名
4. 选择转换类型（EXE或Python脚本）
5. 点击"开始转换"

### 2. API服务功能
1. 勾选"启用API服务"
2. 点击"添加可执行文件"选择API程序
3. 转换时API服务将在后台自动启动
4. 程序关闭时API服务自动停止

### 3. 自定义图标
1. 准备.ico格式的图标文件
2. 在"图标文件"中选择图标路径
3. 仅在转换为EXE时生效

## 📦 依赖库

```txt
pywebview>=3.0    # WebView窗口支持
PyInstaller>=5.0  # EXE打包工具
psutil>=5.0       # 进程管理
ttkthemes>=3.0    # 界面美化（可选）
```

## 🛠️ 开发环境

### Python版本要求
- Python 3.6 或更高版本

### 虚拟环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 📁 项目结构

```
html-to-exe-converter/
│
├── main.py                 # 主程序文件
├── requirements.txt        # 依赖列表
└── README.md              # 说明文档
```

## 🔧 高级功能

### 打包为独立程序
```bash
# 安装pyinstaller
pip install pyinstaller

# 打包为单个exe文件
pyinstaller --onefile --windowed --name "HTML转EXE工具" main.py
```

### 自定义配置
- **窗口大小**：在代码中修改 `width` 和 `height` 参数
- **默认设置**：修改 `__init__` 方法中的默认值
- **界面主题**：修改 `setup_ui` 方法中的主题设置

## 🐛 常见问题

### 1. 转换失败
- 确保HTML项目目录包含所有必要文件
- 检查主HTML文件是否存在
- 确认输出目录有写入权限

### 2. API服务无法启动
- 确保选择的可执行文件路径正确
- 检查文件是否有执行权限
- 查看状态栏获取错误信息

### 3. 界面显示异常
- 尝试安装 `ttkthemes` 获得更好的界面效果
- 确保系统支持tkinter

## 📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情

## 🙏 致谢

- [pywebview](https://github.com/r0x0r/pywebview) - WebView库
- [PyInstaller](https://github.com/pyinstaller/pyinstaller) - 打包工具
- [psutil](https://github.com/giampaolo/psutil) - 系统和进程工具
```
