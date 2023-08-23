import ctfd_manager as ctfdman
import flag_manager as flagman
import box_manager as boxman
import json

f = open('hosts.json')
targets = json.load(f)

known_ports = [80, 22, 64573]
check_only = False

for t in targets:
    print()
    print(f"[+] Configuring {t['ip_address']} for {t['name']}")
    should_inject = boxman.check_services(t, known_ports)
    
    if should_inject and not check_only:
        user_flag = flagman.generate_flag()
        inject_success = boxman.inject_flag(t, user_flag, mode="USER")
        print(f"[+] User flag is injected with value {user_flag}. Status: {inject_success}")
        if (inject_success):
            push_user_chall = ctfdman.create_challenge(name=f"[USER] {t['ip_address']}", description=t['ip_address'], category=t['name'])
            print(f"[+] Pushed user flag to CTFd with value {user_flag}. Status: {push_user_chall['success']}") 
            push_user_flag = ctfdman.create_flag(challenge_id=push_user_chall['data']['id'], flag=user_flag)
        
        root_flag = flagman.generate_flag()
        inject_success = boxman.inject_flag(t, root_flag, mode="ROOT")   
        print(f"[+] Root flag is injected with value {root_flag}. Status: {inject_success}") 
        if (inject_success):
            push_root_chall = ctfdman.create_challenge(name=f"[ROOT] {t['ip_address']}", description=t['ip_address'], category=t['name'])
            print(f"[+] Pushed root flag to CTFd with value {root_flag}. Status: {push_root_chall['success']}") 
            push_root_flag = ctfdman.create_flag(challenge_id=push_root_chall['data']['id'], flag=root_flag)    
    else:
        print(f"[!] Services of {t['name']} are unstable. Skipping...")
    
    print()


