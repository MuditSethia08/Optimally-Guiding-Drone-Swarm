# %%
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

# %%
# Data Preprocessing

data = open("Team 13.txt", "r")
lines = data.readlines()

features = lines[0].split()

data = lines[1:]
data = [x.split() for x in data]
data = np.array(data)

df = pd.DataFrame(data, columns=features)
df = df.drop(columns=[features[0]])

for x in range (3, len(features)):
    df[features[x]] = pd.to_numeric(df[features[x]])

data = df

# %%
# Declaration of Categorical variables

data['x2'] = data['x2'].astype('category')
data['x1']=data['x1'].astype('category')
data['x15']=data['x15'].astype('category')

# %%
# Applying transformations

data_prime = data
data_prime['x4_log'] = np.log(data_prime['x4'])
data_prime['x7_log'] = np.log(data_prime['x7'])
data_prime['x8_log'] = np.log(data_prime['x8'])
data_prime['x14_log'] = np.log(data_prime['x14'])
data_prime['x11_log'] = np.log(data_prime['x11'])
data_prime['x13_log'] = np.log(data_prime['x13'])
data_prime['x9_log'] = np.log(data_prime['x9'])
data_prime['log_y'] = np.log(data_prime['y'])

# %%
# Visual plots

# for column in data_prime.columns:
#   if column!='log_y':  #log_y is basically log of log
#     plt.scatter(data_prime[column],data_prime['log_y'],label=column)
#   plt.xlabel(column)
#   plt.ylabel('Value')
#   plt.title('y vs columns')
#   plt.legend()
#   plt.show()

# %%
#######################
## Log transformed independent variables log_x4, log_x7, log_x8, log_x14 were found to have strong correlation with log_y
## Variables such as x2, x15 provide data about location state of property, number of rooms respectively
#######################

# %%
# Observed Correlation of variables with independent variable and each other dependent variable(s)

# data_prime.describe()
data_prime.corr()

# %%
'''
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x3</th>
      <th>x4</th>
      <th>x5</th>
      <th>x6</th>
      <th>x7</th>
      <th>x8</th>
      <th>y</th>
      <th>x9</th>
      <th>x10</th>
      <th>x11</th>
      <th>...</th>
      <th>x13</th>
      <th>x14</th>
      <th>x4_log</th>
      <th>x7_log</th>
      <th>x8_log</th>
      <th>x14_log</th>
      <th>x11_log</th>
      <th>x13_log</th>
      <th>x9_log</th>
      <th>log_y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>x3</th>
      <td>1.000000</td>
      <td>0.173083</td>
      <td>-0.054878</td>
      <td>0.005771</td>
      <td>0.078075</td>
      <td>0.073047</td>
      <td>0.129475</td>
      <td>-0.098598</td>
      <td>-0.137238</td>
      <td>0.171343</td>
      <td>...</td>
      <td>-0.187715</td>
      <td>0.127074</td>
      <td>0.133045</td>
      <td>0.044722</td>
      <td>0.046961</td>
      <td>0.071714</td>
      <td>0.190111</td>
      <td>-0.197271</td>
      <td>-0.101559</td>
      <td>0.135368</td>
    </tr>
    <tr>
      <th>x4</th>
      <td>0.173083</td>
      <td>1.000000</td>
      <td>0.078372</td>
      <td>-0.029037</td>
      <td>0.940249</td>
      <td>0.923738</td>
      <td>0.886332</td>
      <td>-0.017427</td>
      <td>0.146814</td>
      <td>0.038020</td>
      <td>...</td>
      <td>0.235610</td>
      <td>0.986748</td>
      <td>0.758527</td>
      <td>0.647758</td>
      <td>0.625809</td>
      <td>0.724419</td>
      <td>0.039035</td>
      <td>0.245568</td>
      <td>-0.014871</td>
      <td>0.667133</td>
    </tr>
    <tr>
      <th>x5</th>
      <td>-0.054878</td>
      <td>0.078372</td>
      <td>1.000000</td>
      <td>-0.616310</td>
      <td>0.119699</td>
      <td>0.074532</td>
      <td>0.089941</td>
      <td>0.250584</td>
      <td>0.456097</td>
      <td>0.033976</td>
      <td>...</td>
      <td>-0.031648</td>
      <td>0.071162</td>
      <td>0.078820</td>
      <td>0.162904</td>
      <td>0.054107</td>
      <td>0.061295</td>
      <td>0.052296</td>
      <td>-0.035190</td>
      <td>0.241805</td>
      <td>0.145453</td>
    </tr>
    <tr>
      <th>x6</th>
      <td>0.005771</td>
      <td>-0.029037</td>
      <td>-0.616310</td>
      <td>1.000000</td>
      <td>-0.003129</td>
      <td>0.053278</td>
      <td>-0.035290</td>
      <td>-0.268252</td>
      <td>-0.339229</td>
      <td>0.006578</td>
      <td>...</td>
      <td>0.018591</td>
      <td>-0.022733</td>
      <td>-0.013788</td>
      <td>0.031185</td>
      <td>0.171437</td>
      <td>-0.006856</td>
      <td>0.079886</td>
      <td>0.022940</td>
      <td>-0.243101</td>
      <td>-0.043837</td>
    </tr>
    <tr>
      <th>x7</th>
      <td>0.078075</td>
      <td>0.940249</td>
      <td>0.119699</td>
      <td>-0.003129</td>
      <td>1.000000</td>
      <td>0.950464</td>
      <td>0.820459</td>
      <td>-0.004248</td>
      <td>0.236765</td>
      <td>0.064136</td>
      <td>...</td>
      <td>0.316135</td>
      <td>0.948111</td>
      <td>0.741266</td>
      <td>0.735566</td>
      <td>0.688278</td>
      <td>0.726111</td>
      <td>0.057260</td>
      <td>0.318911</td>
      <td>-0.002399</td>
      <td>0.665181</td>
    </tr>
    <tr>
      <th>x8</th>
      <td>0.073047</td>
      <td>0.923738</td>
      <td>0.074532</td>
      <td>0.053278</td>
      <td>0.950464</td>
      <td>1.000000</td>
      <td>0.856850</td>
      <td>-0.111916</td>
      <td>0.100427</td>
      <td>0.172794</td>
      <td>...</td>
      <td>0.194808</td>
      <td>0.902062</td>
      <td>0.736781</td>
      <td>0.709405</td>
      <td>0.748967</td>
      <td>0.697535</td>
      <td>0.184226</td>
      <td>0.211971</td>
      <td>-0.103822</td>
      <td>0.691413</td>
    </tr>
    <tr>
      <th>y</th>
      <td>0.129475</td>
      <td>0.886332</td>
      <td>0.089941</td>
      <td>-0.035290</td>
      <td>0.820459</td>
      <td>0.856850</td>
      <td>1.000000</td>
      <td>-0.106328</td>
      <td>0.077077</td>
      <td>0.164406</td>
      <td>...</td>
      <td>0.117539</td>
      <td>0.843098</td>
      <td>0.664575</td>
      <td>0.570489</td>
      <td>0.579491</td>
      <td>0.615524</td>
      <td>0.164699</td>
      <td>0.131922</td>
      <td>-0.103740</td>
      <td>0.663201</td>
    </tr>
    <tr>
      <th>x9</th>
      <td>-0.098598</td>
      <td>-0.017427</td>
      <td>0.250584</td>
      <td>-0.268252</td>
      <td>-0.004248</td>
      <td>-0.111916</td>
      <td>-0.106328</td>
      <td>1.000000</td>
      <td>0.707787</td>
      <td>-0.691750</td>
      <td>...</td>
      <td>0.522996</td>
      <td>0.043356</td>
      <td>0.088644</td>
      <td>0.154379</td>
      <td>-0.076056</td>
      <td>0.205410</td>
      <td>-0.658752</td>
      <td>0.553025</td>
      <td>0.995772</td>
      <td>-0.018669</td>
    </tr>
    <tr>
      <th>x10</th>
      <td>-0.137238</td>
      <td>0.146814</td>
      <td>0.456097</td>
      <td>-0.339229</td>
      <td>0.236765</td>
      <td>0.100427</td>
      <td>0.077077</td>
      <td>0.707787</td>
      <td>1.000000</td>
      <td>-0.408424</td>
      <td>...</td>
      <td>0.695362</td>
      <td>0.222230</td>
      <td>0.293387</td>
      <td>0.450137</td>
      <td>0.166693</td>
      <td>0.414220</td>
      <td>-0.487053</td>
      <td>0.676943</td>
      <td>0.680731</td>
      <td>0.242304</td>
    </tr>
    <tr>
      <th>x11</th>
      <td>0.171343</td>
      <td>0.038020</td>
      <td>0.033976</td>
      <td>0.006578</td>
      <td>0.064136</td>
      <td>0.172794</td>
      <td>0.164406</td>
      <td>-0.691750</td>
      <td>-0.408424</td>
      <td>1.000000</td>
      <td>...</td>
      <td>-0.601725</td>
      <td>-0.038739</td>
      <td>-0.015075</td>
      <td>0.012309</td>
      <td>0.198764</td>
      <td>-0.163278</td>
      <td>0.927048</td>
      <td>-0.651354</td>
      <td>-0.705586</td>
      <td>0.185965</td>
    </tr>
    <tr>
      <th>x12</th>
      <td>0.199209</td>
      <td>0.005352</td>
      <td>-0.278527</td>
      <td>0.236309</td>
      <td>-0.050516</td>
      <td>0.007524</td>
      <td>0.043557</td>
      <td>-0.593596</td>
      <td>-0.540907</td>
      <td>0.436947</td>
      <td>...</td>
      <td>-0.322144</td>
      <td>-0.033876</td>
      <td>-0.040605</td>
      <td>-0.172929</td>
      <td>-0.030988</td>
      <td>-0.116490</td>
      <td>0.397657</td>
      <td>-0.350556</td>
      <td>-0.599628</td>
      <td>-0.021548</td>
    </tr>
    <tr>
      <th>x13</th>
      <td>-0.187715</td>
      <td>0.235610</td>
      <td>-0.031648</td>
      <td>0.018591</td>
      <td>0.316135</td>
      <td>0.194808</td>
      <td>0.117539</td>
      <td>0.522996</td>
      <td>0.695362</td>
      <td>-0.601725</td>
      <td>...</td>
      <td>1.000000</td>
      <td>0.347682</td>
      <td>0.410979</td>
      <td>0.499214</td>
      <td>0.275755</td>
      <td>0.588669</td>
      <td>-0.686687</td>
      <td>0.984866</td>
      <td>0.516107</td>
      <td>0.268994</td>
    </tr>
    <tr>
      <th>x14</th>
      <td>0.127074</td>
      <td>0.986748</td>
      <td>0.071162</td>
      <td>-0.022733</td>
      <td>0.948111</td>
      <td>0.902062</td>
      <td>0.843098</td>
      <td>0.043356</td>
      <td>0.222230</td>
      <td>-0.038739</td>
      <td>...</td>
      <td>0.347682</td>
      <td>1.000000</td>
      <td>0.761546</td>
      <td>0.666228</td>
      <td>0.617947</td>
      <td>0.751007</td>
      <td>-0.048017</td>
      <td>0.349476</td>
      <td>0.044895</td>
      <td>0.651063</td>
    </tr>
    <tr>
      <th>x4_log</th>
      <td>0.133045</td>
      <td>0.758527</td>
      <td>0.078820</td>
      <td>-0.013788</td>
      <td>0.741266</td>
      <td>0.736781</td>
      <td>0.664575</td>
      <td>0.088644</td>
      <td>0.293387</td>
      <td>-0.015075</td>
      <td>...</td>
      <td>0.410979</td>
      <td>0.761546</td>
      <td>1.000000</td>
      <td>0.898097</td>
      <td>0.837323</td>
      <td>0.977994</td>
      <td>-0.034418</td>
      <td>0.423437</td>
      <td>0.086916</td>
      <td>0.901710</td>
    </tr>
    <tr>
      <th>x7_log</th>
      <td>0.044722</td>
      <td>0.647758</td>
      <td>0.162904</td>
      <td>0.031185</td>
      <td>0.735566</td>
      <td>0.709405</td>
      <td>0.570489</td>
      <td>0.154379</td>
      <td>0.450137</td>
      <td>0.012309</td>
      <td>...</td>
      <td>0.499214</td>
      <td>0.666228</td>
      <td>0.898097</td>
      <td>1.000000</td>
      <td>0.899649</td>
      <td>0.908456</td>
      <td>-0.001294</td>
      <td>0.511075</td>
      <td>0.155499</td>
      <td>0.852842</td>
    </tr>
    <tr>
      <th>x8_log</th>
      <td>0.046961</td>
      <td>0.625809</td>
      <td>0.054107</td>
      <td>0.171437</td>
      <td>0.688278</td>
      <td>0.748967</td>
      <td>0.579491</td>
      <td>-0.076056</td>
      <td>0.166693</td>
      <td>0.198764</td>
      <td>...</td>
      <td>0.275755</td>
      <td>0.617947</td>
      <td>0.837323</td>
      <td>0.899649</td>
      <td>1.000000</td>
      <td>0.805635</td>
      <td>0.225361</td>
      <td>0.296963</td>
      <td>-0.063721</td>
      <td>0.827195</td>
    </tr>
    <tr>
      <th>x14_log</th>
      <td>0.071714</td>
      <td>0.724419</td>
      <td>0.061295</td>
      <td>-0.006856</td>
      <td>0.726111</td>
      <td>0.697535</td>
      <td>0.615524</td>
      <td>0.205410</td>
      <td>0.414220</td>
      <td>-0.163278</td>
      <td>...</td>
      <td>0.588669</td>
      <td>0.751007</td>
      <td>0.977994</td>
      <td>0.908456</td>
      <td>0.805635</td>
      <td>1.000000</td>
      <td>-0.191623</td>
      <td>0.603124</td>
      <td>0.204055</td>
      <td>0.858859</td>
    </tr>
    <tr>
      <th>x11_log</th>
      <td>0.190111</td>
      <td>0.039035</td>
      <td>0.052296</td>
      <td>0.079886</td>
      <td>0.057260</td>
      <td>0.184226</td>
      <td>0.164699</td>
      <td>-0.658752</td>
      <td>-0.487053</td>
      <td>0.927048</td>
      <td>...</td>
      <td>-0.686687</td>
      <td>-0.048017</td>
      <td>-0.034418</td>
      <td>-0.001294</td>
      <td>0.225361</td>
      <td>-0.191623</td>
      <td>1.000000</td>
      <td>-0.700476</td>
      <td>-0.649452</td>
      <td>0.184364</td>
    </tr>
    <tr>
      <th>x13_log</th>
      <td>-0.197271</td>
      <td>0.245568</td>
      <td>-0.035190</td>
      <td>0.022940</td>
      <td>0.318911</td>
      <td>0.211971</td>
      <td>0.131922</td>
      <td>0.553025</td>
      <td>0.676943</td>
      <td>-0.651354</td>
      <td>...</td>
      <td>0.984866</td>
      <td>0.349476</td>
      <td>0.423437</td>
      <td>0.511075</td>
      <td>0.296963</td>
      <td>0.603124</td>
      <td>-0.700476</td>
      <td>1.000000</td>
      <td>0.553741</td>
      <td>0.281918</td>
    </tr>
    <tr>
      <th>x9_log</th>
      <td>-0.101559</td>
      <td>-0.014871</td>
      <td>0.241805</td>
      <td>-0.243101</td>
      <td>-0.002399</td>
      <td>-0.103822</td>
      <td>-0.103740</td>
      <td>0.995772</td>
      <td>0.680731</td>
      <td>-0.705586</td>
      <td>...</td>
      <td>0.516107</td>
      <td>0.044895</td>
      <td>0.086916</td>
      <td>0.155499</td>
      <td>-0.063721</td>
      <td>0.204055</td>
      <td>-0.649452</td>
      <td>0.553741</td>
      <td>1.000000</td>
      <td>-0.020369</td>
    </tr>
    <tr>
      <th>log_y</th>
      <td>0.135368</td>
      <td>0.667133</td>
      <td>0.145453</td>
      <td>-0.043837</td>
      <td>0.665181</td>
      <td>0.691413</td>
      <td>0.663201</td>
      <td>-0.018669</td>
      <td>0.242304</td>
      <td>0.185965</td>
      <td>...</td>
      <td>0.268994</td>
      <td>0.651063</td>
      <td>0.901710</td>
      <td>0.852842</td>
      <td>0.827195</td>
      <td>0.858859</td>
      <td>0.184364</td>
      <td>0.281918</td>
      <td>-0.020369</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
<p>21 rows × 21 columns</p>
</div>
'''

# %%
# Importing necessary modules

import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.model_selection import train_test_split

# %%
# Test without categorical variables

data_model=data_prime
data_model.dropna(inplace=True)
# X=data_model[['x15','x4_log','x5','x7_log','x14_log0','x7']]
X = data_model[['x4_log', 'x7_log', 'x8_log', 'x14_log']]
y=data_model['log_y']

X=sm.add_constant(X)

# Perform the multiple linear regression
model = sm.OLS(y, X).fit()

# Print out the statistics
print(model.summary())

# %%
'''

                            OLS Regression Results                            
==============================================================================
Dep. Variable:                  log_y   R-squared:                       0.846
Model:                            OLS   Adj. R-squared:                  0.845
Method:                 Least Squares   F-statistic:                     598.6
Date:                Wed, 01 May 2024   Prob (F-statistic):          2.48e-175
Time:                        02:50:18   Log-Likelihood:                -246.62
No. Observations:                 440   AIC:                             503.2
Df Residuals:                     435   BIC:                             523.7
Df Model:                           4                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const         -7.2778      0.738     -9.864      0.000      -8.728      -5.828
x4_log         1.7415      0.139     12.567      0.000       1.469       2.014
x7_log         0.2576      0.060      4.326      0.000       0.141       0.375
x8_log         0.0821      0.052      1.581      0.115      -0.020       0.184
x14_log       -0.8364      0.127     -6.579      0.000      -1.086      -0.587
==============================================================================
Omnibus:                      103.122   Durbin-Watson:                   2.007
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              281.675
Skew:                          -1.122   Prob(JB):                     6.84e-62
Kurtosis:                       6.214   Cond. No.                         659.
==============================================================================

Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

'''

# %%
# Introduced Categorical variable x15

data_model=data_prime
data_model.dropna(inplace=True)

model_cat15 = ols('log_y ~ C(x15) + x4_log + x7_log + x8_log + x14_log', data = data_prime).fit()
model_cat15.summary()

# %%
'''

OLS Regression Results
Dep. Variable:	log_y	R-squared:	0.890
Model:	OLS	Adj. R-squared:	0.889
Method:	Least Squares	F-statistic:	501.5
Date:	Wed, 01 May 2024	Prob (F-statistic):	6.03e-203
Time:	02:51:51	Log-Likelihood:	-172.12
No. Observations:	440	AIC:	360.2
Df Residuals:	432	BIC:	392.9
Df Model:	7		
Covariance Type:	nonrobust		
coef	std err	t	P>|t|	[0.025	0.975]
Intercept	-5.3670	0.657	-8.171	0.000	-6.658	-4.076
C(x15)[T.2]	0.2500	0.051	4.919	0.000	0.150	0.350
C(x15)[T.3]	0.6154	0.049	12.634	0.000	0.520	0.711
C(x15)[T.4]	0.5131	0.059	8.715	0.000	0.397	0.629
x4_log	1.1803	0.128	9.249	0.000	0.929	1.431
x7_log	0.1116	0.053	2.102	0.036	0.007	0.216
x8_log	0.2117	0.048	4.412	0.000	0.117	0.306
x14_log	-0.2750	0.117	-2.347	0.019	-0.505	-0.045
Omnibus:	111.185	Durbin-Watson:	1.998
Prob(Omnibus):	0.000	Jarque-Bera (JB):	544.691
Skew:	-1.000	Prob(JB):	5.27e-119
Kurtosis:	8.070	Cond. No.	694.


Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.

'''

# %%
# Further introducing x2 as a categorical variable

data_model=data_prime
data_model.dropna(inplace=True)

full_model = ols('log_y ~ C(x15) + C(x2) + x4_log + x7_log + x8_log + x14_log', data = data_prime).fit()
full_model.summary()

# %%
'''

OLS Regression Results
Dep. Variable:	log_y	R-squared:	0.917
Model:	OLS	Adj. R-squared:	0.906
Method:	Least Squares	F-statistic:	84.29
Date:	Wed, 01 May 2024	Prob (F-statistic):	2.55e-179
Time:	02:54:59	Log-Likelihood:	-110.44
No. Observations:	440	AIC:	324.9
Df Residuals:	388	BIC:	537.4
Df Model:	51		
Covariance Type:	nonrobust		
coef	std err	t	P>|t|	[0.025	0.975]
Intercept	-5.2403	0.609	-8.602	0.000	-6.438	-4.042
C(x15)[T.2]	-0.2926	0.073	-3.990	0.000	-0.437	-0.148
C(x15)[T.3]	-0.1804	0.136	-1.330	0.184	-0.447	0.086
C(x15)[T.4]	-0.0827	0.087	-0.946	0.345	-0.255	0.089
C(x2)[T.AR]	0.2073	0.266	0.779	0.436	-0.316	0.730
C(x2)[T.AZ]	-0.0157	0.149	-0.105	0.916	-0.310	0.278
C(x2)[T.CA]	-0.0218	0.078	-0.278	0.781	-0.176	0.132
C(x2)[T.CO]	0.1751	0.116	1.509	0.132	-0.053	0.403
C(x2)[T.CT]	-0.6244	0.124	-5.047	0.000	-0.868	-0.381
C(x2)[T.DC]	0.2752	0.356	0.772	0.441	-0.426	0.976
C(x2)[T.DE]	0.0136	0.227	0.060	0.952	-0.433	0.461
C(x2)[T.FL]	0.1954	0.140	1.395	0.164	-0.080	0.471
C(x2)[T.GA]	0.3629	0.168	2.165	0.031	0.033	0.693
C(x2)[T.HI]	0.1920	0.184	1.045	0.297	-0.169	0.553
C(x2)[T.ID]	-0.1108	0.308	-0.360	0.719	-0.716	0.494
C(x2)[T.IL]	0.0095	0.090	0.106	0.916	-0.168	0.187
C(x2)[T.IN]	-0.2397	0.095	-2.521	0.012	-0.427	-0.053
C(x2)[T.KS]	0.4096	0.160	2.565	0.011	0.096	0.723
C(x2)[T.KY]	-0.1649	0.229	-0.719	0.472	-0.616	0.286
C(x2)[T.LA]	0.0402	0.167	0.240	0.810	-0.289	0.369
C(x2)[T.MA]	-0.7337	0.114	-6.456	0.000	-0.957	-0.510
C(x2)[T.MD]	0.1459	0.171	0.854	0.394	-0.190	0.482
C(x2)[T.ME]	-0.4259	0.150	-2.838	0.005	-0.721	-0.131
C(x2)[T.MI]	0.2352	0.088	2.664	0.008	0.062	0.409
C(x2)[T.MN]	-0.0674	0.125	-0.537	0.591	-0.314	0.179
C(x2)[T.MO]	0.0825	0.119	0.695	0.488	-0.151	0.316
C(x2)[T.MS]	-0.0325	0.230	-0.141	0.888	-0.484	0.419
C(x2)[T.MT]	-0.4993	0.309	-1.617	0.107	-1.106	0.108
C(x2)[T.NC]	0.1753	0.149	1.177	0.240	-0.118	0.468
C(x2)[T.ND]	-0.4284	0.308	-1.391	0.165	-1.034	0.177
C(x2)[T.NE]	0.1106	0.182	0.608	0.543	-0.247	0.468
C(x2)[T.NH]	-0.4779	0.164	-2.917	0.004	-0.800	-0.156
C(x2)[T.NJ]	-0.2702	0.093	-2.915	0.004	-0.452	-0.088
C(x2)[T.NM]	0.1802	0.223	0.806	0.421	-0.259	0.620
C(x2)[T.NV]	0.1323	0.223	0.594	0.553	-0.305	0.570
C(x2)[T.NY]	-0.4710	0.093	-5.086	0.000	-0.653	-0.289
C(x2)[T.OH]	-0.3176	0.081	-3.914	0.000	-0.477	-0.158
C(x2)[T.OK]	0.2169	0.208	1.042	0.298	-0.193	0.626
C(x2)[T.OR]	0.0219	0.136	0.161	0.872	-0.246	0.290
C(x2)[T.PA]	-0.8621	0.089	-9.695	0.000	-1.037	-0.687
C(x2)[T.RI]	-0.2545	0.188	-1.351	0.177	-0.625	0.116
C(x2)[T.SC]	0.3375	0.161	2.095	0.037	0.021	0.654
C(x2)[T.SD]	-0.1246	0.307	-0.406	0.685	-0.728	0.479
C(x2)[T.TN]	0.0502	0.172	0.292	0.770	-0.287	0.388
C(x2)[T.TX]	0.3213	0.141	2.273	0.024	0.043	0.599
C(x2)[T.UT]	-0.1883	0.164	-1.148	0.252	-0.511	0.134
C(x2)[T.VA]	0.3294	0.173	1.899	0.058	-0.012	0.670
C(x2)[T.VT]	-0.5784	0.314	-1.843	0.066	-1.195	0.039
C(x2)[T.WA]	0.0517	0.112	0.463	0.644	-0.168	0.271
C(x2)[T.WI]	0.0378	0.104	0.363	0.717	-0.167	0.242
C(x2)[T.WV]	-0.2626	0.354	-0.741	0.459	-0.959	0.434
x4_log	1.3045	0.130	10.014	0.000	1.048	1.561
x7_log	0.1218	0.054	2.237	0.026	0.015	0.229
x8_log	0.2330	0.050	4.636	0.000	0.134	0.332
x14_log	-0.4283	0.122	-3.521	0.000	-0.667	-0.189
Omnibus:	91.189	Durbin-Watson:	1.997
Prob(Omnibus):	0.000	Jarque-Bera (JB):	456.794
Skew:	-0.788	Prob(JB):	6.43e-100
Kurtosis:	7.736	Cond. No.	7.03e+16


Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The smallest eigenvalue is 2.8e-29. This might indicate that there are

'''

# %%
# F-Test on the above model

full_model.f_test('C(x2)[T.AR] = 0, C(x2)[T.AZ] = 0, C(x2)[T.CA] = 0, C(x2)[T.CO] = 0, C(x2)[T.CT] = 0, C(x2)[T.DC] = 0, C(x2)[T.DE] = 0, C(x2)[T.FL] = 0, C(x2)[T.GA] = 0, C(x2)[T.HI] = 0, C(x2)[T.ID] = 0, C(x2)[T.IL] = 0, C(x2)[T.IN] = 0, C(x2)[T.KS] = 0, C(x2)[T.KY] = 0, C(x2)[T.LA] = 0, C(x2)[T.MA] = 0, C(x2)[T.MD] = 0, C(x2)[T.ME] = 0, C(x2)[T.MI] = 0, C(x2)[T.MN] = 0, C(x2)[T.MO] = 0, C(x2)[T.MS] = 0, C(x2)[T.MT] = 0, C(x2)[T.NC] = 0, C(x2)[T.ND] = 0, C(x2)[T.NE] = 0, C(x2)[T.NH] = 0, C(x2)[T.NJ] = 0, C(x2)[T.NM] = 0, C(x2)[T.NV] = 0, C(x2)[T.NY] = 0, C(x2)[T.OH] = 0, C(x2)[T.OK] = 0, C(x2)[T.OR] = 0, C(x2)[T.PA] = 0, C(x2)[T.RI] = 0, C(x2)[T.SC] = 0, C(x2)[T.SD] = 0, C(x2)[T.TN] = 0, C(x2)[T.TX] = 0, C(x2)[T.UT] = 0, C(x2)[T.VA] = 0, C(x2)[T.VT] = 0, C(x2)[T.WA] = 0, C(x2)[T.WI] = 0, C(x2)[T.WV] = 0')

# %%
'''

<class 'statsmodels.stats.contrast.ContrastResults'>
<F test: F=8.003577223673668, p=2.1862867509193086e-34, df_denom=388, df_num=47>

'''

# %%
# In order to avoid overfitting possibilities given the high R-square values, we further 
# verified using train-test split for the regression

train, test = train_test_split(data_prime, test_size=0.2)
fit_train = ols('log_y ~ C(x15) + C(x2) + x4_log + x7_log + x8_log + x14_log', data = train).fit()
fit_train.summary()

# %%
'''

OLS Regression Results
Dep. Variable:	log_y	R-squared:	0.918
Model:	OLS	Adj. R-squared:	0.905
Method:	Least Squares	F-statistic:	68.88
Date:	Wed, 01 May 2024	Prob (F-statistic):	1.29e-136
Time:	02:59:52	Log-Likelihood:	-66.725
No. Observations:	352	AIC:	233.5
Df Residuals:	302	BIC:	426.6
Df Model:	49		
Covariance Type:	nonrobust		
coef	std err	t	P>|t|	[0.025	0.975]
Intercept	-5.1451	0.657	-7.828	0.000	-6.438	-3.852
C(x15)[T.2]	-0.3003	0.077	-3.918	0.000	-0.451	-0.149
C(x15)[T.3]	-0.1807	0.134	-1.348	0.179	-0.444	0.083
C(x15)[T.4]	-0.0870	0.092	-0.946	0.345	-0.268	0.094
C(x2)[T.AR]	0.2220	0.254	0.875	0.382	-0.277	0.721
C(x2)[T.AZ]	0.0130	0.155	0.084	0.933	-0.292	0.318
C(x2)[T.CA]	-0.0203	0.081	-0.251	0.802	-0.180	0.139
C(x2)[T.CO]	0.1672	0.110	1.518	0.130	-0.049	0.384
C(x2)[T.CT]	-0.6090	0.136	-4.485	0.000	-0.876	-0.342
C(x2)[T.DC]	0.2915	0.341	0.856	0.393	-0.379	0.962
C(x2)[T.DE]	0.1067	0.305	0.350	0.726	-0.493	0.706
C(x2)[T.FL]	0.1830	0.136	1.345	0.180	-0.085	0.451
C(x2)[T.GA]	0.3783	0.164	2.304	0.022	0.055	0.701
C(x2)[T.HI]	0.1842	0.173	1.067	0.287	-0.156	0.524
C(x2)[T.ID]	9.99e-18	1.83e-16	0.054	0.957	-3.51e-16	3.71e-16
C(x2)[T.IL]	-0.0109	0.092	-0.118	0.906	-0.191	0.170
C(x2)[T.IN]	-0.3320	0.100	-3.308	0.001	-0.530	-0.135
C(x2)[T.KS]	0.4186	0.153	2.733	0.007	0.117	0.720
C(x2)[T.KY]	-0.2812	0.253	-1.109	0.268	-0.780	0.218
C(x2)[T.LA]	0.0803	0.176	0.457	0.648	-0.266	0.426
C(x2)[T.MA]	-0.7451	0.114	-6.553	0.000	-0.969	-0.521
C(x2)[T.MD]	0.1361	0.173	0.786	0.432	-0.204	0.477
C(x2)[T.ME]	-0.3739	0.159	-2.350	0.019	-0.687	-0.061
C(x2)[T.MI]	0.3086	0.102	3.013	0.003	0.107	0.510
C(x2)[T.MN]	-0.0205	0.141	-0.146	0.884	-0.297	0.256
C(x2)[T.MO]	0.1728	0.121	1.431	0.153	-0.065	0.410
C(x2)[T.MS]	-0.3185	0.338	-0.941	0.347	-0.985	0.348
C(x2)[T.MT]	-0.4933	0.290	-1.703	0.090	-1.063	0.077
C(x2)[T.NC]	0.1158	0.149	0.779	0.436	-0.177	0.408
C(x2)[T.ND]	-0.4010	0.295	-1.361	0.174	-0.981	0.179
C(x2)[T.NE]	-0.0923	0.211	-0.438	0.662	-0.507	0.323
C(x2)[T.NH]	-0.4638	0.181	-2.564	0.011	-0.820	-0.108
C(x2)[T.NJ]	-0.3029	0.101	-3.011	0.003	-0.501	-0.105
C(x2)[T.NM]	0.1966	0.210	0.938	0.349	-0.216	0.609
C(x2)[T.NV]	-2.95e-16	1.31e-16	-2.253	0.025	-5.53e-16	-3.73e-17
C(x2)[T.NY]	-0.5302	0.096	-5.527	0.000	-0.719	-0.341
C(x2)[T.OH]	-0.2443	0.084	-2.922	0.004	-0.409	-0.080
C(x2)[T.OK]	0.2164	0.199	1.089	0.277	-0.175	0.607
C(x2)[T.OR]	0.0008	0.152	0.005	0.996	-0.299	0.300
C(x2)[T.PA]	-0.8338	0.097	-8.639	0.000	-1.024	-0.644
C(x2)[T.RI]	-0.2669	0.182	-1.465	0.144	-0.625	0.092
C(x2)[T.SC]	0.2892	0.165	1.756	0.080	-0.035	0.613
C(x2)[T.SD]	-0.1096	0.293	-0.373	0.709	-0.687	0.468
C(x2)[T.TN]	0.0500	0.164	0.305	0.760	-0.272	0.372
C(x2)[T.TX]	0.3359	0.140	2.401	0.017	0.061	0.611
C(x2)[T.UT]	-0.1670	0.210	-0.795	0.427	-0.580	0.246
C(x2)[T.VA]	0.3274	0.173	1.892	0.059	-0.013	0.668
C(x2)[T.VT]	-0.5582	0.301	-1.856	0.064	-1.150	0.034
C(x2)[T.WA]	0.0319	0.121	0.262	0.793	-0.207	0.271
C(x2)[T.WI]	0.0101	0.108	0.094	0.926	-0.203	0.224
C(x2)[T.WV]	-0.2524	0.338	-0.747	0.456	-0.917	0.412
x4_log	1.2652	0.138	9.142	0.000	0.993	1.538
x7_log	0.0861	0.060	1.446	0.149	-0.031	0.203
x8_log	0.2303	0.056	4.134	0.000	0.121	0.340
x14_log	-0.3524	0.129	-2.728	0.007	-0.607	-0.098
Omnibus:	118.847	Durbin-Watson:	1.953
Prob(Omnibus):	0.000	Jarque-Bera (JB):	673.605
Skew:	-1.294	Prob(JB):	5.35e-147
Kurtosis:	9.263	Cond. No.	6.74e+16


Notes:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
[2] The smallest eigenvalue is 2.42e-29. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular

'''

# %%
# Prediction values 
predtest_log_y = fit_train.predict(test)

# %%
# Calculating R-square of the prediction model
resid_fit_train = (test['log_y'] - predtest_log_y)**2
mean = test['log_y'].sum()/88
tss_fit_train_df = (test['log_y'] - mean)**2
tss_fit_train = tss_fit_train_df.sum()
r_square_fit_train = 1 - resid_fit_train.sum()/tss_fit_train
r_square_fit_train

# %%
# r_square_fit_train : 0.9056827774801053