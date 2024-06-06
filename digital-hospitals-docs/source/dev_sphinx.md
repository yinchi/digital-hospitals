# General documentation with Sphinx

This documentation was written using Sphinx with several extensions, described below. Note that the install and build scripts described [here](dev_install) will automatically handle the installation of Sphinx and all necessary extensions in the appropriate virtual environment.

## MyST Parser

Whereas Sphinx was designed for use with Restructured Text (.rst) documents, [myst-parser](https://myst-parser.readthedocs.io/) is a Sphinx extension that allows Sphinx to understand Markdown documents.  For the best developer experience, install the [VSCode extension](https://marketplace.visualstudio.com/items?itemName=ExecutableBookProject.myst-highlight).

The MyST documentation contains instructions for including links (internal and external), images, code blocks, and admonitions (such as notes). Several extensions to MyST are also available; see `conf.py` for a list of extensions configured for this project.  The VSCode extension for MyST also contains support for several of these extensions, which can be enabled in the extension settings.

```{image} _static/myst.png
:alt: MyST extension settings
:width: 350px
```

## Read the Docs theme with dark mode

A version of the Read the Docs theme with dark mode support is used, courtesy of [MrDogeBro](https://github.com/MrDogeBro/sphinx_rtd_dark_mode).  This is already set up in `conf.py`; you do not need to do anything.

## Kroki

The [`sphinxcontrib.kroki`](https://github.com/sphinx-contrib/kroki) extension automatically turns Kroki code blocks in the documentation into images. By default, this uses the public server at <https://kroki.io/> to automatically generate .svg images during the Sphinx build.

To use Kroki with MyST, insert a code block as follows:

````markdown
```{kroki}
:type: plantuml

@startuml
Alice -> Bob: Hello
@enduml
```
````
