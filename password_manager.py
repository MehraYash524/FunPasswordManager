from cryptography.fernet import Fernet
import os
import pandas as pd

def write_key():
    if not os.path.exists('key.key') or is_key_empty():
        key = Fernet.generate_key()
        with open('key.key', 'wb') as f:
            f.write(key)
        
def is_key_empty():
    file_size = os.path.getsize('key.key')
    if file_size == 0:
        return True
    else: 
        return False
    

write_key()    

       
def load_key(): 
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key

                
key = load_key()
fer = Fernet(key)


def is_master_empty():
    file_size = os.path.getsize('master.txt')
    if file_size == 0:
        return True
    else:
        return False

    
def is_view_empty():
    file_size = os.path.getsize('Password.txt')
    if file_size == 0:
        return True
    else:
        return False

   
def delete_master_contents():
    file = open('master.txt', 'w')
    file.truncate()
    file.close()
    
def delet_uf_contents():
    file = open('Password.txt', 'w')
    file.truncate()
    file.close()
    
    
def m_pwd():
    pwd = input("Register your master password: ")
    with open('master.txt', 'a') as f:
        f.write(fer.encrypt(pwd.encode()).decode())    
                    
def read_mpwd():
            file = open('master.txt', 'r')
            mpwd = file.read()
            file.close()
            set_password = fer.decrypt(mpwd.encode()).decode()
            return set_password


def view():
    data = {}
    w = []
    u = []
    p = []
    with open('Password.txt', 'r') as f:
        for i in f.readlines():
            file = i.rstrip()
            web, user, passw = file.split('|')
            w.append(web)
            u.append(user)
            p.append(fer.decrypt(passw.encode()).decode())
    data['Website'] = w
    data['User Name'] = u
    data['Password'] = p  
    df = pd.DataFrame(data)
    check = int(input("\n1. Search specific through website\n2. View all passwords \n"))
    if check == 1:
        w_name = input(f"Enter the name of website (spelling sensitive):\nWebsites present :{w} ").lower()
        if w_name.strip("''") in w:
            print(df[df['Website'] == w_name.strip("''")])
        else:
            print("Website's name not matching!")
    elif check == 2:
        print(f"\n{df}\n")
    else:
        print("Invalid Input!")
    
    
 
                       
def add():
    user_name = input("Enter your user name : ")
    pwd = input("Enter your password: ")
    Website = input("Enter the name of related website: ").lower()
                    
    with open('Password.txt', 'a') as f:    
        f.write(Website + '|' + user_name + '|' + fer.encrypt(pwd.encode()).decode() + "\n")

def check_master():
    if not os.path.exists('master.txt') or is_master_empty():
        print('\nMaster password does not exist, first set the master password and try again!')
    else:
        master_pwd = input("Enter the master password to proceed continue: ")
        set_password = read_mpwd()
        if set_password == master_pwd and set_password != '':
            return True
        else:
            print("Wrong master password!\nIf you forget your master password select option 5 from main menu.\n")

def get_int(prompt):
    while True:
        n = input(prompt)
        if n.isdigit():
            n = int(n)
            if 1 <= n <= 6:
                break
            else:
                print('Enter between 1 to 6')
                continue
        else:
            print("Enter a number: ")
            continue
    return n    
            
def main():
    print(("\n================================ Welcome to the Password Manager.================================").upper())
    
    while True:
        choice = get_int(f"""\nChoose from the options below to perform certain operation. Select from (1-6)
1. View Passwords
2. Add Passwords
3. Edit Usernames or Passwords
4. Set Master Password
5. Forget Master Password
6. Exit!\nYou choose: """)
        
        if choice == 1:
            if check_master():
                if not os.path.exists('Password.txt') or is_view_empty():
                    print('\nThere is no username or password to view.')
                else:
                    while True:
                        view()
                        if input("Press Enter to view again or (q) to quit to main menu: ").lower() == 'q':
                            break
                        else:
                            continue
            
        
        elif choice == 2:
            if check_master():
                while True:
                    add()
                    if input("Press Enter to add again or (q) to quit to main menu: ").lower() == 'q':
                        break
                    else:
                        continue
            
                            
        elif choice == 3:
            print("\nThis feature does not exist currently! I will add it if I decided to make it more reliable.")
        
        elif choice == 4:
            if not os.path.exists('master.txt') or is_master_empty():                                       
                m_pwd()
                print("Congratulations... You successfully created your master password.")
                print(input("Enter to continue..."))
                
            else:
                print('\nMaster Password already exist\n')
                print(input("Press Enter to continue"))
        
        elif choice == 5:
            
            print("\nThis action can not be undone! It will delet your all saved passwords.")
            wish = int(input("""1. To continue the termination
2. Abort\n"""))
            if wish == 1:
                delete_master_contents()
                delet_uf_contents()
                print('Termination of master password is sucessful!')
        
        elif choice == 6:
            print("Exiting...")
            break
main()