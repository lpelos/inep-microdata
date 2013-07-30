import csv
from models import *

with open("static/data/sudeste-estados-cidades-escolas.csv", "r") as f:
    lines = csv.reader(f, delimiter=",")

    state = last_state_code = None
    city = last_city_code = None
    count = 0

    for line in lines:
        state_acronym, city_code, city_name, school_code, school_name = line
        state_code = city_code[0:2]

        if state_code is not last_state_code:

            state = State.objects(code=state_code).first()
            if not state:
                state = State(code=state_code, acronym=state_acronym)
                state.save()

            last_state_code = state_code


        if city_code is not last_city_code:

            city = City.objects(code=city_code).first()
            if not city:
                city = City(code=city_code, name=city_name, state=state)
                city.save()

            last_city_code = city


        school = School.objects(code=school_code).first()
        if not school:
            school = School(code=school_code, name=school_name, city=city, state=state)
            school.save()

        count += 1
        if count % 1000 is 0: print(count)
