from Action1 import Action1

# !!!!!!!!!--IMPORTANT--!!!!!!!!!
#Create a .env file and specify the API_KEY and API_SECRET obtained from the Action1 platform.
# Use the .env.example fole for reference
# You may find your credentials on the Conosle in the 'API Credentials' menu. https://app.action1.com/console/credentials
# Please read https://www.action1.com/api-documentation for more information.

# !!!!!!!!!--IMPORTANT--!!!!!!!!!
#Specify report IDs of the reports you would like to export.
#IDs can be fount in the report URLs i.e.: 'https://app.action1.com/console/reports/installed_software_1719901847858/summary?details=no&from=0&limit=50&live_only=no&org=<>'
#where 'installed_software_1719901847858' is the report ID

REPORT_IDS = ['reboot_required_1635422625514', 
              'missing_third_party___windows_updates_1671801861492', 
              'installed_software_1635264799139',
              'missing_third_party___windows_updates_1721580481382']

# !!!!!!!!!--IMPORTANT--!!!!!!!!!
#Specify a location to save reports:
REPORTS_LOCATION = '/Users/sergey/Downloads/'

act = Action1(REPORTS_LOCATION)
act.get_accessToken()
organizations = act.get_organizations()

for org in organizations:
    act.set_organization_id(org['id'])
    act.set_organization_name(org['name'])
    for report_id in REPORT_IDS:
        act.set_report_id(report_id)
        act.export_report()
