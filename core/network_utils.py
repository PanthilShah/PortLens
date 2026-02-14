import socket
import ipaddress
import re
from typing import List, Tuple, Optional

class NetworkUtils:
    """Network utility functions"""
    
    @staticmethod
    def validate_ip(ip_address: str) -> bool:
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))
    
    @staticmethod
    def resolve_hostname(hostname: str) -> Optional[str]:
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None
    
    @staticmethod
    def get_local_ip() -> str:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def parse_port_range(port_input: str) -> List[int]:
        ports = []
        try:
            parts = port_input.replace(' ', '').split(',')
            for part in parts:
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
                        ports.extend(range(start, end + 1))
                else:
                    port = int(part)
                    if 1 <= port <= 65535:
                        ports.append(port)
        except ValueError:
            pass
        return sorted(list(set(ports)))