import pandas as pd

def convert_to_df(response):
    data = response.json()
    listings = data.get("listings", [])

    desired_fields = ["_id", "Title", "Address", "Price", "PostedDate", "LeaseType", "Buildingtype"]

    formatted_listings = []
    for listing in listings:
        formatted_listing = {field: listing.get(field) for field in desired_fields}
        formatted_listings.append(formatted_listing)

    df = pd.DataFrame(formatted_listings)

    return df

def save_to_csv(df):
    output_filename = "bamboo_housing_listings.csv"
    df.to_csv(output_filename, index=False)

