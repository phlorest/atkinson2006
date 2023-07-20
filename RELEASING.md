# Releasing

- Install in editable mode:
  ```shell
  pip install -e .[test]
  ```
- Re-create the CLDF dataset:
  ```shell
  cldfbench makecldf --glottolog-version v4.8 cldfbench_atkinson2006.py --with-zenodo --with-cldfreadme
  ```
- Make sure the CLDF is valid:
  ```shell
  pytest
  ```
- Re-create the README:
  ```shell
  cldfbench readme cldfbench_atkinson2006.py
  ```
