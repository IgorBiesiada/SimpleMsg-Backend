import argparse
from models.messages import Message 
from models.user import User
from bcrypt import checkpw

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username")
parser.add_argument("-p", "--password")
parser.add_argument("-t", "--to")
parser.add_argument("-s", "--send")
parser.add_argument("-l", "--list", action="store_true")

args = parser.parse_args()

def list_messages(username, password):
    u = User.load_user_by_username(username)
    if u is None:
        print("Użytkownik o tej nazwie nie istnieje!")
        return

    
    if not checkpw(password.encode('utf-8'), u.hashed_password.encode('utf-8')):
        print("Błędne hasło!")
        return

    
    messages = Message.load_all_messages()
    print(f"\n--- Wiadomości dla użytkownika {username} ---")
    
    found = False
    for msg in messages:
        
        if msg[1] == u.id:
            found = True
            
            print(f"Od: {msg[0]} | Treść: {msg[2]}")
    
    if not found:
        print("Brak wiadomości do wyświetlenia.")

def send_message(username, password, to_username, text):
    
    sender = User.load_user_by_username(username)
    if not sender:
        print("Twój użytkownik nie istnieje!")
        return

    if not checkpw(password.encode('utf-8'), sender.hashed_password.encode('utf-8')):
        print("Błędne hasło!")
        return

    recipient = User.load_user_by_username(to_username)
    if not recipient:
        print(f"Adresat '{to_username}' nie istnieje!")
        return

    if len(text) > 255:
        print("Błąd: Wiadomość jest za długa (max 255 znaków)!")
        return

    new_msg = Message(from_id=sender.id, to_id=recipient.id, text=text)
    new_msg.save_to_db()
    print(f"Sukces! Wiadomość została wysłana do {to_username}.")

if __name__ == "__main__":
    if args.username and args.password and args.to and args.send:
        send_message(args.username, args.password, args.to, args.send)
    elif args.username and args.password and args.list:
        list_messages(args.username, args.password)
    else:
        print("Błąd")
    