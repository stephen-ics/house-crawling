import csv 

def write_houses_csv(rows, csv_path):
    if not rows:
        raise ValueError("No rows to write")

    fieldnames = list(rows[0].keys())
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)