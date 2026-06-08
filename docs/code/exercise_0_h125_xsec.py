
#Import the ROOT libraries
import ROOT

#Define the observable, the 4l invariant mass
m4l = ROOT.RooRealVar("m4l","m_{4l}",70.,1302.,"GeV")

#import the data and lineshapes for signal and background
fInput = ROOT.TFile("h4l_Dataset_and_shapes.root")

#this is the run-1 data
unbinned_4l = fInput.Get("unbinned_m4l")

#Get the histograms that describe the different contributions to the signal and background
M4l4l_Inclusive_H125Unblinded   = fInput.Get("M4l4l_Inclusive_H125Unblinded")
M4l4l_Inclusive_ggZZUnblinded   = fInput.Get("M4l4l_Inclusive_ggZZUnblinded")
M4l4l_Inclusive_qqZZUnblinded   = fInput.Get("M4l4l_Inclusive_qqZZUnblinded")
M4l_ZX_SS_4l_InclusiveUnblinded = fInput.Get("M4l_ZX_SS_4l_InclusiveUnblinded")

#Transform the histograms into PDFs. First you have to create a RooDataHist object (a fancy histogram), then create the PDF
h125hist = ROOT.RooDataHist("h125hist","h125hist",ROOT.RooArgList(m4l),M4l4l_Inclusive_H125Unblinded)
pdfh125  = ROOT.RooHistPdf("pdfh125","pdfh125",ROOT.RooArgSet(m4l),h125hist)

ggZZhist = ROOT.RooDataHist("ggZZhist","ggZZhist",ROOT.RooArgList(m4l),M4l4l_Inclusive_ggZZUnblinded)
pdfggZZ  = ROOT.RooHistPdf("pdfggZZ","pdfggZZ",ROOT.RooArgSet(m4l),ggZZhist)

qqZZhist = ROOT.RooDataHist("qqZZhist","qqZZhist",ROOT.RooArgList(m4l),M4l4l_Inclusive_qqZZUnblinded)
pdfqqZZ  = ROOT.RooHistPdf("pdfqqZZ","pdfqqZZ",ROOT.RooArgSet(m4l),qqZZhist)

ZXhist = ROOT.RooDataHist("ZXhist","ZXhist",ROOT.RooArgList(m4l),M4l_ZX_SS_4l_InclusiveUnblinded)
pdfZX  = ROOT.RooHistPdf("pdfZX","pdfZX",ROOT.RooArgSet(m4l),ZXhist)

#Expected number of signal events, based on SM expectations
#Instead of the number of events, we can fit for the cross section with a simple transformation
eff_h125 = ROOT.RooRealVar("eff_h125","The Higgs reco+id efficiency",0.35,0.00001,1.)
lumi = ROOT.RooRealVar("lumi","The CMS luminosity",24800.,0.00001,50000.,"pb-1")
br_hzz = ROOT.RooRealVar("br_hzz","H->ZZ->4l BR",0.02*0.062*0.062)
cross_h125 = ROOT.RooRealVar("cross_h125","The h125 xsec",3.,0.,100.,"pb")

eff_h125.setConstant(1)
lumi.setConstant(1)

#Now define the number of psi events
Nh125 = ROOT.RooFormulaVar("Nh125","@0*@1*@2*@3",ROOT.RooArgList(eff_h125,lumi,br_hzz,cross_h125))

#Number of events for each background contribution. The initial value is the expectation from theory+simulation
NggZZ = ROOT.RooRealVar("NggZZ","NggZZ",68.4,0.1,200.)
NqqZZ = ROOT.RooRealVar("NqqZZ","NqqZZ",317.8,0.1,500.)
NZX   = ROOT.RooRealVar("NZX","NZX",22.9,0.1,200.)

#Compose the total PDF
totpdf = ROOT.RooAddPdf("totpdf","totpdf",ROOT.RooArgList(pdfh125,pdfggZZ,pdfqqZZ,pdfZX),ROOT.RooArgList(Nh125,NggZZ,NqqZZ,NZX))

#Do the fit to data, printlevel=1 is the default, with =2 you get the full covariance and correlations
totpdf.fitTo(unbinned_4l,ROOT.RooFit.Extended(1),ROOT.RooFit.PrintLevel(1))

#Plot the result. 
#First create a canva
canvas = ROOT.TCanvas("canvas","canvas",1200,600)

#Create a drawable object and fill it
m4lplot = m4l.frame(308) #Number of bins as an argument
unbinned_4l.plotOn(m4lplot)
totpdf.plotOn(m4lplot)

#One can also plot the single components of the total PDF, like the background component
totpdf.plotOn(m4lplot, ROOT.RooFit.Components("pdfqqZZ,pdfggZZ,pdfZX"), ROOT.RooFit.FillColor(ROOT.kGreen),ROOT.RooFit.DrawOption("F"))
totpdf.plotOn(m4lplot, ROOT.RooFit.Components("pdfqqZZ,pdfggZZ"), ROOT.RooFit.FillColor(ROOT.kCyan),ROOT.RooFit.DrawOption("F"))
totpdf.plotOn(m4lplot, ROOT.RooFit.Components("pdfggZZ"), ROOT.RooFit.FillColor(ROOT.kCyan-1),ROOT.RooFit.DrawOption("F"))

#redraw the data on top of the PDF
unbinned_4l.plotOn(m4lplot)

m4lplot.SetAxisRange(70.,751.)

m4lplot.Draw()

canvas.SetLogx(1)
canvas.SaveAs("exercise_0.png")

#Now save the data and the PDF into a Workspace, for later use for statistical analysis
ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(unbinned_4l)
getattr(ws,'import')(totpdf)

fOutput = ROOT.TFile("Workspace_m4lfit.root","RECREATE")
ws.Write()
fOutput.Write()
fOutput.Close()
