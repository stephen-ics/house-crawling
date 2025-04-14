from bamboo_housing.get_bamboo_houses import get_bamboo_listings
from bamboo_housing.format_bamboo_data import convert_to_df, save_to_csv

response = get_bamboo_listings()

if response.status_code == 200:
    df = convert_to_df(response=response)
    save_to_csv(df=df)

else:
    print("Request failed with status code:", response.status_code)

