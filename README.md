# Working with DESI DR1 data


## 🚀 How to Use

This project requires [`Poetry`](https://python-poetry.org/) to be installed on your machine.  
If you don't have it yet, follow these steps:

- 📦 Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

- Then, add Poetry to your `PATH`:
```
export PATH="$HOME/.local/bin:$PATH"
```


### ⚙️ Set Up and Run the Project

#### 1. Clone the repository

```bash
git clone https://github.com/kefrankk/working-with-desi.git
cd working-with-desi
```

#### 2. Install dependencies and activate the virtual environment

```
poetry install
poetry run python src/main.py
```
This will automatically create and activate a virtual environment for the project.
