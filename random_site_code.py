import random
import string
import pandas as pd


def generate_site_code():
    letters = "".join(random.choices(string.ascii_uppercase, k=3))
    numbers = "".join(random.choices(string.digits, k=3))
    return letters + numbers


def generate_site_data(count):
    data = []

    for i in range(count):
        data.append(
            {
                "site_code": generate_site_code(),
                "latitude": round(random.uniform(23.5, 37.5), 2),
                "longitude": round(random.uniform(60.5, 77.5), 2),
            }
        )

    return pd.DataFrame(data)


