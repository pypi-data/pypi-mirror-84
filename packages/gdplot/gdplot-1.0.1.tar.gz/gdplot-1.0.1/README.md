# Project description

'gdplot' is a library to generate  charts of predefined format and produce a chart of specific nature, i.e average sales and timeperiod, using the data available in google sheets.
It requires your google credentials and the file access to produce a chart.

  - No credentials saved
  

# Links
        GitHub: https://github.com/sumankumar0091/gdplot
        PyPI: https://pypi.org/project/gdplot/
        Documentation: 
        Issue Tracker:https://github.com/sumankumar0091/gdplot/issues
        Download: 
  

# Installation
This package runs under Python3.5+, use [pip](https://pip.pypa.io/en/stable/)  to install:
> - $ pip install gdplot  

# Get google Credentials
Log into the [Google Developers Console](https://accounts.google.com/ServiceLogin/signinchooser?service=cloudconsole&passive=1209600&osid=1&continue=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fpypi.org%2F&followup=https%3A%2F%2Fconsole.developers.google.com%2F%3Fref%3Dhttps%3A%2F%2Fpypi.org%2F&flowName=GlifWebSignIn&flowEntry=AddSession) with the Google account to the spreadsheets you want to access. Create (or select) a project and enable the Drive API and Sheets API (under Google Apps APIs).

Go to the Credentials for your project and create New credentials > OAuth client ID > of type Other. In the list of your OAuth 2.0 client IDs click Download JSON for the Client ID you just created. Save the file as client_secrets.json in your home directory (user directory). Another file, named storage.json in this example, will be created after successful authorization to cache OAuth data.
On you first usage of gsheets with this file (holding the client secrets), your webbrowser will be opened, asking you to log in with your Google account to authorize this client read access to all its Google Drive files and Google Sheets.

If this does not work refer to link under See also section. 

# Usage 
```
Syntax:
> import gdplot as gd
> gd.create_chart($credentials, $URL)
```

```
e.g.:
> import gdplot as gd
> gd.create_chart(/gcp_credentials/client_secret.json, https://docs.google.com/spreadsheets/d/1pzmXgLMMMWdsfuNuq3a15tP7kbsHpijVAU0BGAJrOAP/edit#gid=0)
```
### See also
''
https://medium.com/swlh/google-drive-api-with-python-part-i-set-up-credentials-1f729cb0372b 
(Source: https://medium.com/@billydharmawan)
https://medium.com/@osanda.deshan/getting-google-oauth-access-token-using-google-apis-18b2ba11a11a
(Source: https://medium.com/@osanda.deshan)
''
### License
This package is distributed under the **[MIT license](https://opensource.org/licenses/MIT).**








