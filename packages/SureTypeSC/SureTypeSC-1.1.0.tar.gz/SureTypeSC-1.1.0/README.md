# SureTypeSC
SureTypeSC is implementation of algorithm for regenotyping of single cell data.

## Getting Started

After unpacking the installation package, run the setup.py script by supplying command below


```
pip setup.py install 
```

### Prerequisites
* buildins
* git-lfs https://git-lfs.github.com/
* python 3 (tested on Python 3.8.5)
* scikit-learn = v0.23.2 (http://scikit-learn.org/stable/)
* numpy >= v1.19.2 (http://www.numpy.org/)
* pandas >= v1.1.2 (https://pandas.pydata.org/)
* IlluminaBeadArrayFiles >= 1.2.0
* json_tricks >= v3.15.3 (https://pypi.org/project/json_tricks/)
* tabulate >= v0.8.7(https://pypi.org/project/tabulate/)
* scipy==1.5.2

### Usage

* create genome studio file (include name,chromosome,position, genotype, gencall score, x raw intensities, x normalized intensities, y raw instensities and y normalized intensities) [format, pandas dataframe]

```
import SureTypeSC as sc

df = sc.basic("HumanKaryomap-12v1_A.bpm","HumanKaryomap-12v1_A.egt","Samplesheetr.csv")


Parameters:The path of manifest file, the path of cluster file, the path of samplesheet file; 
The template of sample sheet is in Samplesheetr.csv
```

* return call rate of all samples over all chromosomes

```
import SureTypeSC.genome_library as gl

call_rate = gl.callrate(df,th=0.01)

call_rate is the data frame that includes the call rate over all the chromosomes

Parameters: df is the pandas data frame from basic function, th is the threshold based on the GenCall score.
```


* return call rate of all samples of one specific chromosome

```
call_rate_chrom = gl.callrate_chr(df,chr_name,th=0.01)

call_rate_chrom is the data frame that includes the call rate of one chromosome

Paramters: df is the pandas data frame from basic function; chr_name is the name of selected chromosome ('X'); th is the threshold based on the GenCall score
```

* return the M and A features of one locus

```
nc, ab, aa, bb = gl.locus_ma(df,locus_name)

nc, ab, aa and bb are pandas data frame with m and a features

Parameters: df is the pandas data frame from basic function; locus_name is the name of one specific locus ('rs3128117')
```

* return the M and A features of one chromsome of one sample

```
AM = gl.sample_ma(df,sample_name,chr_name)

A and M features of one chromsome of one sample

Parameters: df is the pandas data frame from basic function; sample_name is the name of the sample; chr_name is the name one chromosome
```

* return pca components of all samples over all chromosomes

```
pcs = gl.pca_samples(df,th=0.01,n=2)

pca is the pandas data frame that includes the first component and the second component.

Parameters: df is the pandas data frame from basic function; th is the threshold based on the GenCall score; n is the number of components

```

* return pca components of all samples of one specific chromosome

```
pcs_chr = gl.pca_chr(df,chr_name,th=0.01,n=2)

pcs_chr is the data frame that includes the first component and the second component of one chromosome

Parameters: df is the pandas data frame from basic function; chr_name is the name of the selective chromosome; th is the threshold based on the GenCall score; n is the number of components

```



* Index rearrangement (set index levels (including name chromosome and position))
```
dfs = sc.Data.create_from_frame(df)

dfs is Data type
```

* The attribute of Data type

```
dfs.restrict_chromosomes(['1','2']) (The parameters should be a list include the chromosome name)

dfs.apply_NC_threshold_3(0.01,inplace = True) (where 0.01 is the GenCall threshold)
```

* M,A calculation
```
dfs.calculate_transformations_2()
```
* Load classifier
```
from SureTypeSC import loader

clf = loader('clf_30trees_7228_ratio1_lightweight.clf')

clf_2 = loader('clf_GDA_7228_ratio1_58cells.clf') (input should be the path of classifier)
```
* predict

```
result_rf = clf.predict_decorate(dfs,clftype='rf',inn=['m','a'])  (test is the dataset,clftype is the short for classifier like 'rf' or 'gda'. inn is the input feature)

result_gda = clf.predict_decorate(result_rf,clftype='gda',inn=['m','a'])
```

* Train and predict

```
train = sc.Trainer(result_rf,clfname='gda',inner=['m','a'],outer='rf_ratio:1.0_pred')

train.train()

result_end = train.predict_decorate(result_gda,clftype='rf-gda',inn=['m','a'])
```


* save the result
```
result_end.save_complete_table('fulltable.txt',header=False)
```
* save the different modes

```
recall mode: result_end.save_mode('recall','recall.txt',header=False,ratio=1.0)

standard mode: result_end.save_mode('standard','st.txt',header=False,ratio=1.0)

precision mode: result_end.save_mode('precision','precision.txt',header=False,ratio=1.0)

customized saving: result_end.scsave('name.txt', header=True, clftype='rf',threshold=0.15)
```

```
The program enriches every sample in the input data by :

| Subcolumn name  | Meaning |
| ------------- | ------------- |
| rf_ratio:1_pred  | Random Forest prediction (binary)  |
| rf_ratio:1_prob  | Random Forest Score for the positive class |
| gda_ratio:1_prob | Gaussian Discriminant Analysis score for the positive class  | 
| gda_ratio:1_pred | Gaussian Disciminant Analysis prediction (binary) | 
| rf-gda_ratio:1_prob | combined 2-layer RF and GDA - probability score for the positive class | 
| rf-gda_ratio:1_pred | binary prediction of RF-GDA | 
```


<!---## Running the program - validation--->
<!--- Validation procedures are implemented in SureTypeSC.py. To run a validation procedure equivalent to basic configuration, run:--->
<!---```--->
<!---python genotyping/SureTypeSC.py config/GM12878_basic_test.conf--->
<!---```--->


### Contact
In case of any questions please contact Ivan Vogel (ivogel@sund.ku.dk)
