from flask import Flask, render_template, redirect, url_for, request, jsonify
import db

app = Flask(__name__)


@app.route("/")
def home():
   return render_template('consent.html')



@app.route('/survey', methods=['GET', 'POST'])
def surver():
    if request.method == 'POST':
        name = request.form.get('name')
        frequency = request.form.get('frequency')
        age = request.form.get('age')
        meal_time = request.form.get('meal')
        restaurant = 'restaurant' in request.form
        restaurant_name = request.form.get('conditionalRestaurant', '')

        db.insert_form(name, frequency, age, meal_time, restaurant, restaurant_name)

        print(request.form)
        print("{} -- {} -- {} -- {} -- {} -- {}".format(name, frequency, age, meal_time, restaurant, restaurant_name))
        return redirect(url_for('thanks', name=name))
    return render_template('survey.html')

@app.route("/decline")
def decline():
    return render_template('decline.html')


@app.route("/thanks")
def thanks():
    name = request.args.get('name', None)
    return render_template('thanks.html', name=name)


@app.route("/api/results")
def results():
    order = "reverse" if request.args.get('reverse') == 'true' else ""
    surveys = db.get_data(order)
    return jsonify(surveys)


@app.route("/admin/summary")
def summary():
    age = db.chart_get_age()
    meal_time = db.chart_get_meal_time()
    frequency = db.chart_get_frequency()
    text_responses = db.get_text_responses()
    responses_per_day = db.chart_get_responses_per_day()
    print(meal_time)
    print(responses_per_day)

    return render_template('summary.html', age=age, meal_time=meal_time, frequency=frequency, responses_per_day=responses_per_day, text_responses=text_responses)


if __name__ == '__main__':
   app.run()
