# Discord-Port-Monitor-Bot
這是一個會定期檢查指定主機的 TCP 端口是否能連線，並把狀態變化（開/關）以 embed 訊息推送到指定 Discord 頻道的機器人。 適合監控伺服器服務、Minecraft 伺服器、HTTP / SSH / 自訂服務

# 功能:
定期檢查 config.json 內列舉的主機與端口（非同步檢查）
若某個端口狀態（開或關）發生變化，立刻推播到 Discord
可自訂檢查間隔、超時時間與重試次數
支援 .env 載入 Discord Token 與頻道 ID
可透過 systemd 設為開機自動啟動

# 需求
1.Python 3.10+ 
2.一個擁有管理權限的伺服器 
3.能連外網的主機（Linux）

# 1.建立.env檔
在專案根目錄建立 .env
```
DISCORD_TOKEN=(你的機器人TOKEN)
CHANNEL_ID=(想發文的頻道ID)
ADDRESS=(你想監控的IP)
```

# 2. 在 Discord Developer Portal 建立 Bot
前往 Discord Developer Portal

點擊右上角 「New Application」 → 輸入名稱（例如：Port Monitor Bot）

左邊選單選 Bot → 點 「Add Bot」

點 「Reset Token」 → 複製顯示的 Token（非常重要，稍後放進 .env）

下方 Privileged Gateway Intents 保持預設（不需開啟 Message Intent）

左邊選單進入 OAuth2 → URL Generator

Scopes 勾選 bot

Bot Permissions 勾選：

✅ View Channels

✅ Send Messages

✅ Embed Links

產生的 URL 貼到瀏覽器開啟 → 選擇伺服器 → Authorize

# 3. 取得 Discord 頻道 ID
在 Discord App 開啟 設定 → 進階 → 開啟「開發者模式」

右鍵你要讓 Bot 發送通知的頻道 → Copy ID

把這串數字貼到 .env 的 DISCORD_CHANNEL_ID

# 4.下載與安裝
```
git clone https://github.com/<你的帳號>/discord-port-monitor.git
cd discord-port-monitor

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

# 5.啟動機器人
```
python bot.py
```
正常運行會出現
```
Logged in as PortMonitorBot
```

# 6.(選用）Linux 伺服器常駐執行（systemd）
```
[Unit]
Description=Discord Port Monitor Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/youruser/discord-port-monitor
ExecStart=/home/youruser/discord-port-monitor/venv/bin/python /home/youruser/discord-port-monitor/bot.py
Restart=always
RestartSec=5
User=youruser
EnvironmentFile=/home/youruser/discord-port-monitor/.env

[Install]
WantedBy=multi-user.target
```
執行
```
sudo systemctl daemon-reload
sudo systemctl enable dcportbot
sudo systemctl start dcportbot
sudo systemctl status dcportbot
```
