[![Build Status](https://travis-ci.org/agrc/AmdImportHelper.svg)](https://travis-ci.org/agrc/AmdImportHelper)
AMD Import Helper
=================

A Sublime Text 3 plugin for managing AMD imports

Still very rough. A work in progress.

###Commands
#####AMD Import Helper: Sort AMD Imports
Sorts the existing AMD imports for the current file alphabetically. Packages are separated by a newline. The corresponding parameter names are also reordered.

#####AMD Import Helper: Add AMD Import
Searches your packages for possible imports and displays them in the quick panel. When an import is selected it is added to the imports for the current file. The imports for the current file are then sorted.

###Settings

####`amd_packages_base_path`
The full path to the folder containing your AMD packages. This folder is crawled and all files are made available as imports for the "Add AMD Import" command.

This settings can be set either at the package level (Preferences -> Package Settings -> AmdImportHelper) or in the project file settings. No manual editing of settings files is needed. The user is prompted for the value if it's not present in either the project or package settings the first time that the "Add AMD Import" command is run.
