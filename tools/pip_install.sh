#!/bin/bash

## 创建一个新的虚拟环境
#python -m venv venv
#
## 激活虚拟环境
#source venv/bin/activate

# 安装所需的 Python 包
cd /opt/TestPlatform
pip3 install -r ubuntu_requirements.txt

# 验证下载过程是否出错
if [ $? -eq 0 ]; then
    echo "Packages installed successfully."
else
    echo "Error occurred while installing packages."
fi

# 确认安装的包是否可用
pip freeze > installed_packages.txt
echo "Installed packages:"
cat installed_packages.txt

# 退出虚拟环境
#deactivate
