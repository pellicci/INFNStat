
# Computing Environment

Requirements:

- ROOT with RooFit and RooStats
- Python 3 with PyROOT

All exercises should run on any ROOT installation containing also the RooFit libraries (RooStats is included in the RooFit installation). On your laptop you obtain this by passing the *--enable-roofit* on the configure step of the ROOT installation. If you have a debian based installation, you just need to install the libRooFit library. All the code here uses PyROOT, which is a python interface to ROOT libraries, so a python installation is also required.

Alternatively, if you have a CERN account, most of the central ROOT installations contain RooFit. This is true for the linux environment in many other lab computing pools.

PyROOT programs can be ran using the following command from the shell prompt: 

```bash
python3 macro.py
```

In order to have all ROOT libraries available in PyROOT, the following line should be added at the begin of every program (macro.py, in the previous command line example): 

```python
import ROOT
```
