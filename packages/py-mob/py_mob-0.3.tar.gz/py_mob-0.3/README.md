#### Introduction

As an attempt to mimic the mob R package (https://CRAN.R-project.org/package=mob), the py\_mob is a collection of python functions that would generate the monotonic binning and perform the WoE (Weight of Evidence) transformation used in consumer credit scorecard developments. 

Being a piecewise constant transformation in the context of logistic regressions, the WoE has also been employed in other use cases, such as consumer credit loss estimation, prepayment, and even fraud detection models. In addition to monotonic binning and WoE transformation, Information Value and KS statistic of each independent variables is also calculated to evaluate the variable predictiveness. 

Different from other python packages for the same purpose, the py\_mob package is very lightweight and the underlying computation is driven by the built-in python list or the numpy array. Functions would return lists of dictionaries, which can be easily converted to other data structures, such as pandas.DataFrame or astropy.table. 

What's more, six different monotonic binning algorithms are implemented, namely qtl\_bin(), bad\_bin(), iso\_bin(), rng\_bin(), kmn\_bin(), and gbm\_bin(), that would provide different predictability and cardinality. For details, please see https://github.com/statcompute/py_mob.

People without the background knowledge in the consumer risk modeling might be wondering why the monotonic binning and thereafter the WoE transformation are important. Below are a couple reasons based on my experience. They are perfectly generalizable in other use cases of logistic regression with binary outcomes. 
1. Because the WoE is a piecewise transformation based on the data discretization, all missing values would fall into a standalone category either by itself or to be combined with the neighbor with a similar bad rate. As a result, the special treatment for missing values is not necessary.
2. After the monotonic binning of each variable, since the WoE value for each bin is a projection from the predictor into the response that is defined by the log ratio between event and non-event distributions, any raw value of the predictor doesn't matter anymore and therefore the issue related to outliers would disappear.
3. While many modelers would like to use log or power transformations to achieve a good linear relationship between the predictor and log odds of the response, which is heuristic at best with no guarantee for the good outcome, the WoE transformation is strictly linear with respect to log odds of the response with the unity correlation. It is also worth mentioning that a numeric variable and its strictly monotone functions should converge to the same monotonic WoE transformation.
4. At last, because the WoE is defined as the log ratio between event and non-event distributions, it is indicative of the separation between cases with Y = 0 and cases with Y = 1. As the weighted sum of WoE values with the weight being the difference in event and non-event distributions, the IV (Information Value) is an important statistic commonly used to measure the predictor importance.

 
#### Installation

```python
pip3 install py_mob
```

#### Core Functions

```
py_mob
  |-- qtl_bin()  : An iterative discretization based on quantiles of X.  
  |-- bad_bin()  : A revised iterative discretization for records with Y = 1.
  |-- iso_bin()  : A discretization algorthm driven by the isotonic regression between X and Y. 
  |-- rng_bin()  : A revised iterative discretization based on the equal-width range of X.  
  |-- kmn_bin()  : A discretization algorthm based on the kmean clustering of X.  
  |-- gbm_bin()  : A discretization algorthm based on the gradient boosting machine.  
  |-- summ_bin() : Generates the statistical summary for the binning outcome. 
  |-- view_bin() : Displays the binning outcome in a tabular form. 
  |-- cal_woe()  : Applies the WoE transformation to a numeric vector based on the binning outcome.
  |-- pd_bin()   : Discretizes each vector in a pandas DataFrame.
  |-- pd_woe()   : Applies WoE transformaton to each vector in the pandas DataFrame.
  `-- get_data() : Loads the testing dataset.
```


#### Example 

```
import py_mob, pandas

dt = py_mob.get_data("accepts")

utl = dt["rev_util"]

bad = dt["bad"]

utl_bin = py_mob.qtl_bin(utl, bad)

### SHOW WHAT IS IN THE FINAL BINNING OUTCOME 
for key in utl_bin:
  print(key + ":")
  for lst in utl_bin[key]:
    print(lst)

#cut:
#30.0
#tbl:
#{'bin': 1, 'freq': 2962, 'miss': 0, 'bads': 467.0, 'rate': 0.1577, 'woe': -0.3198, 'iv': 0.047, 
# 'rule': '$X$ <= 30.0'}
#{'bin': 2, 'freq': 2875, 'miss': 0, 'bads': 729.0, 'rate': 0.2536, 'woe': 0.2763, 'iv': 0.0406, 
# 'rule': '$X$ > 30.0'}

### REPORT THE BINNING OUTCOME IN THE TABULAR FORMAT
py_mob.view_bin(utl_bin)

#|  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
#|-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
#|   1   |   2962 |      0 |    467 | 0.1577 | -0.3198 | 0.0470 | 14.71 | $X$ <= 30.0                                   |
#|   2   |   2875 |      0 |    729 | 0.2536 |  0.2763 | 0.0406 |  0.00 | $X$ > 30.0                                    |

### SUMMARIZE THE BINNING OUTCOME
py_mob.summ_bin(utl_bin)

#{'sample size': 5837, 'bad rate': 0.2049, 'iv': 0.0876, 'ks': 14.71, 'missing': 0.0}

### APPLY THE WOE TRANSFORMATION
for x in py_mob.cal_woe(utl[:3], py_mob.iso_bin(utl, bad)):
  print(x)

#{'x':  0.0, 'bin': 1, 'woe': -0.3254}
#{'x':  2.0, 'bin': 1, 'woe': -0.3254}
#{'x': 21.0, 'bin': 1, 'woe': -0.3254}

### DISCRETIZES VECTORS IN PANDAS DATAFRAME
df = pandas.DataFrame(dt)

rst = py_mob.pd_bin(df['bad'], df[['ltv', 'bureau_score', 'tot_derog']])

rst.keys()
# dict_keys(['bin_sum', 'bin_out'])

### APPLIES WOE TRANSFORMATIONS TO VECTORS IN PANDAS DATAFRAME
out = py_mob.pd_woe(df[['ltv', 'bureau_score', 'tot_derog']], rst["bin_out"])

out.head(2)
#       ltv  bureau_score  tot_derog
# 0  0.1619       -1.2560     0.6557
# 1  0.0804       -1.1961    -0.3811
```
