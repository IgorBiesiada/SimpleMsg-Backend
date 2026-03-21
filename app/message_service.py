import argparse
from user_service import get_client
from auth.auth_user import auth_required

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--to")
parser.add_argument("-tx", "--text")
parser.add_argument("-s", "--send")
parser.add_argument("-l", "--list", action="store_true")

args = parser.parse_args()

@auth_required
def list_messages(token):
    
    with get_client(token) as client:
        resp = client.get("/messages_list")
        
        if resp.status_code == 200:
            messages = resp.json()
            for message in messages:
                print(f"od {message['from_id']} || {message['text']}")

        else:
            print("Brak wiadomosci")    

@auth_required
def send_message(token, to_id: int, text: str):
    payload = {'to_id': to_id, 'text': text}
    
    with get_client(token) as client:
        resp = client.post("/message", json=payload)
        
        if resp.status_code == 200:
            print("Wiadomośc wysłana")
        else:
            print("Błąd")


if __name__ == "__main__":
    if args.send:
        if args.to and args.text:
            send_message(args.to, args.send, args.text)
        else:
            print("Błąd")
    
    elif args.username and args.password and args.list:
        list_messages()
    
    else:
        parser.print_help()
    