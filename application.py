# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
from models import *

app = Flask(__name__)

@app.route('/histogram/<int:year>/<institution_code>')
def histograms_show(year=2011, institution_code=35):
    institution = { "code": institution_code, "name": "" }
    try:
        if len(institution_code) is 2:
            institution = State.objects.get(code=institution_code)
            institution.name = institution.acronym
        elif len(institution_code) is 7:
            institution = City.objects.get(code=institution_code)
            institution.name = institution.name
        elif len(institution_code) is 8:
            institution = School.objects.get(code=institution_code)
            institution.name = institution.name
        else:
            raise DoesNotExist

        score_sheet = ScoreSheet.objects.get(year=year, ref=institution).fields
        score_sheet["year"] = year

        return render_template('histograms/show.jinja2', institution=institution, score_sheet=score_sheet)

    except DoesNotExist:
        return "Código da instituição incorreto: não "

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)