from typing import Dict, Optional
import aiohttp
from utils.config import settings


async def check_breach(domain: str) -> Dict:
    domain = domain.lower().strip()
    
    if not settings.hibp_api_key:
        return {
            "domain": domain,
            "note": "API key HaveIBeenPwned tidak dikonfigurasi. "
                   "Dapatkan API key di https://haveibeenpwned.com/API/Key"
        }
    
    result = await check_hibp_domain(domain)
    return result


async def check_hibp_domain(domain: str) -> Dict:
    try:
        headers = {
            "hibp-api-key": settings.hibp_api_key,
            "User-Agent": "Pegasus-OSINT-Bot"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://haveibeenpwned.com/api/v3/breaches",
                headers=headers,
                params={"domain": domain},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    breaches = await response.json()
                    
                    return {
                        "domain": domain,
                        "breach_count": len(breaches),
                        "breaches": [
                            {
                                "name": b.get("Name"),
                                "title": b.get("Title"),
                                "breach_date": b.get("BreachDate"),
                                "added_date": b.get("AddedDate"),
                                "pwn_count": b.get("PwnCount"),
                                "description": b.get("Description", "")[:200],
                                "data_classes": b.get("DataClasses", [])
                            }
                            for b in breaches[:5]
                        ]
                    }
                elif response.status == 404:
                    return {
                        "domain": domain,
                        "breach_count": 0,
                        "note": "Tidak ada data breach yang ditemukan untuk domain ini"
                    }
                elif response.status == 401:
                    return {
                        "domain": domain,
                        "error": "API key tidak valid atau expired"
                    }
                elif response.status == 429:
                    return {
                        "domain": domain,
                        "error": "Rate limit tercapai. Tunggu beberapa saat."
                    }
    except Exception as e:
        return {
            "domain": domain,
            "error": f"Gagal mengakses HaveIBeenPwned: {str(e)}"
        }
    
    return {"domain": domain, "error": "Gagal melakukan pengecekan"}


def format_breach_result(data: Dict) -> str:
    lines = [
        "🔓 <b>Data Breach Check</b>\n",
        f"🎯 <b>Domain:</b> <code>{data['domain']}</code>",
    ]
    
    if "error" in data:
        lines.append(f"\n❌ <b>Error:</b> {data['error']}")
        return "\n".join(lines)
    
    if "note" in data:
        lines.append(f"\n<i>ℹ️ {data['note']}</i>")
        if data.get("breach_count", 0) == 0:
            lines.append("\n✅ Domain ini tidak ditemukan dalam database breach yang diketahui.")
        return "\n".join(lines)
    
    breach_count = data.get("breach_count", 0)
    
    if breach_count == 0:
        lines.append("\n✅ <b>Tidak ada data breach yang ditemukan</b>")
    else:
        lines.append(f"\n⚠️ <b>Ditemukan {breach_count} breach(es)</b>\n")
        
        for breach in data.get("breaches", []):
            lines.append(f"<b>📌 {breach['title']}</b>")
            lines.append(f"  • Name: {breach['name']}")
            lines.append(f"  • Breach Date: {breach['breach_date']}")
            lines.append(f"  • Affected Accounts: {breach['pwn_count']:,}")
            
            if breach.get("data_classes"):
                classes = ", ".join(breach['data_classes'][:5])
                lines.append(f"  • Compromised Data: {classes}")
            
            lines.append("")
    
    lines.append("\n<i>⚠️ Note: Hasil ini hanya menunjukkan breach yang terdaftar di database publik.</i>")
    
    return "\n".join(lines)
