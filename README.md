# Action1-Python-Reports-to-CSV
## An Action1 script to automate export of the specified reports across organizations in CSV format.

### How To Use:

#### Set Your Client ID and Secret

##### Use .env.example to create .env file 
---------
Create a .env file and specify the API_KEY and API_SECRET obtained from the Action1 platform.
Use the .env.example fole for reference
You may find your credentials on the Conosle in the 'API Credentials' menu. https://app.action1.com/console/credentials
Please read https://www.action1.com/api-documentation for more information.
---------

#### Create a list of REPORT_IDS

##### Navigate to the Action1 console, select a report, extract its ID from the URL
--------- 
Specify report IDs of the reports you would like to export.
IDs can be fount in the report URLs i.e.: 'https://app.action1.com/console/reports/installed_software_1719901847858/summary?details=no&from=0&limit=50&live_only=no&org=<>'
where 'installed_software_1719901847858' is the report ID
Add IDs to the REPORT_IDS in the app.py
---------

#### Specify a location to save reports
##### Modify the REPORTS_LOCATION variable in app.py:
---------
Specify a location to save reports:
REPORTS_LOCATION = "C:\Action1_Reports"
---------

