#menu_of_Lumier:

def handler_menu(assistant):
        import os
        os.makedirs("user", exist_ok=True)
        assistant.remember_last_command()

        while True:
            cmd = input("How can I help you..: ").lower()

            if cmd == "last_command":
                assistant.remember_last_command()
                continue

            assistant.detect_mood(cmd)
            
            matched = False
            for command, keywords in assistant.command_map().items():
                if any(keyword in cmd for keyword in keywords):
                    if hasattr(assistant, command):
                        func = getattr(assistant, command)
                        if callable(func):
                            func()
                            matched = True
                            with open("user/last_command.txt", "w") as file:
                                file.write(command)
                            if command == "exit":
                                return
                            break
            
            if not matched:
                suggestion = assistant.closest_match(cmd)
                if suggestion:
                    choice = input(f"Did you mean '{suggestion}'? (yes/no): ").lower()
                    if choice == "yes":
                        func = getattr(assistant, suggestion)
                        if callable(func):
                            func()
                else:
                    print("Invalid command! Please try again.")