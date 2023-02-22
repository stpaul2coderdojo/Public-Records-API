import json
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/lookup')
def lookup():
    phone_number = request.args.get('phone_number')
    if not phone_number:
        return json.dumps({'error': 'Phone number is required'}), 400

    # Call the People Finder API to get the person's information
    people_finder_url = 'https://api.peoplefinder.com/lookup'
    people_finder_params = {'phone_number': phone_number}
    people_finder_response = requests.get(people_finder_url, params=people_finder_params)
    if people_finder_response.status_code != 200:
        return json.dumps({'error': 'Failed to retrieve public records'}), 500
    people_finder_data = people_finder_response.json()

    # Call the IRS e-file API to get the person's W2 information
    irs_url = 'https://api.irs.gov/efile/w2s'
    irs_params = {'ssn': people_finder_data['ssn']}
    irs_response = requests.get(irs_url, params=irs_params)
    if irs_response.status_code != 200:
        return json.dumps({'error': 'Failed to retrieve W2 information'}), 500
    irs_data = irs_response.json()

    # Combine the data and return the response
    response_data = {
        'first_name': people_finder_data['first_name'],
        'last_name': people_finder_data['last_name'],
        'address': people_finder_data['address'],
        'w2': irs_data['w2']
    }
    return json.dumps(response_data), 200
