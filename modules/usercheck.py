from typing import Dict, List
import aiohttp
import asyncio


PLATFORMS = {
    "github": "https://github.com/{}",
    "twitter": "https://twitter.com/{}",
    "instagram": "https://www.instagram.com/{}/",
    "reddit": "https://www.reddit.com/user/{}",
    "medium": "https://medium.com/@{}",
    "telegram": "https://t.me/{}",
    "youtube": "https://www.youtube.com/@{}",
    "tiktok": "https://www.tiktok.com/@{}"
}


async def check_username(username: str, platforms: List[str] = None) -> Dict:
    username = username.strip().lower()
    
    if not username.replace("_", "").replace("-", "").isalnum():
        return {
            "username": username,
            "error": "Username tidak valid. Hanya huruf, angka, underscore, dan dash yang diperbolehkan."
        }
    
    if platforms is None:
        platforms = list(PLATFORMS.keys())
    else:
        platforms = [p.lower() for p in platforms if p.lower() in PLATFORMS]
    
    results = {
        "username": username,
        "checked_platforms": len(platforms),
        "results": {}
    }
    
    tasks = []
    for platform in platforms:
        tasks.append(check_platform(username, platform))
    
    platform_results = await asyncio.gather(*tasks)
    
    for platform, result in zip(platforms, platform_results):
        results["results"][platform] = result
    
    return results


async def check_platform(username: str, platform: str) -> Dict:
    url = PLATFORMS[platform].format(username)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
                allow_redirects=True
            ) as response:
                if response.status == 200:
                    return {
                        "exists": True,
                        "url": url,
                        "status_code": 200
                    }
                elif response.status == 404:
                    return {
                        "exists": False,
                        "url": url,
                        "status_code": 404
                    }
                else:
                    return {
                        "exists": "unknown",
                        "url": url,
                        "status_code": response.status,
                        "note": "Status tidak dapat dipastikan"
                    }
    except asyncio.TimeoutError:
        return {
            "exists": "unknown",
            "url": url,
            "note": "Request timeout"
        }
    except Exception as e:
        return {
            "exists": "unknown",
            "url": url,
            "note": f"Error: {str(e)[:50]}"
        }


def format_usercheck_result(data: Dict) -> str:
    if "error" in data:
        return f"❌ <b>Error:</b> {data['error']}"
    
    lines = [
        "👤 <b>Username Availability Check</b>\n",
        f"🔍 <b>Username:</b> <code>{data['username']}</code>",
        f"📊 <b>Platforms Checked:</b> {data['checked_platforms']}\n",
    ]
    
    results = data.get("results", {})
    
    exists_count = sum(1 for r in results.values() if r.get("exists") is True)
    not_exists_count = sum(1 for r in results.values() if r.get("exists") is False)
    unknown_count = sum(1 for r in results.values() if r.get("exists") == "unknown")
    
    lines.append(f"✅ <b>Found:</b> {exists_count}")
    lines.append(f"❌ <b>Available:</b> {not_exists_count}")
    lines.append(f"❔ <b>Unknown:</b> {unknown_count}\n")
    
    if exists_count > 0:
        lines.append("<b>🟢 Found on:</b>")
        for platform, result in results.items():
            if result.get("exists") is True:
                lines.append(f"  • <b>{platform.title()}:</b> {result['url']}")
    
    if not_exists_count > 0:
        lines.append("\n<b>🔴 Available on:</b>")
        for platform, result in results.items():
            if result.get("exists") is False:
                lines.append(f"  • {platform.title()}")
    
    if unknown_count > 0:
        lines.append("\n<b>⚪ Could not verify:</b>")
        for platform, result in results.items():
            if result.get("exists") == "unknown":
                note = result.get("note", "Unknown status")
                lines.append(f"  • {platform.title()} ({note})")
    
    lines.append("\n<i>⚠️ Note: Hasil ini hanya menunjukkan keberadaan akun publik.</i>")
    
    return "\n".join(lines)
