import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message

from utils.config import settings
from utils.logging import setup_logging, audit_logger
from utils.auth import IsAdmin, IsWhitelisted, admin_required, whitelist_required
from utils.rate_limiting import rate_limiter

from modules.ip import get_ip_info, format_ip_result
from modules.domain import get_domain_info, format_domain_result
from modules.threat import check_threat_intelligence, format_threat_result
from modules.breach import check_breach, format_breach_result
from modules.track import track_package, format_track_result
from modules.postcode import lookup_postcode, format_postcode_result
from modules.usercheck import check_username, format_usercheck_result
from modules.report import report_manager, format_report_summary

logger = setup_logging(settings.log_level, settings.log_file)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

WELCOME_MESSAGE = """
🦅 <b>Pegasus OSINT Bot</b>

Selamat datang di Pegasus OSINT Bot - alat bantu riset OSINT yang fokus pada data teknis dan publik.

⚠️ <b>PERINGATAN PENTING - BACA DENGAN SEKSAMA</b>

Bot ini dirancang untuk penggunaan LEGITIMATE seperti:
• Audit keamanan dengan izin eksplisit
• Riset threat intelligence
• Incident response
• Pengumpulan informasi dari sumber publik

<b>DILARANG KERAS:</b>
❌ Mengakses/mencari data pribadi sensitif (NIK, rekening bank, NPWP, dll)
❌ Tracking individu tanpa izin
❌ Penggunaan untuk aktivitas ilegal
❌ Pengecekan massal tanpa otorisasi
❌ Pelanggaran privasi atau hukum yang berlaku

Dengan menggunakan bot ini, Anda setuju untuk:
✅ Menggunakan hanya untuk tujuan legitimate
✅ Mematuhi hukum dan regulasi yang berlaku
✅ Mendapatkan izin eksplisit sebelum testing/audit
✅ Bertanggung jawab atas penggunaan bot ini

Ketik /help untuk melihat daftar perintah.
"""

HELP_MESSAGE = """
📚 <b>Daftar Perintah</b>

<b>🔍 Lookup & Intelligence:</b>
/ip &lt;alamat_ip&gt; - Lookup informasi IP (WHOIS, geolokasi, ASN)
/domain &lt;nama_domain&gt; - Lookup domain (WHOIS, DNS records)
/threat &lt;ip|domain&gt; - Cek reputasi dari threat intelligence sources
/breach &lt;domain&gt; - Cek data breach yang terkait dengan domain
/usercheck &lt;username&gt; - Cek keberadaan username di platform publik

<b>📦 Utility:</b>
/track &lt;nomor_resi&gt; - Tracking paket kurir/ekspedisi
/postcode &lt;kodepos|area&gt; - Lookup kode pos atau area

<b>📊 Report (Admin Only):</b>
/report &lt;report_id&gt; - Lihat report yang sudah dibuat
/myreports - Lihat daftar report Anda

<b>⚙️ Admin:</b>
/admin - Panel administrasi (admin only)
/stats - Statistik penggunaan bot

<b>ℹ️ Informasi:</b>
/start - Tampilkan pesan selamat datang
/help - Tampilkan pesan ini

<i>Note: Beberapa fitur memerlukan API key yang valid.</i>
"""


async def check_rate_limit(message: Message) -> bool:
    allowed, wait_time = rate_limiter.is_allowed(message.from_user.id)
    
    if not allowed:
        await message.reply(
            f"⏱ Rate limit tercapai. Silakan tunggu {wait_time} detik sebelum mencoba lagi."
        )
        return False
    
    return True


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply(WELCOME_MESSAGE, parse_mode="HTML")
    
    audit_logger.log_command(
        user_id=message.from_user.id,
        username=message.from_user.username,
        command="/start",
        chat_id=message.chat.id
    )


@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(HELP_MESSAGE, parse_mode="HTML")
    
    audit_logger.log_command(
        user_id=message.from_user.id,
        username=message.from_user.username,
        command="/help",
        chat_id=message.chat.id
    )


@dp.message(Command("ip"))
async def cmd_ip(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /ip &lt;alamat_ip&gt;\n"
            "Contoh: /ip 8.8.8.8",
            parse_mode="HTML"
        )
        return
    
    ip_address = args[1].strip()
    
    status_msg = await message.reply("🔍 Sedang mengumpulkan informasi IP...")
    
    try:
        result = await get_ip_info(ip_address)
        formatted = format_ip_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        report_id = report_manager.create_report(
            user_id=message.from_user.id,
            report_type="ip_lookup",
            data=result,
            formatted_output=formatted
        )
        
        await message.reply(
            f"✅ Lookup selesai. Report ID: <code>{report_id}</code>",
            parse_mode="HTML"
        )
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/ip",
            args=ip_address,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /ip command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/ip",
            args=ip_address,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("domain"))
async def cmd_domain(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /domain &lt;nama_domain&gt;\n"
            "Contoh: /domain google.com",
            parse_mode="HTML"
        )
        return
    
    domain = args[1].strip()
    
    status_msg = await message.reply("🔍 Sedang mengumpulkan informasi domain...")
    
    try:
        result = await get_domain_info(domain)
        formatted = format_domain_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        report_id = report_manager.create_report(
            user_id=message.from_user.id,
            report_type="domain_lookup",
            data=result,
            formatted_output=formatted
        )
        
        await message.reply(
            f"✅ Lookup selesai. Report ID: <code>{report_id}</code>",
            parse_mode="HTML"
        )
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/domain",
            args=domain,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /domain command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/domain",
            args=domain,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("threat"))
async def cmd_threat(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /threat &lt;ip|domain&gt;\n"
            "Contoh: /threat 8.8.8.8 atau /threat example.com",
            parse_mode="HTML"
        )
        return
    
    target = args[1].strip()
    
    status_msg = await message.reply("🛡️ Sedang mengecek threat intelligence...")
    
    try:
        result = await check_threat_intelligence(target)
        formatted = format_threat_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        report_id = report_manager.create_report(
            user_id=message.from_user.id,
            report_type="threat_intel",
            data=result,
            formatted_output=formatted
        )
        
        await message.reply(
            f"✅ Check selesai. Report ID: <code>{report_id}</code>",
            parse_mode="HTML"
        )
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/threat",
            args=target,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /threat command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/threat",
            args=target,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("breach"))
async def cmd_breach(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /breach &lt;domain&gt;\n"
            "Contoh: /breach example.com",
            parse_mode="HTML"
        )
        return
    
    domain = args[1].strip()
    
    status_msg = await message.reply("🔓 Sedang mengecek data breach...")
    
    try:
        result = await check_breach(domain)
        formatted = format_breach_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        report_id = report_manager.create_report(
            user_id=message.from_user.id,
            report_type="breach_check",
            data=result,
            formatted_output=formatted
        )
        
        await message.reply(
            f"✅ Check selesai. Report ID: <code>{report_id}</code>",
            parse_mode="HTML"
        )
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/breach",
            args=domain,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /breach command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/breach",
            args=domain,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("track"))
async def cmd_track(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /track &lt;nomor_resi&gt;\n"
            "Contoh: /track JP1234567890",
            parse_mode="HTML"
        )
        return
    
    tracking_number = args[1].strip()
    
    status_msg = await message.reply("📦 Sedang melacak paket...")
    
    try:
        result = await track_package(tracking_number)
        formatted = format_track_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/track",
            args=tracking_number,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /track command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/track",
            args=tracking_number,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("postcode"))
async def cmd_postcode(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /postcode &lt;kodepos|area&gt;\n"
            "Contoh: /postcode 12345 atau /postcode Jakarta",
            parse_mode="HTML"
        )
        return
    
    query = args[1].strip()
    
    status_msg = await message.reply("📮 Sedang mencari kode pos...")
    
    try:
        result = await lookup_postcode(query)
        formatted = format_postcode_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/postcode",
            args=query,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /postcode command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/postcode",
            args=query,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("usercheck"))
async def cmd_usercheck(message: Message):
    if not await check_rate_limit(message):
        return
    
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /usercheck &lt;username&gt;\n"
            "Contoh: /usercheck johndoe",
            parse_mode="HTML"
        )
        return
    
    username = args[1].strip()
    
    status_msg = await message.reply("👤 Sedang mengecek username di berbagai platform...")
    
    try:
        result = await check_username(username)
        formatted = format_usercheck_result(result)
        
        await status_msg.edit_text(formatted, parse_mode="HTML")
        
        report_id = report_manager.create_report(
            user_id=message.from_user.id,
            report_type="username_check",
            data=result,
            formatted_output=formatted
        )
        
        await message.reply(
            f"✅ Check selesai. Report ID: <code>{report_id}</code>",
            parse_mode="HTML"
        )
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/usercheck",
            args=username,
            chat_id=message.chat.id,
            success=True
        )
    
    except Exception as e:
        logger.error(f"Error in /usercheck command: {e}")
        await status_msg.edit_text(f"❌ Terjadi kesalahan: {str(e)}")
        
        audit_logger.log_command(
            user_id=message.from_user.id,
            username=message.from_user.username,
            command="/usercheck",
            args=username,
            chat_id=message.chat.id,
            success=False,
            error_msg=str(e)
        )


@dp.message(Command("report"))
async def cmd_report(message: Message):
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply(
            "❌ Format salah. Gunakan: /report &lt;report_id&gt;\n"
            "Contoh: /report RPT202401010001",
            parse_mode="HTML"
        )
        return
    
    report_id = args[1].strip().upper()
    
    is_admin = message.from_user.id in settings.admin_ids
    user_id = None if is_admin else message.from_user.id
    
    report = report_manager.get_report(report_id, user_id)
    
    if "error" in report:
        await message.reply(f"❌ {report['error']}")
        return
    
    formatted = format_report_summary(report)
    await message.reply(formatted, parse_mode="HTML")
    
    audit_logger.log_command(
        user_id=message.from_user.id,
        username=message.from_user.username,
        command="/report",
        args=report_id,
        chat_id=message.chat.id,
        success=True
    )


@dp.message(Command("myreports"))
async def cmd_myreports(message: Message):
    reports = report_manager.list_user_reports(message.from_user.id)
    
    if not reports:
        await message.reply("📭 Anda belum memiliki report.")
        return
    
    lines = ["📊 <b>Daftar Report Anda</b>\n"]
    
    for report in reports:
        lines.append(
            f"🆔 <code>{report['id']}</code>\n"
            f"   Type: {report['type']}\n"
            f"   Time: {report['timestamp'][:19].replace('T', ' ')}\n"
        )
    
    await message.reply("\n".join(lines), parse_mode="HTML")


@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in settings.admin_ids:
        await message.reply("⛔ Akses ditolak. Perintah ini hanya untuk administrator.")
        return
    
    lines = [
        "⚙️ <b>Admin Panel</b>\n",
        f"👑 Admin ID: <code>{message.from_user.id}</code>",
        f"👥 Total Admins: {len(settings.admin_ids)}",
        f"📊 Total Reports: {len(report_manager.reports)}",
        f"\n<b>Commands:</b>",
        "/stats - Lihat statistik bot",
        "/cleanup - Bersihkan report lama (>24 jam)"
    ]
    
    await message.reply("\n".join(lines), parse_mode="HTML")
    
    audit_logger.log_admin_action(
        admin_id=message.from_user.id,
        action="access_admin_panel"
    )


@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id not in settings.admin_ids:
        await message.reply("⛔ Akses ditolak. Perintah ini hanya untuk administrator.")
        return
    
    total_reports = len(report_manager.reports)
    
    report_types = {}
    for report in report_manager.reports.values():
        report_type = report["type"]
        report_types[report_type] = report_types.get(report_type, 0) + 1
    
    lines = [
        "📊 <b>Bot Statistics</b>\n",
        f"📝 Total Reports: {total_reports}",
        f"\n<b>Report Breakdown:</b>"
    ]
    
    for report_type, count in report_types.items():
        lines.append(f"  • {report_type}: {count}")
    
    await message.reply("\n".join(lines), parse_mode="HTML")


@dp.message(Command("cleanup"))
async def cmd_cleanup(message: Message):
    if message.from_user.id not in settings.admin_ids:
        await message.reply("⛔ Akses ditolak. Perintah ini hanya untuk administrator.")
        return
    
    deleted = report_manager.cleanup_old_reports(max_age_hours=24)
    
    await message.reply(
        f"🧹 Cleanup selesai. {deleted} report lama telah dihapus.",
        parse_mode="HTML"
    )
    
    audit_logger.log_admin_action(
        admin_id=message.from_user.id,
        action="cleanup_reports",
        details=f"Deleted {deleted} reports"
    )


async def main():
    logger.info("Starting Pegasus OSINT Bot...")
    logger.info(f"Admin IDs: {settings.admin_ids}")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
