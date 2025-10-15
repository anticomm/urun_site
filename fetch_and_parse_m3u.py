import requests
import re

def fetch_m3u(url: str) -> str:
    """GitHub raw URL'den M3U dosyasını çeker"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"M3U alınamadı: {response.status_code}")

def parse_m3u(m3u_text: str) -> list:
    """M3U içeriğini kanal adı ve stream URL olarak ayrıştırır"""
    lines = m3u_text.splitlines()
    channels = []
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            name_match = re.search(r',(.+)', lines[i])
            name = name_match.group(1).strip() if name_match else "Bilinmeyen"
            stream_url = lines[i+1] if i+1 < len(lines) else None
            if stream_url and stream_url.startswith("http"):
                channels.append({
                    "name": name,
                    "url": stream_url
                })
    return channels

def validate_stream(url: str) -> bool:
    """Stream URL çalışıyor mu diye kontrol eder"""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def save_verified_m3u(channels: list, output_path: str = "playlist_verified.m3u"):
    """Çalışan stream'leri M3U formatında dosyaya yazar"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            f.write(f"#EXTINF:-1,{ch['name']}\n")
            f.write(f"{ch['url']}\n")

def main():
    github_url = "https://iptv-org.github.io/iptv/index.m3u"
    m3u_text = fetch_m3u(github_url)
    channels = parse_m3u(m3u_text)

    print(f"{len(channels)} kanal bulundu.")
    verified = []

    for i, ch in enumerate(channels[:100]):  # İlk 100 kanalı test ediyoruz
        status = "✅" if validate_stream(ch["url"]) else "❌"
        print(f"{status} {ch['name']} → {ch['url']}")
        if status == "✅":
            verified.append(ch)

    print(f"\n✅ {len(verified)} stream çalışıyor. Dosyaya yazılıyor...")
    save_verified_m3u(verified)
    print("📁 playlist_verified.m3u dosyası oluşturuldu.")

if __name__ == "__main__":
    main()
