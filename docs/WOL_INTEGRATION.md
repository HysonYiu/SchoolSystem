# ⚡ Wake-On-LAN (WOL) 集成指南

> 使用 ESP8266 通過 WiFi 遠程喚醒你的 PC

---

## 📋 概述

SchoolSystem 現在支援通過 **ESP8266-12E** 微控制器遠程喚醒你的 PC。按一個按鈕即可從任何地方開啟電腦。

| 組件 | 說明 |
|------|------|
| **SchoolSystem** | 管理界面 + API 服務器 |
| **ESP8266** | WiFi 網關，發送 Magic Packet |
| **PC** | 接收 WOL 信號並喚醒 |

---

## 🛠️ 硬件要求

- **ESP8266-12E 開發板**（Type-C FT232 版本）
- **WiFi 網絡**（家中或辦公室）
- **Windows/Linux PC**（支援 WOL）
- **USB 線**（燒錄程序）

---

## 🔧 硬件設置

### 第1步：PC BIOS 設置

1. 重啟電腦進入 BIOS（通常按 `F2`、`F10` 或 `Del`）
2. 找 **"Wake-On-LAN"** 或 **"Power On By PCI-E"** 選項
3. **啟用**
4. 保存並退出

### 第2步：Windows 網絡設置

1. **Control Panel** → **Network and Internet** → **Network Connections**
2. 右鍵你的網卡（乙太網路/WiFi）→ **Properties**
3. 點 **Configure** 按鈕
4. **Power Management** 標籤
5. ✅ **"Allow this device to wake the computer"**
6. 點 **OK**

### 第3步：獲取 PC MAC 地址

打開命令提示符：
```cmd
ipconfig /all
```

找你的網卡的 **Physical Address**，例如：
```
A4-0C-66-1B-48-81
```

---

## 📱 ESP8266 設置

### 安裝 Arduino IDE

1. 下載：https://www.arduino.cc/en/software
2. 安裝到預設位置
3. 打開 Arduino IDE

### 添加 ESP8266 支持

1. **File** → **Preferences**
2. **Additional Boards Manager URLs**：
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
3. **OK**

4. **Tools** → **Board** → **Boards Manager**
5. 搜索 `ESP8266`
6. 安裝 **"esp8266 by ESP8266 Community"**

### 編譯和上傳

1. 打開 `esp8266_wol.ino`（已包含在 SchoolSystem 中）
2. 編輯代碼中的配置：
   ```cpp
   const char* WIFI_SSID = "YourWiFiName";
   const char* WIFI_PASS = "YourPassword";
   byte TARGET_MAC[6] = {0xA4, 0x0C, 0x66, 0x1B, 0x48, 0x81}; // 你的 PC MAC
   ```

3. **Tools** 配置：
   - Board: **NodeMCU 1.0 (ESP-12E Module)**
   - Port: **COM3**（或你的 USB 端口）
   - Upload Speed: **115200**

4. **Sketch** → **Upload**

5. **Tools** → **Serial Monitor**（115200 baud）
   ```
   ========== ESP8266 WOL Gateway ==========
   Connecting to WiFi: YourWiFiName
   ✓ Connected!
   IP Address: 192.168.68.55
   HTTP server started on port 80
   ```

📝 **記下 ESP8266 的 IP 地址**（例如：192.168.68.55）

---

## 🔌 SchoolSystem 配置

### 第1步：添加 ESP8266_IP

編輯 `.env` 文件：
```bash
ESP8266_IP=192.168.68.55
```

替換為你的 ESP8266 IP 地址。

### 第2步：重啟 SchoolSystem

```bash
pkill -f "python main.py"
nohup bash start.sh > /dev/null 2>&1 &
```

---

## 🧪 測試

### 方法1：Admin Panel 按鈕

1. 打開 Admin Panel：`http://YOUR_IP:8081/admin`
2. **狀態** 標籤 → **快速操作**
3. 點 **⚡ 開機 PC** 按鈕
4. 看到 ✅ "Magic Packet 已發送"
5. 你的 PC 應該在 1-2 秒內喚醒

### 方法2：直接 HTTP 請求

```bash
curl -X POST http://ESP8266_IP/wol
# 應該返回: {"ok":true,"msg":"Magic packet sent"}
```

### 方法3：檢查 PC 狀態

在 PC 上打開 Event Viewer，查看 **Wake timers** 事件日誌確認收到 WOL 信號。

---

## 📡 技術細節

### Magic Packet 格式

Magic Packet 是一個 102 字節的網絡包：
```
[6 字節 0xFF][16 次重複的目標 MAC 地址]
```

### API 端點

```
POST /admin/wol
```

**必需參數**：
- Admin 認證（Cookie/Header/Query 中的 ADMIN_KEY）

**響應**：
```json
{
  "ok": true,
  "msg": "Magic packet sent"
}
```

### 環境變數

| 變數 | 說明 | 示例 |
|------|------|------|
| `ESP8266_IP` | ESP8266 的 IP 地址 | `192.168.68.55` |

---

## 🆘 故障排除

| 問題 | 原因 | 解決方案 |
|------|------|--------|
| ❌ "ESP8266_IP not set" | 環境變數未設置 | 檢查 `.env` 是否有 ESP8266_IP |
| ❌ "Network error" | 無法連接 ESP8266 | 確保 ESP8266 已連接到 WiFi，IP 正確 |
| ✅ "Magic Packet sent" 但 PC 未喚醒 | BIOS/網卡設置不對 | 檢查 WOL 是否在 BIOS 和網卡中啟用 |
| ❌ ESP8266 無法連接到 WiFi | WiFi 憑証錯誤 | 檢查代碼中的 SSID/密碼是否正確 |
| ❌ Serial Monitor 顯示亂碼 | 波特率不對 | 設置 Serial Monitor 為 **115200** |

---

## 🔒 安全考慮

- ✅ WOL 端點受 **Admin 認證** 保護
- ✅ ESP8266 運行在 **本地 WiFi**（不暴露在互聯網）
- ⚠️ 建議在家中 WiFi 中使用，遠程訪問請配置 VPN

---

## 📚 相關資源

- [ESP8266 官方文檔](https://arduino-esp8266.readthedocs.io/)
- [Wake-On-LAN 維基百科](https://en.wikipedia.org/wiki/Wake-on-LAN)
- [Magic Packet 規範](https://en.wikipedia.org/wiki/Wake-on-LAN#Magic_packet)

---

## 💡 擴展想法

- 🏠 集成家居自動化（燈光、空調等）
- 📱 構建移動應用控制面板
- ⏰ 設置定時開機計劃
- 📊 記錄開機歷史日誌

---

**祝你使用愉快！** 🚀
