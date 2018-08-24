from flask import Flask, render_template
from pycode.services.query_models import company_info as ci
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/companies')
def companies():
    companiesList = ci.get_company_all()
    return render_template('companies.html', companies = companiesList)


@app.route('/companies/<name>')
def companiesByName(name):
    companiesList = ci.get_company_name(name)
    return render_template('companies.html', companies = companiesList)


if __name__ == '__main__':
    app.run()
