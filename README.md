# DropSave
An automated file organizer. Files are extracted from a designated 'DropSave' folder and, based on the file name, stored in their appropriate destination folders with a datestamp prepended to the name. The script uses the first word in the file name to determine where to ultimately save the file.

For example, a file named `receipt March Cable Payment.pdf` would be saved into a receipts folder unde the name `YYMMDD_MarchCablePayment.pdf`

## Setup
This uses `pipenv` to manage the virtual env and all dependencies. If you don't have pipenv install it [here](https://pypi.org/project/pipenv/) then:

```
git clone https://github.com/automagictv/dropsave.git
cd dropsave
pipenv install --ignore-pipfile
```

To run:

```
pipenv run python runner.py
```

If you want to set this up on a cron, you can do something like:

```
# Run at 12:05 AM every day
5 0 * * * TOKEN='YOURTOKEN' LOGFILE='/path/to/logfile' pipenv run python runner.py >> /path/to/cronlog.txt 2>&1
```

You may have to add `/usr/local/bin` to your path for the above to work.

# Architecture

## config.py
Contains the configuration file for the program. This is where the source 'DropSave' folder and various destination folders are set, along with the folder arguments (e.g. in the example above, 'receipt')

## destination_factory.py
Dynamically builds destination paths when given the source directory contents.

## dropbox_helper.py
Helper module to handle dropbox actions.

## runner.py
The control file that runs the full program.
