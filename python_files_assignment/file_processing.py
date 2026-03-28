#step1 :read numbers from file
numbers = []

with open("numbers.txt", "r") as file:
    print("file opened successfully")

    for line in file:
        clean_line = line.strip()    #remove spaces/newlines

        if clean_line: # avoid empty lines
            num = int(clean_line)
            numbers.append(num)

#step2: compute values
count = len(numbers)
total = sum(numbers)
average = total/count if count !=0 else 0

#step3: write logs
with open("results.log", "a") as log:
    log.write("File opened successfully\n")
    log.write(f"Read {count} numbers\n")
    log.write(f"Aversge: {average}\n")
    log.write("Processing completed\n")
    