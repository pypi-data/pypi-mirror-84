# kerfed_api

These are Python bindings used to access the [Kerfed API](https://api.kerfed.com) for analyzing and automatically quoting CAD assemblies. You can create an API key via the management console at [https://kerfed.com/account](https://kerfed.com/account).


## Quick Start
```
pip install kerfed_api

ipython -i
>>> import kerfed_api as ka
>>> quote = ka.Quote('models/camera.3dxml')
>>> quote.parts

```