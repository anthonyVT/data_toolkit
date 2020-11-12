# data_toolkit
*tool kit for data team*

**step 1** (optional*)
- create virtual enviroment
- **RUN** python3 -m venv virtual

**step 2** (optional*)
- enter virtual enviroment
- **RUN** source virtual/bin/activate

**step 3**
- install packages
- **RUN** pip install -r requirements.txt

**step 4**
- initialized your enviroment
- **RUN** ./init.sh

pre-requisite:
- [google sdk](https://cloud.google.com/sdk/docs/install) is needed.
- you should reach to the project manager (currently is CTO) for the related IAM permissions.

### data_agent.py

- edit config.json to set up your task.

- *source* is the data source. eg. **mysql**, **bigquery**

- *query_path* is the path of sql file.

- *gsheets_key* is unique id of google sheet. you can find it the google sheet url.

- you *must* share the google sheet to *vt-etl-agent@lithe-window-713.iam.gserviceaccount.com*

- *sheet_prefix* is the prefix of worksheets.


\*Step1 & 2 are optional.
