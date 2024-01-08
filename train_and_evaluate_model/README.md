# Model development

Note here that we do not perform structure standardization as it was performed in the original paper, as CPSign already performs at least some of the standardization steps done in the Ambit program that was previously used. The Ambit software has not been updated in many years and is no longer actively developed.

The model development is performed in a similar manner as performed in the original paper, here we randomly split out 100,000 records for model evaluation and use the same hyper-parameters that were devised in the original work. However, as we have a belief in the utility of object-based confidence intervals we **do** include an error model in order to get these normalized intervals rather than fixed-size prediction intervals.

## Model training steps:

### 1. Split out random validation-set

Run the python script [split_dataset.py](split_dataset.py), which only requires that you have Pandas installed. The output should be two gzip files: `validation_set.csv.gz`(100,000 observations) and `training_set.csv.gz` (remaining observations). 

### 2. Precompute the signatures for the training set

This require that you download a version of [CPSign](https://github.com/arosbio/cpsign) and place it in the current directory, here using version 2.0.0-rc6 and Java 11. The remaining code also assumes that you add execution file permissions after downloading the jar (`chmod +x <file>`). 

**Note** this step can take quite some time to finish (almost 50 min on our laptop) - as the input is in excess of 2.2M compounds.

```bash
./cpsign-2.0.0-rc6-fatjar.jar precompute \
    --model-type regression \
    --train-data TSV training_set.csv.gz \
    --property cx_logd \
    --model-out output/precomputed_data.jar \
    --logfile output/precompute.log
```

### 3. Remove duplicate entries

After signatures have been generated we filtered duplicate entries by preserving the median value if there there were duplicates found (i.e. only preserving a single observation). **Note**: use CPSign of version `rc7` or later for this step, as the rc6 version did this in `O(N*N)` whereas the rc7 and later uses an improved hashing algorithm to *greatly* improve this (19 hours vs 1 second).

```bash
./cpsign-2.0.0-rc6-fatjar.jar transform \
    --data-set output/precomputed_data.jar \
    --model-out output/precomputed_cleaned.jar \
    --transform KeepMedianLabel \
    --logfile output/clean_data.log
```


### 4. Train the CP model

**Note: here we replace the 10-fold CCP with 10 samples ACP model.** The original paper and previous model used a 10-fold CCP, but many papers that have evaluated the size of the calibration set have found that there is little to gain from having more records placed in the calibration set after a certain size. Perhaps we could do a bit more of performance tuning but here we instead opt to place 50,000 observations in the randomly picked calibration sets (this will not be too few at least) - the 10-fold CCP would have used 2.2M/10 = 220,000 observations in the calibration sets - thus we at least keep more observations for building a better scoring model to improve the midpoint-predictions. 

Further note that as the data set is rather large, we need to increase the available memory for Java for this to run (thus having to call cpsign using `java -Xmx12g -jar <file>` to add more heap space). Secondly, as we aim to publish this as a new webservice we need to include the two arguments for calculating **percentiles** (last two arguments), which is required for generating prediction images of molecules.


```bash
java -Xmx12g -jar cpsign-2.0.0-rc6-fatjar.jar train \
    --data-set output/precomputed_cleaned.jar \
    --model-out output/trained-model.jar \
    --model-name cpLogD_v2 \
    --logfile output/model-training.log \
    --predictor-type ACP_Regression \
    --ncm LogNormalized:beta=0.1 \
    --sampling-strategy Random:numSamples=10:nCalib=50000 \
    --scorer LinearSVR:C=1:epsilon=0.0001 \
    --time \
    --seed 1701945333231 \
    --percentiles \
    --percentiles-data tsv training_set.csv.gz 
```


### 5. Evaluate the model on unseen data

Finally we use the withheld validation set to evaluate how good the final model is. 

```bash
./cpsign-2.0.0-rc6-fatjar.jar validate \
    --model output/trained-model.jar \
    --predict-file tsv validation_set.csv.gz \
    --calibration-points 0.01:0.99:.01 \
    --print-predictions  \
    --output-format tsv \
    --output output/validation_predictions.csv \
    --result-format csv \
    --result-output output/validation_stats.csv
```

As the `validation_predictions.csv` was more than 200MB (too large for GitHub) we compressed it before saving it. 




