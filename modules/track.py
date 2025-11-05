from typing import Dict, Optional
import aiohttp
import re


async def track_package(tracking_number: str) -> Dict:
    tracking_number = tracking_number.strip().upper()
    
    courier = detect_courier(tracking_number)
    
    result = {
        "tracking_number": tracking_number,
        "courier": courier,
        "status": "unknown"
    }
    
    if courier == "unknown":
        result["note"] = (
            "Kurir tidak dapat dideteksi otomatis. "
            "Silakan gunakan format: /track <kurir> <resi>\n"
            "Contoh: /track jne ABC123456789"
        )
        return result
    
    if courier == "jne":
        tracking_result = await track_jne(tracking_number)
    elif courier == "jnt":
        tracking_result = await track_jnt(tracking_number)
    elif courier == "sicepat":
        tracking_result = await track_sicepat(tracking_number)
    else:
        tracking_result = {
            "note": f"Tracking untuk kurir {courier} belum tersedia atau memerlukan API key"
        }
    
    result.update(tracking_result)
    return result


def detect_courier(tracking_number: str) -> str:
    tracking_number = tracking_number.upper()
    
    if re.match(r'^JP\d{12}$', tracking_number):
        return "jne"
    
    if re.match(r'^JT\d{10,15}$', tracking_number):
        return "jnt"
    
    if re.match(r'^\d{12}$', tracking_number):
        return "sicepat"
    
    if tracking_number.startswith(('1Z', 'T')):
        return "ups"
    
    if len(tracking_number) == 10 or len(tracking_number) == 12:
        return "pos_indonesia"
    
    return "unknown"


async def track_jne(tracking_number: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.binderbyte.com/v1/track",
                params={
                    "courier": "jne",
                    "awb": tracking_number
                },
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("status") == 200:
                        tracking_data = data.get("data", {})
                        history = tracking_data.get("history", [])
                        
                        return {
                            "status": "success",
                            "service": tracking_data.get("summary", {}).get("service"),
                            "origin": tracking_data.get("detail", {}).get("origin"),
                            "destination": tracking_data.get("detail", {}).get("destination"),
                            "current_status": history[0] if history else {},
                            "history": history[:5]
                        }
    except Exception as e:
        return {"error": f"Gagal melakukan tracking: {str(e)}"}
    
    return {
        "note": "Tracking JNE memerlukan API key. Daftarkan di https://binderbyte.com"
    }


async def track_jnt(tracking_number: str) -> Dict:
    return {
        "note": "Tracking J&T memerlukan API key resmi dari J&T Express"
    }


async def track_sicepat(tracking_number: str) -> Dict:
    return {
        "note": "Tracking SiCepat memerlukan API key resmi dari SiCepat Ekspres"
    }


def format_track_result(data: Dict) -> str:
    lines = [
        "📦 <b>Package Tracking</b>\n",
        f"📋 <b>Resi:</b> <code>{data['tracking_number']}</code>",
        f"🚚 <b>Kurir:</b> {data['courier'].upper()}",
    ]
    
    if "error" in data:
        lines.append(f"\n❌ <b>Error:</b> {data['error']}")
        return "\n".join(lines)
    
    if "note" in data:
        lines.append(f"\n<i>ℹ️ {data['note']}</i>")
        return "\n".join(lines)
    
    if data.get("status") == "success":
        if data.get("service"):
            lines.append(f"📮 <b>Service:</b> {data['service']}")
        
        if data.get("origin"):
            lines.append(f"📍 <b>Origin:</b> {data['origin']}")
        
        if data.get("destination"):
            lines.append(f"🎯 <b>Destination:</b> {data['destination']}")
        
        current = data.get("current_status", {})
        if current:
            lines.append(f"\n<b>📊 Status Terkini:</b>")
            lines.append(f"  • {current.get('desc', 'N/A')}")
            lines.append(f"  • {current.get('date', 'N/A')}")
        
        history = data.get("history", [])
        if history and len(history) > 1:
            lines.append(f"\n<b>📜 Riwayat:</b>")
            for entry in history[1:4]:
                lines.append(f"  • {entry.get('date', 'N/A')}: {entry.get('desc', 'N/A')}")
    
    return "\n".join(lines)
