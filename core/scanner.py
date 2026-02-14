import socket
import threading
import time
from queue import Queue
from typing import List, Dict, Callable
from datetime import datetime
import config
from .service_detector import ServiceDetector
from .network_utils import NetworkUtils

class PortScanner:
    """Multi-threaded port scanner"""
    
    def __init__(self, timeout: float = config.DEFAULT_TIMEOUT, max_threads: int = config.DEFAULT_THREADS):
        self.timeout = timeout
        self.max_threads = max_threads
        self.service_detector = ServiceDetector()
        self.network_utils = NetworkUtils()
        
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        
        self.total_ports = 0
        self.scanned_ports = 0
        self.start_time = None
        self.end_time = None
        
        self.port_queue = Queue()
        self.lock = threading.Lock()
        self.stop_scan = False
        
        self.progress_callback = None
        self.port_found_callback = None
    
    def set_progress_callback(self, callback: Callable):
        self.progress_callback = callback
    
    def set_port_found_callback(self, callback: Callable):
        self.port_found_callback = callback
    
    def reset(self):
        self.open_ports = []
        self.closed_ports = []
        self.filtered_ports = []
        self.total_ports = 0
        self.scanned_ports = 0
        self.start_time = None
        self.end_time = None
        self.stop_scan = False
        
        while not self.port_queue.empty():
            try:
                self.port_queue.get_nowait()
            except:
                break
    
    def scan_tcp_port(self, host: str, port: int) -> Dict:
        result = {
            'port': port,
            'protocol': 'TCP',
            'state': 'closed',
            'service': 'unknown',
            'description': '',
            'risk': 'low',
            'response_time': None,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            start = time.time()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            connection_result = sock.connect_ex((host, port))
            response_time = (time.time() - start) * 1000
            
            if connection_result == 0:
                result['state'] = 'open'
                result['response_time'] = round(response_time, 2)
                
                service_info = self.service_detector.detect_service(port)
                result.update(service_info)
            
            sock.close()
            
        except socket.timeout:
            result['state'] = 'filtered'
        except socket.error:
            result['state'] = 'closed'
        except Exception:
            result['state'] = 'error'
        
        return result
    
    def worker_thread(self, host: str, scan_type: str):
        while not self.stop_scan:
            try:
                port = self.port_queue.get(timeout=1)
                
                result = self.scan_tcp_port(host, port)
                
                with self.lock:
                    if result['state'] == 'open':
                        self.open_ports.append(result)
                        if self.port_found_callback:
                            self.port_found_callback(result)
                    elif result['state'] == 'closed':
                        self.closed_ports.append(result)
                    else:
                        self.filtered_ports.append(result)
                    
                    self.scanned_ports += 1
                    
                    if self.progress_callback:
                        progress = (self.scanned_ports / self.total_ports) * 100
                        self.progress_callback(progress, self.scanned_ports, self.total_ports)
                
                self.port_queue.task_done()
                
            except:
                break
    
    def scan(self, host: str, ports: List[int], scan_type: str = 'TCP') -> Dict:
        self.reset()
        self.start_time = datetime.now()
        
        target_ip = host
        if not self.network_utils.validate_ip(host):
            target_ip = self.network_utils.resolve_hostname(host)
            if not target_ip:
                return {
                    'success': False,
                    'error': f"Could not resolve hostname: {host}"
                }
        
        self.total_ports = len(ports)
        
        for port in ports:
            self.port_queue.put(port)
        
        threads = []
        num_threads = min(self.max_threads, len(ports))
        
        for _ in range(num_threads):
            t = threading.Thread(target=self.worker_thread, args=(target_ip, scan_type))
            t.daemon = True
            t.start()
            threads.append(t)
        
        self.port_queue.join()
        
        self.stop_scan = True
        for t in threads:
            t.join(timeout=2)
        
        self.end_time = datetime.now()
        scan_duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'success': True,
            'target': host,
            'target_ip': target_ip,
            'scan_type': scan_type,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'duration': round(scan_duration, 2),
            'total_ports': self.total_ports,
            'open_ports': sorted(self.open_ports, key=lambda x: x['port']),
            'closed_ports_count': len(self.closed_ports),
            'filtered_ports_count': len(self.filtered_ports),
            'scan_rate': round(self.total_ports / scan_duration, 2) if scan_duration > 0 else 0
        }
    
    def custom_scan(self, host: str, port_range: str, scan_type: str = 'TCP') -> Dict:
        ports = self.network_utils.parse_port_range(port_range)
        if not ports:
            return {
                'success': False,
                'error': 'Invalid port range specified'
            }
        return self.scan(host, ports, scan_type)
    
    def stop(self):
        self.stop_scan = True