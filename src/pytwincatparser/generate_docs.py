import os
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Tuple, Any, Optional

from .TwincatParser import TwinCatLoader, TcPou, TcDut, TcItf, TcMethod, TcProperty


def generate_documentation(search_path: str | Path, output_dir: str | Path, templates_dir: str | Path = None) -> None:
    """
    Generate HTML documentation for TwinCAT objects.
    
    Args:
        search_path: Path to search for TwinCAT files
        output_dir: Directory to save the generated HTML files
        templates_dir: Directory containing the Jinja2 templates (defaults to 'templates' in the current directory)
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up Jinja2 environment
    if templates_dir is None:
        # Default to 'templates' in the current directory
        templates_dir = Path(__file__).parent.parent.parent / 'templates'
    
    env = Environment(loader=FileSystemLoader(templates_dir))
    
    # Load TwinCAT objects
    tc_objects: List[Tuple[str, Any]] = []
    loader = TwinCatLoader(search_path=search_path, tcObjects=tc_objects)
    loader.load()
    
    # Separate objects by type
    pous: List[Tuple[str, TcPou]] = []
    duts: List[Tuple[str, TcDut]] = []
    itfs: List[Tuple[str, TcItf]] = []
    
    for name, obj in tc_objects:
        if isinstance(obj, TcPou):
            pous.append((name, obj))
        elif isinstance(obj, TcDut):
            duts.append((name, obj))
        elif isinstance(obj, TcItf):
            itfs.append((name, obj))
    
    # Generate index page
    template = env.get_template('index.html')
    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(template.render(pous=pous, duts=duts, itfs=itfs))
    
    # Generate POU pages
    template = env.get_template('tcpou.html')
    for name, pou in pous:
        safe_name = name.replace('.', '_')
        with open(output_dir / f'pou_{safe_name}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(obj=pou))
        
        # Generate method pages
        if pou.methods:
            method_template = env.get_template('tcmethod_single.html')
            for method in pou.methods:
                method_safe_name = f"{safe_name}_{method.name}"
                with open(output_dir / f'method_{method_safe_name}.html', 'w', encoding='utf-8') as f:
                    f.write(method_template.render(obj=method))
        
        # Generate property pages
        if pou.properties:
            property_template = env.get_template('tcproperty_single.html')
            for prop in pou.properties:
                prop_safe_name = f"{safe_name}_{prop.name}"
                with open(output_dir / f'property_{prop_safe_name}.html', 'w', encoding='utf-8') as f:
                    f.write(property_template.render(obj=prop))
    
    # Generate DUT pages
    template = env.get_template('tcdut.html')
    for name, dut in duts:
        safe_name = name.replace('.', '_')
        with open(output_dir / f'dut_{safe_name}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(obj=dut))
    
    # Generate Interface pages
    template = env.get_template('tcitf.html')
    for name, itf in itfs:
        safe_name = name.replace('.', '_')
        with open(output_dir / f'itf_{safe_name}.html', 'w', encoding='utf-8') as f:
            f.write(template.render(obj=itf))
        
        # Generate method pages
        if itf.methods:
            method_template = env.get_template('tcmethod_single.html')
            for method in itf.methods:
                method_safe_name = f"{safe_name}_{method.name}"
                with open(output_dir / f'method_{method_safe_name}.html', 'w', encoding='utf-8') as f:
                    f.write(method_template.render(obj=method))
        
        # Generate property pages
        if itf.properties:
            property_template = env.get_template('tcproperty_single.html')
            for prop in itf.properties:
                prop_safe_name = f"{safe_name}_{prop.name}"
                with open(output_dir / f'property_{prop_safe_name}.html', 'w', encoding='utf-8') as f:
                    f.write(property_template.render(obj=prop))
    
    print(f"Documentation generated in {output_dir}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python -m pytwincatparser.generate_docs <search_path> <output_dir> [templates_dir]")
        sys.exit(1)
    
    search_path = sys.argv[1]
    output_dir = sys.argv[2]
    templates_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    generate_documentation(search_path, output_dir, templates_dir)
