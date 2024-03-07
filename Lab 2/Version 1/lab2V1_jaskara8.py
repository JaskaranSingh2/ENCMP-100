# Copyright (c) 2022, University of Alberta
# Electrical and Computer Engineering
# All rights reserved.
#
# Student name: Jaskaran Singh (100%)
# Student CCID: jaskara8
# Others:
#
# To avoid plagiarism, list the names of persons, Version 0 author(s)
# excluded, whose code, words, ideas, or data you used. To avoid
# cheating, list the names of persons, excluding the ENCMP 100 lab
# instructor and TAs, who gave you compositional assistance.
#
# After each name, including your own name, enter in parentheses an
# estimate of the person's contributions in percent. Without these
# numbers, adding to 100%, follow-up questions may be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.
#
import numpy as np

print('Lab2 - Version 1')
# ----------Students write/modify their code below here ---------------------
code = input('Please enter a code to break: ')
code = np.array(list(code), dtype=int)
# The code in this version include an implementation of rules 1 and 2 and the partial implementation of Rule 3 and 4.

# Rule 1: If the array "code" is not 9 digits long, then the program will exit and print the message "Decoy Message: Not a nine-digit number."
if len(code) != 9:
    print("Decoy Message: Not a nine-digit number.")

# Rule 2: If the sum of the array "code" is even, then the program will exit and print the message "Decoy Message: Sum is even."
elif sum(code) % 2 == 0:
    print("Decoy Message: Sum is Even.")

else:
    # Rule 3: Multiplying the 3rd digit by the 2nd digit and subtracting the 1st digit then displaying the number to the command window.
    third_rule = code[2]*code[1]-code[0]
    print(f"day = {third_rule}")

    # Rule 4:
    # Calculating the value of the 3rd digit to the power of the 2nd digit
    fourth_rule = code[2] ** code[1]
    if fourth_rule % 3 == 0:
        print(f"place = {code[5]-code[4]}")
    else:
        print(f"place = {code[4]-code[5]}")
