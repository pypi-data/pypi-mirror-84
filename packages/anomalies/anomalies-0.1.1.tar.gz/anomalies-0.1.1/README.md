# Anomalies
Implement the anomaly free solution of  [arXiv:1905.13729](https://arxiv.org/abs/1905.13729)

## Install
```bash
$ pip install anomalies
```
## USAGE
```python
>>> from anomalies import anomaly
>>> anomaly.free([-1,1],[4,-2])
array([  3,   3,   3, -12, -12,  15])
>>> anomaly.free.gcd
3
>>> anomaly.free.simplified
array([ 1,  1,  1, -4, -4,  5])
```
