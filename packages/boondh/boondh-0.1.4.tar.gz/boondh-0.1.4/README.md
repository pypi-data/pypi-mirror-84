# boondh
A Personal Library
- Encapsulate boilerplate code
- Data processing code
- ML Frameworks (NLP tasks - SeqClassification, Entity Extractions etc.)

# install
```bash
git clone https://github.com/rohit-mehra/boondh.git
cd boondh
pip install .
```

# sample use

> Parallelize any function
```python
from boondh import mp_func

def base_func(value, sq=True):
    if sq: return value ** 2
    return value

data = [0, 1, 2, 3, 4]
results = mp_func(base_func, 'value', data, sq=True)
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