age = int(input("Enter your age: "))

has_id_input = input("Do you have an ID card? (true/false): ").strip().lower()

if has_id_input == "true":
    has_id = True
elif has_id_input == "false":
    has_id = False
else:
    print("Invalid input for ID. Please enter true or false.")
    exit()

if age >= 18 and has_id:
    print("Entry allowed")
else:
    print("Entry denied")