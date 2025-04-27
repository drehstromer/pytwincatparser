#!/usr/bin/env python3
"""
Example script to demonstrate how to use the getItemByName method to get methods and properties.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pytwincatparser.TwincatParser import TwinCatLoader


def main():
    # Path to the TwinCAT files
    search_path = Path(__file__).parent.parent / 'TwincatFiles'
    
    # Initialize the loader
    tc_objects = []
    loader = TwinCatLoader(search_path=search_path, tcObjects=tc_objects)
    
    # Load all TwinCAT files
    loader.load()
    
    # Print all objects
    print("\nAll loaded objects:")
    for name, obj in tc_objects:
        print(f"  - {name}: {type(obj).__name__}")
        if hasattr(obj, 'methods') and obj.methods:
            print(f"    Methods: {len(obj.methods)}")
            for method in obj.methods:
                print(f"      - {method.name}")
        if hasattr(obj, 'properties') and obj.properties:
            print(f"    Properties: {len(obj.properties)}")
            for prop in obj.properties:
                print(f"      - {prop.name}")
    
    # Get a POU by name
    pou = loader.getItemByName('FB_Base')
    if pou:
        print(f"Found POU: {pou.name}")
        
        # Print methods
        if hasattr(pou, 'methods') and pou.methods:
            print(f"\nMethods in {pou.name}:")
            for i, method in enumerate(pou.methods):
                print(f"  {i}. {method.name} (Return Type: {method.returnType})")
        else:
            print(f"\nNo methods found in {pou.name}")
        
        # Print properties
        if hasattr(pou, 'properties') and pou.properties:
            print(f"\nProperties in {pou.name}:")
            for i, prop in enumerate(pou.properties):
                print(f"  {i}. {prop.name} (Type: {prop.returnType})")
        else:
            print(f"\nNo properties found in {pou.name}")
    
    # Print all objects
    print("\nAll loaded objects:")
    for name, obj in tc_objects:
        print(f"  - {name}: {type(obj).__name__}")
    
    # Get a method by name
    method = loader.getItemByName('FB_Base._ConfigureAlarm')
    if method:
        print(f"\nFound Method: {method.name}")
        print(f"  Return Type: {method.returnType}")
        print(f"  Access Modifier: {method.accessModifier}")
        if method.documentation:
            if method.documentation.brief:
                print(f"  Brief: {method.documentation.brief}")
            if method.documentation.returns:
                print(f"  Returns: {method.documentation.returns}")
    else:
        print("\nMethod not found")
    
    # Get a property by name
    property = loader.getItemByName('FB_Base.DesignationName')
    if property:
        print(f"\nFound Property: {property.name}")
        print(f"  Type: {property.returnType}")
        print(f"  Has Getter: {property.get is not None}")
        print(f"  Has Setter: {property.set is not None}")
    
    # Try to get a non-existent item
    non_existent = loader.getItemByName('NonExistent.Item')
    if non_existent is None:
        print("\nNon-existent item correctly returned None")


if __name__ == '__main__':
    main()
