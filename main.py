from get_houses import get_bamboo_houses
from format_data import convert_to_df, save_to_csv

response = get_bamboo_houses()

if response.status_code == 200:
    df = convert_to_df(response=response)
    save_to_csv(df=df)

else:
    print("Request failed with status code:", response.status_code)

