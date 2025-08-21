# -*- coding: utf-8 -*-
"""
Test Script for Clash Detection Extension
Run this to verify the extension is properly installed
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from Autodesk.Revit import DB
        print("✓ Revit API imported successfully")
    except ImportError as e:
        print("✗ Failed to import Revit API:", e)
        return False
    
    try:
        from pyrevit import revit, forms, script
        print("✓ PyRevit modules imported successfully")
    except ImportError as e:
        print("✗ Failed to import PyRevit modules:", e)
        return False
    
    try:
        # Test if lib folder is in path
        lib_path = os.path.join(os.path.dirname(__file__), '..', '..', 'lib')
        if lib_path not in sys.path:
            sys.path.append(lib_path)
        
        import clash_utils
        print("✓ Clash utilities module imported successfully")
    except ImportError as e:
        print("✗ Failed to import clash utilities:", e)
        return False
    
    return True

def test_revit_connection():
    """Test connection to Revit document"""
    print("\nTesting Revit connection...")
    
    try:
        from pyrevit import revit
        doc = revit.doc
        
        if doc:
            print("✓ Connected to document:", doc.Title)
            print("  Project Information:")
            print("  - Path:", doc.PathName if doc.PathName else "Not saved")
            print("  - Is Family:", doc.IsFamilyDocument)
            print("  - Is Workshared:", doc.IsWorkshared)
        else:
            print("✗ No active document found")
            return False
            
    except Exception as e:
        print("✗ Failed to connect to Revit:", e)
        return False
    
    return True

def test_element_collection():
    """Test element collection"""
    print("\nTesting element collection...")
    
    try:
        from pyrevit import revit
        from Autodesk.Revit import DB
        
        doc = revit.doc
        collector = DB.FilteredElementCollector(doc)
        walls = collector.OfCategory(DB.BuiltInCategory.OST_Walls).ToElements()
        
        print("✓ Found {} walls in model".format(len(walls)))
        
        # Test other categories
        categories = [
            (DB.BuiltInCategory.OST_Columns, "columns"),
            (DB.BuiltInCategory.OST_Floors, "floors"),
            (DB.BuiltInCategory.OST_Doors, "doors"),
            (DB.BuiltInCategory.OST_Windows, "windows")
        ]
        
        for cat, name in categories:
            collector = DB.FilteredElementCollector(doc)
            elements = collector.OfCategory(cat).ToElements()
            print("  - {} {}".format(len(elements), name))
            
    except Exception as e:
        print("✗ Failed to collect elements:", e)
        return False
    
    return True

def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("CLASH DETECTION EXTENSION TEST")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    if not test_imports():
        all_passed = False
    
    if not test_revit_connection():
        all_passed = False
    
    if not test_element_collection():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ ALL TESTS PASSED")
        print("The Clash Detection extension is ready to use!")
    else:
        print("✗ SOME TESTS FAILED")
        print("Please check the installation and try again.")
    print("=" * 50)

if __name__ == '__main__':
    run_tests()
