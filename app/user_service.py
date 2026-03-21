import argparse
from auth.auth_user import auth_required, login
import httpx

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username")
parser.add_argument("-p", "--password")
parser.add_argument("-n", "--new_pass")
parser.add_argument("-l", "--list", action="store_true")
parser.add_argument("-d", "--delete", action="store_true")
parser.add_argument("-e", "--edit", action="store_true")
parser.add_argument("-fn", "--first_name")
parser.add_argument("-ln", "--last_name")
parser.add_argument("-lo", "--login", action="store_true")

args = parser.parse_args()

def get_client(token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return httpx.Client(base_url="http://127.0.0.1:8000", headers=headers)


def create_user(token, username, password, first_name, last_name):
    
    if len(password) < 8:
        print("Za krotkie hasło")
    
    payload = {'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name}

    with get_client(token) as client:
        resp = client.post("/register", json=payload)
        print(resp.json())

@auth_required
def edit_users_password(token, old_password, new_password):
    
    if len(new_password) < 8:
        print("Za krotkie hasło")
        return 
    
    payload = {'old_password': old_password, 'new_password': new_password}

    with get_client(token) as client:
        resp = client.put("/update_password", json=payload)
        print(resp.json())


@auth_required
def delete_user(token):

    with get_client(token) as client:
        resp = client.delete("/delete")
        print(resp.json())

@auth_required
def users_list(token):
    
    with get_client(token) as client:
        resp = client.get("/users_list")
        print(resp.json())

if __name__ == "__main__":
    if args.username and args.password and args.first_name and args.last_name:
        create_user(args.username, args.password, args.first_name, args.last_name)
    
    elif args.username and args.password and args.edit and args.new_pass:
        edit_users_password(username=args.username, old_password=args.password, new_password=args.new_pass)
    
    elif args.delete:
        delete_user()
    
    elif args.list:
        print(users_list())
    
    elif args.login and args.username and args.password:
        login(args.username, args.password)
    
    else:
        parser.print_help()