# aiohttp-peewee-interview

### Step 1
You need to copy the file `config.example.yml` and name it `config.yml`

### Step 2
Write the settings for connecting to the database in the file `config.yml`

### Step 3
Install dependencies using the command  ```pipenv install```

### Step 4
Apply migrations to database using the command `python main.py --migrate`

### Step 5
Load initial data using the command `python main.py --import_data`

### Step 6
Launch the application using the command `python main.py --runserver`