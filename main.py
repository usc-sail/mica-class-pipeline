import os
import re
from parser.parse_scripts_noindent import parse_scripts
from connect.auto_gsheet import create_and_share_spreadsheet
from connect.auto_email import send_email

def run_pipeline(script_file, client_email, spreadsheet_title=None, parsed_scripts_folder="sample_scripts/parsed_scripts/", client_secret_filepath="connect/client-secret.json", project_email="micaclasssail@gmail.com"):
    script_filename = script_file.split("/")[-1].split(".")[0]
    if spreadsheet_title is None:
        client_name = client_email.split("@")[0]
        cleaned_script_filename = re.sub(r"[^a-zA-Z0-9_]", "_", script_filename)
        cleaned_client_name = re.sub(r"[^a-zA-Z0-9_]", "_", client_name)
        spreadsheet_title = cleaned_script_filename + "_" + cleaned_client_name
    demographics_spreadsheet_title = spreadsheet_title + "_demographics"
    os.makedirs(parsed_scripts_folder, exist_ok=True)
    
    print("parsing...")

    parse_scripts(script_file, parsed_scripts_folder)
    utterances_file = os.path.join(parsed_scripts_folder, script_filename + "_parsed_abridged.txt")
    utterance_data = [["CHARACTER","UTTERANCE"]]
    character_to_nutter = {}

    print(f"{script_file} parsed...")
    print(f"character utterances in {utterances_file}...done\n")

    with open(utterances_file) as fr:
        lines = fr.read().strip().split("\n")
        for line in lines:
            character, utterance = line.split("=>")
            character = character.strip()
            utterance = utterance.strip()
            utterance_data.append([character, utterance])
            
            if character not in character_to_nutter:
                character_to_nutter[character] = 0
            character_to_nutter[character] += 1

    print(f"creating {spreadsheet_title} google sheet and sharing...")
    create_and_share_spreadsheet(utterance_data, spreadsheet_title, client_email=client_email, client_secret_filepath=client_secret_filepath, project_email=project_email)

    demographics_data = [["CHARACTER","GENDER","RACE"]]
    characters = sorted(character_to_nutter.keys(), key = lambda ch: character_to_nutter[ch], reverse=True)
    for ch in characters:
        demographics_data.append([ch, "", ""])
    
    print(f"creating {demographics_spreadsheet_title} google sheet and sharing...")
    create_and_share_spreadsheet(demographics_data, demographics_spreadsheet_title, client_email=client_email, client_secret_filepath=client_secret_filepath, project_email=project_email, email_message="Please share demographics information")

    print("..done")

if __name__ == "__main__":
    # run_pipeline("sample_scripts/scripts/Avengers_Endgame.pdf", "sabyasachee.1301@gmail.com", spreadsheet_title="avengers_endgame")
    run_pipeline("sample_scripts/scripts/afterthewedding_screenplay.pdf", "sabyasachee.1301@gmail.com", spreadsheet_title="after_the_wedding")