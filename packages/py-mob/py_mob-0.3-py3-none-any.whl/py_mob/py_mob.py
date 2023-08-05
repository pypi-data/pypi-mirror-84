# py_mob/py_mob.py
# exec(open('py_mob/py_mob.py').read())
# version 0.3

import pandas, numpy, scipy.stats, sklearn.isotonic, sklearn.cluster, lightgbm
import tabulate, pkg_resources


def get_data(data):
  """
  The function loads a testing dataset.

  Parameters:
    data : The name of dataset. It is either "hmeq" or "accepts", both of
           which are loan performance data.

  Returns:
    A dict with the dataset.

  Example:
    data = py_mob.get_data("accepts")

    data.keys()
    # ['bankruptcy', 'bad', 'app_id', 'tot_derog', 'tot_tr', 'age_oldest_tr',
    #  'tot_open_tr', 'tot_rev_tr', 'tot_rev_debt', 'tot_rev_line', 'rev_util',
    #  'bureau_score', 'purch_price', 'msrp', 'down_pyt', 'purpose', 
    #  'loan_term', 'loan_amt', 'ltv', 'tot_income', 'used_ind', 'weight']
  
    py_mob.view_bin(py_mob.qtl_bin(data["ltv"], data["bad"]))
  """

  _p = pkg_resources.resource_filename("py_mob", "data/" + data + ".csv")

  _d = numpy.recfromcsv(_p, delimiter = ',', names = True, encoding = 'latin-1')

  return(dict((_2, [_[_1] for _ in _d]) for _1, _2 in enumerate(_d.dtype.fields)))


########## 01. cal_woe() ########## 

def cal_woe(x, bin):
  """
  The function applies the woe transformation to a numeric vector based on 
  the binning outcome.

  Parameters:
    x   : A numeric vector, which can be a list, 1-D numpy array, or pandas 
          series
    bin : An object containing the binning outcome.

  Returns:
    A list of dictionaries with three keys

  Example:
    ltv_bin = py_mob.qtl_bin(ltv, bad)

    for x in cal_woe(ltv[:3], ltv_bin):
      print(x)

    # {'x': 109.0, 'bin': 6, 'woe': 0.2694}
    # {'x':  97.0, 'bin': 3, 'woe': 0.0045}
    # {'x': 105.0, 'bin': 5, 'woe': 0.1829}
  """

  _cut = sorted([_ for _ in bin['cut']] + [numpy.PINF, numpy.NINF])

  _dat = [[_1[0], _1[1], _2] for _1, _2 in zip(enumerate(x), ~numpy.isnan(x))]

  _m1 = [_[:2] for _ in _dat if _[2] == 0]
  _l1 = [_[:2] for _ in _dat if _[2] == 1]

  _l2 = [[*_1, _2] for _1, _2 in zip(_l1, numpy.searchsorted(_cut, [_[1] for _ in _l1]).tolist())]

  flatten = lambda l: [item for subl in l for item in subl]
 
  _l3 = flatten([[[*l, b['woe']] for l in _l2 if l[2] == b['bin']] for b in bin['tbl'] if b['bin'] > 0])

  if len(_m1) > 0:
    if len([_ for _ in bin['tbl'] if _['miss'] > 0]) > 0:
      _m2 = [l + [_['bin'] for _ in bin['tbl'] if _['miss'] > 0] 
               + [_['woe'] for _ in bin['tbl'] if _['miss'] > 0] for l in _m1]
    else:
      _m2 = [l + [0, 0] for l in _m1]
    _l3.extend(_m2)

  _key = ["x", "bin", "woe"]

  return(list(dict(zip(_key, _[1:])) for _ in sorted(_l3, key = lambda x: x[0])))


########## 02. summ_bin() ########## 

def summ_bin(x):
  """
  The function summarizes the binning outcome generated from a binning function, 
  e.g. qtl_bin() or iso_bin().

  Parameters:
    x: An object containing the binning outcome.

  Returns:
    A dictionary with statistics derived from the binning outcome

  Example:
    py_mob.summ_bin(py_mob.iso_bin(ltv, bad))
    # {'sample size': 5837, 'bad rate': 0.2049, 'iv': 0.185, 'ks': 16.88, 'missing': 0.0002}
  """

  _freq = sum(_['freq'] for _ in x['tbl'])
  _bads = sum(_['bads'] for _ in x['tbl'])
  _miss = sum(_['miss'] for _ in x['tbl'])

  _iv = round(sum(_['iv'] for _ in x['tbl']), 4)
  _ks = round(max(_["ks"] for _ in x["tbl"]), 2)

  _br = round(_bads / _freq, 4)
  _mr = round(_miss / _freq, 4)

  return({"sample size": _freq, "bad rate": _br, "iv": _iv, "ks": _ks, "missing": _mr})


########## 03. view_bin() ########## 

def view_bin(x):
  """
  The function displays the binning outcome generated from a binning function, 
  e.g. qtl_bin() or iso_bin().

  Parameters:
    x: An object containing the binning outcome.

  Returns:
    None

  Example:
    py_mob.view_bin(py_mob.qtl_bin(df.ltv, df.bad))
  """

  tabulate.PRESERVE_WHITESPACE = True

  _sel = ["bin", "freq", "miss", "bads", "rate", "woe", "iv", "ks"]

  _tbl = [{**(lambda v: {k: v[k] for k in _sel})(_), "rule": _["rule"].ljust(45)} for _ in x["tbl"]]

  print(tabulate.tabulate(_tbl, headers = "keys", tablefmt = "github", 
                          colalign = ["center"] + ["right"] * 7 + ["center"],
                          floatfmt = (".0f", ".0f", ".0f", ".0f", ".4f", ".4f", ".4f", ".2f")))


########## 04. qcut() ##########

def qcut(x, n):
  """
  The function discretizes a numeric vector into n pieces based on quantiles.

  Parameters:
    x: A numeric vector.
    n: An integer indicating the number of categories to discretize.

  Returns:
    A list of numeric values to divide the vector x into n categories.

  Example:
    py_mob.qcut(range(10), 3)
    # [3, 6]
  """

  _q = numpy.linspace(0, 100, n, endpoint = False)[1:]
  _x = [_ for _ in x if not numpy.isnan(_)]
  _c = numpy.unique(numpy.percentile(_x, _q, interpolation = "lower"))
  return([_ for _ in _c])


########## 05. manual_bin() ##########

def manual_bin(x, y, cuts):
  """
  The function discretizes the x vector and then summarizes over the y vector
  based on the discretization result.

  Parameters:
    x    : A numeric vector to discretize without missing values, 
           e.g. numpy.nan or math.nan
    y    : A numeric vector with binary values of 0/1 and with the same length 
           of x
    cuts : A list of numeric values as cut points to discretize x.

  Returns:
    A list of dictionaries for the binning outcome. 

  Example:
    for x in py_mob.manual_bin(scr, bad, [650, 700, 750]):
      print(x)

    # {'bin': 1, 'freq': 1311, 'miss': 0, 'bads': 520.0, 'minx': 443.0, 'maxx': 650.0}
    # {'bin': 2, 'freq': 1688, 'miss': 0, 'bads': 372.0, 'minx': 651.0, 'maxx': 700.0}
    # {'bin': 3, 'freq': 1507, 'miss': 0, 'bads': 157.0, 'minx': 701.0, 'maxx': 750.0}
    # {'bin': 4, 'freq': 1016, 'miss': 0, 'bads':  42.0, 'minx': 751.0, 'maxx': 848.0}
  """

  _x = [_ for _ in x]
  _y = [_ for _ in y]
  _c = sorted([_ for _ in set(cuts)] + [numpy.NINF, numpy.PINF])
  _g = numpy.searchsorted(_c, _x).tolist()

  _l1 = sorted(zip(_g, _x, _y), key = lambda x: x[0])
  _l2 = zip(set(_g), [[l for l in _l1 if l[0] == g] for g in set(_g)])

  return(sorted([dict(zip(["bin", "freq", "miss", "bads", "minx", "maxx"],
                          [_1, len(_2), 0,
                           sum([_[2] for _ in _2]),
                           min([_[1] for _ in _2]),
                           max([_[1] for _ in _2])])) for _1, _2 in _l2],
                key = lambda x: x["bin"]))


########## 06. miss_bin() ##########

def miss_bin(y):
  """
  The function summarizes the y vector with binary values of 0/1 and is not 
  supposed to be called directly by users.

  Parameters:
    y : A numeric vector with binary values of 0/1.

  Returns:
    A dictionary.
  """

  return({"bin": 0, "freq": len([_ for _ in y]), "miss": len([_ for _ in y]), 
          "bads": sum([_ for _ in y]), "minx": numpy.nan, "maxx": numpy.nan})


########## 07. gen_rule() ##########

def gen_rule(tbl, pts):
  """
  The function generates binning rules based on the binning outcome table and
  a list of cut points and is an utility function that is not supposed to be 
  called directly by users.

  Parameters:
    tbl : A intermediate table of the binning outcome within each binning 
          function
    pts : A list cut points for the binning

  Returns:
    A list of dictionaries with binning rules 
  """

  for _ in tbl:
    if _["bin"] == 0:
      _["rule"] = "numpy.isnan($X$)"
    elif _["bin"] == len(pts) + 1:
      if _["miss"] == 0:
        _["rule"] = "$X$ > " + str(pts[-1])
      else:
        _["rule"] = "$X$ > " + str(pts[-1]) + " or numpy.isnan($X$)"
    elif _["bin"] == 1:
      if _["miss"] == 0:
        _["rule"] = "$X$ <= " + str(pts[0])
      else:
        _["rule"] = "$X$ <= " + str(pts[0]) + " or numpy.isnan($X$)"
    else:
        _["rule"] = "$X$ > " + str(pts[_["bin"] - 2]) + " and $X$ <= " + str(pts[_["bin"] - 1])

  _sel = ["bin", "freq", "miss", "bads", "rate", "woe", "iv", "ks", "rule"]

  return([{k: _[k] for k in _sel} for _ in tbl])


########## 08. gen_woe() ##########

def gen_woe(x):
  """
  The function calculates weight of evidence and information value based on the 
  binning outcome within each binning function and is an utility function that 
  is not supposed to be called directly by users.

  Parameters:
    x : A list of dictionaries for the binning outcome.

  Returns:
    A list of dictionaries with additional keys to the input.
  """

  _freq = sum(_["freq"] for _ in x)
  _bads = sum(_["bads"] for _ in x)

  _l1 = sorted([{**_, 
                 "rate": round(_["bads"] / _["freq"], 4),
                 "woe" : round(numpy.log((_["bads"] / _bads) / ((_["freq"] - _["bads"]) / (_freq - _bads))), 4),
                 "iv"  : round((_["bads"] / _bads - (_["freq"] - _["bads"]) / (_freq - _bads)) *
                               numpy.log((_["bads"] / _bads) / ((_["freq"] - _["bads"]) / (_freq - _bads))), 4)
                } for _ in x], key = lambda _x: _x["bin"])

  cumsum = lambda x: [sum([_ for _ in x][0:(i + 1)]) for i in range(len(x))]

  _cumb = cumsum([_['bads'] / _bads for _ in _l1])
  _cumg = cumsum([(_['freq'] - _['bads']) / (_freq - _bads) for _ in _l1])
  _ks = [round(numpy.abs(_[0] - _[1]) * 100, 2) for _ in zip(_cumb, _cumg)]
  
  return([{**_1, "ks": _2} for _1, _2 in zip(_l1, _ks)])


########## 09. add_miss() ##########

def add_miss(d, l):
  """
  The function appends missing value category, if any, to the binning outcome 
  and is an utility function and is not supposed to be called directly by 
  the user.  

  Parameters:
    d : A list with lists generated by input vectors of binning functions.
    l : A list of dicts.

  Returns:
    A list of dicts.
  """

  _l = l[:]

  if len([_ for _ in d if _[2] == 0]) > 0:
    _m = miss_bin([_[1] for _ in d if _[2] == 0])
    if _m["bads"] == 0:
      for _ in ['freq', 'miss', 'bads']:
        _l[0][_]  = _l[0][_]  + _m[_]
    elif _m["freq"] == _m["bads"]:
      for _ in ['freq', 'miss', 'bads']:
        _l[-1][_]  = _l[-1][_]  + _m[_]
    else:
      _l.append(_m)

  return(_l)


########## 10. qtl_bin() ##########

def qtl_bin(x, y):
  """
  The function discretizes the x vector based on percentiles and summarizes 
  over the y vector to derive weight of evidence transformaton (WoE) and 
  information value.

  Parameters:
    x : A numeric vector to discretize. It can be a list, 1-D numpy array, or 
        pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It can be a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.qtl_bin(derog, bad)["cut"]
    #  [0.0, 1.0, 3.0]

    py_mob.view_bin(py_mob.qtl_bin(derog, bad)) 

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)                              |
    |   1   |   2850 |      0 |    367 | 0.1288 | -0.5559 | 0.1268 | 20.04 | $X$ <= 0.0                                    |
    |   2   |    891 |      0 |    193 | 0.2166 |  0.0704 | 0.0008 | 18.95 | $X$ > 0.0 and $X$ <= 1.0                      |
    |   3   |    810 |      0 |    207 | 0.2556 |  0.2867 | 0.0124 | 14.63 | $X$ > 1.0 and $X$ <= 3.0                      |
    |   4   |   1073 |      0 |    359 | 0.3346 |  0.6684 | 0.0978 |  0.00 | $X$ > 3.0                                     |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(50, len(numpy.unique(_x)) - 1)))
  _p = set(tuple(qcut(_x, _)) for _ in _n)

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          scipy.stats.spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 11. bad_bin() ##########

def bad_bin(x, y):
  """
  The function discretizes the x vector based on percentiles and then 
  summarizes over the y vector with y = 1 to derive the weight of evidence 
  transformaton (WoE) and information values.

  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array, 
        or pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.bad_bin(derog, bad)["cut"]
    # [0.0, 2.0, 4.0]

    py_mob.view_bin(py_mob.bad_bin(derog, bad))

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)                              |
    |   1   |   2850 |      0 |    367 | 0.1288 | -0.5559 | 0.1268 | 20.04 | $X$ <= 0.0                                    |
    |   2   |   1369 |      0 |    314 | 0.2294 |  0.1440 | 0.0051 | 16.52 | $X$ > 0.0 and $X$ <= 2.0                      |
    |   3   |    587 |      0 |    176 | 0.2998 |  0.5078 | 0.0298 | 10.66 | $X$ > 2.0 and $X$ <= 4.0                      |
    |   4   |    818 |      0 |    269 | 0.3289 |  0.6426 | 0.0685 |  0.00 | $X$ > 4.0                                     |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(50, len(numpy.unique([_[0] for _ in _data if _[1] == 1 and _[2] == 1])) - 1)))

  _p = set(tuple(qcut([_[0] for _ in _data if _[1] == 1 and _[2] == 1], _)) for _ in _n)

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          scipy.stats.spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 12. iso_bin() ##########

def iso_bin(x, y):
  """
  The function discretizes the x vector based on the isotonic regression and 
  then summarizes over the y vector to derive the weight of evidence 
  transformaton (WoE) and information values.

  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array, 
        or pandas series. 
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.iso_bin(derog, bad)["cut"]
    # [1.0, 2.0, 3.0, 23.0]

    py_mob.view_bin(py_mob.iso_bin(derog, bad))

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)                              |
    |   1   |   3741 |      0 |    560 | 0.1497 | -0.3811 | 0.0828 | 18.95 | $X$ <= 1.0                                    |
    |   2   |    478 |      0 |    121 | 0.2531 |  0.2740 | 0.0066 | 16.52 | $X$ > 1.0 and $X$ <= 2.0                      |
    |   3   |    332 |      0 |     86 | 0.2590 |  0.3050 | 0.0058 | 14.63 | $X$ > 2.0 and $X$ <= 3.0                      |
    |   4   |   1064 |      0 |    353 | 0.3318 |  0.6557 | 0.0931 |  0.44 | $X$ > 3.0 and $X$ <= 23.0                     |
    |   5   |      9 |      0 |      6 | 0.6667 |  2.0491 | 0.0090 |  0.00 | $X$ > 23.0                                    |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _cor = scipy.stats.spearmanr(_x, _y)[0]
  _reg = sklearn.isotonic.IsotonicRegression()

  _f = numpy.abs(_reg.fit_transform(_x, list(map(lambda y:  y * _cor / numpy.abs(_cor), _y))))

  _l1 = sorted(list(zip(_f, _x, _y)), key = lambda x: x[0])

  _l2 = [[l for l in _l1 if l[0] == f] for f in sorted(set(_f))]

  _l3 = [[*set(_[0] for _ in l),
          max(_[1] for _ in l),
          numpy.mean([_[2] for _ in l]),
          sum(_[2] for _ in l)] for l in _l2]

  _c = sorted([_[1] for _ in [l for l in _l3 if l[2] < 1 and l[2] > 0 and l[3] > 1]])
  _p = _c[1:-1] if len(_c) > 2 else _c[:-1]
    
  _l4 = sorted(manual_bin(_x, _y, _p), key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _p, "tbl": gen_rule(gen_woe(_l5), _p)})


########## 13. rng_bin() ##########

def rng_bin(x, y):
  """
  The function discretizes the x vector based on the equal-width range and 
  summarizes over the y vector to derive the weight of evidence transformaton 
  (WoE) and information values.

  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array, 
        or pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.rng_bin(derog, bad)["cut"]
    # [7.0, 14.0, 21.0] 

    py_mob.view_bin(py_mob.rng_bin(derog, bad))

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |   ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 | 2.77 | numpy.isnan($X$)                              |
    |   1   |   5243 |      0 |   1001 | 0.1909 | -0.0881 | 0.0068 | 4.94 | $X$ <= 7.0                                    |
    |   2   |    322 |      0 |    104 | 0.3230 |  0.6158 | 0.0246 | 0.94 | $X$ > 7.0 and $X$ <= 14.0                     |
    |   3   |     46 |      0 |     15 | 0.3261 |  0.6300 | 0.0037 | 0.35 | $X$ > 14.0 and $X$ <= 21.0                    |
    |   4   |     13 |      0 |      6 | 0.4615 |  1.2018 | 0.0042 | 0.00 | $X$ > 21.0                                    |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(50, len(numpy.unique(_x)) - 1)))

  _m = [[numpy.median([_[0] for _ in _data if _[2] == 1 and _[1] == 1])],
        [numpy.median([_[0] for _ in _data if _[2] == 1])]]

  _p = list(set(tuple(qcut(numpy.unique(_x), _)) for _ in _n)) + _m

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _p]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          scipy.stats.spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 14. kmn_bin() ##########

def kmn_bin(x, y):
  """
  The function discretizes the x vector based on the kmean clustering and then 
  summarizes over the y vector to derive the weight of evidence transformaton 
  (WoE) and information values.

  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array,
        or pandas series.
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.kmn_bin(derog, bad)['cut']
    # [1.0, 5.0, 11.0]

    py_mob.view_bin(py_mob.kmn_bin(derog, bad)) 

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)                              |
    |   1   |   3741 |      0 |    560 | 0.1497 | -0.3811 | 0.0828 | 18.95 | $X$ <= 1.0                                    |
    |   2   |   1249 |      0 |    366 | 0.2930 |  0.4753 | 0.0550 |  7.37 | $X$ > 1.0 and $X$ <= 5.0                      |
    |   3   |    504 |      0 |    157 | 0.3115 |  0.5629 | 0.0318 |  1.72 | $X$ > 5.0 and $X$ <= 11.0                     |
    |   4   |    130 |      0 |     43 | 0.3308 |  0.6512 | 0.0112 |  0.00 | $X$ > 11.0                                    |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _n = numpy.arange(2, max(3, min(20, len(numpy.unique(_x)) - 1)))

  _m = [[numpy.median([_[0] for _ in _data if _[2] == 1 and _[1] == 1])],
        [numpy.median([_[0] for _ in _data if _[2] == 1])]]

  _c1 = [sklearn.cluster.KMeans(n_clusters = _, random_state = 1).fit(numpy.reshape(_x, [-1, 1])).labels_ for _ in _n]

  _c2 = [sorted(_l, key = lambda x: x[0]) for _l in [list(zip(_, _x)) for _ in _c1]]

  group = lambda x: [[_l for _l in x if _l[0] == _k] for _k in set([_[0] for _ in x])]

  upper = lambda x: sorted([max([_2[1] for _2 in _1]) for _1 in x])

  _c3 = list(set(tuple(upper(_2)[:-1]) for _2 in [group(_1) for _1 in _c2])) + _m

  _l1 = [[_, manual_bin(_x, _y, _)] for _ in _c3]

  _l2 = [[l[0], 
          min([_["bads"] / _["freq"] for _ in l[1]]), 
          max([_["bads"] / _["freq"] for _ in l[1]]),
          scipy.stats.spearmanr([_["bin"] for _ in l[1]], [_["bads"] / _["freq"] for _ in l[1]])[0]
         ] for l in _l1]

  _l3 = [l[0] for l in sorted(_l2, key = lambda x: -len(x[0]))
         if numpy.abs(round(l[3], 8)) == 1 and round(l[1], 8) > 0 and round(l[2], 8) < 1][0]

  _l4 = sorted(*[l[1] for l in _l1 if l[0] == _l3], key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _l3, "tbl": gen_rule(gen_woe(_l5), _l3)})


########## 15. gbm_bin() ########## 

def gbm_bin(x, y):
  """
  The function discretizes the x vector based on the gradient boosting machine 
  and then summarizes over the y vector to derive the weight of evidence 
  transformaton (WoE) and information values.

  Parameters:
    x : A numeric vector to discretize. It is a list, 1-D numpy array, 
        or pandas series. 
    y : A numeric vector with binary values of 0/1 and with the same length 
        of x. It is a list, 1-D numpy array, or pandas series.

  Returns:
    A dictionary with two keys:
      "cut" : A numeric vector with cut points applied to the x vector.
      "tbl" : A list of dictionaries summarizing the binning outcome.

  Example:
    py_mob.gbm_bin(derog, bad)["cut"]
    # [1.0, 2.0, 3.0, 22.0, 26.0]

    py_mob.view_bin(py_mob.gbm_bin(derog, bad))

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |                     rule                      |
    |-------|--------|--------|--------|--------|---------|--------|-------|-----------------------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)                              |
    |   1   |   3741 |      0 |    560 | 0.1497 | -0.3811 | 0.0828 | 18.95 | $X$ <= 1.0                                    |
    |   2   |    478 |      0 |    121 | 0.2531 |  0.2740 | 0.0066 | 16.52 | $X$ > 1.0 and $X$ <= 2.0                      |
    |   3   |    332 |      0 |     86 | 0.2590 |  0.3050 | 0.0058 | 14.63 | $X$ > 2.0 and $X$ <= 3.0                      |
    |   4   |   1063 |      0 |    353 | 0.3321 |  0.6572 | 0.0934 |  0.42 | $X$ > 3.0 and $X$ <= 22.0                     |
    |   5   |      6 |      0 |      3 | 0.5000 |  1.3559 | 0.0025 |  0.23 | $X$ > 22.0 and $X$ <= 26.0                    |
    |   6   |      4 |      0 |      3 | 0.7500 |  2.4546 | 0.0056 |  0.00 | $X$ > 26.0                                    |
  """

  _data = [_ for _ in zip(x, y, ~numpy.isnan(x))]

  _x = [_[0] for _ in _data if _[2] == 1]
  _y = [_[1] for _ in _data if _[2] == 1]

  _cor = scipy.stats.spearmanr(_x, _y)[0]
  _con = "1" if _cor > 0 else "-1"

  _gbm = lightgbm.LGBMRegressor(num_leaves = 100, min_child_samples = 3, n_estimators = 1,
                                random_state = 1, monotone_constraints = _con)
  _gbm.fit(numpy.reshape(_x, [-1, 1]), _y)

  _f = numpy.abs(_gbm.predict(numpy.reshape(_x, [-1, 1])))

  _l1 = sorted(list(zip(_f, _x, _y)), key = lambda x: x[0])

  _l2 = [[l for l in _l1 if l[0] == f] for f in sorted(set(_f))]

  _l3 = [[*set(_[0] for _ in l),
          max(_[1] for _ in l),
          numpy.mean([_[2] for _ in l]),
          sum(_[2] for _ in l)] for l in _l2]

  _c = sorted([_[1] for _ in [l for l in _l3 if l[2] < 1 and l[2] > 0 and l[3] > 1]])

  _p = _c[1:-1] if len(_c) > 2 else _c[:-1]
    
  _l4 = sorted(manual_bin(_x, _y, _p), key = lambda x: x["bads"] / x["freq"])

  _l5 = add_miss(_data, _l4)

  return({"cut": _p, "tbl": gen_rule(gen_woe(_l5), _p)})


########## 16. pd_bin() ########## 

def pd_bin(y, xs, method = 1):
  """
  The function discretizes each vector in the pandas DataFrame, e.g. xs, based 
  on the chosen binning method. 

  Parameters:
    y     : A numeric vector with binary values of 0/1 and with the same length 
            of xs. It can be a list, 1-D numpy array, or pandas series.
    xs    : A pandas DataFrame including all numeric vectors to discretize.
    method: A integer from 1 to 6 referring to implementations below. 
            The default value is 1.
              1 - implementation of iso_bin();  2 - implementation of qtl_bin();
              3 - implementation of bad_bin();  4 - implementation of rng_bin();
              5 - implementation of gbm_bin();  6 - implementation of kmn_bin().

  Returns:
    A dictionary with two keys:
      'bin_sum': A list of binning summary
      'bin_out': A dictionary of binning outcomes for all variables in xs

  Example:
    df = pandas.DataFrame(py_mob.get_data("accepts"))
    
    rst = py_mob.pd_bin(df['bad'], df[['ltv', 'bureau_score', 'tot_derog']])

    rst.keys()
    # dict_keys(['bin_sum', 'bin_out'])

    for _ in rst['bin_sum']:
      print(_)
    {'variable': 'ltv', ... 'iv': 0.185, 'ks': 16.88, 'missing': 0.0002}
    {'variable': 'bureau_score', ... 'iv': 0.8354, 'ks': 35.27, 'missing': 0.054}
    {'variable': 'tot_derog', ... 'iv': 0.2151, 'ks': 18.95, 'missing': 0.0365}

    py_mob.view_bin(rst['bin_out']['tot_derog'])

    |  bin  |   freq |   miss |   bads |   rate |     woe |     iv |    ks |           rule                 |
    |-------|--------|--------|--------|--------|---------|--------|-------|--------------------------------|
    |   0   |    213 |    213 |     70 | 0.3286 |  0.6416 | 0.0178 |  2.77 | numpy.isnan($X$)               |
    |   1   |   3741 |      0 |    560 | 0.1497 | -0.3811 | 0.0828 | 18.95 | $X$ <= 1.0                     |
    |   2   |    478 |      0 |    121 | 0.2531 |  0.2740 | 0.0066 | 16.52 | $X$ > 1.0 and $X$ <= 2.0       |
    |   3   |    332 |      0 |     86 | 0.2590 |  0.3050 | 0.0058 | 14.63 | $X$ > 2.0 and $X$ <= 3.0       |
    |   4   |   1064 |      0 |    353 | 0.3318 |  0.6557 | 0.0931 |  0.44 | $X$ > 3.0 and $X$ <= 23.0      |
    |   5   |      9 |      0 |      6 | 0.6667 |  2.0491 | 0.0090 |  0.00 | $X$ > 23.0                     |
  """

  methods = {1: iso_bin, 2: qtl_bin, 3: bad_bin, 4: rng_bin, 5: gbm_bin, 6: kmn_bin}
  # methods = {1: iso_bin, 2: qtl_bin}

  bin_fn = methods[method]

  xnames = [_ for _ in xs.columns]

  bin_out = dict(zip(xnames, [bin_fn(xs[_], y) for _ in xnames]))

  bin_sum = [{'variable': _, **summ_bin(bin_out.get(_))} for _ in xnames]

  return({'bin_sum': bin_sum, 'bin_out': bin_out})


########## 17. pd_woe() ########## 

def pd_woe(xs, bin_out):
  """
  The function applies WoE transformaton to each vector in the pandas DataFrame
  based on the binning output from py_mob.pd_bin() function. 

  Parameters:
    xs      : A pandas DataFrame including all numeric vectors to do WoE 
              transformatons.
    bin_out : The dictionary of binning outcomes from py_mob.pd_bin(),
              e.g. pd_bin(y, xs)["bin_out"].

  Returns:
    A pandas DataFrame with identical headers as the input xs. However, values 
    of each variable have been transformed to WoE values.
  
  Example:
    df = pandas.DataFrame(py_mob.get_data("accepts"))
    
    rst = py_mob.pd_bin(df['bad'], df[['ltv', 'bureau_score', 'tot_derog']])

    out = py_mob.pd_woe(df[['ltv', 'bureau_score', 'tot_derog']], rst["bin_out"])

    out.head(2)
    #       ltv  bureau_score  tot_derog
    # 0  0.1619       -1.2560     0.6557
    # 1  0.0804       -1.1961    -0.3811
  """

  xnames = [_ for _ in bin_out.keys()]

  woe_out = dict([_, [w["woe"] for w in cal_woe(xs[_], bin_out.get(_))]] for _ in xnames)

  return(pandas.DataFrame(woe_out))

