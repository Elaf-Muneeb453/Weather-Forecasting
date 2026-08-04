import random
import string
import pandas as pd


def generate_site_code():
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    numbers = "".join(random.choices(string.digits, k=3))
    return letters + numbers


def generate_site_data(count):
    data = []
    used_site_codes = set()
    used_coordinates = set()

    while len(data) < count:

        site_code = generate_site_code()
        latitude = round(random.uniform(-90, 90), 2)
        longitude = round(random.uniform(-180, 180), 2)

        # Skip duplicate site codes
        if site_code in used_site_codes:
            continue

        # Skip duplicate coordinates
        if (latitude, longitude) in used_coordinates:
            continue

        used_site_codes.add(site_code)
        used_coordinates.add((latitude, longitude))

        data.append(
            {
                "site_code": site_code,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    return pd.DataFrame(data)
