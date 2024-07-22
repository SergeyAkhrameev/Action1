import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

class Action1:
    def __init__(self,REPORTS_LOCATION, ORGANIZATION_ID=None):
        load_dotenv()
        self.clientId = os.getenv('API_KEY')
        self.clientSecret = os.getenv('API_SECRET')
        self.initial_location = REPORTS_LOCATION
        self.organizationId = ""
        self.organizationName = ""
        self.accessToken = ""
        self.reportId = ""
        self.current_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")

    def get_accessToken(self):
        data = {"client_id":self.clientId, "client_secret":self.clientSecret}
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        url = "https://app.action1.com/api/3.0/oauth2/token"
        req = requests.post(url, headers=headers, data=data).text
        result = json.loads(req)
        self.accessToken = result['access_token']
        return self.accessToken
    
    def set_report_id(self, REPORT_ID):
        self.reportId = REPORT_ID

    def set_organization_id(self, ORGANIZATION_ID):
        self.organizationId = ORGANIZATION_ID

    def set_organization_name(self, ORGANIZATION_NAME):
        self.organizationName = ORGANIZATION_NAME

    def export_report(self):
        url = "https://app.action1.com/api/3.0/reportdata/{}/{}/export?format=csv".format(self.organizationId, self.reportId)
        headers = {"Authorization":"Bearer {}".format(self.accessToken)}
        print(url)
        # Make the request
        try:
            req = requests.get(url, headers=headers)
            req.raise_for_status()
            # Determine content type
            content_type = req.headers.get('Content-Type')
            # Handle CSV response
            if 'text/csv' in content_type and req.text.strip():
                # Read CSV content
                csv_content = req.text
                # Ensure the reports directory exists
                reports_dir = os.path.join(self.initial_location, f'{self.current_time}_reports')
                organization_dir = os.path.join(reports_dir, self.organizationName)

                if not os.path.exists(organization_dir):
                    os.makedirs(organization_dir)
        
                # Save CSV content to a file
                file_path = os.path.join(organization_dir,'{}.csv'.format(self.reportId))
                with open(file_path, 'w', newline='') as csvfile:
                    csvfile.write(csv_content)
                print(f"CSV content saved to {file_path}")
            else:
                print(f"No data available for report {self.reportId} in organization {self.organizationName}")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred for report {self.reportId} in organization {self.organizationName}: {http_err}")
        except Exception as err:
            print(f"An error occurred for report {self.reportId} in organization {self.organizationName}: {err}")
        finally:
            pass

    def get_organizations(self):
        url = "https://app.action1.com/api/3.0/organizations"
        headers = {"Authorization": "Bearer {}".format(self.accessToken)}
        req = requests.get(url, headers=headers)
        # Check for HTTP errors
        if req.status_code != 200:
            req.raise_for_status()
        result = json.loads(req.text)       
        organizations = [{"id": org["id"], "name": org["name"]} for org in result['items']]
        for org in organizations:
            print(f"Organization ID: {org['id']}, Organization Name: {org['name']}")
        return organizations
