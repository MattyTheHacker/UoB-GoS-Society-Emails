import json

def save_emails_to_file(list):
    # save the list to a file
    with open('emails.txt', 'w') as file:
        for item in list:
            file.write("%s\n" % item)

def save_societies_to_file(list):
    # save the list to a file
    with open('societies.txt', 'w') as file:
        for item in list:
            file.write("%s\n" % item)

def save_dict_to_json(dict):
    # save the dict to a file
    with open('emails.json', 'w') as file:
        json.dump(dict, file)