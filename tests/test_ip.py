import pytest
from modules.ip import get_ip_info, format_ip_result, get_reverse_dns


@pytest.mark.asyncio
async def test_get_ip_info_valid():
    result = await get_ip_info("8.8.8.8")
    
    assert "ip" in result
    assert result["ip"] == "8.8.8.8"
    assert result["type"] == "IPv4"
    assert "geolocation" in result
    assert "whois" in result
    assert "error" not in result


@pytest.mark.asyncio
async def test_get_ip_info_invalid():
    result = await get_ip_info("invalid_ip")
    
    assert "error" in result
    assert "tidak valid" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_ip_info_ipv6():
    result = await get_ip_info("2001:4860:4860::8888")
    
    assert "ip" in result
    assert result["type"] == "IPv6"


@pytest.mark.asyncio
async def test_get_reverse_dns_google():
    hostname = await get_reverse_dns("8.8.8.8")
    
    assert hostname is not None
    assert "google" in hostname.lower() or "dns" in hostname.lower()


@pytest.mark.asyncio
async def test_get_reverse_dns_invalid():
    hostname = await get_reverse_dns("0.0.0.0")
    assert hostname is None


def test_format_ip_result_valid():
    data = {
        "ip": "8.8.8.8",
        "type": "IPv4",
        "reverse_dns": "dns.google",
        "geolocation": {
            "country": "United States",
            "country_code": "US",
            "isp": "Google LLC"
        },
        "whois": {
            "org": "Google LLC"
        }
    }
    
    formatted = format_ip_result(data)
    
    assert "8.8.8.8" in formatted
    assert "IPv4" in formatted
    assert "Google" in formatted


def test_format_ip_result_error():
    data = {"error": "Format IP tidak valid"}
    
    formatted = format_ip_result(data)
    
    assert "Error" in formatted
    assert "tidak valid" in formatted
