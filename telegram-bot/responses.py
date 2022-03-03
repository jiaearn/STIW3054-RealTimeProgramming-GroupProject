import collections
import json
import re
from datetime import datetime

import psycopg2


def get_data(message):
    ic_number = message.split("@")[0]
    phone_number = message.split("@")[1]
    try:
        conn = psycopg2.connect(
            "postgres://mrfknbsicvtqjo:40cb1909b8ae034538bb96ca0c1ec827d86753ba50548ada7c97fda44f162738@ec2-3-213-76-170.compute-1.amazonaws.com:5432/dhecvtd68dsm3",
            sslmode='require')
        cursor = conn.cursor()
        cursor.execute("SELECT ic,name,phone FROM victim_app_victim WHERE ic='{}' AND phone='{}'".format(ic_number, phone_number))
        conn.commit()
        output = cursor.fetchall()
        ic = [i[0] for i in output]
        name = [i[1] for i in output]
        hp = [i[2] for i in output]
        age = str(calculate_age(ic[0]))
        personal = "Maklumat Mangsa:\nNombor Pengenalan: " + str(ic[0]) + "\nNama: " + str(name[0]) + "\nNombor Telefon: " + str(
            hp[0]) + "\nUmur: " + age
        cursor.execute(
            "SELECT (SELECT a1.name FROM assistance_app_assistancetype a1 WHERE a1.id=a.assistance_type_id),a.victim_number,a.progress_percentage,a.is_approved,assistance_given_date FROM victim_app_victim v,assistance_app_assistance a WHERE a.victim_id = v.id AND v.ic='{}'".format(
                ic_number))
        conn.commit()
        result = cursor.fetchall()
        result_list = []
        for r in result:
            d = collections.OrderedDict()
            d["Assistance Type"] = str(r[0])
            d["Victim Number"] = str(r[1])
            d["Progress Percentage"] = str(r[2])
            d["Approval Status"] = str(r[3])
            d["Assistance Given Date"] = str(r[4])
            result_list.append(d)
        j = json.dumps(result_list)
        json_dictionary = json.loads(j)
        assistance_list = ""
        for key in json_dictionary:
            assistance = "Jenis Bantuan: " + key['Assistance Type'] + "\nJumlah Tanggungan: " + key[
                'Victim Number'] + "\nStatus Kelulusan: " + interpret_word(key[
                             "Approval Status"]) + "\n\n"
            print(assistance)
            assistance_list += assistance
        bot_response = personal + "\n--------------------------------------------------------------\n" + assistance_list
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        bot_response = "Maaf, saya tidak dapat mencari data anda... Sila semak semula dengan maklumat yang sah"

    return bot_response


def calculate_age(ic):
    ic_year = str(ic[:2])
    cur_year = datetime.now().year
    now = str(cur_year)[:2]
    if int(now + ic_year) <= cur_year:
        return int(cur_year) - (int(now + "00") + int(ic_year))
    else:
        return int(cur_year) - (int(now + "00") - 100 + int(ic_year))


def interpret_word(word):
    if word == "False":
        return "Belum Lulus"
    elif word == "True":
        return "Telah Dilulus"
    elif word == "None":
        return "Belum Diberi"
    else:
        word == ""


def process_message(message, response_array, response):
    # Split the message and the punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    # Scoring System
    score = 0
    for word in list_message:
        if word in response_array:
            score += 1

    print(score, response)
    return [score, response]


def get_response(message):
    # custom response
    response_list = [
        process_message(message, ['hello', 'hi', 'hey'], 'Hello!'),
        process_message(message, ['bye', 'goodbye'], 'Bye Bye, jumpa lagi!'),
    ]

    response_scores = []
    for response in response_list:
        response_scores.append(response[0])

    # Get the max value
    winning_response = max(response_scores)
    matching_response = response_list[response_scores.index(winning_response)]

    # Return the matching response
    if winning_response == 0:
        bot_response = 'Maaf, saya tidak faham apa yang anda maksudkan.'
    else:
        bot_response = matching_response[1]

    print('Bot response:', bot_response)
    return bot_response

# Test your system
# get_response('Hello')
