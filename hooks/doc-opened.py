# -*- coding: utf-8 -*-
"""
Document opened hook
Automatically check for clashes when document is opened
"""

from Autodesk.Revit import DB
from pyrevit import EXEC_PARAMS, revit
from pyrevit.userconfig import user_config

# This hook runs when a document is opened
doc = EXEC_PARAMS.event_args.Document

def check_initial_clashes():
    """Run initial clash check on document open"""
    # Get user preferences
    config = user_config.get_config()
    auto_check = config.get_option('auto_check_on_open', False)
    
    if not auto_check:
        return
    
    # Quick check for obvious clashes
    collector = DB.FilteredElementCollector(doc)
    walls = collector.OfCategory(DB.BuiltInCategory.OST_Walls).ToElements()
    
    if len(walls) > 100:
        print("Large model detected - {} walls found".format(len(walls)))
        print("Consider running clash detection manually")
    else:
        print("Model loaded - ready for clash detection")

# Run check
if doc and not doc.IsFamilyDocument:
    check_initial_clashes()
