from models import *


def add_score(score_sheet, field, score):
  score_range = int(score / 100)
  if score_range > 9: score_range = 9
  score_sheet.fields[field][score_range] += 1

def clear_score_count(year):
    year_key = "score_sheets__%s__exists" % year

    collections = [State, City, School]
    for institution in collections:
        for institution in institution.objects(**{year_key: True}):
            institution.score_sheets.clear()

def get_or_create_score_sheet(institution, year, fields):
    if not institution.score_sheets.get(year):
        institution.score_sheets[year] = ScoreSheet()

        for field in fields:
            institution.score_sheets[year].fields[field] = [0 for n in xrange(0, 10)]

    return institution.score_sheets[year]


def parse(line_data):
    return {
      "school": { "code": line_data[203:211] },
      "city": {
        "code": line_data[211:218],
        "name": line_data[218:318].strip()
      },
      "state": {
        "code": line_data[211:213],
        "acronym": line_data[368:370]
      },
      "score": {
        "cn": line_data[536:545].strip(),
        "ch": line_data[545:554].strip(),
        "lc": line_data[554:563].strip(),
        "mt": line_data[563:572].strip()
      }
    }
    

with open("static/data/enem_cidade_sao_paulo.txt") as f:
    count = 0
    total_lines = len(list(f))

    f.seek(12)
    year = f.read(4)

    print("Limpando contagem de notas de %s..." % year)
    clear_score_count(year)
    print("... pronto")
    print("")
    print("total de linhas a serem lidas: %i" % total_lines)

    f.seek(0)
    print("0%..")
    for line in f:
        data = parse(line)

        state = State.objects.get_or_create(code=data["state"]["code"],
            defaults={"acronym": data["state"]["acronym"]})[0]

        city = City.objects.get_or_create(code=data["city"]["code"],
            defaults={ "name": data["city"]["name"], "state": state})[0]

        institutions = [state, city]
        try:
            school = School.objects.get(code=data["school"]["code"])
            institutions.append(school)
        except: pass

        fields = data["score"].keys()
        for institution in institutions:
            score_sheet = get_or_create_score_sheet(institution, year, fields)

            for field in data["score"].keys():
                try:
                    score = int(float(data["score"][field]))
                    add_score(score_sheet, field, score)

                except ValueError: pass

            institution.save()


        count += 1
        if count % 1000 is 0:
            print("..%s%%.." % str(count*100/total_lines))

    print("..100%")
