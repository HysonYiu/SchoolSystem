# 📚 SchoolSystem - Windows PC 部署指南

> 在 Windows PC 上快速部署 SchoolSystem

---

## 🚀 快速开始（3 个步骤）

### 步骤 1：启动服务
双击 `run.bat` 或在命令提示符运行：
```cmd
run.bat
```

### 步骤 2：访问 Web UI
打开浏览器访问：
- **本地**：`http://127.0.0.1:8081`
- **网络**：`http://192.168.68.53:8081`（替换为你的 IP）

### 步骤 3：首次登录
- **用户密钥**：`schoolsystem2026`（在 `.env` 中配置）
- **管理员密钥**：`admin2026`（在 `.env` 中配置）

---

## ⚙️ 配置文件

编辑 `.env` 文件配置以下内容：

| 项目 | 默认值 | 说明 |
|------|--------|------|
| `SECRET_KEY` | `schoolsystem2026` | 用户登录密钥 |
| `ADMIN_KEY` | `admin2026` | 管理员密钥 |
| `PORT` | `8081` | 服务端口 |
| `BIND_HOST` | `0.0.0.0` | 绑定地址（所有网卡） |
| `ESP8266_IP` | `192.168.68.55` | WOL 网关 IP（如启用） |

### 可选：AI 和 Discord 功能

```env
# Discord Bot（可选）
DISCORD_TOKEN=your_token_here
DISCORD_GUILD_ID=your_guild_id

# AI 功能（可选）
DEEPSEEK_API_KEY=your_key_here
POE_API_KEY=your_key_here
```

---

## 🛑 停止服务

### 方法 1：双击停止脚本
```cmd
stop.bat
```

### 方法 2：命令行
```cmd
taskkill /F /IM python.exe
```

### 方法 3：Ctrl + C（前台模式）
如果在命令提示符运行，按 `Ctrl + C` 停止

---

## 📊 开启时自动启动

### 方法 1：创建快捷方式到启动文件夹

1. 右键点击 `run.bat`
2. **发送到** → **桌面（创建快捷方式）**
3. 将快捷方式移到：
   ```
   C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```
4. 重启电脑时自动启动

### 方法 2：Windows 任务计划（推荐）

1. 打开 **任务计划程序**（`taskschd.msc`）
2. **创建任务** → 设置以下内容：
   - **名称**：SchoolSystem
   - **触发器**：登录时
   - **操作**：启动程序
   - **程序**：`C:\Users\user\Downloads\SchoolSystem\run.bat`
   - **起始于**：`C:\Users\user\Downloads\SchoolSystem`

---

## 🔗 网络访问

### 同一 WiFi 网络
其他设备可以访问：
```
http://192.168.68.53:8081
```

### 远程访问（VPN）
推荐使用 L2TP VPN 连接家中网络

### 不同网络（无 VPN）
❌ **不支持** - 出于安全考虑

---

## 📜 日志

查看运行日志：
```cmd
type schoolsystem.log
```

或在文本编辑器中打开 `schoolsystem.log`

---

## 🆘 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|--------|
| "Python not found" | Python 未安装 | 安装 Python 3.10+：https://www.python.org |
| 端口已被占用 | 其他程序使用 8081 | 改 `.env` 中的 `PORT` |
| 无法访问（本地可以） | 防火墙阻止 | 允许 Python 通过防火墙 |
| 数据库损坏 | `.db` 文件损坏 | 删除 `schoolsystem.db`，重启自动重建 |

---

## 🔄 更新系统

1. 打开 Admin Panel：`http://127.0.0.1:8081/admin`
2. 登入 **Admin Key**
3. 点 **📊 更新** 标签
4. 点 **立即更新** 按钮
5. 系统自动重启

---

## 🎯 常见任务

### 改密钥
编辑 `.env`：
```env
SECRET_KEY=your_new_key
ADMIN_KEY=your_new_admin_key
```
然后重启服务

### 改端口
编辑 `.env`：
```env
PORT=8082
```

### 启用 Discord Bot
获取 Discord Token 后，编辑 `.env`：
```env
DISCORD_TOKEN=your_token
DISCORD_GUILD_ID=your_guild_id
```
重启服务

### 启用 AI 功能
获取 API Key 后，编辑 `.env`：
```env
DEEPSEEK_API_KEY=sk-xxxxx
POE_API_KEY=your_poe_key
```
重启服务

---

## 💾 备份数据

### 备份数据库
复制 `schoolsystem.db` 到安全位置

### 备份配置
复制 `.env` 文件到安全位置

### 完整备份
复制整个 `SchoolSystem` 文件夹

---

## 🔒 安全建议

- ✅ 更改默认密钥（`.env`）
- ✅ 在家中 WiFi 中使用
- ✅ 远程访问时使用 VPN
- ✅ 定期备份数据
- ⚠️ 不要在公网上直接暴露

---

## 📱 移动设备访问

在同一 WiFi 中，手机/平板可以访问：
```
http://192.168.68.53:8081
```

---

## 📞 获取帮助

- 📖 查看 `README.md` 了解功能
- 🐛 报告 Bug：https://github.com/HysonYiu/SchoolSystem/issues
- 💬 讨论：https://github.com/HysonYiu/SchoolSystem/discussions

---

**祝你使用愉快！** 🚀
