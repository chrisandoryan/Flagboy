import ctfd_manager as ctfdman
import flag_manager as flagman
import box_manager as boxman
import json
import secrets

f = open('hosts.json')
targets = json.load(f)

known_ports = [80, 22, 4650, 7978]
check_only = False

for t in targets:
    target_name = t['name']
    print()
    print(f"[+] Configuring {t['ip_address']} for {target_name}")
    should_inject = boxman.check_services(t, known_ports)
    
    with open(f'./data/{target_name}.txt', 'w') as f:
        if should_inject and not check_only:
            user_flag = flagman.generate_flag()
            inject_success = boxman.inject_flag(t, user_flag, mode="USER")
            print(f"[+] User flag is injected with value {user_flag}. Status: {inject_success}")

            new_password = secrets.token_urlsafe(12)
            change_password_success = boxman.change_box_password(t, new_password, mode="USER")
            print(f"[+] User password is changed to: {new_password}. Status: {change_password_success}")

            if (inject_success and change_password_success):
                push_user_chall = ctfdman.create_challenge(name=f"[USER] {t['ip_address']}", description=t['ip_address'], category=t['name'])
                print(f"[+] Pushed user flag to CTFd with value {user_flag}. Status: {push_user_chall['success']}") 
                push_user_flag = ctfdman.create_flag(challenge_id=push_user_chall['data']['id'], flag=user_flag)
                f.write(f"user,{new_password},{user_flag}\n")
            
            root_flag = flagman.generate_flag()
            inject_success = boxman.inject_flag(t, root_flag, mode="ROOT")
            print(f"[+] Root flag is injected with value {root_flag}. Status: {inject_success}") 
            
            new_password = secrets.token_urlsafe(12)
            change_password_success = boxman.change_box_password(t, new_password, mode="ROOT")
            print(f"[+] Root password is changed to {new_password}. Status: {change_password_success}")

            if (inject_success and change_password_success):
                push_root_chall = ctfdman.create_challenge(name=f"[ROOT] {t['ip_address']}", description=t['ip_address'], category=t['name'])
                print(f"[+] Pushed root flag to CTFd with value {root_flag}. Status: {push_root_chall['success']}") 
                push_root_flag = ctfdman.create_flag(challenge_id=push_root_chall['data']['id'], flag=root_flag)    
                f.write(f"root,{new_password},{root_flag}\n")
        else:
            print(f"[!] Services of {t['name']} are unstable. Skipping...")
        
        print()


