# Working with DESI DR1 data


## 🚀 How to Use


This project requires Python version `>=3.10,<3.12` to ensure compatibility with key dependencies such as `astro-datalab`.  
Make sure your environment is using a supported Python version before running `poetry install`.

You can check your current version with:

```bash
python --version
```

### 📦 Poetry Setup
This project uses [`Poetry`](https://python-poetry.org/) for dependency management and environment isolation. If you don’t have Poetry installed, you can set it up with the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installing `Poetry`, you need to ensure it's available globally in your terminal. To do this, add the following line to your shell configuration file (`~/.bashrc`):
```
export PATH="$HOME/.local/bin:$PATH"
```


### ⚙️ Set Up and Run the Project

#### 1. Clone the repository

```bash
git clone https://github.com/kefrankk/working-with-desi.git
cd working-with-desi
```

#### 2. Install dependencies

```
poetry install
```
This will automatically create and activate a virtual environment for the project.


### ⚙️ Running the Code

The entry point of this project is the script `src/main.py`.
It allows you to query DESI DR1 spectra by providing coordinate ranges and (optionally) redshift.

#### 1. Start the script
```
poetry run python src/main.py
```

#### 2. Provide the input ranges
You will be asked to type the RA (Right Ascension) and Dec (Declination) ranges in the format:
```
Type the right ascension range (X.XXX, Y.YYY): 150.0, 151.0
Type the declination range (X.XXX, Y.YYY): 1.0, 2.0
```

Then, you can choose whether to also filter by redshift:
```
Do you want to search by redshift too? (y/n): y
Type the redshift range (X.XXX, Y.YYY): 0.01, 0.05
```
➡️ If you type n, the search will only use RA and Dec.


#### 3. Data retrieval

- The script queries SPARCL for galaxies in DESI DR1 that match your ranges.

- Results are saved automatically in the folder `./data/` as a compressed `.parquet` file.

- If the parquet file already exists, it will be reused instead of running a new query.

#### 4. Optional outputs

After retrieving the data, you can choose to export spectra in additional formats:

- **TXT**: ASCII file with wavelength, flux, and flux error (ready for STARLIGHT
).

- **FITS**: Flexible Image Transport System format (standard in astronomy).

Example prompts:
```
Do you want to create a .txt file with wavelength, flux and flux error for Starlight input? (y/n): y
Do you want to create a fits file? (y/n): n
```

### 🛠 What Can Be Changed

- **Saving directory**: by default, results are saved in `./data/`. You can edit this in `src/main.py` if you want another location.

- **Spectral type**: currently, the query is restricted to `spectype = 'GALAXY'`. You can modify this in the cons dictionary inside `main()` in `src/main.py`.

- **Output formats**: choose `.parquet`, `.txt`, `.fits`, or a combination.

- **File name**: default is `DESI_DR1_spec.parquet`, but you can change it in the function `main(saving_dir)` in `src/main.py`.




## 📚 Referências

- [Dark Energy Spectroscopic Instrument (DESI DR1)](https://data.desi.lbl.gov/doc/releases/dr1/)

- [SPectra Analysis and Retrievable Catalog Lab (SPARCL)](https://astrosparcl.datalab.noirlab.edu/)

