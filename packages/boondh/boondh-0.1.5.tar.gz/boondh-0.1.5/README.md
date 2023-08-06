# boondh
A Personal Library
- Encapsulate boilerplate code
- Data processing code
- ML Frameworks (NLP tasks - SeqClassification, Entity Extractions etc.)

# install
```bash
pip3 install -U boondh
```

For nightly

```bash
git clone https://github.com/rohit-mehra/boondh.git
cd boondh
pip install .
```

# sample use

> Parallelize any function
```python
from boondh import mp_func

# Any function to be applied on each element of data
def base_func(value, sq=True):
    if sq: return value ** 2
    return value

# Any data
data = [0, 1, 2, 3, 4]

# Collected results - Ordered by default
results = mp_func(base_func, # apply this in parallel
                 'value', # the data argument name in above function
                  data, # contains elements to be processed
                  sq=True # any arg of the `to be applied` function
                  )
```

```python
# configure chunksize and set ordered as False for perfromance gain
results = mp_func(base_func, 'value', data, chunksize=200, ordered=False, sq=True)
```

> Arrange files in your directory (usually the `Download` directory.. :smile:)

- This will scan the directory and create `type folders` like `csv_`, `txt_` etc.
- Move respective filetypes into these folders.

```bash
python -m boondh.utils.arrange_files -D "$(pwd)"
```
OR
```bash
python -m boondh.utils.arrange_files -D /Users/<myusername>/Downloads/
```