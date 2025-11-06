import re
import logging
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)


class SensitiveDataDetector:
    """
    Mendeteksi dan memblokir query yang mencoba mengakses data sensitif.
    Sesuai dengan kebijakan SECURITY.md dan prinsip privasi bot.
    """
    
    # Pattern untuk NIK (16 digit)
    NIK_PATTERN = re.compile(r'\b\d{16}\b')
    
    # Pattern untuk KTP (mirip NIK)
    KTP_PATTERN = re.compile(r'\b(?:ktp|nik|nomor.*induk|identitas.*kependudukan)\b', re.IGNORECASE)
    
    # Pattern untuk nomor rekening bank (10-16 digit, sering dengan spasi/dash)
    BANK_ACCOUNT_PATTERN = re.compile(r'\b\d{10,16}\b|\b\d{3,4}[-\s]\d{3,4}[-\s]\d{3,8}\b')
    
    # Pattern untuk kartu kredit (Luhn algorithm compatible)
    CREDIT_CARD_PATTERN = re.compile(r'\b(?:\d{4}[-\s]?){3}\d{4}\b')
    
    # Pattern untuk NPWP (15 digit dengan format xx.xxx.xxx.x-xxx.xxx)
    NPWP_PATTERN = re.compile(r'\b\d{2}[.\s]?\d{3}[.\s]?\d{3}[.\s]?\d[-.\s]?\d{3}[.\s]?\d{3}\b')
    
    # Keyword untuk data bank
    BANK_KEYWORDS = re.compile(
        r'\b(?:rekening|account.*number|bank.*account|bca|mandiri|bni|bri|balance|saldo|pin|cvv|cvc)\b',
        re.IGNORECASE
    )
    
    # Keyword untuk rekam kriminal
    CRIMINAL_KEYWORDS = re.compile(
        r'\b(?:rekam.*kriminal|criminal.*record|police.*record|catatan.*polisi|tahanan|penjara|terpidana|bui)\b',
        re.IGNORECASE
    )
    
    # Keyword untuk password/credential
    PASSWORD_KEYWORDS = re.compile(
        r'\b(?:password|passwd|pwd|credential|login.*info|email.*password|hack.*email|breach.*email)\b',
        re.IGNORECASE
    )
    
    # Keyword untuk biometric data
    BIOMETRIC_KEYWORDS = re.compile(
        r'\b(?:face.*recogni\w*|facial.*recogni\w*|finger.*print|retina.*scan|iris.*scan|biometric|sidik.*jari|wajah.*pengenalan)\b',
        re.IGNORECASE
    )
    
    # Keyword untuk proprietary/internal data
    PROPRIETARY_KEYWORDS = re.compile(
        r'\b(?:proprietary|confidential|internal.*data|trade.*secret|rahasia.*dagang|data.*internal|non.*public)\b',
        re.IGNORECASE
    )
    
    # Keyword untuk law enforcement
    LAW_ENFORCEMENT_KEYWORDS = re.compile(
        r'\b(?:law.*enforcement|penegak.*hukum|kepolisian|fbi|cia|interpol|bnn|kpk)\b',
        re.IGNORECASE
    )
    
    @classmethod
    def check_input(cls, text: str) -> Tuple[bool, List[str]]:
        """
        Mengecek apakah input mengandung data sensitif.
        
        Args:
            text: Input text untuk dicek
            
        Returns:
            Tuple (is_sensitive, violations_list)
        """
        violations = []
        
        # Check NIK/KTP
        if cls.NIK_PATTERN.search(text):
            violations.append("NIK/KTP (16 digit detected)")
        if cls.KTP_PATTERN.search(text):
            violations.append("Kata kunci KTP/NIK terdeteksi")
        
        # Check bank data
        if cls.BANK_KEYWORDS.search(text):
            violations.append("Kata kunci data bank terdeteksi")
        if cls.BANK_ACCOUNT_PATTERN.search(text) and any(
            keyword in text.lower() for keyword in ['bank', 'rekening', 'account', 'bca', 'mandiri', 'bni', 'bri']
        ):
            violations.append("Pola nomor rekening bank terdeteksi")
        
        # Check credit card
        if cls.CREDIT_CARD_PATTERN.search(text):
            potential_cc = cls.CREDIT_CARD_PATTERN.findall(text)
            for cc in potential_cc:
                digits_only = re.sub(r'[-\s]', '', cc)
                if len(digits_only) == 16 and cls._luhn_check(digits_only):
                    violations.append("Pola nomor kartu kredit terdeteksi")
                    break
        
        # Check NPWP
        if cls.NPWP_PATTERN.search(text):
            violations.append("Pola NPWP terdeteksi")
        
        # Check criminal records
        if cls.CRIMINAL_KEYWORDS.search(text):
            violations.append("Kata kunci rekam kriminal terdeteksi")
        
        # Check passwords/credentials
        if cls.PASSWORD_KEYWORDS.search(text):
            violations.append("Kata kunci password/credential terdeteksi")
        
        # Check biometric
        if cls.BIOMETRIC_KEYWORDS.search(text):
            violations.append("Kata kunci data biometrik terdeteksi")
        
        # Check proprietary
        if cls.PROPRIETARY_KEYWORDS.search(text):
            violations.append("Kata kunci data proprietary terdeteksi")
        
        # Check law enforcement
        if cls.LAW_ENFORCEMENT_KEYWORDS.search(text):
            violations.append("Kata kunci data penegak hukum terdeteksi")
        
        is_sensitive = len(violations) > 0
        
        if is_sensitive:
            logger.warning(f"Sensitive data detected: {violations}")
        
        return is_sensitive, violations
    
    @staticmethod
    def _luhn_check(card_number: str) -> bool:
        """
        Validasi nomor kartu kredit menggunakan Luhn algorithm.
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        for d in odd_digits:
            checksum += d
        for d in even_digits:
            doubled = d * 2
            checksum += doubled if doubled < 10 else doubled - 9
        return checksum % 10 == 0
    
    @staticmethod
    def get_warning_message(violations: List[str]) -> str:
        """
        Generate pesan warning untuk user.
        """
        violation_text = "\n".join([f"• {v}" for v in violations])
        
        return f"""
🚫 <b>PELANGGARAN TERDETEKSI</b>

Query Anda mengandung data sensitif yang dilarang:

{violation_text}

<b>Bot ini TIDAK DAPAT dan TIDAK AKAN mengakses:</b>
❌ Data pribadi sensitif (NIK/KTP, data bank, NPWP)
❌ Rekam kriminal atau data penegak hukum
❌ Akun email target atau password
❌ Face recognition atau identifikasi biometrik
❌ Data internal yang dilindungi atau proprietary

<b>PERINGATAN HUKUM:</b>
Penggunaan bot untuk mengakses data sensitif tanpa izin melanggar:
• UU Perlindungan Data Pribadi (UU PDP)
• UU Informasi dan Transaksi Elektronik (UU ITE)
• Peraturan internasional (GDPR, dll)

Aktivitas ini telah dicatat dalam audit log.

Gunakan /ethics untuk memahami penggunaan yang legitimate.
"""


class SensitiveDataFilter:
    """
    Middleware untuk memfilter dan memblokir query sensitif.
    """
    
    @staticmethod
    async def filter_message(text: str) -> Tuple[bool, str]:
        """
        Filter pesan untuk data sensitif.
        
        Returns:
            Tuple (allowed, warning_message)
        """
        is_sensitive, violations = SensitiveDataDetector.check_input(text)
        
        if is_sensitive:
            warning = SensitiveDataDetector.get_warning_message(violations)
            return False, warning
        
        return True, ""


# Ethics education content
ETHICS_MESSAGE = """
📚 <b>Panduan Etika & Penggunaan Legitimate</b>

<b>✅ PENGGUNAAN YANG DIPERBOLEHKAN:</b>

<b>1. Security Research & Auditing</b>
• Audit keamanan infrastruktur ANDA SENDIRI
• Penetration testing dengan izin tertulis
• Vulnerability assessment dengan scope terdefinisi
• Bug bounty hunting sesuai program rules

<b>2. Threat Intelligence</b>
• Mengecek reputasi IP/domain untuk incident response
• Analisis indikator of compromise (IoC)
• Monitoring threat landscape
• Attribution research dari sumber publik

<b>3. Digital Forensics</b>
• Investigasi insiden keamanan
• Analisis malware infrastructure
• Chain of custody untuk evidence
• Timeline reconstruction dari data publik

<b>4. OSINT Legitimate</b>
• Riset akademis dengan ethical clearance
• Journalism investigation untuk kepentingan publik
• Due diligence untuk business purposes
• Background checks dengan izin subjek

<b>❌ PENGGUNAAN YANG DILARANG:</b>

• Stalking atau harassment individu
• Doxing (expose informasi pribadi)
• Identity theft atau impersonation
• Unauthorized access ke sistem/akun
• Mass surveillance tanpa legal basis
• Pengecekan data pribadi tanpa consent
• Aktivitas yang melanggar Terms of Service
• Penggunaan untuk tujuan diskriminasi

<b>🎯 PRINSIP YANG HARUS DIIKUTI:</b>

<b>1. Legal Compliance</b>
• Patuhi UU PDP, UU ITE, dan regulasi terkait
• Respect Terms of Service dari platform/API
• Jangan bypass access controls
• Document legal basis untuk aktivitas

<b>2. Explicit Consent</b>
• Dapatkan izin tertulis untuk testing
• Respect scope & boundaries yang disepakati
• Stop immediately jika diminta
• Report findings securely & responsibly

<b>3. Data Minimization</b>
• Kumpulkan hanya data yang necessary
• Jangan store PII tanpa justifikasi
• Delete data setelah tidak diperlukan
• Use pseudonymization jika mungkin

<b>4. Do No Harm</b>
• Jangan cause damage atau disruption
• Protect individuals' privacy
• Consider potential consequences
• Prioritize safety & security

<b>📖 CONTOH KASUS PENGGUNAAN:</b>

<b>✅ BAIK:</b>
• "Saya admin server, ingin cek apakah IP 1.2.3.4 yang mengakses server saya adalah malicious"
• "Domain abc.com masuk email phishing, ingin cek reputasi & IoC terkait"
• "Riset akademis tentang botnet infrastructure (dengan ethical approval)"

<b>❌ BURUK:</b>
• "Cek NIK/KTP orang ini untuk verifikasi identitas"
• "Bagaimana cara hack email mantan pacar saya?"
• "Cari data bank target untuk penipuan"
• "Track lokasi seseorang tanpa sepengetahuan mereka"

<b>🔗 RESOURCES LEBIH LANJUT:</b>

• OWASP Code of Conduct: https://owasp.org/www-policy/operational/code-of-conduct
• SANS Ethics Guidelines: https://www.sans.org/ethics/
• EC-Council Code of Ethics: https://www.eccouncil.org/code-of-ethics/
• Indonesia UU PDP: https://jdih.kominfo.go.id/

<b>📞 LAPORKAN PENYALAHGUNAAN:</b>

Jika Anda menemukan instance bot ini yang disalahgunakan:
• Email: abuse@example.com
• Sertakan evidence (screenshots, logs)
• Kami akan investigate & take action

<i>Dengan menggunakan bot ini, Anda menyetujui untuk mematuhi pedoman etika di atas.</i>

Ketik /help untuk kembali ke menu utama.
"""


def get_ethics_content() -> str:
    """Return ethics education content."""
    return ETHICS_MESSAGE
