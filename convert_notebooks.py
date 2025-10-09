#!/usr/bin/env python3
"""
Script to convert Jupyter notebooks to HTML for Jekyll integration.
Run this script to generate HTML versions of notebooks that can be embedded in Jekyll pages.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def convert_notebook_to_html(notebook_path, output_dir="_includes/notebooks"):
    """Convert a single notebook to HTML using nbconvert"""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get notebook name without extension
    notebook_name = Path(notebook_path).stem
    output_path = os.path.join(output_dir, f"{notebook_name}.html")
    
    try:
        # Use nbconvert to convert notebook to HTML
        cmd = [
            "jupyter", "nbconvert",
            "--to", "html",
            "--template", "basic",
            "--output-dir", output_dir,
            "--output", notebook_name,
            notebook_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Converted {notebook_path} to {output_path}")
            return output_path
        else:
            print(f"❌ Failed to convert {notebook_path}")
            print(f"Error: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ Jupyter/nbconvert not found. Please install with: pip install jupyter")
        return None

def convert_all_notebooks(notebooks_dir="assets/notebooks"):
    """Convert all notebooks in the notebooks directory"""
    
    if not os.path.exists(notebooks_dir):
        print(f"❌ Notebooks directory {notebooks_dir} not found")
        return
    
    notebook_files = []
    for file in os.listdir(notebooks_dir):
        if file.endswith('.ipynb') and not file.startswith('.'):
            notebook_files.append(os.path.join(notebooks_dir, file))
    
    if not notebook_files:
        print(f"❌ No notebook files found in {notebooks_dir}")
        return
    
    print(f"Found {len(notebook_files)} notebooks to convert:")
    
    converted_files = []
    for notebook_path in notebook_files:
        output_path = convert_notebook_to_html(notebook_path)
        if output_path:
            converted_files.append(output_path)
    
    print(f"\n✅ Successfully converted {len(converted_files)} notebooks")
    print("\nTo use these in your Jekyll pages, include them with:")
    print("{% include notebooks/NOTEBOOK_NAME.html %}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Convert specific notebook
        notebook_path = sys.argv[1]
        if os.path.exists(notebook_path):
            convert_notebook_to_html(notebook_path)
        else:
            print(f"❌ Notebook file {notebook_path} not found")
    else:
        # Convert all notebooks
        convert_all_notebooks()
