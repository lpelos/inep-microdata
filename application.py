# -*- coding: utf-8 -*-
from flask import Flask, jsonify, redirect, render_template
from models import *

app = Flask(__name__)

@app.route('/')
def root():
    return redirect("/histogramas/sp/cidades/3550308")


@app.route('/histograms/<state_acronym>/cities/<city_code>', methods=["GET"])
@app.route('/histogramas/<state_acronym>/cidades/<city_code>', methods=["GET"])
def histograms(state_acronym="SP", city_code="3550308"):
    city = City.objects.get(code=city_code)

    # to-do: descobrir como fazer query que traga apenas os registros que
    # contenham qualquer chave em score_sheets, como score_sheets__exists
    # (que não funciona)
    schools = School.objects(
        city=city, score_sheets__2011__exists=True).order_by('name')

    schools_index = {school.name.encode('ascii', 'ignore'): str(school.code) for school in schools}

    return render_template("histograms/index.jinja2",
        city={"name": city.name, "state":city.state.acronym},
        schools=schools_index)


@app.route('/api/histograms/<year>/schools/<school_code>', methods=["GET"])
def histograms_school(school_code, year="2011"):

    def scores_obj(fields):
        score_obj = {"absolute": fields, "relative": {}}

        for field in fields:
            total = sum(fields[field])
            score_obj["relative"][field] = [score*100/total for score in fields[field]]

        return score_obj

    try:
        school = School.objects.get(code=school_code)
        city = school.city
        state = school.state

        school_scores = scores_obj(school.score_sheets[year].fields)
        city_scores = scores_obj(city.score_sheets[year].fields)

        state_scores = scores_obj(state.score_sheets[year].fields)

        return jsonify({
            "year": year,
            "code": school.code,
            "name": school.name,
            "school_scores": school_scores,
            "city_scores": city_scores,
            "state_scores": state_scores
        })

    except KeyError:
        return jsonify({"error": "Sem dados para esta instituicao"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)