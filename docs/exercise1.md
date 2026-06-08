## Exercise #1: Calculate the p-value of your excess

From the plot and the fit result from the previous exercise, we may conclude that indeed the Higgs boson exist. How can we quantify this?
[RooStats](https://twiki.cern.ch/twiki/bin/view/Main/RooStats)
allows you to calculate the pvalue of your observation, i.e. the probability that what you're observing is at least compatible with a background fluctuation of that size. Different methods are available for this, we'll use the
`ProfileLikelihoodCalculator`
.

First of all, create a skeleton python program and call it, for instance,
`exercise_1_pval.py`
. Load
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
:

```python
#Import the ROOT libraries
import ROOT
```

Import the workspace from the file produced in the previous exercise:

```python
#Open the rootfile and get the workspace from the exercise_0
fInput = ROOT.TFile("Workspace_m4lfit.root")
ws = fInput.Get("ws")
ws.Print()
```

[RooStats](https://twiki.cern.ch/twiki/bin/view/Main/RooStats)
needs to configure the PDF model using the class
`ModelConfig`
:

```python
#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("totpdf")
```

Let's access the parameter
`cross_h125`
from the workspace and take a "snapshot" (i.e.: a clone). We want to set
`cross_h125=0`
in order to determine the significance, measured from the p-value corresponding to the background-only hypothesis:

```python
#Here we explicitly set the value of the parameters for the null hypothesis
#We want no signal contribution, so cross section = 0
cross_h125 = ws.var("cross_h125")
poi = ROOT.RooArgSet(cross_h125)
nullParams = poi.snapshot()
nullParams.setRealValue("cross_h125",0.)
```

We use the class
[ProfileLikelihoodCalculator](https://root.cern.ch/doc/master/classRooStats_1_1ProfileLikelihoodCalculator.html)
to implement the profile-likelihood method and determine the significance with the class
[HypoTestResult](https://root.cern.ch/root/html/RooStats_1_1HypoTestResult.html)
:

```python
#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("unbinned_m4l"), model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)
```

Now we just need to print out the result:

```python
#We get a HypoTestResult out of the calculator, and we can query it.
htr = plc.GetHypoTest()

print("-------------------------------------------------")
print("The p-value for the null is ", htr.NullPValue())
print("Corresponding to a signifcance of ", htr.Significance())
print("-------------------------------------------------")
```

So, is the excess at 125
[GeV](https://twiki.cern.ch/twiki/bin/view/Main/GeV)
significant?

The full exercise can be found here:
[exercise_1_pval.py](code/exercise_1_pval.py)


## Downloadable code

- [`exercise_1_pval.py`](code/exercise_1_pval.py)
