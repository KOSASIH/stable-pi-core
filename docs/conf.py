# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Stable Pi Core'
copyright = '2025, KOSASIH'  # Replace with your name or organization
author = 'KOSASIH'  # Replace with your name or organization

# The full version, including alpha/beta/rc tags
release = '0.1.0'  # Replace with your project's version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # Automatically document Python modules
    'sphinx.ext.viewcode',  # Add links to highlighted source code
    'sphinx.ext.napoleon',  # Support for Google style docstrings
    'sphinx.ext.githubpages',  # For GitHub Pages support
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Add any paths that contain static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files.
html_static_path = ['_static']

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'  # You can change this to any Sphinx theme you prefer

# Theme options are theme-specific and customize the look and feel of the theme.
html_theme_options = {
    'description': 'A stable cryptocurrency solution with advanced features.',
    'github_user': 'KOSASIH',  # Your GitHub username
    'github_repo': 'stable-pi-core',  # Your repository name
    'github_banner': True,
    'show_powered_by': False,
}

# Add any extra paths that contain custom themes here, relative to this directory.
html_theme_path = []

# Output file base name for HTML help builder.
htmlhelp_basename = 'StablePiCoredoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    'preamble': r'''
        \usepackage{amsmath}
        \usepackage{amsfonts}
        \usepackage{amssymb}
    ''',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (master_doc, 'StablePiCore.tex', 'Stable Pi Core Documentation',
     author, 'manual'),
]

# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, 'stablepicore', 'Stable Pi Core Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (master_doc, 'StablePiCore', 'Stable Pi Core Documentation',
     author, 'StablePiCore', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

epub_title = project
epub_exclude_files = ['search.html']
