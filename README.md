### Install the required packages and virtual environment 
```bash
python -m venv env 
pip install -r requirements.txt 
```

### Activate the virtual environment 

```bash
#Windows 
./env/Scripts/activate 
#mac/linux 
source env/bin/activate 
```

### Run the tracker server on a node first 

```bash
python tracker.py 
```

### Run the application 

```bash
python main.py 
```