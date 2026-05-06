numbers = [1, 2, 3, 4, 5, 6]

total = 0

for num in numbers:
    if num % 2 == 0:
        total = total + num

print("Sum of even numbers:", total)
