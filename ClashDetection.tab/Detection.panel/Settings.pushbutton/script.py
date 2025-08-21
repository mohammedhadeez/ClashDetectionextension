# -*- coding: utf-8 -*-
"""
Clash Detection Settings
Configure clash detection parameters
"""

__title__ = "Settings"
__author__ = "Your Name"  
__doc__ = "Configure clash detection settings and tolerances"

from pyrevit import forms, script
from pyrevit.userconfig import user_config
import json

# Get script configuration
config = script.get_config()

def save_settings(settings):
    """Save settings to config"""
    for key, value in settings.items():
        config.set_option(key, value)
    script.save_config()

def load_settings():
    """Load current settings"""
    defaults = {
        'tolerance': 0.001,  # meters
        'check_mep': True,
        'check_structure': True,
        'check_architecture': True,
        'export_format': 'Excel',
        'highlight_color': 'Red',
        'auto_isolate': True
    }
    
    settings = {}
    for key, default in defaults.items():
        settings[key] = config.get_option(key, default)
    return settings

def main():
    """Main settings dialog"""
    current_settings = load_settings()
    
    # Create settings form
    components = [
        forms.Label("Clash Detection Settings"),
        forms.Separator(),
        forms.Label("Tolerance (mm):"),
        forms.TextBox("tolerance", 
                     default=str(current_settings['tolerance'] * 1000)),
        forms.Separator(),
        forms.Label("Categories to Check:"),
        forms.CheckBox("check_mep", "MEP Elements", 
                      default=current_settings['check_mep']),
        forms.CheckBox("check_structure", "Structural Elements",
                      default=current_settings['check_structure']),
        forms.CheckBox("check_architecture", "Architectural Elements",
                      default=current_settings['check_architecture']),
        forms.Separator(),
        forms.Label("Export Format:"),
        forms.ComboBox("export_format", 
                      ["Excel", "CSV", "JSON", "HTML"],
                      default=current_settings['export_format']),
        forms.Separator(),
        forms.Label("Visualization:"),
        forms.ComboBox("highlight_color",
                      ["Red", "Yellow", "Blue", "Green"],
                      default=current_settings['highlight_color']),
        forms.CheckBox("auto_isolate", "Auto-isolate clashing elements",
                      default=current_settings['auto_isolate']),
        forms.Separator(),
        forms.Button("Save Settings")
    ]
    
    form = forms.FlexForm("Clash Detection Settings", components)
    form.show()
    
    if form.values:
        # Process and save settings
        new_settings = {
            'tolerance': float(form.values['tolerance']) / 1000,
            'check_mep': form.values['check_mep'],
            'check_structure': form.values['check_structure'],
            'check_architecture': form.values['check_architecture'],
            'export_format': form.values['export_format'],
            'highlight_color': form.values['highlight_color'],
            'auto_isolate': form.values['auto_isolate']
        }
        save_settings(new_settings)
        forms.alert("Settings saved successfully!", title="Success")

if __name__ == '__main__':
    main()
