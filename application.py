# -*- coding: utf-8 -*-
from flask import Flask, jsonify, redirect, render_template
from models import *

app = Flask(__name__)

@app.route('/')
def root():
    return redirect("/histogramas/sp/cidades/3550308")


@app.route('/histograms/<state_acronym>/cities/<city_code>', methods=["GET"])
@app.route('/histogramas/<state_acronym>/cidades/<city_code>', methods=["GET"])
def histograms(year=2011, state_acronym="SP", city_code="3550308"):
    city = City.objects.get(code=city_code)
    schools = [{"code": school.code, "name": school.name} for school in
        School.objects(city=city).order_by('name')]

    return render_template("histograms/index.jinja2",
        city={"name": city.name, "state":city.state.acronym}, schools=schools)


@app.route('/api/histograms/<int:year>/schools/<school_code>', methods=["GET"])
def histograms_school(school_code, year=2011):
    try:
        school = School.objects.get(code=school_code)
        city = school.city
        state = school.state

        def scores_obj(fields):
            score_obj = {"absolute": fields, "relative": {}}

            for field in fields:
                total = sum(fields[field])
                score_obj["relative"][field] = [score*100/total for score in fields[field]]

            return score_obj

        school_scores = scores_obj(ScoreSheet.objects.get(
            year=year, ref=school).fields)

        city_scores = scores_obj(ScoreSheet.objects.get(
            year=year, ref=city).fields)
        
        state_scores = scores_obj(ScoreSheet.objects.get(
            year=year, ref=state).fields)


        return jsonify({
            "year": year,
            "code": school.code,
            "name": school.name,
            "school_scores": school_scores,
            "city_scores": city_scores,
            "state_scores": state_scores
        })

    except DoesNotExist:
        # to-do: retornar resposta http adequada
        return jsonify({"error": "Sem dados para esta instituicao"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)