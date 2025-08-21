# -*- coding: utf-8 -*-
"""
Quick Clash Check
Fast clash detection for active view elements
"""

__title__ = "Quick\nCheck"
__author__ = "Your Name"
__doc__ = "Quick clash check for elements in active view"

from Autodesk.Revit import DB
from Autodesk.Revit.UI import TaskDialog
from pyrevit import revit, forms
import clr

doc = revit.doc
uidoc = revit.uidoc

def quick_check():
    """Perform quick clash check on visible elements"""
    # Get active view
    active_view = doc.ActiveView
    
    # Filter for model elements in view
    collector = DB.FilteredElementCollector(doc, active_view.Id)
    elements = collector.WhereElementIsNotElementType().ToElements()
    
    # Filter for geometric elements only
    geo_elements = []
    categories_to_check = [
        DB.BuiltInCategory.OST_Walls,
        DB.BuiltInCategory.OST_Columns,
        DB.BuiltInCategory.OST_StructuralFraming,
        DB.BuiltInCategory.OST_Floors,
        DB.BuiltInCategory.OST_Roofs,
        DB.BuiltInCategory.OST_Doors,
        DB.BuiltInCategory.OST_Windows,
        DB.BuiltInCategory.OST_DuctCurves,
        DB.BuiltInCategory.OST_PipeCurves
    ]
    
    for elem in elements:
        try:
            if elem.Category and elem.Category.Id.IntegerValue in [cat.value__ for cat in categories_to_check]:
                geo_elements.append(elem)
        except:
            pass
    
    # Quick bounding box check
    clashes = []
    for i in range(len(geo_elements)):
        for j in range(i + 1, len(geo_elements)):
            elem1 = geo_elements[i]
            elem2 = geo_elements[j]
            
            # Get bounding boxes
            bb1 = elem1.get_BoundingBox(active_view)
            bb2 = elem2.get_BoundingBox(active_view)
            
            if bb1 and bb2:
                # Check if bounding boxes intersect
                if (bb1.Min.X <= bb2.Max.X and bb1.Max.X >= bb2.Min.X and
                    bb1.Min.Y <= bb2.Max.Y and bb1.Max.Y >= bb2.Min.Y and
                    bb1.Min.Z <= bb2.Max.Z and bb1.Max.Z >= bb2.Min.Z):
                    clashes.append((elem1, elem2))
    
    # Report results
    if clashes:
        message = "Potential clashes found: {}\n\n".format(len(clashes))
        message += "First 5 potential clashes:\n"
        for clash in clashes[:5]:
            message += "• {} <-> {}\n".format(
                clash[0].Name if hasattr(clash[0], 'Name') else clash[0].Id,
                clash[1].Name if hasattr(clash[1], 'Name') else clash[1].Id
            )
        TaskDialog.Show("Quick Check Results", message)
    else:
        TaskDialog.Show("Quick Check", "No potential clashes detected!")

if __name__ == '__main__':
    quick_check()
