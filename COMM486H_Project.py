import pandas_datareader as web

import datetime

import pandas as pd

import numpy as np

from scipy.stats import pearsonr

import matplotlib.pyplot as plt



directory = 'C:\\Users\\CelineZhou\\Desktop\\Assignment_1'

filename = directory + '\\' + 'TSX_Listing-2016_V2.csv'

#Load the csv file with the TSX Tickers

tickers1 = pd.read_csv(filename)

tickers = list(tickers1['YAHOO_TICKER'])

start = datetime.datetime(2015, 1, 1)

end = datetime.datetime(2015, 12, 31)



#Here is an example of the web data reader being used

# Options for web.DataReader function:

"""

input 1: ticker in string form - Ex: OSPTX is for the S&P/TSX

input 2: the source (ex: 'yahoo' or 'google') to download the data from

input 3: start time in datatime.datetime format

input 4: end time in datatime.datetime format

"""

#f2AAPL = web.DataReader('AAPL', 'yahoo', start, end)



#Intiate the dictionnary that will store all the downloaded tick data

d = pd.DataFrame()

#Loop over each tickers to load the data to be stored in the dictionnary d

for tick in tickers:

    try:

        f = web.DataReader(tick, 'yahoo', start, end)

        d[tick] = f['Adj Close']

    except:

        print()

     

#print(f,'complete')

#print(d,'complete')



#Calculate the simple returns and log returns using the stock price

ret = d.pct_change()

lret = np.log(1+ret)

#calculating difference between log returns in T+1 & T day

lret2 = np.log(d) - np.log(d.shift())



#calculate the mean and the standard deviation for both simple returns and log returns

ret_mean=ret.mean()

lret_mean=lret.mean()

#mean of returns

ret_mean=ret.mean()

lret_mean=lret.mean()



#variance of returns

ret_var=ret.var()

lret_var=lret.var()



#standard deviation of returns

ret_std = ret.std()

ret_std2 = pd.DataFrame(ret.std())





#calculate autocorrelation of returns

#skewness

#from scipy.stats import skew

ret_skew=ret.skew()



data=ret.dropna()

autocorr_res = []

acres_ln =[]



# i is column header

for i in ret.columns:

# ret[i] is the whole column in ret table

    data0 = ret[i]

    data = data0.dropna()

    corr, pval=pearsonr(data[:-1], data[1:])

    autocorr_res.append(corr)

    data1 = lret[i]

    data = data1.dropna()

    corr, pval=pearsonr(data[:-1], data[1:])

    acres_ln.append(corr)

   



out1 = pd.DataFrame(ret_mean)

out2 = out1.rename(columns={0: 'mean'})

#join with ret_std2 instead of ret_std, because they need to be dataframes

out3 = out2.join(ret_std2)

out4 = out3.rename(columns={0: 'std'})



#autocorr_res is a list data type

out4['autocorr'] = autocorr_res

#print(out4)



#lret_mean is a timeseries data type, take its values

out4['lmn']=lret_mean.values



out4['lstd']=lret.std().values



out4['lac']=acres_ln



out4['skew'] = ret_skew.values





ss1 = pd.DataFrame(out4.mean())

ss1 = ss1.rename(columns={0: 'summary stat mean'})

ss1['summary stat std'] = out4.std().values



p10 = []

p50 = []

p90 = []

for cc in out4.columns:

    temp1 = out4[cc].values

    temp1.sort()

#take the 6th, 16th and 31st value in the column of out4 after sorting

    p10.append(temp1[5])

    p50.append(temp1[15])

    p90.append(temp1[30])



ss1['p10'] = p10

ss1['p50'] = p50

ss1['p90'] = p90



ss1=ss1.T



#out4.to_csv(directory +  '\\' + 'out4.csv')

#ss1.to_csv(directory +  '\\' + 'ss1.csv')



df=out4

df=df.sample(n=10,axis='rows')



print(df)



fig=plt.errorbar(df.index,df['mean'],yerr=df['std'], fmt='o', color='Black', elinewidth=30,capthick=3,errorevery=3, alpha=0.2, ms=4, capsize = 5)

plt.bar(df.index,df['mean'],tick_label=df.index)              

plt.xlabel('ticker')

plt.ylabel('Average Performance')





#random sample

#import random

#sample=random.sample(d,10)

#sample_data=sample.dropna()

#autocorr_sample=np.corrcoef(sample)







#Assignment 2 (continue from Assignment 1)

#print(out4)



out5 = out3.rename(columns={0: 'std'})

out5['autocorr'] = autocorr_res



ss2 = pd.DataFrame(out5.mean())

ss2 = ss2.rename(columns={0: 'Sample averages'})

ss2['Sample standard deviation'] = out5.std().values



p10 = []

p50 = []

p90 = []

for column in out5.columns:

    temp2 = out5[column].values

    temp2.sort()

#take the 6th, 16th and 31st value in the column of out4 after sorting

    p10.append(temp2[5])

    p50.append(temp2[25])

    p90.append(temp2[45])



ss2['10th percentile'] = p10

ss2['50th percentile'] = p50

ss2['90th percentile'] = p90



out5=out5.T

print(out5)

out6 = out5.join(ss2)

out6=out6.T

print(out6)





SC_sample_filename = directory + '\\' + 'CDN SC sample.csv'

#Load the csv file with the TSX Tickers

SC_sample = pd.read_csv(SC_sample_filename)

SC_tickers = list(SC_sample['YAHOO_TICKER'])

start = datetime.datetime(2015, 1, 1)

end = datetime.datetime(2015, 12, 31)



result = pd.DataFrame()

#Loop over each tickers to load the data to be stored in the dictionnary d

for tick in SC_tickers:

    try:

        s = web.DataReader(tick, 'yahoo', start, end)

        result[tick] = s['Adj Close']

    except:

        print()



print(result)



ret_sc = result.pct_change()

ret_mean_sc=ret_sc.mean()



#variance of returns

ret_var_sc=ret_sc.var()



#standard deviation of returns

ret_std_sc = ret_sc.std()

ret_std2_sc = pd.DataFrame(ret_sc.std())



#calculate autocorrelation of returns

#skewness

#from scipy.stats import skew



data_sc=ret_sc.dropna()

autocorr_res_sc = []

acres_ln_sc =[]





out_sc_1 = pd.DataFrame(ret_mean_sc)

out_sc_2 = out_sc_1.rename(columns={0: 'mean'})

#join with ret_std2 instead of ret_std, because they need to be dataframes

out_sc_3 = out_sc_2.join(ret_std2_sc)

out_sc_4 = out_sc_3.rename(columns={0: 'std'})



ss3 = pd.DataFrame(out_sc_4.mean())

ss3 = ss3.rename(columns={0: 'summary stat mean_sc'})

ss3['summary stat std_sc'] = out_sc_4.std().values



p10_sc = []

p50_sc = []

p90_sc = []

for i in out_sc_4.columns:

    temp_sc = out_sc_4[i].values

    temp_sc.sort()

#take the 6th, 16th and 31st value in the column of out4 after sorting

    p10_sc.append(temp1[2])

    p50_sc.append(temp1[5])

    p90_sc.append(temp1[18])



ss3['p10'] = p10_sc

ss3['p50'] = p50_sc

ss3['p90'] = p90_sc



ss3=ss3.T

print(ss3)





out_sc_4=out_sc_4.T

print(out_sc_4)

out7 = out_sc_4.join(ss2)

out7=out7.T

print(out7)



#out4.to_csv(directory +  '\\' + 'out4.csv')

#ss1.to_csv(directory +  '\\' + 'ss1.csv')
