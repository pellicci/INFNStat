
#Import the ROOT libraries
import ROOT

#Open the rootfile and get the workspace from the exercise_0
fInput = ROOT.TFile("Workspace_m4lfit_Hmass.root")
ws = fInput.Get("ws")
ws.Print()

#Let the model know what is the parameter of interest
m0_sig = ws.var("m0_sig")
m0_sig.setRange(120., 130.)  #this is mostly for plotting reasons
poi = ROOT.RooArgSet(m0_sig)

#Configure the model
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("totpdf")
model.SetParametersOfInterest(poi)

#Set confidence level
confidenceLevel = 0.68

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("unbinned_m4l"), model)
plc.SetParameters(poi)
plc.SetConfidenceLevel(confidenceLevel)

#Get the interval
pl_Interval = plc.GetInterval()

#Now let's determine the Bayesian probability interval
#We could use the standard Bayesian Calculator, but this would be very slow for the integration
#So we profit of the Markov-Chain MC capabilities of RooStats to speed things up
mcmc = ROOT.RooStats.MCMCCalculator(ws.data("unbinned_m4l") , model)
mcmc.SetConfidenceLevel(confidenceLevel)
mcmc.SetNumIters(500000)           #Metropolis-Hastings algorithm iterations
mcmc.SetNumBurnInSteps(200)       #first N steps to be ignored as burn-in
mcmc.SetLeftSideTailFraction(0.5) #for central interval

MCMC_interval = mcmc.GetInterval()

#Let's make a plot
dataCanvas = ROOT.TCanvas("dataCanvas")
dataCanvas.Divide(2,1)

dataCanvas.cd(1)
plot_Interval = ROOT.RooStats.LikelihoodIntervalPlot(pl_Interval)
plot_Interval.SetTitle("Profile Likelihood Ratio")
plot_Interval.SetMaximum(3.)
plot_Interval.Draw()

dataCanvas.cd(2)
plot_MCMC = ROOT.RooStats.MCMCIntervalPlot(MCMC_interval)
plot_MCMC.SetTitle("Bayesian probability interval (Markov Chain)")
plot_MCMC.Draw()

dataCanvas.SaveAs("exercise_2_massInt.png")

#Now print the interval for mH for the two methods
print("PLC interval is [", pl_Interval.LowerLimit(m0_sig), ", ", pl_Interval.UpperLimit(m0_sig), "]")

print("Bayesian interval is [", MCMC_interval.LowerLimit(m0_sig), ", ", MCMC_interval.UpperLimit(m0_sig), "]")

#pyROOT sometimes fails cleaning memory, this helps
del mcmc

