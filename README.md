AMD Butler [![Build Status](https://travis-ci.org/agrc/AmdButler.svg)](https://travis-ci.org/agrc/AmdButler)
==========
Serving Up AMD Module Imports

A Sublime Text 3 plugin for managing AMD dependency import statements. It helps you quickly sort, add, and remove AMD import statements. With features such as auto sorting and auto module name discovery it allows you to focus more on your code rather than worrying your AMD imports.

## Commands

#### AMD Butler: Sort AMD Imports
Sorts the existing AMD imports for the current file alphabetically. Packages are separated by a blank line. The corresponding parameter names are also reordered.

![quickcast-26-11-2014-12-21-42 1](https://cloud.githubusercontent.com/assets/1326248/5207476/de48852c-7567-11e4-99f8-da43bd1ee742.gif)

#### AMD Butler: Add AMD Import
Searches your packages for possible imports and displays them in the quick panel. When an import is selected it is added to the imports for the current file. The imports for the current file are then sorted.

![quickcast-26-11-2014-12-33-46](https://cloud.githubusercontent.com/assets/1326248/5207582/cc7d5858-7568-11e4-8fce-c6e8b91946c9.gif)

#### AMD Butler: Remove AMD Import
Displays a quick list of all of your current imports. Selecting an import from the quick list removes it from your file. The imports are also automatically sorted.

![quickcast-26-11-2014-12-35-07](https://cloud.githubusercontent.com/assets/1326248/5207584/d2cc22b6-7568-11e4-8923-bfc43e4696e9.gif)

#### AMD Butler: Refresh Available Imports
Refreshes the cache of available imports for the current view. This can be helpful after creating a new file that you want to import into the current view.

## Installation

#### Package Control
The preferred method for installation is via [package control](https://sublime.wbond.net/). First [install package control](https://sublime.wbond.net/installation), then run "Package Control: Install Package" and search for "AMD Butler".

#### Manual
Clone the [source code](https://github.com/agrc/AmdButler) for this plugin to your Sublime Packages folder.

## Settings

#### `amd_butler_packages_base_path`
The name of the folder containing your AMD packages. This folder is crawled and all files are made available as imports for the "Add AMD Import" command.

This settings can be set either at the package level (Preferences -> Package Settings -> AmdButler) or in the project file settings. No manual editing of settings files is needed. The user is prompted for the value if it's not present in either the project or package settings the first time that the "Add AMD Import" command is run.

## Contributing
Please match existing code style. 

To execute tests run: [`nosetests`](https://nose.readthedocs.org/en/latest/) from the root of the project.