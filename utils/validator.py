import re
import ipaddress
from typing import Tuple, Optional

class InputValidator:
    """Input validation"""
    
    @staticmethod
    def validate_target(target: str) -> Tuple[bool, Optional[str]]:
        if not target or not target.strip():
            return False, "Target cannot be empty"
        
        target = target.strip()
        
        if InputValidator._is_valid_ip(target):
            return True, None
        
        if '/' in target:
            try:
                ipaddress.ip_network(target, strict=False)
                return True, None
            except ValueError:
                return False, "Invalid CIDR notation"
        
        if InputValidator._is_valid_hostname(target):
            return True, None
        
        return False, "Invalid target format"
    
    @staticmethod
    def validate_ports(port_input: str) -> Tuple[bool, Optional[str]]:
        if not port_input or not port_input.strip():
            return False, "Port input cannot be empty"
        
        port_input = port_input.strip().replace(' ', '')
        parts = port_input.split(',')
        
        for part in parts:
            if '-' in part:
                try:
                    start, end = part.split('-')
                    start_port = int(start)
                    end_port = int(end)
                    
                    if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
                        return False, f"Port range must be between 1-65535"
                    
                    if start_port > end_port:
                        return False, f"Invalid range: {start_port}-{end_port}"
                except ValueError:
                    return False, f"Invalid port range: {part}"
            else:
                try:
                    port = int(part)
                    if not (1 <= port <= 65535):
                        return False, f"Port must be between 1-65535"
                except ValueError:
                    return False, f"Invalid port number: {part}"
        
        return True, None
    
    @staticmethod
    def validate_threads(threads: int) -> Tuple[bool, Optional[str]]:
        if not isinstance(threads, int):
            return False, "Thread count must be an integer"
        if threads < 1:
            return False, "Thread count must be at least 1"
        if threads > 500:
            return False, "Thread count too high (max 500)"
        return True, None
    
    @staticmethod
    def _is_valid_ip(ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def _is_valid_hostname(hostname: str) -> bool:
        if len(hostname) > 255:
            return False
        if hostname[-1] == ".":
            hostname = hostname[:-1]
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        return all(allowed.match(x) for x in hostname.split("."))