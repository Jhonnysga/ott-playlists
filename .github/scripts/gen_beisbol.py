#!/usr/bin/env python3
"""Genera beisbol.otc desde el backend de BéisbolPlay (vía funnel público)."""
import json
import urllib.request
import urllib.parse

FUNNEL = "https://jhon-pc.tailc7b9f2.ts.net"
OUT = "beisbol.otc"

def main():
    with urllib.request.urlopen(f"{FUNNEL}/index.php?api=videos", timeout=30) as r:
        data = json.loads(r.read().decode())
    live = data.get("live", []) if isinstance(data, dict) else []
    cats = {}
    channels = []
    for v in live:
        vid = v.get("id", "")
        if not vid:
            continue
        name = str(v.get("title", vid)).strip()
        logo = v.get("logo") or v.get("thumbnail") or ""
        group = v.get("channel") or "BéisbolPlay"
        if group not in cats:
            cats[group] = {"icon": "", "name": group}
        stream = f"{FUNNEL}/proxy.php?m3u8={urllib.parse.quote(vid)}"
        channels.append({
            "name": name,
            "icon": logo,
            "category": group,
            "epg_name": name,
            "url": stream,
        })
    otc = {
        "categories": cats,
        "provider": {
            "epg": "",
            "max_connections": 4,
            "refresh_minutes": 30,
            "user_message": "BéisbolPlay",
        },
        "channels": channels,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(otc, f, ensure_ascii=False)
    print(f"Generado {OUT} con {len(channels)} canales")

if __name__ == "__main__":
    main()
