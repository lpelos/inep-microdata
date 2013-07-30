import csv
from models import *

with open("static/data/sudeste-estados-cidades-escolas.csv", "r") as f:
    lines = csv.reader(f, delimiter=",")

    state = last_state_code = None
    city = last_city_code = None
    count = 0
    total_lines = len(list(f))
    f.seek(0)

    print("0%..")
    for line in lines:
        state_acronym, city_code, city_name, school_code, school_name = line
        state_code = city_code[0:2]

        if state_code is not last_state_code:
            state = State.objects.get_or_create(code=state_code, defaults={"acronym": state_acronym})[0]
            last_state_code = state_code

        if city_code is not last_city_code:
            city = City.objects.get_or_create(code=city_code, defaults={"name": city_name, "state": state})[0]
            last_city_code = city

        school = School.objects.get_or_create(code=school_code, defaults={"name": school_name, "city": city, "state": state})[0]

        count += 1
        if count % 1000 is 0:
            print("..%s%%.." % str(count*100/total_lines))

    print("..100%")
