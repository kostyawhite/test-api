import requests
import json
from faker import Faker
import random
import configparser


parser = configparser.ConfigParser()
parser.read('config.ini')

URL = parser.get('service', 'url')
HEADERS = {'Content-Type': 'application/json'}

fake = Faker()


def create_fake_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "age": random.randint(1, 100),
        "mobile": fake.phone_number()
    }


def add_fake_user():
    responce = requests.request("POST", URL, data=json.dumps(
        create_fake_user()), headers=HEADERS)
    return responce.status_code


def get_last_created_user():
    return requests.get(URL).json()[-1]


def get_users():
    return requests.get(URL).json()


def get_user_id(user):
    return user["ID"]


def get_user_ids(users):
    return list(map(get_user_id, users))


def test_post_users():
    payload = create_fake_user()
    responce = requests.request("POST", URL, data=json.dumps(
        payload), headers=HEADERS)
    assert responce.status_code == 201


def test_get_last_created_user():
    last_created_user = get_last_created_user()
    id = last_created_user["ID"]
    responce = requests.get("{}{}".format(URL, id))
    assert responce.status_code == 200
    assert responce.json()["name"] == last_created_user["name"]
    assert responce.json()["email"] == last_created_user["email"]
    assert responce.json()["age"] == last_created_user["age"]
    assert responce.json()["mobile"] == last_created_user["mobile"]


def test_update_user_name():
    id = get_last_created_user()["ID"]
    payload = get_last_created_user()
    payload["name"] = fake.name()
    responce = requests.put("{}{}".format(URL, id), data=json.dumps(
        payload), headers=HEADERS)
    assert responce.json()["name"] == payload["name"]


def test_update_user_age():
    id = get_last_created_user()["ID"]
    payload = get_last_created_user()
    payload["age"] = random.randint(1, 100)
    responce = requests.put("{}{}".format(URL, id), data=json.dumps(
        payload), headers=HEADERS)
    assert responce.json()["age"] == payload["age"]


def test_update_user_email():
    id = get_last_created_user()["ID"]
    payload = get_last_created_user()
    payload["email"] = fake.email()
    responce = requests.put("{}{}".format(URL, id), data=json.dumps(
        payload), headers=HEADERS)
    assert responce.json()["email"] == payload["email"]


def test_update_user_mobile():
    id = get_last_created_user()["ID"]
    payload = get_last_created_user()
    payload["mobile"] = fake.phone_number()
    responce = requests.put("{}{}".format(URL, id), data=json.dumps(
        payload), headers=HEADERS)
    assert responce.json()["mobile"] == payload["mobile"]


def test_delete_user():
    id = get_last_created_user()["ID"]
    responce = requests.delete("{}{}".format(URL, id))
    assert responce.status_code == 200
    assert responce.text == "User deleted"


def test_user_does_not_exist():
    id = random.randint(1000, 2000)
    responce = requests.get("{}{}".format(URL, id))
    assert responce.status_code == 404


def test_get_random_user():
    user_ids = get_user_ids(get_users())
    id = random.choice(user_ids)
    responce = requests.get("{}{}".format(URL, id))
    assert responce.status_code == 200
