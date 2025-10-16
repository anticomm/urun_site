import requests
import json

# Kaynaklar
BASE_URL = "https://iptv-org.github.io/api"
CHANNELS_URL = f"{BASE_URL}/channels.json"
STREAMS_URL = f"{BASE_URL}/streams.json"
LOGOS_URL = f"{BASE_URL}/logos.json"
BLOCKLIST_URL = f"{BASE_URL}/blocklist.json"

# Verileri çek
channels = requests.get(CHANNELS_URL).json()
streams = requests.get(STREAMS_URL).json()
logos = requests.get(LOGOS_URL).json()
blocklist = requests.get(BLOCKLIST_URL).json()

# Blocklist'e giren kanalları filtrele
blocked_channels = set(blocklist)

# Kanal ID → kanal adı eşlemesi
channel_map = {c["id"]: c for c in channels}
logo_map = {l["channel"]: l["url"] for l in logos}

# M3U dosyasını oluştur
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for stream in streams:
        cid = stream["channel"]
        if cid not in channel_map or cid in blocked_channels:
            continue

        channel = channel_map[cid]
        name = stream.get("title") or channel.get("name") or "Unknown"
        url = stream["url"]
        logo = logo_map.get(cid, "")
        group = channel.get("country", "Unknown")

        extinf = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{url}\n'
        f.write(extinf)

print("✅ playlist.m3u dosyası oluşturuldu.")
