import customtkinter as ctk
from .styles import UIStyles

class StatsCard(ctk.CTkFrame):
    """Statistics card widget"""
    
    def __init__(self, master, title: str, value: str = "0", icon: str = "📊", **kwargs):
        super().__init__(master, **UIStyles.FRAME_STYLES['card'], **kwargs)
        
        self.title_label = ctk.CTkLabel(
            self,
            text=icon + " " + title,
            **UIStyles.LABEL_STYLES['secondary']
        )
        self.title_label.pack(padx=15, pady=(15, 5))
        
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=('Segoe UI', 32, 'bold'),
            text_color=UIStyles.COLORS['success']
        )
        self.value_label.pack(padx=15, pady=(0, 15))
    
    def update_value(self, value: str):
        self.value_label.configure(text=value)

class ProgressSection(ctk.CTkFrame):
    """Progress display section"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color='transparent', **kwargs)
        
        self.progress_bar = ctk.CTkProgressBar(self, **UIStyles.PROGRESS_STYLE)
        self.progress_bar.pack(fill='x', pady=(0, 10))
        self.progress_bar.set(0)
        
        stats_frame = ctk.CTkFrame(self, fg_color='transparent')
        stats_frame.pack(fill='x')
        
        self.progress_label = ctk.CTkLabel(
            stats_frame,
            text="Ready to scan",
            **UIStyles.LABEL_STYLES['normal']
        )
        self.progress_label.pack(side='left')
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="",
            **UIStyles.LABEL_STYLES['secondary']
        )
        self.stats_label.pack(side='right')
    
    def update_progress(self, progress: float, scanned: int, total: int):
        self.progress_bar.set(progress / 100)
        self.progress_label.configure(text=f"Scanning... {progress:.1f}%")
        self.stats_label.configure(text=f"{scanned}/{total} ports")
    
    def reset(self):
        self.progress_bar.set(0)
        self.progress_label.configure(text="Ready to scan")
        self.stats_label.configure(text="")
    
    def complete(self, message: str):
        self.progress_bar.set(1)
        self.progress_label.configure(text=message)