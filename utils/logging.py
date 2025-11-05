import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class AuditLogger:
    def __init__(self, log_file: str = "logs/audit.log"):
        self.log_file = log_file
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_command(
        self,
        user_id: int,
        username: Optional[str],
        command: str,
        args: str = "",
        chat_id: Optional[int] = None,
        success: bool = True,
        error_msg: Optional[str] = None
    ):
        status = "SUCCESS" if success else "FAILED"
        log_entry = (
            f"[{status}] User: {user_id} (@{username or 'unknown'}) | "
            f"Chat: {chat_id} | Command: {command} | Args: {args[:100]}"
        )
        
        if error_msg:
            log_entry += f" | Error: {error_msg}"
        
        self.logger.info(log_entry)
    
    def log_admin_action(
        self,
        admin_id: int,
        action: str,
        details: str = ""
    ):
        log_entry = f"[ADMIN] Admin: {admin_id} | Action: {action} | Details: {details}"
        self.logger.info(log_entry)


def setup_logging(log_level: str = "INFO", log_file: str = "logs/bot.log"):
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


audit_logger = AuditLogger()
