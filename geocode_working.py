import pandas as pd
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="merchant_geocoder")
df = pd.read_csv('active_merchants_feb_2026(active_merchants).csv')
latitudes = []
longitudes = []

for index, row in df.iterrows():
    address = str(row['MERCHANT_ADDRESS_LINE_1']) + ', ' + str(row['MERCHANT_CITY']) + ', ' + str(row['MERCHANT_ZIP']) + ', ' + str(row['MERCHANT_COUNTRY'])
    print(f"Processing {index+1}/{len(df)}: {address}")
    try:
        location = geolocator.geocode(address)
        latitudes.append(location.latitude if location else None)
        longitudes.append(location.longitude if location else None)
    except:
        latitudes.append(None)
        longitudes.append(None)
    time.sleep(1)

df['LATITUDE'] = latitudes
df['LONGITUDE'] = longitudes
df.to_csv('active_merchants_feb_2026_geocoded.csv', index=False)
print("Complete!")
