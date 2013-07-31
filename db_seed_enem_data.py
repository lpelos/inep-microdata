from models import *

def add_score(ref, field, score):
  score_sheet = ScoreSheet.objects.get_or_create(year=year, ref=ref)[0]

  score_range = int(score / 100)
  if score_range > 9: score_range = 9

  if not score_sheet.fields.get(field):
      score_sheet.fields[field] = [0 for n in xrange(0, 10)]

  score_sheet.fields[field][score_range] += 1
  score_sheet.save()


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
    print("total de linhas a serem lidas: %i" % total_lines)

    f.seek(12)
    year = int(f.read(4))

    ScoreSheet.objects(year=year).delete()

    f.seek(0)
    print("0%..")
    for line in f:
        data = parse(line)

        state = State.objects.get_or_create(code=data["state"]["code"],
            defaults={"acronym": data["state"]["acronym"]})[0]

        city = City.objects.get_or_create(code=data["city"]["code"],
            defaults={ "name": data["city"]["name"], "state": state})[0]

        school = School.objects(code=data["school"]["code"]).first()

        for field in data["score"].keys():
            try:
                score = int(float(data["score"][field]))

                add_score(state, field, score)
                add_score(city, field, score)
                if school: add_score(school, field, score)

            except ValueError: pass

        count += 1
        if count % 500 is 0:
            print("..%s%%.." % str(float(count)*100.00/float(total_lines)))

    print("..100%")
