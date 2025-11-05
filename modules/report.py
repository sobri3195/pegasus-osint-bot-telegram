from typing import Dict
from datetime import datetime
import json


class ReportManager:
    def __init__(self):
        self.reports = {}
        self.counter = 0
    
    def create_report(
        self,
        user_id: int,
        report_type: str,
        data: Dict,
        formatted_output: str
    ) -> str:
        self.counter += 1
        report_id = f"RPT{datetime.now().strftime('%Y%m%d')}{self.counter:04d}"
        
        report = {
            "id": report_id,
            "user_id": user_id,
            "type": report_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "formatted_output": formatted_output
        }
        
        self.reports[report_id] = report
        return report_id
    
    def get_report(self, report_id: str, user_id: int = None) -> Dict:
        report = self.reports.get(report_id)
        
        if not report:
            return {"error": "Report tidak ditemukan"}
        
        if user_id and report["user_id"] != user_id:
            return {"error": "Anda tidak memiliki akses ke report ini"}
        
        return report
    
    def list_user_reports(self, user_id: int, limit: int = 10) -> list:
        user_reports = [
            r for r in self.reports.values() 
            if r["user_id"] == user_id
        ]
        
        user_reports.sort(key=lambda x: x["timestamp"], reverse=True)
        return user_reports[:limit]
    
    def delete_report(self, report_id: str, user_id: int = None) -> bool:
        report = self.reports.get(report_id)
        
        if not report:
            return False
        
        if user_id and report["user_id"] != user_id:
            return False
        
        del self.reports[report_id]
        return True
    
    def cleanup_old_reports(self, max_age_hours: int = 24):
        now = datetime.now()
        to_delete = []
        
        for report_id, report in self.reports.items():
            report_time = datetime.fromisoformat(report["timestamp"])
            age = (now - report_time).total_seconds() / 3600
            
            if age > max_age_hours:
                to_delete.append(report_id)
        
        for report_id in to_delete:
            del self.reports[report_id]
        
        return len(to_delete)


def format_report_summary(report: Dict) -> str:
    if "error" in report:
        return f"❌ <b>Error:</b> {report['error']}"
    
    lines = [
        "📊 <b>Report Summary</b>\n",
        f"🆔 <b>Report ID:</b> <code>{report['id']}</code>",
        f"📋 <b>Type:</b> {report['type'].upper()}",
        f"⏰ <b>Generated:</b> {report['timestamp'][:19].replace('T', ' ')}",
        f"\n{'='*40}\n",
        report['formatted_output']
    ]
    
    return "\n".join(lines)


report_manager = ReportManager()
