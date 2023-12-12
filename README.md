# cpLogD v2.0

This is a re-take of the cpLogD model previously published in [A confidence predictor for logD using conformal regression and a support-vector machine](https://link.springer.com/article/10.1186/s13321-018-0271-1). The main update will be the version of [CPSign](https://github.com/arosbio/cpsign) which is now open source for non-commercial use, and based on a newer version of [ChEMBL](https://www.ebi.ac.uk/chembl/) (v33, May 2023). **Note: the old cpLogD was based on computed property `acd_logd` which is no longer supplied, and have been replaced by the `CX LogD 7.4` property which we will now use.**

## Steps for generation

### 1. Downloading data from ChEMBL

The latest version of ChEMBL was downloaded from the [download page](https://chembl.gitbook.io/chembl-interface-documentation/downloads), version 33 published in May 2023. The MySQL version was downloaded and loaded in a local MySQL community server following their instructions. 

