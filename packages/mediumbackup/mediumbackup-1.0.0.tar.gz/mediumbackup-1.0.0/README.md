# mediumbackup - A Backup Utility for Medium

Saves all your Medium stories locally as html or markdown files. 

## Installation
```
pip install mediumbackup
```

## Usage
### As a script from the command line
```
python -m mediumbackup "<your username>"
```
### As a module
```
import mediumbackup as mb

username = "<your username>"
mb.backup_stories(username)
```

## Options

Specify a Folder.
``` 
python -m mediumbackup --backup_dir "backup 2020-11-01"
```
Save as markdown.
``` 
python -m mediumbackup --format "md"
```
