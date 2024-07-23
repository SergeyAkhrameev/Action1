import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

class Action1:
    def __init__(self,REPORTS_LOCATION, ORGANIZATION_ID=None):
        load_dotenv()
        self.client_id = os.getenv('API_KEY')
        self.client_secret = os.getenv('API_SECRET')
        self.initial_location = REPORTS_LOCATION
        self.organization_id = ''
        self.organization_name = ''
        self.access_token = ''
        self.report_id = ''
        self.current_time = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")

    def get_access_token(self):
        data = {'client_id':self.client_id, 'client_secret':self.client_secret}
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        url = 'https://app.action1.com/api/3.0/oauth2/token'
        try:
            req = requests.post(url, headers=headers, data=data)
            req.raise_for_status()
            result = json.loads(req.text)
            self.access_token = result['access_token']
            return self.access_token
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except KeyError as key_err:
            print(f'Key error: {key_err}')
        except Exception as err:
            print(f'An error occurred: {err}')
    
    def set_report_id(self, REPORT_ID):
        self.report_id = REPORT_ID

    def set_organization_id(self, ORGANIZATION_ID):
        self.organization_id = ORGANIZATION_ID

    def set_organization_name(self, ORGANIZATION_NAME):
        self.organization_name = ORGANIZATION_NAME

    def export_report(self):
        url = 'https://app.action1.com/api/3.0/reportdata/{}/{}/export?format=csv'.format(self.organization_id, self.report_id)
        headers = {'Authorization':'Bearer {}'.format(self.access_token)}
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
                organization_dir = os.path.join(reports_dir, self.organization_name)

                if not os.path.exists(organization_dir):
                    os.makedirs(organization_dir)
        
                # Save CSV content to a file
                file_path = os.path.join(organization_dir,'{}.csv'.format(self.report_id))
                with open(file_path, 'w', newline='') as csvfile:
                    csvfile.write(csv_content)
                print(f'CSV content saved to {file_path}')
            else:
                print(f'No data available for report {self.report_id} in organization {self.organization_name}')
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred for report {self.report_id} in organization {self.organization_name}: {http_err}')
        except Exception as err:
            print(f'An error occurred for report {self.report_id} in organization {self.organization_name}: {err}')
        finally:
            pass

    def get_organizations(self):
        url = 'https://app.action1.com/api/3.0/organizations'
        headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
        req = requests.get(url, headers=headers)
        # Check for HTTP errors
        if req.status_code != 200:
            req.raise_for_status()
        result = json.loads(req.text)       
        organizations = [{'id': org['id'], 'name': org['name']} for org in result['items']]
        for org in organizations:
            print(f"Organization ID: {org['id']}, Organization Name: {org['name']}")
        return organizations
