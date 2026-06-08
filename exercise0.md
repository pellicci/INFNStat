
# Exercise 0: Fit the invariant mass spectrum

Goal: build a signal+background model for the four-lepton invariant mass distribution and fit it to CMS data.

## Dataset

The ROOT file is available in:

`assets/h4l_Dataset_and_shapes.root`

## Main steps

1. Define the observable `m4l`
2. Load data and histograms
3. Convert histograms into RooHistPdf objects
4. Build a combined RooAddPdf model
5. Perform an extended maximum-likelihood fit
6. Plot the result
7. Save everything into a RooWorkspace

## Output

![Fit result](assets/exercise_0.png)

## Variable transformation

The exercise also demonstrates replacing the signal yield with a cross-section parameter using RooFormulaVar.

See:

- `code/exercise_0_h125_xsec.py`
