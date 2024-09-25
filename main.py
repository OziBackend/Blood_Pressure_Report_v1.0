from chatgptFunction import search_gpt
import json
from flask import Flask, jsonify, request, abort, render_template

app = Flask(__name__)

@app.route('/health-report', methods=['POST'])
def health_report():
    # Ensure all required fields are provided in the request
    required_fields = ['systolic', 'diastolic', 'heart_rate', 'patient_name', 'patient_age', 'patient_weight', 'patient_height', 'patient_gender']
    if not request.json or not all(field in request.json for field in required_fields):
        abort(400)

    # Extract the values from the request
    systolic = request.json['systolic']
    diastolic = request.json['diastolic']
    heart_rate = request.json['heart_rate']
    patient_name = request.json['patient_name']
    patient_age = request.json['patient_age']
    patient_weight = request.json['patient_weight']
    patient_height = request.json['patient_height']
    patient_gender = request.json['patient_gender']

    # Update the GPT prompt to include the new fields
    prompt = f"""I am a {patient_age}-year-old {patient_gender}, weighing {patient_weight} and standing {patient_height} tall. 
    My blood pressure is {systolic}/{diastolic} mmHg, and my heart rate is {heart_rate} bpm. 
    Generate a report, the response should only contain the dictionary object, properly formatted. 
    There should be no data other than the "value":
        {{
            "Interpretation": "value",
            "Caution": "value",
            "Medication": "value", 
            "Nutrition": "value",
            "Physical_Activity": "value",
            "Mental_Health": "value",
            "Preventive_Care": "value",
            "Sleep_Hygiene": "value",
            "Avoid_Harmful_Behaviors": "value" 
        }}"""

    # Call the GPT function to generate the/ report
    report = search_gpt(prompt)
    print("GPT Response:", report)  # Debug output

    try:
        # Parse the GPT response into a JSON object
        json_report = json.loads(report)
    except json.JSONDecodeError:
        print("Error decoding JSON:", report)
        abort(500)  # Internal server error

    # Add patient details to the report
    json_report['Patient_Name'] = patient_name
    json_report['Patient_Age'] = patient_age
    json_report['Patient_Weight'] = patient_weight
    json_report['Patient_Height'] = patient_height
    json_report['Patient_Gender'] = patient_gender
    json_report['systolic'] = systolic
    json_report['diastolic'] = diastolic
    json_report['heart_rate'] = heart_rate

    # Render the report in an HTML template
    test_report = render_template('report.html', **json_report)
    
    return test_report

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
