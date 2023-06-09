# chess-opening-study

Overview:
* This tool lets you create your own 'opening book' (i.e. list of opening moves you would like to make) in a Google Sheet and connect that sheet to a Jupyter Notebook where you can easily study them, flashcard-style.

Installation:
* Clone the Repository
* Create Environment:
    * Option 1: Conda: `conda env create --name envname --file=environments.yml`
    * Option 2: pip:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Setup:
* Create a Google Workspace project
    * Go to https://console.cloud.google.com/
    * create a a Google Workspace project, then create a service account with the 'view' role, then create a key for that service account and download into a file 'credentials.json'
* Create a Google Sheet with 'White' and 'Black' tabs, each with opening moves enumerated
    * see examples below
    * Use indentation for deeper moves as shown. Must use official [Chess Algebraic Notation](https://en.wikipedia.org/wiki/Algebraic_notation_(chess)).
    * Each box should have two moves separated by a space (with the exception of the very first move), with the opponent's move first and the move to learn second.
    * Note: substitute the '#' character for any move to learn in the Google Sheet (e.g. '2...d5 3.#'), and the trainer will ignore that opening move. This can be useful when dealing with chess boards reached by multiple paths.
* Share the Google Sheet with the email address associated with the service account (grant 'View' access)
* In the root directory, create sheet_name.txt (a single-line text file with the Google Sheet name)
* Move credentials.json (from the Google Workspace step) to root directory

Usage:
* Once in the new Conda environment, run `jupyter notebook`
* Run the chunks in Train.ipynb

![Example Run](example_run.png)
![Example White](example_white.png)
![Example Black](example_black.png)
