# data_toolkit
*tool kit for data team*

**step 1**

- python3 -m venv {/path/to/new/virtual/environment}

**step 2**

- source {/path/to/new/virtual/environment}/bin/activate

**step 3**

- pip install -r reqirement.txt

### data_agent.py

- edit config.json to set up your task.

- *source* is the data source. eg. **mysql**, **bigquery**

- *query_path* is the path of sql file.

- *gsheets_key* is unique id of google sheet. you can find it the google sheet url.

- *sheet_prefix* is the prefix of worksheets.
