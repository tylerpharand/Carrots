import requests
import json
import datetime
import time
import schedule
import numpy as np

url = 'https://api.carrotrewards.ca/v1/steps'

# values can be found by sniffing POST requests
token = ''
signature = ''
user_agent = ''
authorization = ''

header = {
    'Content-Type': 'application/json',
    'X-Client-Token': token,
    'X-Request-Signature': signature,
    'X-Device-Platform': 'iOS',
    'X-Timezone-Offset': '-04:00',
    'Accept-Language': 'en',
    'X-App-Version': '1.7.9',
    'User-Agent': user_agent,
    'Authorization': authorization
}
success = 202  # request accepted
steps = 5700


def date_range(start, end):
    for n in range(int((end - start).days) + 1):
        yield start + datetime.timedelta(n)


def step_randomizer(step_count):
    return step_count + int(abs(np.random.normal(0, 0.15, 1)[0]*20000))


def set_steps(step_count, date):
    payload = [{"value": step_count, "timestamp": -1, "source": "iphone", "day": str(date)}]  # Format: "YYYY-MM-DD"
    response = requests.post(url, headers=header, data=json.dumps(payload))

    if response.status_code == success:
        print("🥕 Updated step count on {} to {}".format(date, step_count))
    else:
        print("Error: {}".format(response.status_code))
        print("Error: {}".format(response.content))

    return response


def carrot_today():
    start_date = datetime.date.today()
    end_date = datetime.date.today()
    carrot(start_date, end_date, steps)


if __name__ == '__main__':
    print("🥕 Carrots is up and running!")
    schedule.every().day.at("14:00").do(carrot_today)

    while 1:
        schedule.run_pending()
        time.sleep(10)

