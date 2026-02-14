import logging
import os
from datetime import datetime
import config

class ScanLogger:
    """Logger for scan operations"""
    
    def __init__(self, name: str = "PortScanner"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            formatter = logging.Formatter(config.LOG_FORMAT)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            log_filename = f"portscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            log_path = os.path.join(config.LOGS_DIR, log_filename)
            file_handler = logging.FileHandler(log_path)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        self.scan_start_time = None
    
    def start_scan(self, target: str, port_count: int):
        self.scan_start_time = datetime.now()
        msg = f"Started scan on {target} - {port_count} ports"
        self.logger.info(msg)
    
    def log_open_port(self, port: int, service: str):
        msg = f"Open port found: {port} ({service})"
        self.logger.info(msg)
    
    def complete_scan(self, open_count: int, total_count: int):
        duration = (datetime.now() - self.scan_start_time).total_seconds()
        msg = f"Scan completed - {open_count}/{total_count} ports open in {duration:.2f}s"
        self.logger.info(msg)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str):
        self.logger.error(message)