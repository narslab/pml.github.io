# Notebook Integration Guide

This guide explains how the Jekyll site has been configured to display and provide downloads for Jupyter notebooks.

## Overview

The site now supports three ways to interact with Jupyter notebooks:

1. **Download**: Direct download of `.ipynb` files
2. **View Online**: Display notebooks using nbviewer (GitHub's notebook renderer)
3. **Run in Cloud**: Open notebooks in Google Colab for immediate execution

## What's Been Set Up

### 1. Notebook Layout (`_layouts/notebook.html`)
A custom layout that provides:
- Download button for the notebook file
- Link to view in nbviewer
- Link to open in Google Colab
- Clean presentation of notebook content

### 2. Notebook Pages (`/notebooks/`)
Individual pages for each notebook with:
- Descriptive content about what the notebook covers
- Easy navigation through the Notebooks section
- Consistent styling and controls

### 3. CSS Styling (`_sass/custom/notebook.scss`)
Custom styles for:
- Notebook control buttons
- Responsive design for mobile devices
- Clean notebook presentation

### 4. Navigation Integration
- Added "Notebooks" section to site navigation
- Each notebook gets its own page with proper URLs
- Integrated with the existing module schedule

## File Structure

```
notebooks/
├── index.md                      # Main notebooks page
├── glm-notebook.md              # GLM notebook page
├── ridge-lasso-notebook.md      # Ridge/Lasso notebook page
├── classification-performance.md # Classification metrics notebook
├── linear-regression.md         # Linear regression notebook
└── logistic-regression.md       # Logistic regression notebook

_layouts/
├── notebook.html                # Layout for notebook pages
└── notebook-simple.html         # Alternative simplified layout

_sass/custom/
└── notebook.scss                # Notebook-specific styles

assets/notebooks/
├── GLM.ipynb                    # Your existing notebooks
├── ridge-lasso.ipynb
├── M1-Classification-Performance.ipynb
├── M2-Linear-Regression.ipynb
└── M2-Logistic-Regression.ipynb
```

## How It Works

### For Students:
1. Visit the **Notebooks** section in the site navigation
2. Browse available notebooks with descriptions
3. Choose to:
   - **Download** the notebook to run locally
   - **View** the notebook rendered cleanly online
   - **Open in Colab** to run immediately in the browser

### For Instructors:
1. Add new notebooks to `assets/notebooks/`
2. Create a new page in `notebooks/` using the template
3. Update module pages to link to the new notebook page

## Adding New Notebooks

To add a new notebook:

1. **Add the notebook file** to `assets/notebooks/`

2. **Create a notebook page** in `notebooks/`:
```markdown
---
layout: notebook
title: "Your Notebook Title"
description: "Brief description of what this notebook covers"
notebook_path: "assets/notebooks/your-notebook.ipynb"
nav_order: 6  # Increment for each new notebook
parent: Notebooks
---

## Notebook Contents

Brief description of topics covered:
- Topic 1
- Topic 2
- Topic 3

Use the buttons above to download the notebook or open it in your preferred environment.
```

3. **Link from module pages** in `_modules/`:
```markdown
: **NOTEBOOK**{: .label .label-activity}[Your Notebook Title](/notebooks/your-notebook-page/)
```

## Optional: HTML Conversion

For even better integration, you can convert notebooks to HTML:

1. **Install requirements**:
   ```bash
   pip install jupyter nbconvert
   ```

2. **Run the conversion script**:
   ```bash
   python convert_notebooks.py
   ```

3. **Use the generated HTML** by adding to your notebook page:
   ```yaml
   notebook_html: "notebooks/your-notebook.html"
   ```

This will embed a rendered preview directly in the page.

## Benefits

- **Easy Access**: Students can quickly download or view notebooks
- **Multiple Platforms**: Support for local Jupyter, Colab, and nbviewer
- **Professional Appearance**: Clean, consistent presentation
- **Mobile Friendly**: Responsive design works on all devices
- **SEO Friendly**: Each notebook has its own discoverable URL
- **GitHub Integration**: Seamless integration with GitHub repository
