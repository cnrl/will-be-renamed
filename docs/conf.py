# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

from sphinx.ext.autodoc import DataDocumenter, ModuleLevelDocumenter, SUPPRESS
from sphinx.util.inspect import object_description

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'cerebro'
copyright = '2019, Alireza Abolghasemi, Amirmohammad Asadi, Ashena Gorgan Mohammadi, Alireza Mahmudi, ' \
            'Alireza Mohammadi, Arya Sadeghi, Motahare Sadeghian, Parisa Safaryazdi'
author = 'Alireza Abolghasemi, Amirmohammad Asadi, Ashena Gorgan Mohammadi, Alireza Mahmudi, Alireza Mohammadi, ' \
         'Arya Sadeghi, Motahare Sadeghian, Parisa Safaryazdi'

# The full version, including alpha/beta/rc tags
release = '0.0.1 beta'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': False,
    'show-inheritance': True,
    'exclude-members': '__weakref__'
}


def add_directive_header(self, sig):
    ModuleLevelDocumenter.add_directive_header(self, sig)
    if not self.options.annotation:
        try:
            objrepr = object_description(self.object)

            # PATCH: truncate the value if longer than 50 characters
            if len(objrepr) > 10:
                objrepr = objrepr[:10] + "..."

        except ValueError:
            pass
        else:
            self.add_line(u'   :annotation: = ' + objrepr, '<autodoc>')
    elif self.options.annotation is SUPPRESS:
        pass
    else:
        self.add_line(u'   :annotation: %s' % self.options.annotation,
                      '<autodoc>')


DataDocumenter.add_directive_header = add_directive_header
