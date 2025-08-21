# -*- coding: utf-8 -*-
"""
Export Clash Report
Export clash detection results to various formats
"""

__title__ = "Export\nReport"
__author__ = "Your Name"
__doc__ = "Export clash detection results to Excel, CSV or HTML"

from pyrevit import revit, forms, script
from Autodesk.Revit import DB
import os
import csv
import json
from datetime import datetime

doc = revit.doc

def export_to_csv(clashes, filepath):
    """Export clashes to CSV format"""
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['Index', 'Element1_Id', 'Element1_Name', 'Element1_Category',
                     'Element2_Id', 'Element2_Name', 'Element2_Category',
                     'Clash_Volume', 'Level', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, clash in enumerate(clashes, 1):
            writer.writerow({
                'Index': i,
                'Element1_Id': clash['elem1'].Id.IntegerValue,
                'Element1_Name': clash['elem1'].Name,
                'Element1_Category': clash['elem1'].Category.Name,
                'Element2_Id': clash['elem2'].Id.IntegerValue,
                'Element2_Name': clash['elem2'].Name,
                'Element2_Category': clash['elem2'].Category.Name,
                'Clash_Volume': clash.get('volume', 'N/A'),
                'Level': clash.get('level', 'N/A'),
                'Status': clash.get('status', 'New')
            })

def export_to_html(clashes, filepath):
    """Export clashes to HTML format"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clash Detection Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .summary { background-color: #e7f3fe; padding: 15px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>Clash Detection Report</h1>
        <div class="summary">
            <h2>Summary</h2>
            <p>Project: {}</p>
            <p>Date: {}</p>
            <p>Total Clashes: {}</p>
        </div>
        <table>
            <tr>
                <th>#</th>
                <th>Element 1</th>
                <th>Category 1</th>
                <th>Element 2</th>
                <th>Category 2</th>
                <th>Status</th>
            </tr>
    """.format(doc.Title, datetime.now().strftime("%Y-%m-%d %H:%M"), len(clashes))
    
    for i, clash in enumerate(clashes, 1):
        html_content += """
            <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
            </tr>
        """.format(i, 
                  clash['elem1'].Name,
                  clash['elem1'].Category.Name,
                  clash['elem2'].Name,
                  clash['elem2'].Category.Name,
                  clash.get('status', 'New'))
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(filepath, 'w') as f:
        f.write(html_content)

def main():
    """Main export function"""
    # Get stored clash data (in real implementation, this would come from detection)
    # For demo, create sample data
    sample_clashes = []
    
    # Ask user for export format
    formats = ['CSV', 'HTML', 'JSON']
    selected_format = forms.SelectFromList.show(
        formats,
        title='Select Export Format',
        button_name='Export'
    )
    
    if not selected_format:
        return
    
    # Get save location
    save_dialog = forms.save_file(file_ext=selected_format.lower())
    if not save_dialog:
        return
    
    # Export based on format
    if selected_format == 'CSV':
        export_to_csv(sample_clashes, save_dialog)
    elif selected_format == 'HTML':
        export_to_html(sample_clashes, save_dialog)
    elif selected_format == 'JSON':
        with open(save_dialog, 'w') as f:
            json.dump(sample_clashes, f, indent=4, default=str)
    
    forms.alert("Report exported successfully!", title="Export Complete")

if __name__ == '__main__':
    main()
