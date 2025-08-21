# -*- coding: utf-8 -*-
"""
Clash Detection Tool
Detects clashes between selected elements or categories
"""

__title__ = "Run\nDetection"
__author__ = "Your Name"
__doc__ = "Performs clash detection between selected elements or categories"

# Imports
from Autodesk.Revit import DB
from Autodesk.Revit.UI import TaskDialog, TaskDialogCommonButtons, TaskDialogResult
from pyrevit import revit, forms, script
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# Get current document
doc = revit.doc
uidoc = revit.uidoc

def get_element_geometry(element):
    """Extract solid geometry from element"""
    options = DB.Options()
    options.ComputeReferences = True
    options.IncludeNonVisibleObjects = False
    
    geo_elem = element.get_Geometry(options)
    solids = []
    
    if geo_elem:
        for geo_obj in geo_elem:
            if isinstance(geo_obj, DB.Solid) and geo_obj.Volume > 0:
                solids.append(geo_obj)
            elif isinstance(geo_obj, DB.GeometryInstance):
                instance_geo = geo_obj.GetInstanceGeometry()
                for inst_obj in instance_geo:
                    if isinstance(inst_obj, DB.Solid) and inst_obj.Volume > 0:
                        solids.append(inst_obj)
    return solids

def check_intersection(solid1, solid2):
    """Check if two solids intersect"""
    try:
        intersection = DB.BooleanOperationsUtils.ExecuteBooleanOperation(
            solid1, solid2, DB.BooleanOperationsType.Intersect
        )
        if intersection and intersection.Volume > 0:
            return True, intersection.Volume
    except:
        pass
    return False, 0

def main():
    """Main function"""
    # Get selected elements
    selection = uidoc.Selection.GetElementIds()
    
    if selection.Count < 2:
        TaskDialog.Show("Clash Detection", 
                       "Please select at least 2 elements to check for clashes")
        return
    
    elements = [doc.GetElement(id) for id in selection]
    
    # Progress bar
    with forms.ProgressBar(title='Detecting Clashes...') as pb:
        clashes = []
        total_checks = len(elements) * (len(elements) - 1) / 2
        current = 0
        
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                current += 1
                pb.update_progress(current, total_checks)
                
                elem1 = elements[i]
                elem2 = elements[j]
                
                solids1 = get_element_geometry(elem1)
                solids2 = get_element_geometry(elem2)
                
                for solid1 in solids1:
                    for solid2 in solids2:
                        has_clash, volume = check_intersection(solid1, solid2)
                        if has_clash:
                            clashes.append({
                                'elem1': elem1,
                                'elem2': elem2,
                                'volume': volume
                            })
    
    # Report results
    if clashes:
        message = "Found {} clashes:\n\n".format(len(clashes))
        for clash in clashes[:10]:  # Show first 10
            message += "• {} <-> {}\n".format(
                clash['elem1'].Name,
                clash['elem2'].Name
            )
        
        if len(clashes) > 10:
            message += "\n... and {} more".format(len(clashes) - 10)
        
        TaskDialog.Show("Clash Detection Results", message)
    else:
        TaskDialog.Show("Clash Detection", "No clashes found!")

if __name__ == '__main__':
    main()
