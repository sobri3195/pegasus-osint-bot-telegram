from typing import Dict, List
import aiohttp


async def lookup_postcode(query: str) -> Dict:
    query = query.strip()
    
    if query.isdigit():
        result = await search_by_postcode(query)
    else:
        result = await search_by_area(query)
    
    return result


async def search_by_postcode(postcode: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kodepos.vercel.app/search",
                params={"q": postcode},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("data"):
                        results = data["data"][:10]
                        return {
                            "query": postcode,
                            "query_type": "postcode",
                            "count": len(results),
                            "results": [
                                {
                                    "postcode": r.get("postalCode"),
                                    "province": r.get("province"),
                                    "city": r.get("city"),
                                    "subdistrict": r.get("subdistrict"),
                                    "urban": r.get("urban")
                                }
                                for r in results
                            ]
                        }
                    else:
                        return {
                            "query": postcode,
                            "query_type": "postcode",
                            "count": 0,
                            "note": "Kode pos tidak ditemukan"
                        }
    except Exception as e:
        return {
            "query": postcode,
            "error": f"Gagal melakukan pencarian: {str(e)}"
        }
    
    return {"query": postcode, "error": "Gagal melakukan pencarian"}


async def search_by_area(area: str) -> Dict:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://kodepos.vercel.app/search",
                params={"q": area},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get("data"):
                        results = data["data"][:10]
                        return {
                            "query": area,
                            "query_type": "area",
                            "count": len(results),
                            "results": [
                                {
                                    "postcode": r.get("postalCode"),
                                    "province": r.get("province"),
                                    "city": r.get("city"),
                                    "subdistrict": r.get("subdistrict"),
                                    "urban": r.get("urban")
                                }
                                for r in results
                            ]
                        }
                    else:
                        return {
                            "query": area,
                            "query_type": "area",
                            "count": 0,
                            "note": "Area tidak ditemukan"
                        }
    except Exception as e:
        return {
            "query": area,
            "error": f"Gagal melakukan pencarian: {str(e)}"
        }
    
    return {"query": area, "error": "Gagal melakukan pencarian"}


def format_postcode_result(data: Dict) -> str:
    lines = [
        "📮 <b>Postal Code Lookup</b>\n",
        f"🔍 <b>Query:</b> {data['query']}",
        f"📊 <b>Type:</b> {data.get('query_type', 'unknown').title()}",
    ]
    
    if "error" in data:
        lines.append(f"\n❌ <b>Error:</b> {data['error']}")
        return "\n".join(lines)
    
    if "note" in data:
        lines.append(f"\n<i>ℹ️ {data['note']}</i>")
        return "\n".join(lines)
    
    count = data.get("count", 0)
    lines.append(f"📈 <b>Found:</b> {count} result(s)")
    
    if count > 0:
        lines.append("")
        for i, result in enumerate(data.get("results", []), 1):
            lines.append(f"<b>{i}. {result.get('urban', 'N/A')}</b>")
            lines.append(f"   📮 Kode Pos: <code>{result.get('postcode', 'N/A')}</code>")
            lines.append(f"   📍 Kecamatan: {result.get('subdistrict', 'N/A')}")
            lines.append(f"   🏙 Kota/Kab: {result.get('city', 'N/A')}")
            lines.append(f"   🗺 Provinsi: {result.get('province', 'N/A')}")
            lines.append("")
    
    return "\n".join(lines)
