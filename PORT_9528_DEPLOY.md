# 客户自动调研系统 - 传统部署指南（自定义端口版）

## 🚀 最简单的执行命令（复制粘贴即用）

### 假设你已经上传了 zip 包到服务器，现在要部署到 9528 端口

#### 第 1 步：解压 zip 文件

```bash
cd /tmp
unzip customer-research-system.zip
# 或者 unzip /path/to/your/file.zip
```

#### 第 2 步：移动到应用目录

```bash
sudo mkdir -p /srv/apps/customer-research-system
cd /tmp/customer-research-system  # 根据实际解压目录调整
sudo cp -r . /srv/apps/customer-research-system/
cd /srv/apps/customer-research-system
sudo chown -R $USER:$USER .
```

#### 第 3 步：配置环境变量

```bash
cp backend/.env.example backend/.env
nano backend/.env
# 找到 DEEPSEEK_API_KEY 改成你的 API Key
# 按 Ctrl+X → Y → Enter 保存
```

#### 第 4 步：安装依赖

```bash
cd backend
sudo pip3 install --upgrade pip
sudo pip3 install -r requirements.txt
sudo pip3 install gunicorn
```

#### 第 5 步：配置 Systemd 服务（关键：指定 9528 端口）

```bash
APP_DIR="/srv/apps/customer-research-system/backend"
USER=$(whoami)

sudo tee /etc/systemd/system/customer-research.service > /dev/null << EOF
[Unit]
Description=Customer Research System
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
Environment="PATH=/usr/local/bin:/usr/bin"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:9528 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
```

#### 第 6 步：启动应用

```bash
sudo systemctl start customer-research
sudo systemctl enable customer-research

# 验证
sleep 2
curl http://localhost:9528/api/health
```

#### 第 7 步（可选）：配置 Nginx（推荐用 Nginx 代理）

```bash
sudo apt-get install -y nginx

sudo tee /etc/nginx/sites-available/customer-research > /dev/null << 'EOF'
upstream app {
    server 127.0.0.1:9528;
}

server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    client_max_body_size 20M;

    access_log /var/log/nginx/customer-research-access.log;
    error_log /var/log/nginx/customer-research-error.log;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120;
        proxy_connect_timeout 120;
    }

    location /api/ {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 180;
        proxy_connect_timeout 180;
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
EOF

sudo ln -sf /etc/nginx/sites-available/customer-research /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

---

## ✅ 完成！现在你可以访问应用了

### 方式 1：直接访问 9528 端口

```bash
# 获取服务器 IP
hostname -I

# 然后在浏览器中访问
http://your_server_ip:9528
```

### 方式 2：通过 Nginx 代理访问（推荐）

```bash
# 在浏览器中访问（自动代理到 9528）
http://your_server_ip:80
```

---

## 📋 常用命令速查

| 操作 | 命令 |
|------|------|
| 查看状态 | `sudo systemctl status customer-research` |
| 查看日志 | `sudo journalctl -u customer-research -f` |
| 停止应用 | `sudo systemctl stop customer-research` |
| 重启应用 | `sudo systemctl restart customer-research` |
| 查看 9528 端口 | `sudo netstat -tulpn \| grep 9528` |
| 查看 Nginx 日志 | `sudo tail -f /var/log/nginx/customer-research-error.log` |
| 测试 API | `curl http://localhost:9528/api/health` |

---

## 🔥 一条命令验证是否成功

```bash
# 检查 9528 端口是否开放
sudo netstat -tulpn | grep 9528

# 应该看到类似输出：
# tcp        0      0 0.0.0.0:9528            0.0.0.0:*               LISTEN      12345/gunicorn

# 测试 API 端点
curl http://localhost:9528/api/health

# 应该看到：
# {"status": "ok", "message": "Service is running"}
```

---

## ⚠️ 重要提示

1. **防火墙配置**
   ```bash
   # 如果有防火墙，需要开放 9528 端口
   sudo ufw allow 9528/tcp
   sudo ufw allow 80/tcp
   ```

2. **端口被占用**
   ```bash
   # 查看 9528 端口是否被占用
   sudo lsof -i :9528
   
   # 如果有其他进程占用，需要先停止它
   sudo kill -9 <PID>
   ```

3. **修改端口后要重启应用**
   ```bash
   sudo systemctl restart customer-research
   ```

---

## 🎯 快速参考

- **应用内部运行端口**：9528（Gunicorn）
- **Nginx 代理端口**：80（可选）
- **配置文件**：`/etc/systemd/system/customer-research.service`
- **应用目录**：`/srv/apps/customer-research-system`
- **日志**：`sudo journalctl -u customer-research -f`

---

**就这么简单！现在你的应用运行在 9528 端口上了！** 🚀
