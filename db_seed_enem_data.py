from models import *

def add_score(ref, field, score):
  score_sheet = ScoreSheet.objects.get_or_create(year=year, ref=ref)[0]

  if not score_sheet.fields.get(field):
      score_sheet.fields[field] = [0 for n in xrange(0, 10)]

  score_range = int(score / 100)
  score_sheet.fields[field][score_range] += 1


def parse(line_data):
    return {
      "school": { "code": line_data[203:210] },
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

    f.seek(0)
    print("0%..")
    for line in list(f)[:10000]:
        data = parse(line)

        for field in data["score"].keys():
            try:
                score = int(float(data["score"][field]))

                state = State.objects.get_or_create(
                    code=data["state"]["code"],
                    defaults={
                        "acronym": data["state"]["acronym"]})[0]
                add_score(state, field, score)

                city = City.objects.get_or_create(code=data["city"]["code"],
                    defaults={
                        "name": data["city"]["name"],
                        "state": state})[0]
                add_score(city, field, score)

                school = School.objects(code=data["school"]["code"]).first()
                if school: add_score(school, field, score)

            except ValueError: pass

        count += 1
        if count % 500 is 0:
            print("..%s%%.." % str(float(count)*100.00/float(total_lines)))

    print("..100%")
