import config

class UIStyles:
    """UI styling constants"""
    
    COLORS = config.COLORS
    COLORS.update({
        "background": "#1C1F26",
        "card": "#232733",
        "border": "#2E3442"
    })
    
    FONTS = {
        'title': ('Segoe UI', 24, 'bold'),
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'normal': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'code': ('Consolas', 9)
    }
    
    BUTTON_STYLES = {
        'primary': {
            'fg_color': COLORS['success'],
            'hover_color': '#00cc70',
            'text_color': COLORS['primary'],
            'font': FONTS['subheading'],
            'corner_radius': 8,
            'height': 40
        },
        'secondary': {
            'fg_color': '#2A2F3A',
            'hover_color': '#343A48',
            'text_color': COLORS['text'],
            'font': FONTS['normal'],
            'corner_radius': 8,
            'height': 35
        },
        'danger': {
            'fg_color': COLORS['danger'],
            'hover_color': '#cc0000',
            'text_color': 'white',
            'font': FONTS['subheading'],
            'corner_radius': 8,
            'height': 40
        },
        'export': {
            'fg_color': COLORS['info'],
            'hover_color': '#00b8e6',
            'text_color': COLORS['primary'],
            'font': FONTS['normal'],
            'corner_radius': 6,
            'height': 32
        }
    }
    
    ENTRY_STYLE = {
        'fg_color': COLORS['card'],
        'text_color': COLORS['text'],
        'font': FONTS['normal'],
        'corner_radius': 6,
        'height': 35
    }
    
    FRAME_STYLES = {
        'main': {
            'fg_color': COLORS['background'],
            'corner_radius': 0
        },
        'card': {
            'fg_color': COLORS['card'],
            'corner_radius': 12
        },
        'section': {
            'fg_color': COLORS['secondary'],
            'corner_radius': 8
        }
    }
    
    LABEL_STYLES = {
        'title': {
            'text_color': COLORS['success'],
            'font': FONTS['title']
        },
        'heading': {
            'text_color': COLORS['text'],
            'font': FONTS['heading']
        },
        'normal': {
            'text_color': COLORS['text'],
            'font': FONTS['normal']
        },
        'secondary': {
            'text_color': COLORS['text_secondary'],
            'font': FONTS['small']
        }
    }
    
    PROGRESS_STYLE = {
        'fg_color': COLORS['card'],
        'progress_color': COLORS['success'],
        'height': 25,
        'corner_radius': 12
    }
    
    TEXTBOX_STYLE = {
        'fg_color': COLORS['card'],
        'text_color': COLORS['text'],
        'font': FONTS['code'],
        'corner_radius': 8
    }
    
    @staticmethod
    def get_risk_color(risk_level: str) -> str:
        risk_colors = {
            'high': '#ff4444',
            'medium': '#ffd700',
            'low': '#00ff88',
            'unknown': '#888888'
        }
        return risk_colors.get(risk_level.lower(), risk_colors['unknown'])