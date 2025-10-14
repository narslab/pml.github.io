#!/usr/bin/env python3
"""
Script to convert LaTeX files to HTML-friendly markdown for Jekyll LaTeX preview pages.
"""

import os
import sys
import re
import argparse
from pathlib import Path

def clean_latex_for_html(latex_content):
    """Convert LaTeX content to HTML-friendly format with MathJax compatibility"""
    
    # Remove LaTeX document structure
    latex_content = re.sub(r'\\documentclass.*?\n', '', latex_content)
    latex_content = re.sub(r'\\usepackage.*?\n', '', latex_content)
    latex_content = re.sub(r'\\begin\{document\}', '', latex_content)
    latex_content = re.sub(r'\\end\{document\}', '', latex_content)
    latex_content = re.sub(r'\\maketitle', '', latex_content)
    
    # Convert LaTeX sections to HTML headers
    latex_content = re.sub(r'\\section\*?\{([^}]+)\}', r'## \1', latex_content)
    latex_content = re.sub(r'\\subsection\*?\{([^}]+)\}', r'### \1', latex_content)
    latex_content = re.sub(r'\\subsubsection\*?\{([^}]+)\}', r'#### \1', latex_content)
    
    # Convert LaTeX lists to HTML/Markdown
    latex_content = re.sub(r'\\begin\{itemize\}', r'<ul>', latex_content)
    latex_content = re.sub(r'\\end\{itemize\}', r'</ul>', latex_content)
    latex_content = re.sub(r'\\begin\{enumerate\}', r'<ol>', latex_content)
    latex_content = re.sub(r'\\end\{enumerate\}', r'</ol>', latex_content)
    latex_content = re.sub(r'\\item\s+', r'<li>', latex_content)
    
    # Convert text formatting
    latex_content = re.sub(r'\\textbf\{([^}]+)\}', r'**\1**', latex_content)
    latex_content = re.sub(r'\\textit\{([^}]+)\}', r'*\1*', latex_content)
    latex_content = re.sub(r'\\emph\{([^}]+)\}', r'*\1*', latex_content)
    latex_content = re.sub(r'\\texttt\{([^}]+)\}', r'`\1`', latex_content)
    
    # Handle LaTeX environments
    latex_content = re.sub(r'\\begin\{theorem\}', r'<div class="theorem"><strong>Theorem:</strong> ', latex_content)
    latex_content = re.sub(r'\\end\{theorem\}', r'</div>', latex_content)
    latex_content = re.sub(r'\\begin\{definition\}', r'<div class="definition"><strong>Definition:</strong> ', latex_content)
    latex_content = re.sub(r'\\end\{definition\}', r'</div>', latex_content)
    latex_content = re.sub(r'\\begin\{lemma\}', r'<div class="lemma"><strong>Lemma:</strong> ', latex_content)
    latex_content = re.sub(r'\\end\{lemma\}', r'</div>', latex_content)
    latex_content = re.sub(r'\\begin\{proof\}', r'<div class="proof"><strong>Proof:</strong> ', latex_content)
    latex_content = re.sub(r'\\end\{proof\}', r'</div>', latex_content)
    latex_content = re.sub(r'\\begin\{example\}', r'<div class="example"><strong>Example:</strong> ', latex_content)
    latex_content = re.sub(r'\\end\{example\}', r'</div>', latex_content)
    
    # Handle math environments (keep as-is for MathJax)
    # Inline math: \( ... \) or $ ... $
    # Display math: \[ ... \] or $$ ... $$
    # These will be handled by MathJax
    
    # Clean up extra whitespace
    latex_content = re.sub(r'\n\s*\n\s*\n', r'\n\n', latex_content)
    latex_content = latex_content.strip()
    
    return latex_content

def create_latex_page(latex_file, output_dir="latex-previews", title=None):
    """Create a Jekyll page for LaTeX preview"""
    
    latex_path = Path(latex_file)
    if not latex_path.exists():
        print(f"❌ LaTeX file {latex_file} not found")
        return None
    
    # Read LaTeX content
    try:
        with open(latex_path, 'r', encoding='utf-8') as f:
            latex_content = f.read()
    except UnicodeDecodeError:
        try:
            with open(latex_path, 'r', encoding='latin-1') as f:
                latex_content = f.read()
        except Exception as e:
            print(f"❌ Could not read {latex_file}: {e}")
            return None
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate page title
    if not title:
        title = latex_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    # Clean LaTeX content
    cleaned_content = clean_latex_for_html(latex_content)
    
    # Generate slug for filename
    slug = latex_path.stem.lower().replace('_', '-')
    output_file = os.path.join(output_dir, f"{slug}.md")
    
    # Check for corresponding PDF
    pdf_file = latex_path.with_suffix('.pdf')
    pdf_exists = pdf_file.exists()
    pdf_relative_path = str(pdf_file.relative_to(Path.cwd())) if pdf_exists else None
    
    # Create Jekyll page content
    page_content = f"""---
layout: latex
title: "{title}"
description: "LaTeX document preview with download options"
latex_file: "{latex_path.relative_to(Path.cwd())}"
"""
    
    if pdf_exists:
        page_content += f'pdf_file: "{pdf_relative_path}"\n'
    
    page_content += f"""nav_exclude: true
---

## Document Preview

This page provides a preview of the LaTeX document. Use the buttons above to download the source file or view the compiled PDF.

### Content

<div class="latex-rendered-content">
<div class="math-loading">Loading mathematical content...</div>

{cleaned_content}

</div>
"""
    
    # Write the page
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(page_content)
    
    print(f"✅ Created LaTeX preview page: {output_file}")
    print(f"📄 LaTeX source: {latex_file}")
    if pdf_exists:
        print(f"📋 PDF found: {pdf_file}")
    print(f"🔗 Page URL: /{output_dir}/{slug}/")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Create Jekyll preview pages for LaTeX files')
    parser.add_argument('latex_files', nargs='+', help='LaTeX files to convert')
    parser.add_argument('--output-dir', '-o', default='latex-previews', 
                       help='Output directory for preview pages (default: latex-previews)')
    parser.add_argument('--title', '-t', help='Override page title')
    
    args = parser.parse_args()
    
    created_pages = []
    for latex_file in args.latex_files:
        page = create_latex_page(latex_file, args.output_dir, args.title)
        if page:
            created_pages.append(page)
    
    print(f"\n✅ Successfully created {len(created_pages)} LaTeX preview pages")
    
    if created_pages:
        print("\nTo link these in your modules, use:")
        for page in created_pages:
            page_path = Path(page)
            slug = page_path.stem
            output_dir = page_path.parent.name
            print(f": **LECTURE**{{: .label .label-blue }}[Title](/{output_dir}/{slug}/)")

if __name__ == "__main__":
    main()
