import pytest
from modules.domain import (
    get_domain_info,
    format_domain_result,
    is_valid_domain,
    resolve_domain
)


def test_is_valid_domain():
    assert is_valid_domain("google.com") == True
    assert is_valid_domain("sub.domain.example.com") == True
    assert is_valid_domain("123.com") == True
    
    assert is_valid_domain("invalid domain") == False
    assert is_valid_domain("domain..com") == False
    assert is_valid_domain("") == False
    assert is_valid_domain("a" * 255) == False


@pytest.mark.asyncio
async def test_resolve_domain_valid():
    ips = await resolve_domain("google.com")
    
    assert len(ips) > 0
    assert all("." in ip or ":" in ip for ip in ips)


@pytest.mark.asyncio
async def test_resolve_domain_invalid():
    ips = await resolve_domain("this-domain-definitely-does-not-exist-12345.com")
    
    assert len(ips) == 0


@pytest.mark.asyncio
async def test_get_domain_info_valid():
    result = await get_domain_info("google.com")
    
    assert "domain" in result
    assert result["domain"] == "google.com"
    assert "dns_records" in result
    assert "ip_addresses" in result
    assert "error" not in result


@pytest.mark.asyncio
async def test_get_domain_info_invalid():
    result = await get_domain_info("invalid domain with spaces")
    
    assert "error" in result


def test_format_domain_result_valid():
    data = {
        "domain": "example.com",
        "ip_addresses": ["93.184.216.34"],
        "dns_records": {
            "A": ["93.184.216.34"],
            "MX": ["10 mail.example.com"]
        },
        "whois": {
            "registrar": "Example Registrar"
        }
    }
    
    formatted = format_domain_result(data)
    
    assert "example.com" in formatted
    assert "93.184.216.34" in formatted
    assert "DNS Records" in formatted


def test_format_domain_result_error():
    data = {"error": "Format domain tidak valid"}
    
    formatted = format_domain_result(data)
    
    assert "Error" in formatted
