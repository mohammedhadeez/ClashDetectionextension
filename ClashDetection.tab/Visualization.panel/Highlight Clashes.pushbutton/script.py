# -*- coding: utf-8 -*-
"""
Highlight Clashes
Visually highlight clashing elements in the model
"""

__title__ = "Highlight\nClashes"
__author__ = "Your Name"
__doc__ = "Highlight and isolate clashing elements in the active view"

from Autodesk.Revit import DB
from Autodesk.Revit.UI import TaskDialog
from pyrevit import revit, forms
import clr

clr.AddReference('System')
from System.Collections.Generic import List

doc = revit.doc
uidoc = revit.uidoc
app = revit.app

def create_override_settings(color):
    """Create graphic override settings with specified color"""
    override = DB.OverrideGraphicSettings()
    
    # Set projection lines color
    override.SetProjectionLineColor(color)
    override.SetProjectionLineWeight(5)
    
    # Set surface patterns
    override.SetSurfaceForegroundPatternVisible(True)
    override.SetSurfaceForegroundPatternColor(color)
    
    # Set cut patterns
    override.SetCutForegroundPatternVisible(True)
    override.SetCutForegroundPatternColor(color)
    
    return override

def highlight_elements(element_ids, color_name="Red"):
    """Apply graphic overrides to highlight elements"""
    
    # Define colors
    colors = {
        "Red": DB.Color(255, 0, 0),
        "Yellow": DB.Color(255, 255, 0),
        "Blue": DB.Color(0, 0, 255),
        "Green": DB.Color(0, 255, 0),
        "Orange": DB.Color(255, 165, 0)
    }
    
    color = colors.get(color_name, colors["Red"])
    override = create_override_settings(color)
    
    # Apply overrides in active view
    view = doc.ActiveView
    
    with revit.Transaction("Highlight Clashes"):
        for element_id in element_ids:
            view.SetElementOverrides(element_id, override)

def isolate_elements(element_ids):
    """Isolate specified elements in view"""
    view = doc.ActiveView
    
    if not view.CanBePrinted:
        TaskDialog.Show("Error", "Cannot isolate elements in this view type")
        return
    
    # Convert to ICollection
    id_collection = List[DB.ElementId](element_ids)
    
    with revit.Transaction("Isolate Clashing Elements"):
        view.IsolateElementsTemporary(id_collection)

def reset_view():
    """Reset all temporary isolation and overrides"""
    view = doc.ActiveView
    
    with revit.Transaction("Reset View"):
        # Reset temporary isolation
        if view.IsInTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate):
            view.DisableTemporaryViewMode(DB.TemporaryViewMode.TemporaryHideIsolate)
        
        # Reset graphic overrides
        collector = DB.FilteredElementCollector(doc, view.Id)
        elements = collector.WhereElementIsNotElementType().ToElements()
        
        for elem in elements:
            view.SetElementOverrides(elem.Id, DB.OverrideGraphicSettings())

def main():
    """Main function"""
    # Options for user
    options = ["Highlight Selected", "Isolate Selected", 
               "Reset View", "Auto-Detect and Highlight"]
    
    selected_option = forms.SelectFromList.show(
        options,
        title='Clash Visualization',
        button_name='Apply'
    )
    
    if not selected_option:
        return
    
    if selected_option == "Reset View":
        reset_view()
        TaskDialog.Show("Success", "View reset completed")
        return
    
    # Get selected elements
    selection = uidoc.Selection.GetElementIds()
    
    if not selection:
        TaskDialog.Show("Error", "Please select elements first")
        return
    
    if selected_option == "Highlight Selected":
        # Ask for color
        colors = ["Red", "Yellow", "Blue", "Green", "Orange"]
        color = forms.SelectFromList.show(colors, title="Select Color")
        if color:
            highlight_elements(selection, color)
            TaskDialog.Show("Success", "Elements highlighted")
    
    elif selected_option == "Isolate Selected":
        isolate_elements(selection)
        TaskDialog.Show("Success", "Elements isolated")

if __name__ == '__main__':
    main()
