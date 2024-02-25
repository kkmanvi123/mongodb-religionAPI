import csv
import json

population_by_state = {
    "CA": 38889770, "TX": 30976754, "FL": 22975931, "NY": 19469232, "PA": 12951275, "IL": 12516863, "OH": 11812173,
    "GA": 11145304, "NC": 10975017, "MI": 10041241, "NJ": 9320865, "VA": 8752297, "WA": 7841283, "AZ": 7497004,
    "TN": 7204002, "MA": 7020058, "IN": 6892124, "MO": 6215144, "MD": 6196525, "WI": 5931367, "CO": 5914181,
    "MN": 5761530, "SC": 5464155, "AL": 5143033, "LA": 4559475, "KY": 4540745, "OR": 4227337, "OK": 4088377,
    "CT": 3625646, "UT": 3454232, "IA": 3214315, "NV": 3210931, "AR": 3089060, "KS": 2944376, "MS": 2940452,
    "NM": 2115266, "ID": 1990456, "NE": 1988698, "WV": 1766107, "HI": 1430877, "NH": 1405105, "ME": 1402106,
    "MT": 1142746, "RI": 1098082, "DE": 1044321, "SD": 928767, "ND": 788940, "AK": 733536, "VT": 647818,
    "WY": 586485
}

def csv_to_json(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location_info = {
                "address": {
                    "street": row["ADDRESS"],
                    "street2": row["ADDRESS2"],
                    "city": row["CITY"],
                    "state": row["STATE"],
                    "zip": row["ZIP"],
                    "zip4": row["ZIPP4"],
                    "county": row["COUNTY"]
                },
                "coordinates": [float(row["X"]),float(row["Y"])],
                "state_pop": population_by_state.get(row["STATE"]),
            }
            institution_info = {
                "name": row["NAME"],
                "contact": {
                    "telephone": row["TELEPHONE"]
                },
                "subtype": row["SUBTYPE"],
                "denomination": {
                    "name": row["DENOM"],
                    "members": row["MEMBERS"],
                    "attendance": row["ATTENDANCE"]
                },
                "location_type": row["LOC_TYPE"],
                "religious_affiliation": {
                    "protestant": row["PROT"],
                    "catholic": row["CATH"]
                }
            }
            other_info = {
                "fips": row["FIPS"],
                "contact": {
                    "date": row["CONTDATE"],
                    "how": row["CONTHOW"]
                },
                "geo": {
                    "date": row["GEODATE"],
                    "how": row["GEOHOW"],
                    "link_id": row["GEOLINKID"],
                    "precision": row["GEOPREC"]
                },
                "naics": {
                    "code": row["NAICSCODE"],
                    "description": row["NAICSDESCR"]
                },
                "vendor": {
                    "name": row["ST_VENDOR"],
                    "version": row["ST_VERSION"]
                },
                "phone_location": row["PHONELOC"],
                "qc_qa": row["QC_QA"]
            }
            data = {
                "location_info": location_info,
                "institution_info": institution_info,
                "other_info": other_info
            }
            yield json.dumps(data, separators=(',', ':'))

def main():
    csv_file = "All_Places_of_Worship.csv"
    output_json_file = "places_of_worship.json"
    with open(output_json_file, 'w') as jsonfile:
        for line in csv_to_json(csv_file):
            jsonfile.write(line + '\n')

if __name__ == "__main__":
    main()

