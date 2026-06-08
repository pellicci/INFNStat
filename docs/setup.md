## Computing environment

All exercises should run on any
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
installation containing also the
[RooFit](https://twiki.cern.ch/twiki/bin/view/Main/RooFit)
libraries (
[RooStats](https://twiki.cern.ch/twiki/bin/view/Main/RooStats)
is included in the
[RooFit](https://twiki.cern.ch/twiki/bin/view/Main/RooFit)
installation).
On your laptop you obtain this by passing the
*--enable-roofit*
on the
*configure*
step of the
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
installation. If you have a debian based installation, you just need to install the libRooFit library.
All the code here uses
[PyROOT](https://twiki.cern.ch/twiki/bin/view/Main/PyROOT)
, which is a python interface to
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
libraries, so a python installation is also required.

Alternatively, if you have a CERN account, most of the central
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
installations contain
[RooFit](https://twiki.cern.ch/twiki/bin/view/Main/RooFit)
. This is true for the linux environment in many other lab computing pools.

[PyROOT](https://twiki.cern.ch/twiki/bin/view/Main/PyROOT)
programs can be ran using the following command from the shell prompt:


```bash
python3 macro.py
```

In order to have all
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
libraries available in
[PyROOT](https://twiki.cern.ch/twiki/bin/view/Main/PyROOT)
, the following line should be added at the begin of every program (
`macro.py`
, in the previous command line example):


```python
import ROOT
```
