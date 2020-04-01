from time import sleep
from tqdm import tqdm
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_client(client_secret_filepath):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret_filepath, scope)
        gc = gspread.authorize(credentials)
        return gc
    except Exception as e:
        print("unable to get client")
        print(e)

def create_spreadsheet(client, title):
    try:
        sh = client.create(title)
        return sh
    except Exception as e:
        print("unable to create spreadsheet")
        print(e)

def delete_spreadsheet(client, id=None, title=None):
    try:
        if not id:
            client.del_spreadsheet(id)
        elif not title:
            for file in client.list_spreadsheet_files():
                if file["name"] == title:
                    client.del_spreadsheet(file["id"])
                    break
            else:
                print(f"spreadsheet {title} not found")
    except Exception as e:
        print("unable to delete spreadsheet")
        print(e)

def populate_spreadsheet(spreadsheet, data):
    try:
        ws = spreadsheet.sheet1
        nrows, ncols = len(data), len(data[0])
        cells = ws.range(1, 1, nrows, ncols)

        for r in range(nrows):
            for c in range(ncols):
                cells[r*ncols + c].value = data[r][c]

        ws.update_cells(cells)
    except Exception as e:
        print("unable to populate spreadsheet")
        print(e)

def share_spreadsheet(spreadsheet, email, message=""):
    try:
        spreadsheet.share(email, perm_type="user", role="writer", email_message=message)
    except Exception as e:
        print("unable to share spreadsheet")
        print(e)

def create_and_share_spreadsheet(data, spreadsheet_title, client_email, client_secret_filepath, project_email = "micaclasssail@gmail.com", email_message=""):
    client = get_client(client_secret_filepath)
    spreadsheet = create_spreadsheet(client, spreadsheet_title)
    share_spreadsheet(spreadsheet, project_email)
    populate_spreadsheet(spreadsheet, data)
    share_spreadsheet(spreadsheet, client_email, message=email_message)

def main():
    create_and_share_spreadsheet([["CHARACTER","UTTERANCE"],["LUCAS","I am a video game player."],["LUKE","I assemble computers"]], "test_sheet_2", "sabyasachee.1301@gmail.com", "client-secret.json")

if __name__ == "__main__":
    main()