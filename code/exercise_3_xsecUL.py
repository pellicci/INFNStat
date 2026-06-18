
#Import the ROOT libraries
import ROOT

#Open the rootfile and get the workspace
fInput = ROOT.TFile("Workspace_m4lfit_newres.root")
ws = fInput.Get("ws")
ws.Print()

#Make the h125 shape rigid, for stability and speed
ws.var("m0_sig").setConstant(1)

#Configure the model, we need both the S+B and the B only models
sbModel = ROOT.RooStats.ModelConfig()
sbModel.SetWorkspace(ws)
sbModel.SetPdf("totpdf")
sbModel.SetName("S+B Model")

poi = ROOT.RooArgSet(ws.var("Nh145"))
sbModel.SetParametersOfInterest(poi)

bModel = sbModel.Clone()
bModel.SetPdf("totpdf")
bModel.SetName( sbModel.GetName() + "_with_poi_0")
poi.find("Nh145").setVal(0)
bModel.SetSnapshot(poi)

#First example is with a frequentist approach
fc = ROOT.RooStats.FrequentistCalculator(ws.data("unbinned_m4l"), bModel, sbModel)
fc.SetToys(1000,1000)

#Configure ToyMC Sampler of the frequentist calculator
toymcs = fc.GetTestStatSampler()

#Use profile likelihood as test statistics 
profll = ROOT.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
#for CLs (bounded intervals) use one-sided profile likelihood
profll.SetOneSided(1)

#set the test statistic to use for toys
toymcs.SetTestStatistic(profll)

#Create hypotest inverter passing the desired calculator 
calc = ROOT.RooStats.HypoTestInverter(fc)

#set confidence level (e.g. 95% upper limits)
calc.SetConfidenceLevel(0.95)

#use CLs
calc.UseCLs(1)

#reduce the noise
calc.SetVerbose(0)

npoints = 15 #Number of points to scan
# min and max for the scan (better to choose smaller intervals)
poimin = 0.
poimax = 15.

print("Doing a fixed scan  in interval : ", poimin, " , ", poimax)
calc.SetFixedScan(npoints,poimin,poimax);

result = calc.GetInterval() #This is a HypoTestInveter class object
upperLimit = result.UpperLimit()

#Example using the BayesianCalculator
#Now we also need to specify a prior in the ModelConfig
#To be quicker, we'll use the PDF factory facility of RooWorkspace
#Careful! For simplicity, we are using a flat prior, but this doesn't mean it's the best choice!
ws.factory("Uniform::prior(Nh145)")

#Fix many other parameters. This is not usually correct, but it's necessary for the code to converge in this class.
#In general, for complex problems, standard Bayersian calculators are not recommended, and you can use stuff like the Markov-Chain calculator
ws.var("Nh125").setConstant(1)
ws.var("NZX").setConstant(1)
ws.var("NggZZ").setConstant(1)
ws.var("NqqZZ").setConstant(1)

sbModel.SetPriorPdf(ws.pdf("prior"))

#Construct the bayesian calculator
bc = ROOT.RooStats.BayesianCalculator(ws.data("unbinned_m4l"), sbModel)
bc.SetConfidenceLevel(0.95)
bc.SetLeftSideTailFraction(0.) # for upper limit

bcInterval = bc.GetInterval()

#Now let's print the result of the two methods
#First the CLs
print("################")
print("The observed CLs upper limit is: ", upperLimit)

#Compute expected limit
print("Expected upper limits, using the B (alternate) model : ")
print(" expected limit (median) ", result.GetExpectedUpperLimit(0))
print(" expected limit (-1 sig) ", result.GetExpectedUpperLimit(-1))
print(" expected limit (+1 sig) ", result.GetExpectedUpperLimit(1))
print("################")

#Now let's see what the bayesian limit is
print("Bayesian upper limit on Nh145 = ", bcInterval.UpperLimit())

#Plot now the result of the scan 

#First the CLs
freq_plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","Frequentist scan result for psi xsec",result)
#Then the Bayesian posterior
bc_plot = bc.GetPosteriorPlot()

#Plot in a new canvas with style
dataCanvas = ROOT.TCanvas("dataCanvas")
dataCanvas.Divide(2,1)
dataCanvas.SetLogy(0)
dataCanvas.cd(1)
freq_plot.Draw("2CL")
dataCanvas.cd(2)
bc_plot.Draw()
dataCanvas.SaveAs("exercise_3_UL.png")
