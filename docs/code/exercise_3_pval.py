
#Import the ROOT libraries
import ROOT

#Open the rootfile and get the workspace from the exercise_0
fInput = ROOT.TFile("Workspace_m4lfit_newres.root")
ws = fInput.Get("ws")
ws.Print()

#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("totpdf")

#Here we explicitly set the value of the parameters for the null hypothesis
#We want no signal contribution, so cross section = 0
Nh145 = ws.var("Nh145")
poi = ROOT.RooArgSet(Nh145)
nullParams = poi.snapshot()
nullParams.setRealValue("Nh145",0.)

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("unbinned_m4l"), model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)

#We get a HypoTestResult out of the calculator, and we can query it.
htr = plc.GetHypoTest()

print("-------------------------------------------------")
print("The p-value for the null is ", htr.NullPValue())
print("Corresponding to a signifcance of ", htr.Significance())
print("-------------------------------------------------")
