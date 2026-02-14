import json
import os
from typing import Dict, Optional
import config

class ServiceDetector:
    """Service detection and vulnerability assessment"""
    
    def __init__(self):
        self.common_ports = self._load_common_ports()
        self.vulnerabilities = self._load_vulnerabilities()
    
    def _load_common_ports(self) -> Dict:
        try:
            ports_file = os.path.join(config.DATA_DIR, 'common_ports.json')
            with open(ports_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _load_vulnerabilities(self) -> Dict:
        try:
            vuln_file = os.path.join(config.DATA_DIR, 'vulnerabilities.json')
            with open(vuln_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def detect_service(self, port: int) -> Dict:
        port_str = str(port)
        service_info = {
            'port': port,
            'service': 'unknown',
            'description': 'Unknown Service',
            'risk': 'low'
        }
        
        if port_str in self.common_ports:
            port_data = self.common_ports[port_str]
            service_info.update({
                'service': port_data.get('service', 'unknown'),
                'description': port_data.get('description', 'Unknown Service'),
                'risk': port_data.get('risk', 'low')
            })
        
        return service_info
    
    def get_vulnerabilities(self, port: int) -> Optional[Dict]:
        port_str = str(port)
        if port_str in self.vulnerabilities:
            return self.vulnerabilities[port_str]
        return None