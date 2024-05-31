import pandas as pd
from matplotlib import pyplot as plt 
import seaborn as sns

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_spreadsheet(filename='sheets_key.json', spreadsheet_name='Body Measures') -> pd.DataFrame:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)
    gc = gspread.authorize(credentials)
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WQO93q8adtEC18akaUj9puZY3rrDTQRQXdCKKBKeBG8/edit?usp=sharing'
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet(spreadsheet_name)
    values = worksheet.get_all_values()
    dataframe = pd.DataFrame(values[1:], columns=values[0])
    return dataframe

def preprocess_body_dataframe(body_dataframe: pd.DataFrame) -> pd.DataFrame:
    body_dataframe['date'] = pd.to_datetime(body_dataframe[''], errors='coerce')
    body_dataframe = body_dataframe[body_dataframe.date.notna()]
    body_dataframe['weight'] = body_dataframe['Weight (kg)']
    body_dataframe['exercising'] = body_dataframe['Exercising (scale)']
    body_dataframe['diet'] = body_dataframe['Diet quality ']
    body_dataframe['protein'] = body_dataframe['Protein intake (g)']
    body_dataframe['kcal'] = body_dataframe['Daily cal (kcal)']
    body_dataframe = body_dataframe[['date', 'weight', 'exercising', 'diet','protein', 'kcal']]
    for label in ['weight', 'exercising', 'diet', 'protein', 'kcal']:
        body_dataframe[label] = pd.to_numeric(body_dataframe[label], errors='coerce')
    return body_dataframe

def plot_body_weight(figsize=(30,15)):
    df = preprocess_body_dataframe(load_spreadsheet())
    sns.set_theme(style='darkgrid')
    fig, ax = plt.subplots(figsize=figsize)

    sns.lineplot(data=df, x='date', y='weight', color=[.2,.8,1], ax=ax)
    sns.lineplot(x=df.date, y=df.weight.rolling(7).mean(), color=[1,0,0], ax=ax)
    sns.lineplot(x=df.date, y=df.weight.rolling(21).mean(), color=[0,1,0], ax=ax)

    plt.axvline(x=pd.to_datetime('2024-03-20'), color=[.9,.7,.3], linestyle='--') # Mudança p/ Santos
    plt.axvline(x=pd.to_datetime('2023-09-10'), color=[.9,.7,.3], linestyle='--') # Nascimento Xande
    plt.axvline(x=pd.to_datetime('2022-12-15'), color=[.9,.7,.3], linestyle='--') # Viagem Europa

    plt.axvline(x=pd.to_datetime('2023-01-01'), color=[1,0,0], linestyle='--')
    plt.axvline(x=pd.to_datetime('2024-01-01'), color=[1,0,0], linestyle='--')

    return fig
