# cpLogD v2.0

This is a re-take of the cpLogD model previously published in [A confidence predictor for logD using conformal regression and a support-vector machine](https://link.springer.com/article/10.1186/s13321-018-0271-1). The main update will be the version of [CPSign](https://github.com/arosbio/cpsign) which is now open source for non-commercial use, and based on a newer version of [ChEMBL](https://www.ebi.ac.uk/chembl/) (v33, May 2023). **Note: the old cpLogD was based on computed property `acd_logd` which is no longer supplied, and have been replaced by the `CX LogD 7.4` property which we will now use.**

## Steps for generation

### 1. Downloading data from ChEMBL

The latest version of ChEMBL was downloaded from the [download page](https://chembl.gitbook.io/chembl-interface-documentation/downloads), version 33 published in May 2023. The MySQL version was downloaded and loaded in a local MySQL community server following their instructions. See [download data](download_dataset/README.md) for how to extract the data from ChEMBL.


### 2. Model development and evaluation

How the modeling was performed is detailed in [train and evaluate model](train_and_evaluate_model/README.md). Model evaluation was performed in the same way as for the initial model, using a withheld dataset of 100,000 test compounds. 

## Model performance

Here we show the model performance for the new cpLogD model and compare it to the old model.

### Model calibration
![image](train_and_evaluate_model/output/calibration.png)

The error rate exactly matches the significance level from 0.6 significance and above, and even produces slightly lower error rate for significance levels lower than 0.6. In short - this shows that the model is indeed well calibrated and the predictions can be trusted.


### Model efficiency

The original work compared different hyper-parameter settings and presented Median Prediction Interval (MPI) for a set of confidence levels:

![image](cpLogD_v1_efficiency.png)

Here are the MPI for the new (v2) model:

| 10%   | 20%   | 30%   | 40%   | 50%   | 60%   | 70%   | 80%   | 90%   | 95%   | 99%  |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|------|
| 0.043 | 0.085 | 0.127 | 0.169 | 0.213 | 0.262 | 0.325 | 0.418 | 0.606 | 0.849 | 1.77 |

The new model (v2) thus beats the old models (bold faced in the first table) at all significance levels except for 10% confidence where it only differs on the last digit. As stated in the original paper, confidence levels 70-99% are the most interesting, where the new model almost halves the MPI for confidence levels 70-95%. All results can be found in [validation_stats](train_and_evaluate_model/output/validation_stats.csv). For convenience we also plot these based on the significance level: 


![image](train_and_evaluate_model/output/efficiency.png)

### Accuracy of midpoint prediction

The original paper also presented the accuracy of the underlying SVM model, thus we present the same values here (**Q$^2$**=squared correlation coefficient, **RMSEP**=root mean square error of prediction):

|Model|Q$^2$ |RMSEP|
|--|--|--|
|v1|0.973|0.41|
|v2|0.984|0.315|

Our new model thus also improve the midpoint of the predictions.