account_balance = int(input("Enter account balance: "))
withdrawal_amount = int(input("Enter withdrawal amount: "))
is_verified = input("Verified (true/false): ").lower() == "true"

print("\n--- Transaction Details ---")
print("Account Balance:", account_balance)
print("Withdrawal Amount:", withdrawal_amount)
print("Verified:", is_verified)

if is_verified and withdrawal_amount <= account_balance:
    remaining_balance = account_balance - withdrawal_amount
    print("\nWithdrawal successful")
    print("Remaining Balance:", remaining_balance)
else:
    print("\nTransaction denied")
