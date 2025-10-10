---
layout: page
title: Notebooks
nav_order: 6
has_children: true
---

This section contains interactive Jupyter notebooks used throughout the course. Each notebook provides multiple ways to access the content:

- **📓 Embedded Preview**: View the complete notebook rendered directly on this site
- **📥 Download**: Get the `.ipynb` file to run locally with Jupyter
- **👁️ View on GitHub**: Clean display using GitHub's native notebook viewer
- **🚀 Open in Colab**: Run immediately in Google Colab (no local setup required)

## Available Notebooks

### Module 1: Foundations
- [**Classification Performance**](/notebooks/classification-performance/) - Metrics and evaluation techniques for classification models

### Module 2: Linear Methods  
- [**GLM - Poisson and Logistic**](/notebooks/glm-notebook/) - Generalized Linear Models with practical examples
- [**Ridge and Lasso Regression**](/notebooks/ridge-lasso-notebook/) - Regularized regression techniques
- [**Linear Regression**](/notebooks/linear-regression/) - Linear regression fundamentals and implementation
- [**Logistic Regression**](/notebooks/logistic-regression/) - Binary and multiclass classification

## Getting Started

### Running Locally
1. Download any notebook using the download button
2. Install Jupyter: `pip install jupyter notebook`
3. Start Jupyter: `jupyter notebook`
4. Navigate to and open the downloaded file

### Using Google Colab
1. Click the "🚀 Open in Colab" button on any notebook page
2. Sign in with your Google account
3. Run cells directly in your browser
4. Save copies to your Google Drive

### Required Packages
Most notebooks require these Python packages:
```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

For specific requirements, check the first cell of each notebook.
