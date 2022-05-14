from google_drive_downloader import GoogleDriveDownloader as gdd
import pandas as pd
'''
    This file will attempt to download the csv file that contains all of the customer's appointment requests
    and tries to assign workers based on their availability and work notice.
'''

URL = "https://docs.google.com/spreadsheets/d/11G5X1aMFBRqRV7kphT3b1hZkr0KaAfs0P2GASoNZqE4/edit?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
df = pd.read_csv(path)
print(df.head())