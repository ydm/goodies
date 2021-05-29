# goodies

conda install jupyterlab

### TODO
```Python
# Under some unresolved circumstances pd.to_datetime()
# yields an object.  This ensures the desired type.
pd.to_datetime(ts, utc=True).astype('datetime64[ns]')

# Compare two dataframes.
np.allclose(one, two)

Multi indexing:
                     alpha
date       asset          
2019-03-20 A      0.000000
           B      0.920731
           C      0.703412
           D      0.596373
           E      0.611381
...                    ...
2021-05-27 V     -0.010958
           W      1.676388
           X      1.445200
           Y      0.952216
           Z      1.646791

[20800 rows x 1 columns]

alpha.loc[(slice('2020-01-01', '2020-02-01'), slice(None)),:]

                     alpha
date       asset          
2020-01-01 A     -0.713335
           B     -0.458934
           C      0.072503
           D      0.230143
           E     -0.354242
...                    ...
2020-02-01 V      2.790067
           W      1.998978
           X      3.426980
           Y      2.649550
           Z      2.438424

[832 rows x 1 columns]

```
