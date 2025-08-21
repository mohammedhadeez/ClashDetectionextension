# -*- coding: utf-8 -*-
"""
Clash Detection Utilities
Shared utilities for clash detection extension
"""

from Autodesk.Revit import DB
from math import sqrt

class ClashDetectionEngine:
    """Main clash detection engine"""
    
    def __init__(self, doc, tolerance=0.001):
        self.doc = doc
        self.tolerance = tolerance  # in meters
        self.clashes = []
        
    def get_element_solids(self, element):
        """Extract all solid geometry from element"""
        options = DB.Options()
        options.ComputeReferences = True
        options.IncludeNonVisibleObjects = False
        
        solids = []
        geo_elem = element.get_Geometry(options)
        
        if geo_elem:
            for geo_obj in geo_elem:
                solids.extend(self._extract_solids(geo_obj))
        
        return solids
    
    def _extract_solids(self, geo_obj):
        """Recursively extract solids from geometry object"""
        solids = []
        
        if isinstance(geo_obj, DB.Solid) and geo_obj.Volume > 0:
            solids.append(geo_obj)
        elif isinstance(geo_obj, DB.GeometryInstance):
            instance_geo = geo_obj.GetInstanceGeometry()
            for inst_obj in instance_geo:
                solids.extend(self._extract_solids(inst_obj))
        elif isinstance(geo_obj, DB.GeometryElement):
            for item in geo_obj:
                solids.extend(self._extract_solids(item))
        
        return solids
    
    def check_clash(self, elem1, elem2):
        """Check if two elements clash"""
        solids1 = self.get_element_solids(elem1)
        solids2 = self.get_element_solids(elem2)
        
        for solid1 in solids1:
            for solid2 in solids2:
                try:
                    intersection = DB.BooleanOperationsUtils.ExecuteBooleanOperation(
                        solid1, solid2, DB.BooleanOperationsType.Intersect
                    )
                    if intersection and intersection.Volume > self.tolerance:
                        return True, intersection.Volume
                except:
                    # Fallback to bounding box check
                    if self._check_bounding_box_intersection(solid1, solid2):
                        return True, 0
        
        return False, 0
    
    def _check_bounding_box_intersection(self, solid1, solid2):
        """Check if bounding boxes of two solids intersect"""
        bb1 = solid1.GetBoundingBox()
        bb2 = solid2.GetBoundingBox()
        
        if not bb1 or not bb2:
            return False
        
        # Check overlap in all three dimensions
        return (bb1.Min.X <= bb2.Max.X and bb1.Max.X >= bb2.Min.X and
                bb1.Min.Y <= bb2.Max.Y and bb1.Max.Y >= bb2.Min.Y and
                bb1.Min.Z <= bb2.Max.Z and bb1.Max.Z >= bb2.Min.Z)
    
    def get_clash_point(self, elem1, elem2):
        """Get approximate center point of clash"""
        bb1 = elem1.get_BoundingBox(None)
        bb2 = elem2.get_BoundingBox(None)
        
        if bb1 and bb2:
            # Get intersection of bounding boxes
            min_x = max(bb1.Min.X, bb2.Min.X)
            min_y = max(bb1.Min.Y, bb2.Min.Y)
            min_z = max(bb1.Min.Z, bb2.Min.Z)
            max_x = min(bb1.Max.X, bb2.Max.X)
            max_y = min(bb1.Max.Y, bb2.Max.Y)
            max_z = min(bb1.Max.Z, bb2.Max.Z)
            
            # Return center of intersection
            return DB.XYZ(
                (min_x + max_x) / 2,
                (min_y + max_y) / 2,
                (min_z + max_z) / 2
            )
        
        return None


class ClashFilter:
    """Filter clashes based on various criteria"""
    
    def __init__(self):
        self.filters = []
    
    def add_category_filter(self, categories):
        """Filter by element categories"""
        def category_filter(clash):
            cat1 = clash['elem1'].Category.Name
            cat2 = clash['elem2'].Category.Name
            return cat1 in categories or cat2 in categories
        
        self.filters.append(category_filter)
    
    def add_level_filter(self, levels):
        """Filter by levels"""
        def level_filter(clash):
            level1 = self._get_element_level(clash['elem1'])
            level2 = self._get_element_level(clash['elem2'])
            return level1 in levels or level2 in levels
        
        self.filters.append(level_filter)
    
    def apply_filters(self, clashes):
        """Apply all filters to clash list"""
        filtered = clashes
        for filter_func in self.filters:
            filtered = [c for c in filtered if filter_func(c)]
        return filtered
    
    def _get_element_level(self, element):
        """Get level of element"""
        try:
            level_param = element.get_Parameter(DB.BuiltInParameter.SCHEDULE_LEVEL_PARAM)
            if level_param:
                return self.doc.GetElement(level_param.AsElementId()).Name
        except:
            pass
        return "Unknown"
