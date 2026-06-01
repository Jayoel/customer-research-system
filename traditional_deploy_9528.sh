#!/bin/bash

# 客户自动调研系统 - 传统部署脚本（9528 端口版）
# 需求: Python 3.10+, pip, unzip
# 使用: bash traditional_deploy_9528.sh

set -e

echo "========================================"
echo "客户自动调研系统 - 9528 端口部署"
echo "========================================"
echo ""

# 彩色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PORT=9528

# 步骤 1: 检查 Python 版本
echo -e "${YELLOW}[步骤1/8]${NC} 检查 Python 版本..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[步骤1/8] ✗ Python3 未安装${NC}"
    echo "请执行: sudo apt-get install -y python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}[步骤1/8] ✓ Python 版本: $PYTHON_VERSION${NC}"

# 步骤 2: 查找 zip 文件
echo -e "${YELLOW}[步骤2/8]${NC} 查找 zip 文件..."

ZIP_FILE=$(find /tmp -maxdepth 2 -name "*.zip" 2>/dev/null | head -1)

if [ -z "$ZIP_FILE" ]; then
    echo "请输入 zip 文件的完整路径："
    read -p "输入 zip 路径: " ZIP_FILE
fi

if [ ! -f "$ZIP_FILE" ]; then
    echo -e "${RED}[步骤2/8] ✗ zip 文件不存在: $ZIP_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}[步骤2/8] ✓ 找到 zip 文件: $ZIP_FILE${NC}"

# 步骤 3: 解压文件
echo -e "${YELLOW}[步骤3/8]${NC} 解压 zip 文件..."

if ! command -v unzip &> /dev/null; then
    echo -e "${YELLOW}安装 unzip...${NC}"
    sudo apt-get install -y unzip
fi

# 创建应用目录
APP_DIR="/srv/apps/customer-research-system"
sudo mkdir -p "$APP_DIR"
cd /tmp

# 中间解压目录
EXTRACT_DIR="/tmp/extract_$$"
mkdir -p "$EXTRACT_DIR"
cd "$EXTRACT_DIR"

unzip -q "$ZIP_FILE"

# 找到项目根目录
if [ -d "customer-research-system" ]; then
    sudo cp -r customer-research-system/* "$APP_DIR/"
elif [ -d "$(ls -d */ 2>/dev/null | head -1)" ]; then
    PROJ_DIR=$(ls -d */ | head -1)
    sudo cp -r "$PROJ_DIR"* "$APP_DIR/"
else
    sudo cp -r . "$APP_DIR/"
fi

# 清理中间目录
cd /tmp
rm -rf "$EXTRACT_DIR"

echo -e "${GREEN}[步骤3/8] ✓ 解压完成${NC}"

# 步骤 4: 配置环境变量
echo -e "${YELLOW}[步骤4/8]${NC} 配置环境变量..."

cd "$APP_DIR"

if [ ! -f "backend/.env" ]; then
    if [ -f "backend/.env.example" ]; then
        sudo cp backend/.env.example backend/.env
    else
        echo -e "${RED}不存在 .env.example 模板${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}[步骤4/8] ✓ .env 文件配置完成${NC}"
echo -e "${YELLOW}请手动编辑 backend/.env 文件${NC}"
echo -e "${YELLOW}找到 DEEPSEEK_API_KEY 一行，改成你的 API Key${NC}"
echo ""
echo -e "${YELLOW}sudo nano $APP_DIR/backend/.env${NC}"
echo ""
read -p "编辑完成后按 Enter 继续..."

# 步骤 5: 安装 Python 依赖
echo -e "${YELLOW}[步骤5/8]${NC} 安装 Python 依赖..."

cd "$APP_DIR/backend"

# 升级 pip
sudo pip3 install --upgrade pip setuptools wheel

# 安装依赖
if [ -f "requirements.txt" ]; then
    sudo pip3 install -r requirements.txt
else
    echo -e "${RED}不存在 requirements.txt${NC}"
    exit 1
fi

echo -e "${GREEN}[步骤5/8] ✓ Python 依赖安装完成${NC}"

# 步骤 6: 配置 Systemd 服务
echo -e "${YELLOW}[步骤6/8]${NC} 配置 Systemd 服务..."

WORKDIR="$APP_DIR/backend"
USER=$(whoami)

sudo tee /etc/systemd/system/customer-research.service > /dev/null << EOF
[Unit]
Description=Customer Research System
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$WORKDIR
Environment="PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:$PORT --timeout 120 --access-logfile /var/log/customer-research/access.log --error-logfile /var/log/customer-research/error.log app:app
Restart=on-failure
RestartSec=10
KillMode=mixed
KillSignal=SIGQUIT

[Install]
WantedBy=multi-user.target
EOF

# 创建日志目录
sudo mkdir -p /var/log/customer-research
sudo chown $USER:$USER /var/log/customer-research

# 重新加载 systemd
sudo systemctl daemon-reload

echo -e "${GREEN}[步骤6/8] ✓ Systemd 服务配置完成${NC}"

# 步骤 7: 启动应用
echo -e "${YELLOW}[步骤7/8]${NC} 启动应用..."

sudo systemctl start customer-research
sudo systemctl enable customer-research

sleep 3

if sudo systemctl is-active --quiet customer-research; then
    echo -e "${GREEN}[步骤7/8] ✓ 应用启动成功${NC}"
else
    echo -e "${RED}[步骤7/8] ✗ 应用启动失败${NC}"
    sudo systemctl status customer-research
    exit 1
fi

# 步骤 8: 验证应用
echo -e "${YELLOW}[步骤8/8]${NC} 验证应用..."

if curl -s http://localhost:$PORT/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}[步骤8/8] ✓ 应用验证成功${NC}"
else
    echo -e "${YELLOW}[步骤8/8] ⚠ 无法通过 localhost 访问，但应用已启动${NC}"
    echo -e "${YELLOW}请检查防火墙或使用外部 IP 测试${NC}"
fi

echo ""
echo "========================================"
echo -e "${GREEN}✓ 部署完成！${NC}"
echo "========================================"
echo ""
echo -e "${GREEN}应用地址${NC}": http://$(hostname -I | awk '{print $1}'):$PORT"
echo ""
echo -e "${GREEN}常用命令${NC}"
echo "  查看状态:     sudo systemctl status customer-research"
echo "  查看日志:     sudo journalctl -u customer-research -f"
echo "  停止应用:     sudo systemctl stop customer-research"
echo "  重新启动:     sudo systemctl restart customer-research"
echo "  查看 $PORT 端口: sudo netstat -tulpn | grep $PORT"
echo ""
echo -e "${YELLOW}防火墙配置${NC}:"
echo "  sudo ufw allow $PORT/tcp"
echo ""
