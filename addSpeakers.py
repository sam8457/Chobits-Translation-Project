#!/usr/bin/env python3


import json
from pprint import pprint


def addNames():
    # Use this to add names to textboxes to aid in translation, requires tran_script.json file to already exist

    # Add more names as found. Refer to faceExploration.txt for method of finding
    # Some lines don't contain names, when that happens it keeps the same face as last time
    names = {
        bytes.fromhex("1000"):"Hidden/Unknown",
        bytes.fromhex("1001"):"Hideki",
        bytes.fromhex("1002"):"Speaker 1002", # 18 matches
        bytes.fromhex("1003"):"Chi",
        bytes.fromhex("1004"):"Ms. Hibiya",
        bytes.fromhex("1005"):"Ms. Shimizu",
        bytes.fromhex("1006"):"Yumi",
        bytes.fromhex("1007"):"Shinbo",
        bytes.fromhex("1008"):"Speaker 1008", # 428, Minoru?, mentions Chobits
        bytes.fromhex("1009"):"Mr. Omura",
        bytes.fromhex("100A"):"Sumomo",
        bytes.fromhex("100B"):"Speaker 100B", # 25 matches
        bytes.fromhex("100C"):"Speaker 100C", # 89 matches
        bytes.fromhex("100D"):"Speaker 100D", # 56 
        bytes.fromhex("100E"):"Speaker 100E", # 201
        bytes.fromhex("100F"):"Speaker 100F", # 79
        bytes.fromhex("1010"):"Speaker 1010", # 4
        bytes.fromhex("1011"):"Speaker 1011", # 21
        bytes.fromhex("1012"):"Speaker 1012", # 0 
        bytes.fromhex("1013"):"Speaker 1013", # 0
        bytes.fromhex("1014"):"Speaker 1014", # 35 
        bytes.fromhex("1015"):"Speaker 1015", # 35
        bytes.fromhex("1016"):"Speaker 1016", # 0
        bytes.fromhex("1017"):"Speaker 1017", # 0
        bytes.fromhex("1018"):"Speaker 1018", # 0
        bytes.fromhex("1019"):"Speaker 1019", # 0
        bytes.fromhex("101A"):"Speaker 101A", # 0
        bytes.fromhex("101B"):"Speaker 101B", # 0
        bytes.fromhex("101C"):"Speaker 101C", # 0
        bytes.fromhex("101D"):"Speaker 101D", # 0
        bytes.fromhex("101E"):"Speaker 101E", # 0
        bytes.fromhex("101F"):"Speaker 101F", # 0, have not looked after this
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

        found = False
        for code, name in names.items():

            # Don't overwrite with later ones if it already has a match
            if found:
                break

            if code in this_box_data:

                tran_data[nth_box]["name"] = name
                found = True 

        index += 1

    with open('tran_script.json','w') as file:
        json.dump(tran_data, file, ensure_ascii=False, indent=2)



if __name__ == "__main__":

    addNames()