#!/usr/bin/env python3
"""
Example script to generate HTML documentation for TwinCAT objects.

This script demonstrates how to use the generate_docs module to create
HTML documentation for TwinCAT objects.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pytwincatparser.generate_docs import generate_documentation


def main():
    # Path to the TwinCAT files
    search_path = Path(__file__).parent.parent / 'TwincatFiles'
    
    # Directory to save the generated HTML files
    output_dir = Path(__file__).parent / 'docs'
    
    # Path to the templates directory
    templates_dir = Path(__file__).parent.parent / 'templates'
    
    # Generate the documentation
    generate_documentation(search_path, output_dir, templates_dir)
    
    print(f"Documentation generated in {output_dir}")
    print(f"Open {output_dir / 'index.html'} in your browser to view the documentation.")


if __name__ == '__main__':
    main()
