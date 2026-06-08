## Exercise #4: Testing parameters with toy-MCs

Let's say we want to test the statistical properties of some of the parameters from the initial fit, for example the cross section of the Higgs. A good way to do this, is with toy-MCs, where we generate N times the observable distributions, fit them each time, and study the distribution of the fitted parameter in the N toy-MCs.

First, let's create a new program, say
`exercise_4_toymc.py`
. We need as usual to import
[ROOT](https://twiki.cern.ch/twiki/bin/view/Main/ROOT)
and open the
`RooWorkspace`
with the fit and the data:

```python
import ROOT

#Open the rootfile and get the workspace from the exercise_0
fInput = ROOT.TFile("Workspace_m4lfit.root")
ws = fInput.Get("ws")
ws.Print()
```

In order to run the toys, we need the observable to be generated and the PDF to be used:

```python
#Get the observable and PDF out of the Workspace
m4l = ws.var("m4l")
totPDF = ws.pdf("totpdf")
```

[RooFit](https://twiki.cern.ch/twiki/bin/view/Main/RooFit)
has a class to facilitate toy-MC studies, let's initialize it, and tell it to generate and fit 1000 toy-MCs:

```python
#Initialize RooMCStudy
mc_study = ROOT.RooMCStudy(totPDF, ROOT.RooArgSet(m4l), ROOT.RooFit.Extended(1), ROOT.RooFit.FitOptions(ROOT.RooFit.Save(1)) )

#Generate 1000 experiments and fit each one, each fluctuating in Nevents = NJpsi + Npsi + Nbkg
mc_study.generateAndFit(1000)
```

Say we want to study the cross section parameter,
`cross_h125`
. We want to see the distribution of the fitted parameters, their errors, and their pulls. We can also plot the likelihood function for each toy:

```python
#Now let's see the results. For example, the study of the cross section variable
cross_h125 = ws.var("cross_h125")
frame_cross_par = mc_study.plotParam(cross_h125, ROOT.RooFit.Bins(40))
frame_cross_err = mc_study.plotError(cross_h125, ROOT.RooFit.Bins(40), ROOT.RooFit.FrameRange(0.,30.) )
frame_cross_pul = mc_study.plotPull(cross_h125, ROOT.RooFit.Bins(40), ROOT.RooFit.FitGauss(1) )

#Also, let's see the distribution of the NLL for all the fits
frame_nll = mc_study.plotNLL(ROOT.RooFit.Bins(40))
```

Let's now plot all that:

```python
#Now plot the whole thing
ROOT.gStyle.SetOptStat(0)

mcstudy_Canvas = ROOT.TCanvas("mcstudy_Canvas")
mcstudy_Canvas.Divide(2,2)

mcstudy_Canvas.cd(1)
frame_cross_par.Draw()

mcstudy_Canvas.cd(2)
frame_cross_err.Draw()

mcstudy_Canvas.cd(3)
frame_cross_pul.Draw()

mcstudy_Canvas.cd(4)
frame_nll.Draw()

mcstudy_Canvas.SaveAs("exercise_4.png")
```

The resulting plot should look similar to this:

![exercise_4.png](assets/exercise_4.png)

You can find the toy-MC program here:
[exercise_4_toyMC.py](code/exercise_4_toyMC.py)
.

--
[MarioPelliccioni](https://twiki.cern.ch/twiki/bin/view/Main/MarioPelliccioni)
- 2026-06-03


## Downloadable code

- [`exercise_4_toymc.py`](code/exercise_4_toymc.py)
