from flask import Flask, render_template
from flask import request
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from DB import SqlDB
import os

app = Flask(__name__)

DB = SqlDB()

db_host = os.environ.get('POSTGRES_HOST', 'database')
db_port = os.environ.get('POSTGRES_PORT', '5432')
db_user = os.environ.get('POSTGRES_USER', 'postgres')
db_password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
db_name = os.environ.get('POSTGRES_DB', 'postgres')

conn = DB.connect(user=db_user, password=db_password, host=db_host, port=db_port, database=db_name)
# conn = DB.connect(user='postgres', password='9580', host='localhost', port='5432', database='postgres')

DB.create_tables()


@app.route("/")
def route():
    return render_template("Home_page.html")


@app.route('/new_client', methods=["POST", "GET"])
def new_client():
    if request.method == "POST":
        try:
            prams = {
                "id": request.form.get('id'),
                "full_name": None if request.form.get('fullName') == '' else request.form.get('fullName'),
                "address": None if request.form.get('address') == '' else request.form.get('address'),
                "phone_number": None if request.form.get('telephone') == '' else request.form.get('telephone'),
                "cell_phone": None if request.form.get('cellphone') == '' else request.form.get('cellphone'),
                "date_of_birth": None if request.form.get('birthday') == '' else request.form.get('birthday')
            }
            DB.append_record(DB.MEMBERS_TABLE, prams)
        except errors.lookup(UNIQUE_VIOLATION) as _:
            return render_template("fail.html", error="This ID already exists in the database")
        except Exception as e:
            return render_template("fail.html", error=e)
        return render_template("success.html")
    else:
        return render_template("new_client.html")


@app.route('/new_covid', methods=['POST', 'GET'])
def new_covid():
    if request.method == 'POST':
        vaccination_number = int(request.form.get('vaccination_number'))

        manufacturer = ''
        vaccination_date = ''
        for i in range(1, vaccination_number + 1):
            key = "vaccine_" + str(i)
            manufacturer += request.form.get(key + "_manufacturer") + " , "
            vaccination_date += request.form.get(key + "_date") + " , "

        if len(manufacturer) > 0:
            manufacturer = manufacturer[:-2]
            vaccination_date = vaccination_date[:-2]
        print(type(request.form.get('positive')))
        prams = {
            "id": request.form.get('id'),
            "vaccination_date": None if vaccination_date == '' else vaccination_date,
            "manufacturer": None if manufacturer == '' else manufacturer,
            "positive_result_date": None if request.form.get('positive') == '' else request.form.get('positive'),
            "recovery_date": None if request.form.get('recovery') == '' else request.form.get('recovery')
        }
        try:
            DB.append_record(DB.COVID_TABLE, prams)
        except errors.lookup(UNIQUE_VIOLATION) as _:
            return render_template("fail.html", error="This ID already exists in the database")
        except Exception as e:
            return render_template("fail.html", error=e)
        return render_template("success.html")
    else:
        return render_template("new_covid.html")


@app.route('/retrieve_members', methods=['GET'])
def retrieve_members():
    DB.get_data(DB.MEMBERS_TABLE)
    return render_template(f"{DB.MEMBERS_TABLE}_data.html")


@app.route('/retrieve_covid', methods=['GET'])
def retrieve_covid():
    DB.get_data(DB.COVID_TABLE)
    return render_template(f"{DB.COVID_TABLE}_data.html")


@app.route('/not_vaccinated', methods=['GET'])
def not_vaccinated():
    try:
        number = DB.not_vaccinated()
    except Exception as e:
        return render_template("fail.html", error=e)
    return render_template("not_vaccinated.html", count=number)


@app.route('/active_patient', methods=['GET'])
def active_patient():
    try:
        DB.active_patient()
    except Exception as e:
        return render_template("fail.html", error=e)
    return '<h1 style ="text-align: center"> Active Patients For Each Day Per Specific Month</h1>' \
           '<center><img src="static/images/active_patient.png" width=600 "></center>'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
