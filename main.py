import requests
import os
import datetime
from logo import logo

SHEETY_API_KEY = os.environ.get("Sheety_API_KEY")
NUTRITIONIX_API_ID = os.environ.get("Nutritionix_API_ID")
NUTRITIONIX_API_KEY = os.environ.get("Nutritionix_API_KEY")
SHEETY_ENDPOINT = os.environ.get("Sheety_endpoint")
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"


def get_calorie():

    """ Use Nutritionix API to get caloric output of exercise with plain language input """

    header = {
        "x-app-id": NUTRITIONIX_API_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "x-remote-user-id": "0",
    }

    nutritionix_params = {
        "query": input("\nWhat exercise did you perform? "),
        "gender": "male",
        "weight_kg": 60,
        "height_cm": 170,
        "age": 35
    }

    response = requests.post(url=NUTRITIONIX_ENDPOINT, json=nutritionix_params, headers=header)

    return response.json()


def update_sheets(date, time, exercise, duration, calories):

    """ Use Sheety API to upload exercise parameters to registered Google sheets document """

    header = {
        "Authorization": SHEETY_API_KEY,
        "Content-Type": "application/json"
    }

    sheets_params = {
        "sheet1": {
            "date": date,
            "time": time,
            "exercise": exercise.title(),
            "duration": duration,
            "calories": calories
        }
    }

    response = requests.post(url=SHEETY_ENDPOINT, json=sheets_params, headers=header).json()

    print(f"\nDate:{response['sheet1']['date']} \n"
          f"Time:{response['sheet1']['time']} \n"
          f"Exercise:{response['sheet1']['exercise']} \n"
          f"Duration:{response['sheet1']['duration']} \n"
          f"Calories:{response['sheet1']['calories']}"
          )


print(logo)

is_running = True

while is_running:

    today_date = datetime.datetime.now()
    today_date.strftime("%d/%m/%Y")

    exercise_results = get_calorie()

    update_sheets(
                date=today_date.strftime("%d/%m/%Y"),
                time=today_date.strftime("%H:%M:%S"),
                exercise=exercise_results["exercises"][0]["name"],
                duration=exercise_results["exercises"][0]["duration_min"],
                calories=exercise_results["exercises"][0]["nf_calories"]
                )

    if input("Add another exercise ? Yes or No ").lower() == "no":
        is_running = False

