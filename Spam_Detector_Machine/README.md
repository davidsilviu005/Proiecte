# Spam Detector Machine

This Python project generates a synthetic email dataset, explores its features, and trains a Random Forest classifier to distinguish spam from non-spam messages.

## Files

- `generare_csv.py` creates `train.csv` and `test.csv` with features such as message length, links, attachments, domain, capital letters, and offers.
- `grafice_EDA.py` prints descriptive statistics and displays exploratory charts for the generated data.
- `programare_model.py` encodes categorical fields, trains a `RandomForestClassifier`, and prints its accuracy on the test set.

## Run

Install `numpy`, `pandas`, `matplotlib`, `seaborn`, and `scikit-learn`. From this folder, run the scripts in order: `python generare_csv.py`, optionally `python grafice_EDA.py`, then `python programare_model.py`. The CSV files are generated locally and are not included in this folder.
