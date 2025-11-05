import dns.resolver
import dns.exception
import socket
from typing import Dict, List
import aiohttp
import asyncio


async def get_domain_info(domain: str) -> Dict:
    domain = domain.lower().strip()
    
    if not is_valid_domain(domain):
        return {"error": "Format domain tidak valid"}
    
    result = {
        "domain": domain,
        "dns_records": await get_dns_records(domain),
        "whois": await get_domain_whois(domain),
        "ip_addresses": await resolve_domain(domain)
    }
    
    return result


def is_valid_domain(domain: str) -> bool:
    if not domain or len(domain) > 253:
        return False
    
    if '..' in domain:
        return False
    
    if not all(len(label) <= 63 for label in domain.split('.')):
        return False
    
    allowed = set('abcdefghijklmnopqrstuvwxyz0123456789.-')
    return all(c in allowed for c in domain.lower())


async def resolve_domain(domain: str) -> List[str]:
    try:
        loop = asyncio.get_event_loop()
        addr_info = await loop.run_in_executor(
            None, socket.getaddrinfo, domain, None
        )
        ips = list(set([addr[4][0] for addr in addr_info]))
        return ips
    except (socket.gaierror, socket.herror):
        return []


async def get_dns_records(domain: str) -> Dict:
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
    
    loop = asyncio.get_event_loop()
    
    for record_type in record_types:
        try:
            answers = await loop.run_in_executor(
                None, lambda: dns.resolver.resolve(domain, record_type)
            )
            
            if record_type == 'MX':
                records[record_type] = [
                    f"{r.preference} {r.exchange.to_text()}" 
                    for r in answers
                ]
            elif record_type == 'SOA':
                soa = answers[0]
                records[record_type] = [
                    f"Primary NS: {soa.mname.to_text()}, "
                    f"Admin: {soa.rname.to_text()}"
                ]
            else:
                records[record_type] = [r.to_text() for r in answers]
        
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.Timeout):
            continue
        except Exception:
            continue
    
    return records


async def get_domain_whois(domain: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.whoisxmlapi.com/whoisserver/WhoisService",
                params={
                    "domainName": domain,
                    "outputFormat": "json"
                },
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    whois_record = data.get("WhoisRecord", {})
                    
                    return {
                        "registrar": whois_record.get("registrarName"),
                        "created_date": whois_record.get("createdDate"),
                        "updated_date": whois_record.get("updatedDate"),
                        "expires_date": whois_record.get("expiresDate"),
                        "status": whois_record.get("status"),
                        "name_servers": whois_record.get("nameServers", {}).get("hostNames", [])
                    }
    except Exception:
        pass
    
    return {"note": "WHOIS data requires API key for detailed info"}


def format_domain_result(data: Dict) -> str:
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    lines = [
        "🌐 <b>Domain Lookup</b>\n",
        f"🔖 <b>Domain:</b> <code>{data['domain']}</code>",
    ]
    
    if data.get("ip_addresses"):
        lines.append(f"\n<b>📍 IP Addresses:</b>")
        for ip in data["ip_addresses"][:5]:
            lines.append(f"  • <code>{ip}</code>")
    
    dns = data.get("dns_records", {})
    if dns:
        lines.append("\n<b>🗂 DNS Records:</b>")
        
        for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']:
            if record_type in dns:
                lines.append(f"\n  <b>{record_type}:</b>")
                for record in dns[record_type][:3]:
                    lines.append(f"    • {record}")
    
    whois = data.get("whois", {})
    if whois and "note" not in whois:
        lines.append("\n<b>ℹ️ WHOIS Info:</b>")
        if whois.get("registrar"):
            lines.append(f"  • Registrar: {whois['registrar']}")
        if whois.get("created_date"):
            lines.append(f"  • Created: {whois['created_date']}")
        if whois.get("expires_date"):
            lines.append(f"  • Expires: {whois['expires_date']}")
    elif whois.get("note"):
        lines.append(f"\n<i>{whois['note']}</i>")
    
    return "\n".join(lines)
