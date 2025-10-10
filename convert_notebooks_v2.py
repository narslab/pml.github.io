#!/usr/bin/env python3
"""
Enhanced script to convert Jupyter notebooks to HTML for Jekyll integration.
Creates clean HTML versions that embed nicely in Jekyll pages.
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def convert_notebook_to_html(notebook_path, output_dir="_includes/notebooks"):
    """Convert a single notebook to HTML using nbconvert with post-processing"""
    
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
            # Post-process the HTML to make it Jekyll-friendly
            with open(output_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Clean up the HTML for Jekyll inclusion
            cleaned_content = clean_html_for_jekyll(html_content)
            
            # Write the cleaned content
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ Converted {notebook_path} to {output_path}")
            return output_path
        else:
            print(f"❌ Failed to convert {notebook_path}")
            print(f"Error: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ Jupyter/nbconvert not found. Please install with: pip install jupyter")
        return None

def clean_html_for_jekyll(html_content):
    """Clean HTML content to make it suitable for Jekyll inclusion"""
    
    # Remove DOCTYPE, html, head, and body tags
    html_content = re.sub(r'<!DOCTYPE[^>]*>', '', html_content)
    html_content = re.sub(r'<html[^>]*>', '', html_content)
    html_content = re.sub(r'</html>', '', html_content)
    html_content = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<body[^>]*>', '', html_content)
    html_content = re.sub(r'</body>', '', html_content)
    
    # Clean up whitespace
    html_content = re.sub(r'\n\s*\n', '\n', html_content)
    html_content = html_content.strip()
    
    # Wrap in a container div
    html_content = f'<div class="jupyter-notebook-content">\n{html_content}\n</div>'
    
    return html_content

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
        print(f"Converting {notebook_path}...")
        output_path = convert_notebook_to_html(notebook_path)
        if output_path:
            converted_files.append(output_path)
    
    print(f"\n✅ Successfully converted {len(converted_files)} out of {len(notebook_files)} notebooks")
    
    if converted_files:
        print("\nTo use these in your Jekyll notebook pages, add to the frontmatter:")
        print("notebook_html: \"notebooks/NOTEBOOK_NAME.html\"")
        print("\nAvailable notebook HTML files:")
        for converted_file in converted_files:
            filename = Path(converted_file).name
            print(f"  - notebook_html: \"notebooks/{filename}\"")

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
