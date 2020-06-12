# author - Sabyasachee Baruah
# This file contains the main calling function for the mica class pipeline

import os
import re
from parser.parse_scripts_noindent import parse_scripts
from connect.auto_gsheet import create_and_share_spreadsheet
from connect.auto_email import send_email

def run_pipeline(script_file, client_email, spreadsheet_title=None, parsed_scripts_folder="sample_scripts/parsed_scripts/", client_secret_file="connect/client-secret.json", project_email="micaclasssail@gmail.com"):
    '''
    Parses a screenplay file, creates a spreadsheet containing names of characters and their utterances and shares with client.
    Creates a blank demographics spreadsheet and shares with client asking them to fill it.

    Parameters
    ----------
    script_file : 
        Path to screenplay pdf.

    client_email : 
        Email address of the client.

    spreadsheet_title : 
        Name of the Google Sheets file created for writing the parsed output.
        If empty (None), a name will be created using the script_file and client_email.

    parsed_scripts_folder : 
        Folder where the parsed output will be stored.
        If folder is absent, it will be created. It defaults to sample_scripts/parsed_scripts/

    client_secret_file : 
        Json file that contains the credentials to connect to Google Sheets API
        See gspread documentation on how to create this.

    project_email: 
        Google account email associated with the project.
        All Google Sheets and emails are created and sent respectively using this account.
        If you wish to change this, you must also change the client_secret_file.
    '''

    # spreadsheet title is the name of the Google Sheets file containing the parser's output
    # create a spreadsheet title from script_file and client_email if it is empty
    # e.g. script_file = "*/Back_to_the_Future.pdf" and client_email = "rec-entertainment@xyz.com" creates 
    # spreadsheet_title = "Back_to_the_Future_rec_entertainment"
    script_filename = script_file.split("/")[-1].split(".")[0]
    if spreadsheet_title is None:
        client_name = client_email.split("@")[0]
        cleaned_script_filename = re.sub(r"[^a-zA-Z0-9_]", "_", script_filename)
        cleaned_client_name = re.sub(r"[^a-zA-Z0-9_]", "_", client_name)
        spreadsheet_title = cleaned_script_filename + "_" + cleaned_client_name

    # demographic title is the name of the Google Sheets file containing the demographic information of characters
    demographics_spreadsheet_title = spreadsheet_title + "_demographics"

    # create the parsed_scripts_folder if it doesn't exist
    # it is used to store the parser output - the parsed screenplay and character utterances
    os.makedirs(parsed_scripts_folder, exist_ok=True)
    
    print("parsing...")

    # parse the script_file and write the parser output and character utterances in two different files in parsed_scripts_folder
    # parser output file name is the script_file name appended with "_parsed"
    # utterances file name is the script_file name appended with "_parsed_abridged"
    parse_scripts(script_file, parsed_scripts_folder)
    utterances_file = os.path.join(parsed_scripts_folder, script_filename + "_parsed_abridged.txt")
    utterance_data = [["CHARACTER","UTTERANCE"]]
    character_to_nutter = {}

    print(f"{script_file} parsed...")
    print(f"character utterances in {utterances_file}...done\n")

    # find the character utterances from the utterances file
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

    # create Google spreadsheet and write the character utterances
    # share with client email
    print(f"creating {spreadsheet_title} google sheet and sharing...")
    create_and_share_spreadsheet(utterance_data, spreadsheet_title, client_email=client_email, client_secret_filepath=client_secret_file, project_email=project_email)

    # sort the characters in descending order of the number of utterances
    demographics_data = [["CHARACTER","GENDER","RACE"]]
    characters = sorted(character_to_nutter.keys(), key = lambda ch: character_to_nutter[ch], reverse=True)
    for ch in characters:
        demographics_data.append([ch, "", ""])
    
    # creates a Google spreadsheet with columns CHARACTER, GENDER and RACE
    # only the CHARACTER column is filled
    # share with client email with the email notification requesting to fill in the demographic data
    print(f"creating {demographics_spreadsheet_title} google sheet and sharing...")
    create_and_share_spreadsheet(demographics_data, demographics_spreadsheet_title, client_email=client_email, client_secret_filepath=client_secret_file, project_email=project_email, email_message="Please share demographics information")

    print("..done")

if __name__ == "__main__":
    # run_pipeline("sample_scripts/scripts/Avengers_Endgame.pdf", "sabyasachee.1301@gmail.com", spreadsheet_title="avengers_endgame")
    # run_pipeline("sample_scripts/scripts/afterthewedding_screenplay.pdf", "sabyasachee.1301@gmail.com", spreadsheet_title="after_the_wedding")

    run_pipeline("sample_scripts/scripts/ampwga.pdf", "somandep@usc.edu", spreadsheet_title="ampwga")
