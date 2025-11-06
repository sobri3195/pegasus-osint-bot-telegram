import pytest
from utils.sensitive_data import SensitiveDataDetector, SensitiveDataFilter


class TestSensitiveDataDetector:
    """Test cases for sensitive data detection."""
    
    def test_nik_detection(self):
        """Test NIK (16 digit) detection."""
        text = "Tolong cek NIK 1234567890123456 ini"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("NIK" in v or "16 digit" in v for v in violations)
    
    def test_ktp_keyword_detection(self):
        """Test KTP keyword detection."""
        text = "Bagaimana cara cek nomor KTP seseorang?"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("KTP" in v or "NIK" in v for v in violations)
    
    def test_bank_keyword_detection(self):
        """Test bank-related keyword detection."""
        text = "Cari tahu nomor rekening bank dia"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("bank" in v.lower() for v in violations)
    
    def test_npwp_pattern_detection(self):
        """Test NPWP pattern detection."""
        text = "NPWP 12.345.678.9-012.345"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("NPWP" in v for v in violations)
    
    def test_criminal_record_detection(self):
        """Test criminal record keyword detection."""
        text = "Cek rekam kriminal orang ini"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("kriminal" in v.lower() for v in violations)
    
    def test_password_detection(self):
        """Test password/credential keyword detection."""
        text = "Hack email password target"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("password" in v.lower() or "credential" in v.lower() for v in violations)
    
    def test_biometric_detection(self):
        """Test biometric keyword detection."""
        text = "Face recognition untuk identifikasi"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("biometric" in v.lower() or "biometrik" in v.lower() for v in violations)
    
    def test_proprietary_detection(self):
        """Test proprietary data keyword detection."""
        text = "Akses confidential internal data perusahaan"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("proprietary" in v.lower() or "confidential" in v.lower() or "internal" in v.lower() for v in violations)
    
    def test_law_enforcement_detection(self):
        """Test law enforcement keyword detection."""
        text = "Data kepolisian atau penegak hukum"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("penegak hukum" in v.lower() or "kepolisian" in v.lower() for v in violations)
    
    def test_legitimate_ip_query(self):
        """Test that legitimate IP queries are not flagged."""
        text = "8.8.8.8"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert not is_sensitive
        assert len(violations) == 0
    
    def test_legitimate_domain_query(self):
        """Test that legitimate domain queries are not flagged."""
        text = "google.com"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert not is_sensitive
        assert len(violations) == 0
    
    def test_legitimate_username_query(self):
        """Test that legitimate username queries are not flagged."""
        text = "johndoe"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert not is_sensitive
        assert len(violations) == 0
    
    def test_tracking_number_not_flagged(self):
        """Test that tracking numbers are not falsely flagged."""
        text = "JP1234567890"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert not is_sensitive
    
    def test_postcode_not_flagged(self):
        """Test that postal codes are not flagged."""
        text = "12345"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert not is_sensitive
    
    def test_credit_card_pattern(self):
        """Test credit card pattern detection with Luhn check."""
        text = "4539-1488-0343-6467"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert any("kartu kredit" in v.lower() for v in violations)
    
    def test_multiple_violations(self):
        """Test detection of multiple violations in one text."""
        text = "Cek NIK 1234567890123456 dan rekening bank serta password email"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
        assert len(violations) >= 3
    
    def test_case_insensitive_detection(self):
        """Test that detection is case-insensitive."""
        text = "REKAM KRIMINAL"
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        assert is_sensitive
    
    def test_warning_message_generation(self):
        """Test that warning message is properly generated."""
        violations = ["NIK detected", "Bank keyword detected"]
        warning = SensitiveDataDetector.get_warning_message(violations)
        assert "PELANGGARAN TERDETEKSI" in warning
        assert "NIK detected" in warning
        assert "Bank keyword detected" in warning
    
    def test_luhn_algorithm_valid(self):
        """Test Luhn algorithm with valid credit card number."""
        valid_cc = "4539148803436467"
        assert SensitiveDataDetector._luhn_check(valid_cc)
    
    def test_luhn_algorithm_invalid(self):
        """Test Luhn algorithm with invalid credit card number."""
        invalid_cc = "1234567890123456"
        assert not SensitiveDataDetector._luhn_check(invalid_cc)


class TestSensitiveDataFilter:
    """Test cases for sensitive data filter."""
    
    @pytest.mark.asyncio
    async def test_filter_allows_legitimate_input(self):
        """Test that filter allows legitimate queries."""
        text = "8.8.8.8"
        allowed, warning = await SensitiveDataFilter.filter_message(text)
        assert allowed
        assert warning == ""
    
    @pytest.mark.asyncio
    async def test_filter_blocks_sensitive_input(self):
        """Test that filter blocks sensitive queries."""
        text = "NIK 1234567890123456"
        allowed, warning = await SensitiveDataFilter.filter_message(text)
        assert not allowed
        assert warning != ""
        assert "PELANGGARAN" in warning
    
    @pytest.mark.asyncio
    async def test_filter_with_bank_data(self):
        """Test filter with bank-related query."""
        text = "cek rekening bank mandiri"
        allowed, warning = await SensitiveDataFilter.filter_message(text)
        assert not allowed
        assert "bank" in warning.lower()
    
    @pytest.mark.asyncio
    async def test_filter_with_domain_query(self):
        """Test filter allows domain queries."""
        text = "google.com"
        allowed, warning = await SensitiveDataFilter.filter_message(text)
        assert allowed


class TestEthicsContent:
    """Test ethics content availability."""
    
    def test_ethics_content_exists(self):
        """Test that ethics content is available."""
        from utils.sensitive_data import get_ethics_content
        content = get_ethics_content()
        assert content is not None
        assert len(content) > 0
        assert "Panduan Etika" in content
        assert "PENGGUNAAN YANG DIPERBOLEHKAN" in content
        assert "PENGGUNAAN YANG DILARANG" in content
