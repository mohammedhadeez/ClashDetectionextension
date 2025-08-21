# -*- coding: utf-8 -*-
"""
View Clash History
View and manage clash detection history
"""

__title__ = "View\nHistory"
__author__ = "Your Name"
__doc__ = "View clash detection history and track resolution status"

from pyrevit import revit, forms, script, DB
from datetime import datetime
import json
import os

doc = revit.doc
config = script.get_config()

def load_history():
    """Load clash history from config"""
    history = config.get_option('clash_history', [])
    return history

def save_history(history):
    """Save clash history to config"""
    config.set_option('clash_history', history)
    script.save_config()

def main():
    """Display clash history"""
    history = load_history()
    
    if not history:
        forms.alert("No clash detection history found.", title="History")
        return
    
    # Format history for display
    history_items = []
    for record in history:
        date = record.get('date', 'Unknown')
        count = record.get('clash_count', 0)
        resolved = record.get('resolved', 0)
        pending = count - resolved
        
        item = "{} - Total: {} | Resolved: {} | Pending: {}".format(
            date, count, resolved, pending
        )
        history_items.append(item)
    
    # Show history list
    selected = forms.SelectFromList.show(
        history_items,
        title='Clash Detection History',
        button_name='View Details',
        multiselect=False
    )
    
    if selected:
        # Show detailed view
        index = history_items.index(selected)
        record = history[index]
        
        details = """
        Date: {}
        Total Clashes: {}
        Resolved: {}
        Pending: {}
        Categories Checked: {}
        Detection Method: {}
        """.format(
            record.get('date', 'Unknown'),
            record.get('clash_count', 0),
            record.get('resolved', 0),
            record.get('clash_count', 0) - record.get('resolved', 0),
            ', '.join(record.get('categories', [])),
            record.get('method', 'Standard')
        )
        
        forms.alert(details, title="Clash Detection Details")

if __name__ == '__main__':
    main()
