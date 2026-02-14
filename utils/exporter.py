import json
import csv
import os
from datetime import datetime
from typing import Dict
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import config

class ResultExporter:
    """Export scan results"""
    
    def __init__(self):
        self.exports_dir = config.EXPORTS_DIR
    
    def export_to_json(self, results: Dict, filename: str = None) -> str:
        if not filename:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filepath
    
    def export_to_csv(self, results: Dict, filename: str = None) -> str:
        if not filename:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Port', 'Protocol', 'State', 'Service', 'Description', 'Risk'])
            
            for port_info in results.get('open_ports', []):
                writer.writerow([
                    port_info.get('port', ''),
                    port_info.get('protocol', ''),
                    port_info.get('state', ''),
                    port_info.get('service', ''),
                    port_info.get('description', ''),
                    port_info.get('risk', '')
                ])
        
        return filepath
    
    def export_to_txt(self, results: Dict, filename: str = None) -> str:
        if not filename:
            filename = f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("PORT SCAN RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Target: {results.get('target', 'N/A')}\n")
            f.write(f"Scan Type: {results.get('scan_type', 'N/A')}\n")
            f.write(f"Duration: {results.get('duration', 0)} seconds\n")
            f.write(f"Open Ports: {len(results.get('open_ports', []))}\n\n")
            
            open_ports = results.get('open_ports', [])
            if open_ports:
                f.write("-" * 80 + "\n")
                f.write(f"OPEN PORTS ({len(open_ports)} found)\n")
                f.write("-" * 80 + "\n\n")
                
                for port in sorted(open_ports, key=lambda x: x.get('port', 0)):
                    f.write(f"Port: {port.get('port')}\n")
                    f.write(f"  Service: {port.get('service')}\n")
                    f.write(f"  Risk: {port.get('risk', 'unknown').upper()}\n\n")
        
        return filepath
    
    def export_to_pdf(self, results: Dict, filename: str = None) -> str:
        if not filename:
            filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        filepath = os.path.join(self.exports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        story.append(Paragraph("Port Scan Security Report", styles['Title']))
        story.append(Spacer(1, 0.3*inch))
        
        scan_info_data = [
            ['Target:', results.get('target', 'N/A')],
            ['Duration:', f"{results.get('duration', 0)} seconds"],
            ['Open Ports:', str(len(results.get('open_ports', [])))]
        ]
        
        info_table = Table(scan_info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))
        
        open_ports = results.get('open_ports', [])
        if open_ports:
            port_data = [['Port', 'Service', 'Risk']]
            for port in sorted(open_ports, key=lambda x: x.get('port', 0)):
                port_data.append([
                    str(port.get('port', '')),
                    port.get('service', '')[:20],
                    port.get('risk', '').upper()
                ])
            
            port_table = Table(port_data)
            port_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(port_table)
        
        doc.build(story)
        return filepath