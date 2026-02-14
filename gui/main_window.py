import customtkinter as ctk
import threading
from tkinter import messagebox
import config
from .styles import UIStyles
from .widgets import StatsCard, ProgressSection
from core import PortScanner, ServiceDetector, NetworkUtils
from utils import ResultExporter, InputValidator, ScanLogger

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PortScannerGUI:
    """Main GUI application"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.configure(fg_color=UIStyles.COLORS['background'])
        
        self.scanner = PortScanner()
        self.service_detector = ServiceDetector()
        self.network_utils = NetworkUtils()
        self.exporter = ResultExporter()
        self.validator = InputValidator()
        self.logger = ScanLogger()
        
        self.is_scanning = False
        self.scan_results = None
        self.scan_thread = None
        
        self.scanner.set_progress_callback(self.update_progress)
        self.scanner.set_port_found_callback(self.on_port_found)
        
        self.build_ui()
        self.center_window()
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def build_ui(self):
        main_container = ctk.CTkFrame(self.root, fg_color='transparent')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.build_header(main_container)
        
        content_frame = ctk.CTkFrame(main_container, fg_color='transparent')
        content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        left_column = ctk.CTkFrame(content_frame, fg_color='transparent')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.build_config_section(left_column)
        self.build_preset_section(left_column)
        
        right_column = ctk.CTkFrame(content_frame, fg_color='transparent')
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.build_results_section(right_column)
    
    def build_header(self, parent):
        header_frame = ctk.CTkFrame(parent, **UIStyles.FRAME_STYLES['card'], height=100)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"🔍 {config.APP_NAME}",
            **UIStyles.LABEL_STYLES['title']
        )
        title_label.pack(side='left', padx=30, pady=20)
        
        info_label = ctk.CTkLabel(
            header_frame,
            text=f"v{config.APP_VERSION} | By {config.APP_AUTHOR}",
            **UIStyles.LABEL_STYLES['secondary']
        )
        info_label.pack(side='left', padx=(0, 20))
        
        local_ip = self.network_utils.get_local_ip()
        ip_label = ctk.CTkLabel(
            header_frame,
            text=f"📍 Your IP: {local_ip}",
            **UIStyles.LABEL_STYLES['normal']
        )
        ip_label.pack(side='right', padx=30)
    
    def build_config_section(self, parent):
        config_frame = ctk.CTkFrame(parent, **UIStyles.FRAME_STYLES['card'])
        config_frame.pack(fill='both', padx=0, pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            config_frame,
            text="⚙️ Scan Configuration",
            **UIStyles.LABEL_STYLES['heading']
        )
        title_label.pack(padx=20, pady=(20, 15))
        
        # Target input
        target_frame = ctk.CTkFrame(config_frame, fg_color='transparent')
        target_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        target_label = ctk.CTkLabel(
            target_frame,
            text="Target (IP/Hostname):",
            **UIStyles.LABEL_STYLES['normal'],
            anchor='w'
        )
        target_label.pack(fill='x', pady=(0, 5))
        
        self.target_entry = ctk.CTkEntry(
            target_frame,
            placeholder_text="e.g., 192.168.1.1 or scanme.nmap.org",
            **UIStyles.ENTRY_STYLE
        )
        self.target_entry.pack(fill='x')
        
        # Ports input
        ports_frame = ctk.CTkFrame(config_frame, fg_color='transparent')
        ports_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        ports_label = ctk.CTkLabel(
            ports_frame,
            text="Ports (e.g., 80,443,8000-9000):",
            **UIStyles.LABEL_STYLES['normal'],
            anchor='w'
        )
        ports_label.pack(fill='x', pady=(0, 5))
        
        self.ports_entry = ctk.CTkEntry(
            ports_frame,
            placeholder_text="80,443,8080",
            **UIStyles.ENTRY_STYLE
        )
        self.ports_entry.pack(fill='x')
        
        # Options row
        options_frame = ctk.CTkFrame(config_frame, fg_color='transparent')
        options_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        type_col = ctk.CTkFrame(options_frame, fg_color='transparent')
        type_col.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        type_label = ctk.CTkLabel(
            type_col,
            text="Scan Type:",
            **UIStyles.LABEL_STYLES['normal'],
            anchor='w'
        )
        type_label.pack(fill='x', pady=(0, 5))
        
        self.scan_type_var = ctk.StringVar(value="TCP")
        self.scan_type_menu = ctk.CTkOptionMenu(
            type_col,
            values=config.SCAN_TYPES,
            variable=self.scan_type_var,
            **UIStyles.ENTRY_STYLE
        )
        self.scan_type_menu.pack(fill='x')
        
        threads_col = ctk.CTkFrame(options_frame, fg_color='transparent')
        threads_col.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        threads_label = ctk.CTkLabel(
            threads_col,
            text="Threads:",
            **UIStyles.LABEL_STYLES['normal'],
            anchor='w'
        )
        threads_label.pack(fill='x', pady=(0, 5))
        
        self.threads_entry = ctk.CTkEntry(
            threads_col,
            placeholder_text=str(config.DEFAULT_THREADS),
            **UIStyles.ENTRY_STYLE
        )
        self.threads_entry.insert(0, str(config.DEFAULT_THREADS))
        self.threads_entry.pack(fill='x')
        
        # Progress section
        self.progress_section = ProgressSection(config_frame)
        self.progress_section.pack(fill='x', padx=20, pady=(0, 15))
        
        # Action buttons
        button_frame = ctk.CTkFrame(config_frame, fg_color='transparent')
        button_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        self.scan_button = ctk.CTkButton(
            button_frame,
            text="🚀 Start Scan",
            command=self.start_scan,
            **UIStyles.BUTTON_STYLES['primary'],
            width=200
        )
        self.scan_button.pack(side='left', padx=(0, 10))
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Stop Scan",
            command=self.stop_scan,
            **UIStyles.BUTTON_STYLES['danger'],
            width=150,
            state='disabled'
        )
        self.stop_button.pack(side='left')
    
    def build_preset_section(self, parent):
        preset_frame = ctk.CTkFrame(parent, **UIStyles.FRAME_STYLES['card'])
        preset_frame.pack(fill='x', padx=0)
        
        title_label = ctk.CTkLabel(
            preset_frame,
            text="⚡ Quick Scan Presets",
            **UIStyles.LABEL_STYLES['heading']
        )
        title_label.pack(padx=20, pady=(20, 15))
        
        presets = [
            ("Quick Scan", "21,22,23,80,443,3306,3389,8080"),
            ("Web Servers", "80,443,8000,8080,8443"),
            ("Databases", "3306,5432,6379,27017"),
            ("Common Ports", "21,22,23,25,80,110,143,443,445,3389")
        ]
        
        for title, ports in presets:
            btn = ctk.CTkButton(
                preset_frame,
                text=title,
                command=lambda p=ports: self.apply_preset(p),
                **UIStyles.BUTTON_STYLES['secondary']
            )
            btn.pack(fill='x', padx=20, pady=(0, 10))
        
        ctk.CTkLabel(preset_frame, text="").pack(pady=10)
    
    def build_results_section(self, parent):
        results_frame = ctk.CTkFrame(parent, **UIStyles.FRAME_STYLES['card'])
        results_frame.pack(fill='both', expand=True)
        
        header_frame = ctk.CTkFrame(results_frame, fg_color='transparent')
        header_frame.pack(fill='x', padx=20, pady=(20, 15))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Scan Results",
            **UIStyles.LABEL_STYLES['heading']
        )
        title_label.pack(side='left')
        
        export_frame = ctk.CTkFrame(header_frame, fg_color='transparent')
        export_frame.pack(side='right')
        
        for fmt in ['JSON', 'CSV', 'TXT', 'PDF']:
            btn = ctk.CTkButton(
                export_frame,
                text=fmt,
                command=lambda f=fmt: self.export_results(f.lower()),
                **UIStyles.BUTTON_STYLES['export'],
                width=60
            )
            btn.pack(side='left', padx=2)
        
        stats_frame = ctk.CTkFrame(results_frame, fg_color='transparent')
        stats_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        self.total_ports_card = StatsCard(stats_frame, "Total", "0", "📡")
        self.total_ports_card.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        self.open_ports_card = StatsCard(stats_frame, "Open", "0", "✅")
        self.open_ports_card.pack(side='left', fill='x', expand=True, padx=5)
        
        self.scan_time_card = StatsCard(stats_frame, "Time", "0s", "⏱️")
        self.scan_time_card.pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        self.results_text = ctk.CTkTextbox(
            results_frame,
            **UIStyles.TEXTBOX_STYLE
        )
        self.results_text.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        # Risk status label (NEW FEATURE)
        self.risk_label = ctk.CTkLabel(
            results_frame,
            text="Risk Level: Not Scanned",
            font=("Arial", 14, "bold"),
            text_color="#00FFAA"
        )
        self.risk_label.pack(pady=(0, 20))

    def calculate_risk(self, open_ports):
        high_risk_ports = {22, 3306, 5432, 27017, 6379}
        medium_risk_ports = {80, 443, 8080}

        if not open_ports:
            return "LOW RISK 🟢"

        for port in open_ports:
            if port in high_risk_ports:
                return "HIGH RISK 🔴"

        return "MEDIUM RISK 🟡"
    
    def apply_preset(self, ports: str):
        self.ports_entry.delete(0, 'end')
        self.ports_entry.insert(0, ports)
    
    def validate_inputs(self) -> bool:
        target = self.target_entry.get().strip()
        is_valid, error = self.validator.validate_target(target)
        if not is_valid:
            messagebox.showerror("Invalid Target", error)
            return False
        
        ports = self.ports_entry.get().strip()
        is_valid, error = self.validator.validate_ports(ports)
        if not is_valid:
            messagebox.showerror("Invalid Ports", error)
            return False
        
        try:
            threads = int(self.threads_entry.get())
            is_valid, error = self.validator.validate_threads(threads)
            if not is_valid:
                messagebox.showerror("Invalid Threads", error)
                return False
        except ValueError:
            messagebox.showerror("Invalid Threads", "Must be a number")
            return False
        
        return True
    
    def start_scan(self):
        if self.is_scanning:
            messagebox.showwarning("Scan in Progress", "Already scanning")
            return
        
        if not self.validate_inputs():
            return
        
        self.clear_results()
        
        self.is_scanning = True
        self.scan_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        
        target = self.target_entry.get().strip()
        port_range = self.ports_entry.get().strip()
        scan_type = self.scan_type_var.get()
        threads = int(self.threads_entry.get())
        
        self.scanner.max_threads = threads
        
        self.scan_thread = threading.Thread(
            target=self.run_scan,
            args=(target, port_range, scan_type),
            daemon=True
        )
        self.scan_thread.start()
    
    def run_scan(self, target: str, port_range: str, scan_type: str):
        try:
            ports_list = self.network_utils.parse_port_range(port_range)
            self.logger.start_scan(target, len(ports_list))
            
            results = self.scanner.custom_scan(target, port_range, scan_type)
            
            self.scan_results = results
            self.root.after(0, self.display_results, results)
            
            if results.get('success'):
                open_count = len(results.get('open_ports', []))
                total_count = results.get('total_ports', 0)
                self.logger.complete_scan(open_count, total_count)
            
        except Exception as e:
            self.logger.error(str(e))
            self.root.after(0, lambda: messagebox.showerror("Scan Error", str(e)))
        finally:
            self.root.after(0, self.scan_complete)
    
    def stop_scan(self):
        if self.is_scanning:
            self.scanner.stop()
            messagebox.showinfo("Scan Stopped", "Scan has been stopped")
    
    def scan_complete(self):
        self.is_scanning = False
        self.scan_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        
        if self.scan_results and self.scan_results.get('success'):
            self.progress_section.complete("Scan completed!")
        else:
            self.progress_section.complete("Scan stopped")
    
    def update_progress(self, progress: float, scanned: int, total: int):
        self.root.after(0, self.progress_section.update_progress, progress, scanned, total)
    
    def on_port_found(self, port_data: dict):
        port = port_data.get('port')
        service = port_data.get('service')
        self.logger.log_open_port(port, service)
    
    def clear_results(self):
        self.total_ports_card.update_value("0")
        self.open_ports_card.update_value("0")
        self.scan_time_card.update_value("0s")
        self.results_text.delete('1.0', 'end')
        self.progress_section.reset()
        self.risk_label.configure(text="Risk Level: Not Scanned", text_color="#00FFAA")
    
    def display_results(self, results: dict):
        if not results.get('success'):
            messagebox.showerror("Scan Failed", results.get('error', 'Unknown error'))
            return
        
        self.total_ports_card.update_value(str(results.get('total_ports', 0)))
        open_count = len(results.get('open_ports', []))
        self.open_ports_card.update_value(str(open_count))
        
        # Calculate Risk
        open_ports_data = results.get('open_ports', [])
        open_ports_list = [p.get('port') for p in open_ports_data]
        risk = self.calculate_risk(open_ports_list)
        
        color = UIStyles.get_risk_color(risk.split()[0])
        self.risk_label.configure(text=f"Risk Level: {risk}", text_color=color)
        self.scan_time_card.update_value(f"{results.get('duration', 0)}s")
        
        self.display_detailed_results(results)
    
    def display_detailed_results(self, results: dict):
        self.results_text.delete('1.0', 'end')
        
        output = []
        output.append("=" * 80)
        output.append("SCAN RESULTS")
        output.append("=" * 80)
        output.append(f"Target: {results.get('target', 'N/A')}")
        output.append(f"Duration: {results.get('duration', 0)} seconds")
        output.append(f"Total Ports: {results.get('total_ports', 0)}")
        output.append(f"Open Ports: {len(results.get('open_ports', []))}")
        output.append(f"Overall Risk Level: {self.risk_label.cget('text')}")
        output.append("")
        
        open_ports = results.get('open_ports', [])
        if open_ports:
            output.append("-" * 80)
            output.append(f"OPEN PORTS ({len(open_ports)} found)")
            output.append("-" * 80)
            output.append("")
            
            for port in sorted(open_ports, key=lambda x: x.get('port', 0)):
                output.append(f"Port: {port.get('port')}")
                output.append(f"  Service: {port.get('service')}")
                output.append(f"  Risk: {port.get('risk', 'unknown').upper()}")
                output.append(f"  Description: {port.get('description', 'N/A')}")
                
                vulns = self.service_detector.get_vulnerabilities(port.get('port'))
                if vulns:
                    output.append(f"  ⚠️  Vulnerabilities: {len(vulns.get('vulnerabilities', []))}")
                
                output.append("")
        
        output.append("=" * 80)
        
        self.results_text.insert('1.0', '\n'.join(output))
    
    def export_results(self, format: str):
        if not self.scan_results or not self.scan_results.get('success'):
            messagebox.showwarning("No Results", "No scan results to export")
            return
        
        try:
            if format == 'json':
                filepath = self.exporter.export_to_json(self.scan_results)
            elif format == 'csv':
                filepath = self.exporter.export_to_csv(self.scan_results)
            elif format == 'pdf':
                filepath = self.exporter.export_to_pdf(self.scan_results)
            elif format == 'txt':
                filepath = self.exporter.export_to_txt(self.scan_results)
            else:
                messagebox.showerror("Invalid Format", f"Unsupported: {format}")
                return
            
            messagebox.showinfo("Export Successful", f"Saved to:\n{filepath}")
            self.logger.info(f"Exported to {format.upper()}: {filepath}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
    
    def run(self):
        self.root.mainloop()