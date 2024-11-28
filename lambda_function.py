import gspread
from oauth2client.service_account import ServiceAccountCredentials

def last_x_days(currency_series,number_of_days):
    r = requests.get('https://www.bankofcanada.ca/valet/observations/{}/json?recent={}'.format(currency_series,number_of_days))
    if r.status_code != 200:
        return 'Failed to retrieve data'
    else:
        df = pd.DataFrame(r.json()['observations'])
        df.rename(columns={'d':'Date',currency_series:'Value'},inplace=True)
        df['Value'] = df['Value'].apply(lambda x:float(x['v']))
        df['Currency_Label'] = currency_series
        return df
    
    def data_between_dates(start_date,end_date,currency_series):
    r = requests.get('https://www.bankofcanada.ca/valet/observations/{}/json?start_date={}&end_date={}'.format(currency_series,start_date,end_date))
    if r.status_code != 200:
        return 'Failed to retrieve data'
    else:
        df = pd.DataFrame(r.json()['observations'])
    df.rename(columns={'d':'Date',currency_series:'Value'},inplace=True)
    df['Value'] = df['Value'].apply(lambda x:float(x['v']))
    df['Currency_Label'] = currency_series
    return df

df = data_between_dates('2023-01-01','2024-07-29','FXUSDCAD')

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Add your credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('dev-voice-429818-u7-a152c79581e2.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(credentials)

# Open the google spreadsheet (using the title of the sheet)
spreadsheet = client.open('USD to CAD')

# Select the first sheet
sheet = spreadsheet.sheet1

df = df.astype(str)
rows = df.values.tolist()
existing_rows = len(sheet.get_all_values())

sheet.append_rows(rows,existing_rows)

import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
