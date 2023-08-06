import sys
import os
import argparse
import logging
from math import isnan

from numpy import percentile
from scipy.stats import norm
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import math
from IlluminaBeadArrayFiles import LocusAggregate, BeadPoolManifest, GenotypeCalls, ClusterFile, RefStrand

import warnings
warnings.filterwarnings("ignore")

nan = float("nan")

def map_name(data):
    frame  = pd.read_csv(data)
    value = frame.values
    for i in range(value.shape[0]):
        if value[i][0] == 'Sample_ID' :
            start = i+1
    value = np.asarray(value[start:])
    #value = np.asarray(value)
    id_n = list(value[:,0]); bar = value[:,1]; pos = value[:,2]

    #path of the files
    path = list(value[:,3])

    file_a = list(map(lambda x,y:x+'_'+y,bar,pos))
    #map_dict = dictionary = dict(zip(file, id_n))
    
    return id_n,file_a,path

def map_genotype(a):
    if a == 0:
        return 'NC'
    if a == 1:
        return 'AA'
    if a == 2:
        return 'AB'
    if a == 3:
        return 'BB'

# Quality Control

def callrate(df,th=0):
    '''
    callrate function is to calculate the callrate over all the samples 

    Args: 
        df (the pandas dataframe from GenomeStudio or basic function);
        th (the threshold)

    Return:
        Dict: callrate of samples

    '''
    aa = np.asarray(list(df.columns))
    pos = np.where(aa == 'Position')[0][0]
    gtype = aa[pos+1:len(aa):8];score = aa[pos+2:len(aa):8] 
    name = [i[:-6] for i in gtype]
    gtype = df[gtype].values; score = df[score].values
    thresh = np.where(score <= th)
    gtype[thresh] = 'NC'; gtype = pd.DataFrame(gtype)   
    counting = (gtype.apply(pd.value_counts)).values
    call = (np.sum(counting,axis=0)[0] - counting[3])/np.float(np.sum(counting,axis=0)[0])
    
    #name_c = np.concatenate((name,call),axis=1)

    return pd.DataFrame(call,index=name,columns=['Call_rate']) 


def allele_freq(df,th=0):
    '''
    callrate function is to calculate the allele frequency over all the samples 

    Args: 
        df (the pandas dataframe from GenomeStudio or basic function);
        th (the threshold)

    Return:
        pd.dataframe: allele frequency over all the samples 

    '''   

    aa = np.asarray(list(df.columns))
    pos = np.where(aa == 'Position')[0][0]
    gtype = aa[pos+1:len(aa):8];score = aa[pos+2:len(aa):8] 
    name = [i[:-6] for i in gtype]
    gtype = df[gtype].values; score = df[score].values
    thresh = np.where(score <= th)
    gtype[thresh] = 'NC'; gtype = pd.DataFrame(gtype,columns=name)   
    counting = gtype.apply(pd.value_counts)

    return counting



def get_multiind_frame(df):
   df = df.set_index(['Name','Chr','Position','individual'])
   df.index = df.index.set_levels([df.index.levels[0],df.index.levels[1].astype(str),df.index.levels[2].astype(int),df.index.levels[3].astype(str)])
   #f=df.sort_index(axis=0)
   ret=df.unstack(level=-1).swaplevel(0,1,axis=1)
   ret.columns.set_names(['individual', 'feature'], inplace=True)
   return ret

def callrate_chr(df,chr_name,th=0):
    '''
    To calculate the call rate over all the chromosomes over all the samples

    Args:
        df: pandas dataframe from basic function
        chr_name: the name of selected chromosomes
        th: threshold
    Return:
        dict: callrate of samples of one specific chromosome
    '''
    aa = np.asarray(list(df.columns))
    pos = np.where(aa == 'Position')[0][0]
    gtype = aa[pos+1:len(aa):8];score = aa[pos+2:len(aa):8]
    name = [i[:-6] for i in gtype]
    gtype_all_in = ['Chr'] + list(gtype);gtype_all = df[gtype_all_in].values;score = df[score].values  
    thresh = np.where(score <= th);gtype_all[:,1:][thresh] = 'NC'
    gtype_all = pd.DataFrame(gtype_all,columns=list(gtype_all_in))
    a = gtype_all[gtype].groupby(gtype_all['Chr']);b_chr = a.get_group(chr_name)
    cc =np.asarray(b_chr.apply(pd.value_counts));cc[np.where(cc != cc)] = 0
    summ = np.sum(cc[:,0],axis=0); cc_3 = (-cc[3,:] + summ)/np.float(summ)
    
    return pd.DataFrame(cc_3,index=name,columns=['Call_rate'])



def chr_freq(df,chr_name,th=0):
    '''
    To calculate the call rate over all the chromosomes over all the samples

    Args:
        df: pandas dataframe from basic function
        chr_name: the name of selected chromosomes
        th: threshold
    Return:
        pd.Dataframe: frequency of all alleles
    '''
    aa = np.asarray(list(df.columns))
    pos = np.where(aa == 'Position')[0][0]
    gtype = aa[pos+1:len(aa):8];score = aa[pos+2:len(aa):8]
    name = [i[:-6] for i in gtype]
    
    gtype_all_in = ['Chr'] + list(gtype);gtype_all = df[gtype_all_in].values;score = df[score].values  
    thresh = np.where(score <= th);gtype_all[:,1:][thresh] = 'NC'; gtype = name
    name = ['Chr'] + name
    gtype_all = pd.DataFrame(gtype_all,columns=name)
    a = gtype_all[gtype].groupby(gtype_all['Chr']);b_chr = a.get_group(chr_name)
    cc =(b_chr.apply(pd.value_counts))
    return cc

def locus_cluster(df,locus):
    '''
    To do intensity aggregation at a specific locus

    Args:
        df: pandas DataFrame from basic function
        locus_name: the name of locus

    Return:
        dict: the intensity of AA, AB, BB and NC at one locus
    '''
    ex = (((df.ix[df.Name==locus,:]).values)[0])[4:]
    col = df.columns[4:]; nam = col[0:len(col):8]; nam = np.asarray([i[:-8] for i in nam])

    inx = ex[2:len(ex):8]; iny = ex[3:len(ex):8]
    inx = np.reshape(inx,(len(inx),1)); iny = np.reshape(iny,(len(iny),1))
    
    
    
    nc = list(map(int,(np.where(ex == 'NC')[0])/6)); nc_in = np.concatenate((inx[nc],iny[nc]),axis=1)
    ab = list(map(int,(np.where(ex == 'AB')[0])/6)); ab_in = np.concatenate((inx[ab],iny[ab]),axis=1)
    aa = list(map(int,(np.where(ex == 'AA')[0])/6)); aa_in = np.concatenate((inx[aa],iny[aa]),axis=1)
    bb = list(map(int,(np.where(ex == 'BB')[0])/6)); bb_in = np.concatenate((inx[bb],iny[bb]),axis=1)
    
    return pd.DataFrame(nc_in,index=nam[nc],columns=['NC_X','NC_Y']),pd.DataFrame(ab_in,index=nam[ab],columns=['AB_X','AB_Y']),pd.DataFrame(aa_in,index=nam[aa],columns=['AA_X','AA_Y']),pd.DataFrame(bb_in,index=nam[bb],columns=['BB_X','BB_Y'])


def sample_ma(df,sample_name,chr_name):
    '''
    To do intensity aggregation at a specific locus

    Args:
        df: pandas DataFrame from basic function
        sample_name: the name of the sample
        chr_name: the name of the chromosome

    Return:
        pandas data frame of a and m
    '''

    sample = df[['Chr',sample_name+'.GType',sample_name+'.X',sample_name+'.Y']]
    sam_group = (sample.groupby(sample['Chr'])).get_group(chr_name)
    inx = list(sam_group[sample_name+'.X']) ; iny = list(sam_group[sample_name+'.Y'])
    inx = [i + 0.0001 for i in inx] ; iny = [i+0.0001 for i in iny]
    inx = [math.log(i,2) for i in inx]
    iny = [math.log(i,2) for i in iny]
    inx = np.reshape(inx,(len(inx),1)); iny = np.reshape(iny,(len(iny),1))
    
    m = inx - iny; a = 0.5*(inx+iny)
    
    am = np.concatenate((a,m),axis=1)
    
    return pd.DataFrame(am,columns=['A','M'])

def locus_ma(df,locus):
    '''
    To do m and a normalization aggregation at a specific locus

    Args:
        df: pandas DataFrame from basic function
        locus_name: the name of locus

    Return:
        pandas data frame: the m and a features of AA, AB, BB and NC at one locus
    '''
    ex = (((df.ix[df.Name==locus,:]).values)[0])[4:]
    col = df.columns[4:]; nam = col[0:len(col):8]; nam = np.asarray([i[:-6] for i in nam])

    inx = ex[2:len(ex):8]; iny = ex[3:len(ex):8]
    inx = [math.log(i,2) for i in inx] ; iny = [math.log(i,2) for i in iny]
    inx = np.reshape(inx,(len(inx),1)); iny = np.reshape(iny,(len(iny),1))
    
    m = inx - iny; a = 0.5*(inx+iny)
    
    

    nc = list(map(int,(np.where(ex == 'NC')[0])/6)); nc_in = np.concatenate((a[nc],m[nc]),axis=1)
    ab = list(map(int,(np.where(ex == 'AB')[0])/6)); ab_in = np.concatenate((a[ab],m[ab]),axis=1)
    aa = list(map(int,(np.where(ex == 'AA')[0])/6)); aa_in = np.concatenate((a[aa],m[aa]),axis=1)
    bb = list(map(int,(np.where(ex == 'BB')[0])/6)); bb_in = np.concatenate((a[bb],m[bb]),axis=1)
    
    
    return pd.DataFrame(nc_in,index=nam[nc],columns=['NC_A','NC_M']),pd.DataFrame(ab_in,index=nam[ab],columns=['AB_A','AB_M']),pd.DataFrame(aa_in,index=nam[aa],columns=['AA_A','AA_M']),pd.DataFrame(bb_in,index=nam[bb],columns=['BB_A','BB_M'])


def get_df_with_multi_index(df):
    pass 


def pca_samples(df,th=0,n=2):
    '''
    To apply principle component annalysis on frequency dataframe of samples

    Args:
        df: pd.dataframe from basic function
        th: threshold
        n: the number of components after dimensionality reduction
    '''
    sam = allele_freq(df,th); name = sam.columns; sam_v = np.asarray(sam)
    pca_n = PCA(n_components = n); 
    trans_v = pca_n.fit_transform(sam_v.T); ratio = pca_n.explained_variance_ratio_
    
    print('The variance of components:', ratio)

    return  pd.DataFrame(trans_v,index=name,columns=['PC1','PC2'])

def pca_chr(df,chr_name,th=0,n=2):
    '''
    To apply principle component annalysis on frequency dataframe of chromosomes over all samples

    Args:
        df: pd.dataframe from basic function
        chr_name: the selected chromosome
        th: threshold
        n: the number of components after dimensionality reduction
    '''

    sam = chr_freq(df,chr_name,th=0); name = sam.columns; sam_v = np.asarray(sam)
    sam_v[np.where(sam_v != sam_v)] = 0; 
    pca_n = PCA(n_components = n)
    trans_v = pca_n.fit_transform(sam_v.T); ratio = pca_n.explained_variance_ratio_
    
    print('The variance of components:', ratio)

    return pd.DataFrame(trans_v,index=name,columns=['PC1','PC2'])

def k_cluster(df,k=2):
    name = list(df.columns); df = np.asarray(df)
    clf = KMeans(n_clusters=k).fit(df.T)
    labelkmeans = list(clf.labels_)

    return pd.DataFrame(labelkmeans,index=name,columns=['Label'])












class LocusSummary(object):
    def __init__(self, genotype_counts, score_stats,x_raw,y_raw):
        self.genotype_counts = genotype_counts
        self.score_stats = score_stats
        #self.genotype = genotype
        self.x_raw = x_raw
        self.y_raw = y_raw
        #sef.x_norm = x_norm
        #self.y_norm = y_norm

class GenotypeCounts(object):
    """
    Summarize information about genotype counts for diploid genotyping counting
    """

    def __init__(self, genotypes):
        self.no_calls = 0
        self.aa_count = 0
        self.ab_count = 0
        self.bb_count = 0

        for genotype in genotypes:
            if genotype == 0:
                self.no_calls += 1
            elif genotype == 1:
                self.aa_count += 1
            elif genotype == 2:
                self.ab_count += 1
            elif genotype == 3:
                self.bb_count += 1

    def get_num_calls(self):
        """
        Get the number of calls (i.e., not no-calls)

        Returns:
            int: The number of calls
        """
        return self.aa_count + self.ab_count + self.bb_count

    def get_call_frequency(self):
        """
        Get the call rate

        Returns:
            float: The frequency of calls
        """
        num_calls = self.get_num_calls()
        return num_calls / float(num_calls + self.no_calls) if num_calls + self.no_calls > 0 else nan

    def get_aa_frequency(self):
        """
        Frequency of AA genotype (as fraction of all calls)

        Returns:
            float: AA genotype frequency
        """
        return self.aa_count / float(self.get_num_calls()) if self.get_num_calls() > 0 else nan

    def get_ab_frequency(self):
        """
        Frequency of AB genotype (as fraction of all calls)

        Returns:
            float: AB genotype frequency
        """
        return self.ab_count / float(self.get_num_calls()) if self.get_num_calls() > 0 else nan

    def get_bb_frequency(self):
        """
        Frequency of BB genotype (as fraction of all calls)

        Returns:
            float: BB genotype frequency
        """
        return self.bb_count / float(self.get_num_calls()) if self.get_num_calls() > 0 else nan

    def get_minor_frequency(self):
        """
        Comoputes and return the minor allele frequency. If no calls, will be NaN

        Returns:
            float
        """
        a_allele_count = self.aa_count * 2 + self.ab_count
        a_frequency = a_allele_count / \
            float(2 * self.get_num_calls()) if self.get_num_calls() > 0 else nan
        return min(a_frequency, 1.0 - a_frequency) if not isnan(a_frequency) else nan

    def compute_hardy_weinberg(self):
        """
        Computes and returns statistics related to HW equilibrium

        Returns:
            (float, float): Het excess and ChiSq 100 statistics, respectively
        """
        num_calls = self.get_num_calls()
        if num_calls == 0:
            return (0.0, 0.0)

        if self.aa_count + self.ab_count == 0 or self.ab_count + self.bb_count == 0:
            return (1.0, 0.0)

        num_calls = float(num_calls)

        q = self.get_minor_frequency()
        p = 1 - q

        temp = 0.013 / q
        k = temp * temp * temp * temp
        dh = ((self.ab_count / num_calls + k) / (2 * p * q + k)) - 1
        if dh < 0:
            hw = (2 * norm.cdf(dh, 0, 1 / 10.0))
        else:
            hw = (2 * (1 - norm.cdf(dh, 0, 1 / 10.0)))

        return (hw, dh)


class ScoreStatistics(object):
    """
    Capture statistics related to the gencall score distribution

    Attributes:
        gc_10 : 10th percentile of Gencall score distribution
        gc_50 : 50th percentile of Gencall score distribution
    """

    def __init__(self, scores, genotypes):
        """
        Create new ScoreStatistics object

        Args:
            score (list(float)): A list of gencall scores
            genotypes (list(int)): A list of genotypes

        Returns:
            ScoreStatistics
        """
        #called_scores = sorted([score for (score, genotype) in zip(scores, genotypes) if genotype != 0])
        called_scores = sorted([score for (score, genotype) in zip(scores, genotypes)])
        self.gc_10 = ScoreStatistics.percentile(called_scores, 10)
        self.gc_50 = ScoreStatistics.percentile(called_scores, 50)
        self.called_scores = called_scores
        self.scores = scores
        self.genotypes = genotypes

    @staticmethod
    def percentile(scores, percentile):
        """
        Percentile as calculated in GenomeStudio

        Args:
            scores (list(float)): list of scores (typically for called genotypes)
            percentile (int): percentile to calculate
        
        Returns:
            float
        """
        num_scores = len(scores)
        if num_scores == 0:
            return nan

        idx = int(num_scores*percentile/100)
        fractional_index = num_scores*percentile/100.0 - idx
        if fractional_index < 0.5 :
            idx -= 1

        if idx < 0:
            return scores[0]

        if idx >= num_scores - 1:
            return scores[-1]

        x1 = 100 * (idx + 0.5)/float(num_scores)
        x2 = 100 * (idx + 1 + 0.5)/float(num_scores)
        y1 = float(scores[idx])
        y2 = float(scores[idx+1])

        return y1 + (y2 - y1) / (x2 - x1) * (percentile - x1)




def summarize_locus(locus_aggregate):
    """
    Generate a locus summary based on aggregated locus information

    Args:
        LocusAggregate : Aggregated information for a locus
    
    Returns
        LocusSummary
    """
    genotype_counts = GenotypeCounts(locus_aggregate.genotypes)
    score_stats = ScoreStatistics(locus_aggregate.scores, locus_aggregate.genotypes)
    return LocusSummary(genotype_counts, score_stats)

def basic_locus(locus_aggregate):
    """
    Generate a locus summary based on aggregated locus information

    Args:
        LocusAggregate : Aggregated information for a locus
    
    Returns
        LocusSummary
    """
    genotype_counts = GenotypeCounts(locus_aggregate.genotypes)
    score_stats = ScoreStatistics(locus_aggregate.scores, locus_aggregate.genotypes)
    #genotype = locus_aggregate.genotypes
    #score_stats = locus_aggregate.scores
    x_raw = locus_aggregate.x_intensities
    y_raw = locus_aggregate.y_intensities
    norm = locus_aggregate.transforms
    #print(x_raw[:20])
    #print(type(norm))
    #print(len(norm))
    #print(norm[:10])
    #(x_norm,y_norm) = 
    
    return LocusSummary(genotype_counts, score_stats,x_raw,y_raw)


def get_logger():
    # set up log file
    # create logger
    logger = logging.getLogger('Locus Summary Report')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger



def basic(manifest_filename, cluster_filename, samplesheet):
    #print "Reading cluster file" 
    #with open(cluster_filename, "rb") as cluster_handle:
        #egt = ClusterFile.read_cluster_file(cluster_handle)

    print('Reading sample file') 

    try:
        map_name(samplesheet)
    except:
        
        raise NameError( "'Check the format of samplesheet. There should be 'Sample_ID' index' The template format is https://github.com/Meiomap/SureTypeSC_2/blob/master/Samplesheetr.csv '.")
        


    id_n,code,paths = map_name(samplesheet)

    print('Number of samples:',len(id_n))

    #cate = []

    #for i in range(len(id_n)):
    #    cate.append(id_n[i]+'.GType')
    #    cate.append(id_n[i]+'.Score')
    #    cate.append(id_n[i]+'.X')
    #    cate.append(id_n[i]+'.Y')
    #    cate.append(id_n[i]+'.X Raw')
    #    cate.append(id_n[i]+'.Y Raw')
    #    cate.append(id_n[i]+'.Log R Ratio')
    #    cate.append(id_n[i]+'.B Allele Freq')
    


    print("Reading manifest file") 
    bpm = BeadPoolManifest(manifest_filename)
    samples = []

    print("Initializing genotype data") 

    count = 0
    gtc_files = []
    for gtc_file in code:
        gtc_file = gtc_file + '.gtc'
        gtc_files.append(os.path.join(paths[count], gtc_file))
        count +=1

    try:
        samples = list(map(GenotypeCalls, gtc_files))

    except:
        #print "'The GTC files doesn't exist according to the file paths. Check your file paths in samplesheet.'"
        raise NameError("'The GTC files doesn't exist according to the file paths. Check your file paths in samplesheet.'")


    #set flag indicating logr in the data
    
    try:
        samples[0].get_logr_ratios()
        flag_logr=True
    except:
        flag_logr=False
  
    cate = []

    for i in range(len(id_n)):
        cate.append(id_n[i]+'.GType')
        cate.append(id_n[i]+'.Score')
        cate.append(id_n[i]+'.X')
        cate.append(id_n[i]+'.Y')
        cate.append(id_n[i]+'.X Raw')
        cate.append(id_n[i]+'.Y Raw')
        if flag_logr:
            cate.append(id_n[i]+'.Log R Ratio')
            cate.append(id_n[i]+'.B Allele Freq')

    print("Generating") 


    title = ["Name","Chr","Position"]

    locus_name = bpm.names

    #address = bpm.addresses

    chroms = bpm.chroms

    position = bpm.map_infos

    map_dict  = dict(list(zip(title, [locus_name,chroms,position])))

    df = pd.DataFrame(map_dict)

    #test_count =0

    for j in range(len(samples)):
        print(code[j])
        sam = samples[j]
        
        if flag_logr:
            i = 8*j
        else:
            i = 6*j
        gene = sam.get_genotypes()
        gene = list(map(map_genotype,gene))

        try:
            df[cate[i]] = gene
        except:
            raise ValueError("The manifest file doesn't corresponds to the sample, please change the manifest file")


        scores = sam.get_genotype_scores()
        df[cate[i+1]] = scores

        norm = sam.get_normalized_intensities(bpm.normalization_lookups)
        norm = np.asarray(norm)
        x_norm = list(norm[:,0])
        y_norm = list(norm[:,1])
        df[cate[i+2]] = x_norm
        df[cate[i+3]] = y_norm

        x_raw = sam.get_raw_x_intensities()
        df[cate[i+4]] = x_raw
        y_raw = sam.get_raw_y_intensities()
        df[cate[i+5]] = y_raw

        if flag_logr:
            df[cate[i+6]]=sam.get_logr_ratios()
            df[cate[i+7]]=sam.get_ballele_freqs()  

        #test_count +=1

        #if test_count >=2:
            #break




    
    print("Finish parsing")
    #df.to_csv(output_filename, sep=delim,encoding='utf-8')

    return df








def statistic(manifest_filename, cluster_filename, samplesheet):
    print("Reading cluster file") 
    with open(cluster_filename, "rb") as cluster_handle:
        egt = ClusterFile.read_cluster_file(cluster_handle)

    print("Reading manifest file")
    bpm = BeadPoolManifest(manifest_filename)
    samples = []

    print('Reading sample file') 

    try:
        map_name(samplesheet)
    except:
        
        raise NameError( "'Check the format of samplesheet. There should be 'Sample_ID' index' The template format is https://github.com/Meiomap/SureTypeSC_2/blob/master/Samplesheetr.csv '.")
        

    #print "Initializing genotype data"

    id_n,code,paths = map_name(samplesheet)

    print('Number of samples:',len(id_n))

    count = 0
    gtc_files = []
    for gtc_file in code:
        gtc_file = gtc_file + '.gtc'
        gtc_files.append(os.path.join(paths[count], gtc_file))
        count +=1

    try:
        samples = list(map(GenotypeCalls, gtc_files))

    except:
        #print "'The GTC files doesn't exist according to the file paths. Check your file paths in samplesheet.'"
        raise NameError("'The GTC files doesn't exist according to the file paths. Check your file paths in samplesheet.'")

    print("Generating") 
 

    samples = list(map(GenotypeCalls, gtc_files))

    #logger.info("Generating report")
    loci = list(range(len(bpm.normalization_lookups)))
    print('length of loci',len(loci))

    title = 'Chr,Row,Locus_Name,Illumicode_Name,#No_Calls,#Calls,Call_Freq,A/A_Freq,A/B_Freq,B/B_Freq,Minor_Freq,Gentrain_Score,50%_GC_Score,10%_GC_Score,Het_Excess_Freq,ChiTest_P100,Cluster_Sep,AA_T_Mean,AA_T_Std,AB_T_Mean,AB_T_Std,BB_T_Mean,BB_T_Std,AA_R_Mean,AA_R_Std,AB_R_Mean,AB_R_Std,BB_R_Mean,BB_R_Std,Plus/Minus Strand'
    
    title = title.split(',')

    df = pd.DataFrame(columns = title)
    #print LocusAggregate.aggregate_samples(samples, loci, basic_locus, bpm.normalization_lookups)

    #print (LocusAggregate.aggregate_samples(samples, loci, basic_locus, bpm.normalization_lookups)).genotype_counts.get_num_calls()

        #output_handle.write(delim.join("Row,Locus_Name,Illumicode_Name,#No_Calls,#Calls,Call_Freq,A/A_Freq,A/B_Freq,B/B_Freq,Minor_Freq,Gentrain_Score,50%_GC_Score,10%_GC_Score,Het_Excess_Freq,ChiTest_P100,Cluster_Sep,AA_T_Mean,AA_T_Std,AB_T_Mean,AB_T_Std,BB_T_Mean,BB_T_Std,AA_R_Mean,AA_R_Std,AB_R_Mean,AB_R_Std,BB_R_Mean,BB_R_Std,Plus/Minus Strand".split(",")) + "\n")
    for (locus, locus_summary) in zip(loci, LocusAggregate.aggregate_samples(samples, loci, basic_locus, bpm.normalization_lookups)):
        locus_name = bpm.names[locus]
        cluster_record = egt.get_record(locus_name)
        row_data = []
        row_data.append(bpm.chroms)
        row_data.append(locus + 1)
        row_data.append(locus_name)
        row_data.append(cluster_record.address)
        row_data.append(locus_summary.genotype_counts.no_calls)
        row_data.append(locus_summary.genotype_counts.get_num_calls())
        row_data.append(locus_summary.genotype_counts.get_call_frequency())
        row_data.append(locus_summary.genotype_counts.get_aa_frequency())
        row_data.append(locus_summary.genotype_counts.get_ab_frequency())
        row_data.append(locus_summary.genotype_counts.get_bb_frequency())
        row_data.append(
            locus_summary.genotype_counts.get_minor_frequency())
        row_data.append(cluster_record.cluster_score.total_score)
        row_data.append(locus_summary.score_stats.gc_50)
        row_data.append(locus_summary.score_stats.gc_10)

        (hw_equilibrium, het_excess) = locus_summary.genotype_counts.compute_hardy_weinberg()
        row_data.append(het_excess)
        row_data.append(hw_equilibrium)

        row_data.append(cluster_record.cluster_score.cluster_separation)

        for cluster_stats in (cluster_record.aa_cluster_stats, cluster_record.ab_cluster_stats, cluster_record.bb_cluster_stats):
            row_data.append(cluster_stats.theta_mean)
            row_data.append(cluster_stats.theta_dev)

        for cluster_stats in (cluster_record.aa_cluster_stats, cluster_record.ab_cluster_stats, cluster_record.bb_cluster_stats):
            row_data.append(cluster_stats.r_mean)
            row_data.append(cluster_stats.r_dev)

        if len(bpm.ref_strands) > 0:
            row_data.append(RefStrand.to_string(bpm.ref_strands[locus]))
        else:
            row_data.append("U")

        df.loc[locus] = row_data


        #print locus
    df.to_csv(output_filename, delim, encoding='utf-8')
    return df

            #output_handle.write(delim.join(map(str, row_data)) + "\n")
        #print "Report generation complete"






