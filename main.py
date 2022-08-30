import requests
from datetime import datetime
import os

GENDER = "male"
WEIGHT_KG = "75"
HEIGHT_CM = "175"
AGE = "38"

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")


headers = {
    "x-app-id": APP_ID,
    "x-app-key":API_KEY,
}

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
workout_sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

exercise_query = input("Tell me what exercise you did: ")

exercise_parameters = {
    "query": exercise_query,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

exercise_response = requests.post(url=exercise_endpoint, json=exercise_parameters, headers=headers)
exercise_data = exercise_response.json()


today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_headers = {
    "Authorization": f"Bearer {os.environ.get('TOKEN')}"
}

for exercise in exercise_data["exercises"]:
    sheet_input = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=workout_sheet_endpoint, json=sheet_input, headers=sheety_headers)
    print(sheet_response.text)
