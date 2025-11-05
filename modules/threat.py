from typing import Dict, Optional
import aiohttp
from utils.config import settings


async def check_threat_intelligence(target: str, target_type: str = "auto") -> Dict:
    if target_type == "auto":
        if all(c in "0123456789." for c in target.replace(":", "")):
            target_type = "ip"
        else:
            target_type = "domain"
    
    results = {
        "target": target,
        "type": target_type,
        "sources": {}
    }
    
    if settings.virustotal_api_key:
        vt_result = await check_virustotal(target, target_type)
        if vt_result:
            results["sources"]["virustotal"] = vt_result
    
    if settings.abuseipdb_api_key and target_type == "ip":
        abuse_result = await check_abuseipdb(target)
        if abuse_result:
            results["sources"]["abuseipdb"] = abuse_result
    
    if not results["sources"]:
        results["note"] = "Tidak ada API key yang dikonfigurasi untuk threat intelligence"
    
    return results


async def check_virustotal(target: str, target_type: str) -> Optional[Dict]:
    if not settings.virustotal_api_key:
        return None
    
    try:
        headers = {"x-apikey": settings.virustotal_api_key}
        
        if target_type == "ip":
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{target}"
        else:
            url = f"https://www.virustotal.com/api/v3/domains/{target}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    attributes = data.get("data", {}).get("attributes", {})
                    stats = attributes.get("last_analysis_stats", {})
                    
                    return {
                        "malicious": stats.get("malicious", 0),
                        "suspicious": stats.get("suspicious", 0),
                        "harmless": stats.get("harmless", 0),
                        "undetected": stats.get("undetected", 0),
                        "reputation": attributes.get("reputation", 0),
                        "total_votes": {
                            "harmless": attributes.get("total_votes", {}).get("harmless", 0),
                            "malicious": attributes.get("total_votes", {}).get("malicious", 0)
                        }
                    }
                elif response.status == 404:
                    return {"note": "Target tidak ditemukan di database VirusTotal"}
                elif response.status == 401:
                    return {"error": "API key tidak valid"}
    except Exception as e:
        return {"error": f"Gagal mengakses VirusTotal: {str(e)}"}
    
    return None


async def check_abuseipdb(ip: str) -> Optional[Dict]:
    if not settings.abuseipdb_api_key:
        return None
    
    try:
        headers = {
            "Key": settings.abuseipdb_api_key,
            "Accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.abuseipdb.com/api/v2/check",
                headers=headers,
                params={"ipAddress": ip, "maxAgeInDays": 90},
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    ip_data = data.get("data", {})
                    
                    return {
                        "abuse_confidence_score": ip_data.get("abuseConfidenceScore", 0),
                        "total_reports": ip_data.get("totalReports", 0),
                        "num_distinct_users": ip_data.get("numDistinctUsers", 0),
                        "is_whitelisted": ip_data.get("isWhitelisted", False),
                        "country_code": ip_data.get("countryCode"),
                        "usage_type": ip_data.get("usageType"),
                        "isp": ip_data.get("isp")
                    }
                elif response.status == 401:
                    return {"error": "API key tidak valid"}
    except Exception as e:
        return {"error": f"Gagal mengakses AbuseIPDB: {str(e)}"}
    
    return None


def format_threat_result(data: Dict) -> str:
    lines = [
        "🛡️ <b>Threat Intelligence Check</b>\n",
        f"🎯 <b>Target:</b> <code>{data['target']}</code>",
        f"📊 <b>Type:</b> {data['type'].upper()}",
    ]
    
    if "note" in data:
        lines.append(f"\n<i>ℹ️ {data['note']}</i>")
        return "\n".join(lines)
    
    sources = data.get("sources", {})
    
    if "virustotal" in sources:
        vt = sources["virustotal"]
        if "error" in vt:
            lines.append(f"\n<b>🔍 VirusTotal:</b> ❌ {vt['error']}")
        elif "note" in vt:
            lines.append(f"\n<b>🔍 VirusTotal:</b> ℹ️ {vt['note']}")
        else:
            lines.append("\n<b>🔍 VirusTotal:</b>")
            lines.append(f"  • Malicious: {vt['malicious']} 🔴")
            lines.append(f"  • Suspicious: {vt['suspicious']} 🟡")
            lines.append(f"  • Harmless: {vt['harmless']} 🟢")
            lines.append(f"  • Undetected: {vt['undetected']}")
            lines.append(f"  • Reputation: {vt['reputation']}")
    
    if "abuseipdb" in sources:
        abuse = sources["abuseipdb"]
        if "error" in abuse:
            lines.append(f"\n<b>📊 AbuseIPDB:</b> ❌ {abuse['error']}")
        else:
            lines.append("\n<b>📊 AbuseIPDB:</b>")
            score = abuse['abuse_confidence_score']
            
            if score >= 75:
                risk = "🔴 HIGH RISK"
            elif score >= 50:
                risk = "🟠 MEDIUM RISK"
            elif score >= 25:
                risk = "🟡 LOW RISK"
            else:
                risk = "🟢 CLEAN"
            
            lines.append(f"  • Abuse Score: {score}% {risk}")
            lines.append(f"  • Total Reports: {abuse['total_reports']}")
            lines.append(f"  • Distinct Users: {abuse['num_distinct_users']}")
            
            if abuse.get("is_whitelisted"):
                lines.append(f"  • Status: ✅ Whitelisted")
            
            if abuse.get("country_code"):
                lines.append(f"  • Country: {abuse['country_code']}")
            if abuse.get("isp"):
                lines.append(f"  • ISP: {abuse['isp']}")
    
    if not sources:
        lines.append("\n<i>⚠️ Tidak ada sumber threat intelligence yang tersedia</i>")
    
    return "\n".join(lines)
