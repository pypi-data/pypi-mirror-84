### Simple Utilities

![Python Package using Conda](https://github.com/psilons/pypigeonhole-simple-utils/workflows/Python%20Package%20using%20Conda/badge.svg)
![Test Coverage](https://raw.githubusercontent.com/psilons/pypigeonhole-simple-utils/master/coverage.svg)
[![PyPI version](https://badge.fury.io/py/pypigeonhole-simple-utils.svg)](https://badge.fury.io/py/pypigeonhole-simple-utils)
![Anaconda version](https://anaconda.org/psilons/pypigeonhole-simple-utils/badges/version.svg)
![Anaconda_platform](https://anaconda.org/psilons/pypigeonhole-simple-utils/badges/platforms.svg)
![License](https://anaconda.org/psilons/pypigeonhole-simple-utils/badges/license.svg)


Provide convenience for some common tasks, with simplified interfaces.
Simple utilities does not spill over one file. Otherwise, create separate library.
They do not need docs - code speaks itself.


#### With no external dependencies except Python SDK
___
- email
- logging
- timer
- Shell command runner
- file system operations
- string manipulations

#### With 3rd party dependencies
___
- encryption needs pycryptodome 


#### Dev Process
On Linux, use pphsdlc.sh; on windows, use pphsdlc or pphsdlc.bat.
- ```conda deactivate``` back to base environment
- ```conda install -c psilons pypigeonhole-build``` to install build tool
- ```pphsdlc setup 2>&1 | tee a.log``` create a new conda environment 
- ```conda activate pypigeonhole_simple_utils```
- ```pphsdlc test``` run unittest
- ```pphsdlc package pip``` package to pip wheel
- ```pphsdlc package conda 2>&1 | tee b.log``` package to conda bz2
- ```conda env list``` if the conda env is mislabel, close window and open a
  new one. Redo step 4.
- ```pphsdlc upload pip``` upload to pip central server
- ```pphsdlc upload conda``` upload to conda central server
- To upload to local conda channel, set the environment variable
  ```set CONDA_UPLOAD_CHANNEL=file:///D:\conda-repo\channel``` and then run 
  ```pphsdlc upload conda``` again.
- check in all changes to GIT
- ```pphsdlc release``` tag change in GIT with the current version number, 
  then bump up the version.
- ```pphsdlc cleanup``` remove all build folders.
