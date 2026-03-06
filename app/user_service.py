import argparse
from models.user import User
from psycopg2.errors import UniqueViolation
from bcrypt import checkpw

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username")
parser.add_argument("-p", "--password")
parser.add_argument("-n", "--new_pass")
parser.add_argument("-l", "--list", action="store_true")
parser.add_argument("-d", "--delete", action="store_true")
parser.add_argument("-e", "--edit", action="store_true")
parser.add_argument("-fn", "--first_name")
parser.add_argument("-ln", "--last_name")

args = parser.parse_args()

def create_user(username, password, first_name, last_name):
    
    if len(password) < 8:
        print("Za krotkie hasło")
    
    try:
        u = User(username=username, password=password, first_name=first_name, last_name=last_name)
        u._insert()
    except UniqueViolation:
        print("Uzytkonik o takiej nazwie juz istnieje")

def edit_users_password(username, old_password, new_password):
    
    if len(new_password) < 8:
        print("Za krotkie hasło")
        return 
    
    u = User.load_user_by_username(username=username)
    
    if u is None:
        print("Błąd uzytkownik o takiej nazwie nie istnieje")
        return

    try:
        u.set_new_pass(old_password=old_password, new_password=new_password)
        u._update()
    except UniqueViolation:
        print("Uzytkonik o takiej nazwie nie istnieje")

def delete_user(username, password):

    u = User.load_user_by_username(username=username)
        
    if not u:
        print("Błąd uzytkownik o takiej nazwie nie istnieje")
        return 
    
    if len(password) < 8:
        print("Za krotkie hasło")

    if not checkpw(password.encode('utf-8'), u.hashed_password.encode('utf-8')):
        print("Incorrect Password!")
        return    
    
    try:
        u._delete(username=username)

    except UniqueViolation:      
        print("błąd")


def users_list():
    u = User.load_all_users()
    return u

if __name__ == "__main__":
    if args.username and args.password and args.first_name and args.last_name:
        create_user(args.username, args.password, args.first_name, args.last_name)
    elif args.username and args.password and args.edit and args.new_pass:
        edit_users_password(username=args.username, old_password=args.password, new_password=args.new_pass)
    elif args.username and args.password and args.delete:
        delete_user(args.username, args.password)
    elif args.list:
        print(users_list())
    else:
        parser.print_help()