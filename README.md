cmip6
===============

ES-DOC CMIP6 command line interface for managing CMIP6 documentation.


What is ES-DOC ?
--------------------------------------

ES-DOC stands for Earth Science - Documentation.  It's goal is to provide software tools and services in order to support the distribution of earth science documentation.


What is cmip6 ?
--------------------------------------

cmip6 is a command line interface for interacting with the es-doc CMIP6 documentation eco-system.


Why cmip6 ?
--------------------------------------

There is a need to support command line programs for streamlining deployments, publishing ... etc. 


Who uses cmip6 ?
--------------------------------------

ES-DOC software engineers.

How to install cmip6 ?
--------------------------------------

Note that [`pyenv`](https://github.com/pyenv/pyenv) and
[`pipenv`](https://pipenv.pypa.io/en/latest/) must be installed on your
machine for the following commands to succeed.

```
# Set repo.
cd YOUR_WORKING_DIRECTORY
git clone https://github.com/ES-DOC/cmip6

# Set virtual environment.
cd ./cmip6
pyenv local 2.7.18
pipenv install

# Setup.
export PYESSV_ARCHIVE_HOME=$(pwd)/archives/pyessv-archive
source $(pwd)/activate
cmip6-setup
```

How to auto-activate cmip6 ?
--------------------------------------

```
cd YOUR_WORKING_DIRECTORY

cat >> $HOME/.bashrc <<- EOM

# ----------------------------------------------------------------------
# ES-DOC - CMIP6
# ----------------------------------------------------------------------

# Set path to pyessv archive.
export PYESSV_ARCHIVE_HOME=$(pwd)/archives/pyessv-archive

# Activate CMIP6 shell.
source $(pwd)/activate

EOM
```


Further Information ?
--------------------------------------

Please refer to the [splash page](http:es-doc.org) for further information.
