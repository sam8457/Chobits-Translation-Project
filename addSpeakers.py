#!/usr/bin/env python3


import json
from pprint import pprint


def addNames():
    # Use this to add names to textboxes to aid in translation, requires tran_script.json file to already exist

    # Add more names as found. Refer to faceExploration.txt for method of finding
    names = {
        bytes.fromhex("1001"):"Hideki",
        bytes.fromhex("1003"):"Chi",
        bytes.fromhex("1004"):"Ms. Hibiya",
        bytes.fromhex("1007"):"Shinbo",
        bytes.fromhex("100A"):"Sumomo",
        bytes.fromhex("1005"):"Ms. Shimizu",
    }

    tran_file = open('tran_script.json','r')
    tran_data = json.loads(tran_file.read())
    tran_file.close()

    orig_file = open('SLPM_652.55.fontmodded', 'rb')
    input_data = orig_file.read()
    orig_file.close()

    limit = 999999 # originally used for testing
    index = 0

    for nth_box, box_data in tran_data.items():

        if index >= limit:
            break

        try:
            n_less_1_box = tran_data[str(int(nth_box) - 1)]
        except KeyError:
            print("Skipping first/last value.")
            continue

        prev_offset = n_less_1_box["end_offset"]
        this_offset = box_data["end_offset"]

        this_box_data = input_data[prev_offset:this_offset]

        for code, name in names.items():

            if code in this_box_data:

                tran_data[nth_box]["name"] = name

        index += 1

    with open('tran_script.json','w') as file:
        json.dump(tran_data, file, ensure_ascii=False, indent=2)

'''
  "0": {
    "end_offset": 1061803,
    "orig": "東京か…やっぱ都会だよなぁ。\nオレの田舎なんか、緑と牛しか\nなくてまったりしてたんだけど、",
    "orig_len": 88,
    "custom?": false,
    "tran": "Tokyo... Really is the big\ncity, eh? Back home, there's\njust grass and cows, so lax.",
    "tran_len": null,
    "shorten?": null
  },
'''


if __name__ == "__main__":

    addNames()