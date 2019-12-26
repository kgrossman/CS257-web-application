'''
    API.py
    Authors: Kate Grossman and Matt Stritzel
    Date: May 23, 2019
    CS257--Eric Alexander
    '''

import psycopg2
import csv
import sys
import flask
from flask import Flask, render_template, request
import json

database = 'stritzelm'
user = 'stritzelm'
password = 'lion627puppy'

state_list = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
              "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
              "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
              "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
              "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
              "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
              "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
              "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

cause_list = ["Influenza and pneumonia", "Kidney disease", "CLRD", "Stroke", "Suicide", "Cancer", "All causes", "Unintentional injuries", "Heart disease", "Alzheimer's disease", "Diabetes"]

''' Make connection to our database '''
try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()


''' Creates flask app '''
app = flask.Flask(__name__)


@app.route('/')
def hello():
    '''Displays welcome information when site is launched'''
    return render_template('main_page.html')


@app.route('/mostDeadly/<state>')
def get_most_deadly(state):
    
    deadliest_disease_in_state_list = get_most_deadly_from_db(state)
    return render_template('go_page.html', deadliest_disease_in_state_list=deadliest_disease_in_state_list, state=state)

def get_most_deadly_from_db(state):
    ''' Returns the most common cause of death in a user-specified state '''

    if state not in state_list:
        raise ValueError("Invalid value.")
    else:
        name = state
        deadliest_disease_in_state_json_list = []

        query = ("SELECT cause_name, SUM(amt_of_deaths) FROM main_data_categories WHERE state_name= '%s' GROUP BY cause_name ORDER BY sum DESC" % name)

        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()

        #Creates dictionary object w/ returned data from query; Adds dictionary to list; Returns list in json format '''
        for row in cursor:
            state_dict = {'cause': row[0], 'deaths': row[1]}
            deadliest_disease_in_state_json_list.append(state_dict)

        return deadliest_disease_in_state_json_list



@app.route('/mostDeathsInState')
def get_which_state_has_most_deaths():
    deadliest_states = get_which_state_has_most_deaths_from_db()
    return render_template('causes_killing_most_people_page.html', deadliest_states=deadliest_states)


def get_which_state_has_most_deaths_from_db():

    json_deadliest_state_list = []
    try:
        cursor = connection.cursor()
        query = 'SELECT state_name, SUM(amt_of_deaths) FROM main_data_categories GROUP BY state_name ORDER BY sum DESC'
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    # Creates dictionary object w/ returned data from query; Adds dictionary to list; Returns list in json format
    for row in cursor:
        deadliest_state_dict ={'state': row[0], 'deaths': row[1]}
        json_deadliest_state_list.append(deadliest_state_dict)
    return json_deadliest_state_list



@app.route('/trend/<cause_of_death>')
def get_national_trend(cause_of_death):
    trend_list = get_national_trend_from_db(cause_of_death)
    return render_template('frequency_search_page.html', trend_list=trend_list, cause_of_death=cause_of_death)


def get_national_trend_from_db(cause_of_death):
    ''' Returns nationwide deathtolls from 1999-2016 of a user-specified disease '''

    if cause_of_death not in cause_list:
        raise ValueError("Invalid value.")
    else:
        cause = cause_of_death
        json_trend_list = []
        try:
            cursor = connection.cursor()
            query = ("SELECT year, SUM(amt_of_deaths) FROM main_data_categories WHERE cause_name= '%s' GROUP BY year ORDER BY year ASC" %cause_of_death)
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()

        #Creates dictionary object w/ returned data from query; Adds dictionary to list; Returns list in json format
        for row in cursor:
            deaths_per_year_dict = {'year': row[0], 'deaths': row[1]}
            json_trend_list.append(deaths_per_year_dict)

    return json_trend_list



@app.route('/mainSearch')
def get_table():

    cause_name = flask.request.args.get('main_search_cause')
    state_name = flask.request.args.get('main_search_state')
    start_year = flask.request.args.get('main_search_start_year')
    end_year = flask.request.args.get('main_search_end_year')

    table_data = get_table_from_db(cause_name, state_name, start_year, end_year)

    return render_template('main_search.html', table_data=table_data, cause_name=cause_name, state_name=state_name,
                           start_year=start_year, end_year=end_year)


def get_table_from_db(cause_name, state_name, start_year, end_year):
    ''' Returns data asscociated w/ user-specified search categories '''
    start_year = int(start_year)
    end_year = int(end_year)
    print(start_year)

    table_list =[]

    if cause_name not in cause_list or state_name not in state_list or start_year>end_year or start_year<1999 or start_year>2016 or end_year<1999 or end_year>2016:
        raise ValueError("Invalid value.")

    else:

        try:
            cursor = connection.cursor()
            query = ("SELECT year, SUM(amt_of_deaths) FROM main_data_categories WHERE cause_name='%s' AND state_name='%s' AND year BETWEEN %s AND %s GROUP BY year ORDER BY year" % (cause_name, state_name, start_year, end_year))
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()


        #Creates dictionary object w/ returned data from query; Adds dictionary to list; Returns list in json format
        for row in cursor:
            table_dict = {'year': row[0], 'deaths': row[1]}
            table_list.append(table_dict)

    return table_list

@app.route('/README.html')
def return_readme():
    return render_template('README.html')

#connection.close()

''' MAIN '''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
