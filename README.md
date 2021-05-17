# goodies

conda install jupyterlab

### TODO
```Python
# Under some unresolved circumstances pd.to_datetime()
# yields an object.  This ensures the desired type.
pd.to_datetime(ts, utc=True).astype('datetime64[ns]')

# Compare two dataframes.
np.allclose(one, two)
```
