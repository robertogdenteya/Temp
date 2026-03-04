import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def geocode_address(address):
    geolocator = Nominatim(user_agent="merchant_geocoder")
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return geocode_address(address)  # Retry on timeout

def main():
    # Read the CSV file
    input_file = 'active_merchants_feb_2026(active_merchants).csv'
    output_file = 'active_merchants_feb_2026_geocoded.csv'
    merchants_df = pd.read_csv(input_file)

    # Construct full addresses
    merchants_df['FULL_ADDRESS'] = merchants_df['MERCHANT_ADDRESS_LINE_1'] + ', ' + 
                                    merchants_df['MERCHANT_CITY'] + ', ' + 
                                    merchants_df['MERCHANT_ZIP'] + ', ' + 
                                    merchants_df['MERCHANT_COUNTRY']

    # Initialize lists for latitude and longitude
    latitudes = []
    longitudes = []

    # Geocode each address
    for index, row in merchants_df.iterrows():
        address = row['FULL_ADDRESS']
        print(f"Geocoding: {address} (Row {index + 1}/{len(merchants_df)})")
        lat, long = geocode_address(address)
        latitudes.append(lat)
        longitudes.append(long)
        time.sleep(1)  # To avoid hitting the API too rapidly

    # Add latitude and longitude to the dataframe
    merchants_df['LATITUDE'] = latitudes
    merchants_df['LONGITUDE'] = longitudes

    # Save to a new CSV file
    merchants_df.to_csv(output_file, index=False)
    print(f"Geocoding completed. Results saved to {output_file}")

if __name__ == "__main__":
    main()