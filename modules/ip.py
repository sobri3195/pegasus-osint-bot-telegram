import socket
import ipaddress
from typing import Optional, Dict
import asyncio
import aiohttp


async def get_ip_info(ip: str) -> Dict:
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return {"error": "Format IP tidak valid"}
    
    result = {
        "ip": ip,
        "type": "IPv4" if "." in ip else "IPv6",
        "reverse_dns": await get_reverse_dns(ip),
        "geolocation": await get_geolocation(ip),
        "whois": await get_whois_info(ip)
    }
    
    return result


async def get_reverse_dns(ip: str) -> Optional[str]:
    try:
        loop = asyncio.get_event_loop()
        hostname, _, _ = await loop.run_in_executor(
            None, socket.gethostbyaddr, ip
        )
        return hostname
    except (socket.herror, socket.gaierror):
        return None


async def get_geolocation(ip: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"http://ip-api.com/json/{ip}",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "success":
                        return {
                            "country": data.get("country"),
                            "country_code": data.get("countryCode"),
                            "region": data.get("regionName"),
                            "city": data.get("city"),
                            "isp": data.get("isp"),
                            "org": data.get("org"),
                            "as": data.get("as"),
                            "lat": data.get("lat"),
                            "lon": data.get("lon")
                        }
    except Exception as e:
        return {"error": str(e)}
    
    return {}


async def get_whois_info(ip: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://ipinfo.io/{ip}/json",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "hostname": data.get("hostname"),
                        "org": data.get("org"),
                        "asn": data.get("org", "").split()[0] if data.get("org") else None,
                        "postal": data.get("postal"),
                        "timezone": data.get("timezone")
                    }
    except Exception:
        pass
    
    return {}


def format_ip_result(data: Dict) -> str:
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    lines = [
        "🔍 <b>IP Lookup</b>\n",
        f"📍 <b>IP:</b> <code>{data['ip']}</code>",
        f"🔢 <b>Type:</b> {data['type']}",
    ]
    
    if data.get("reverse_dns"):
        lines.append(f"🌐 <b>Reverse DNS:</b> <code>{data['reverse_dns']}</code>")
    
    geo = data.get("geolocation", {})
    if geo and "error" not in geo:
        lines.append("\n<b>📍 Geolocation:</b>")
        if geo.get("country"):
            lines.append(f"  • Country: {geo['country']} ({geo.get('country_code', 'N/A')})")
        if geo.get("region"):
            lines.append(f"  • Region: {geo['region']}")
        if geo.get("city"):
            lines.append(f"  • City: {geo['city']}")
        if geo.get("isp"):
            lines.append(f"  • ISP: {geo['isp']}")
        if geo.get("org"):
            lines.append(f"  • Organization: {geo['org']}")
        if geo.get("as"):
            lines.append(f"  • ASN: {geo['as']}")
        if geo.get("lat") and geo.get("lon"):
            lines.append(f"  • Coordinates: {geo['lat']}, {geo['lon']}")
    
    whois = data.get("whois", {})
    if whois:
        lines.append("\n<b>ℹ️ WHOIS Info:</b>")
        if whois.get("hostname"):
            lines.append(f"  • Hostname: {whois['hostname']}")
        if whois.get("org"):
            lines.append(f"  • Organization: {whois['org']}")
        if whois.get("timezone"):
            lines.append(f"  • Timezone: {whois['timezone']}")
    
    return "\n".join(lines)
