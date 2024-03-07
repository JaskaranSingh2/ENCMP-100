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

print('Lab 2 - Version 2')
# ----------Students write/modify their code below here ---------------------
code = input('Please enter a code to break: ')
code = np.array(list(code), dtype=int)
# The code in this version include an implementation of rules 1 and 2 and the partial implementation of Rule 3 and 4.

# Rule1:
# If the array "code" is not 9 digits long, then the program will stop and print the message "Decoy Message: Not a nine-digit number."
if len(code) != 9:
    print("Decoy message: Not a nine-digit number.")

# Rule2:
# If the sum of the array "code" is even, then the program will stop and print the message "Decoy Message: Sum is even."
elif sum(code) % 2 == 0:
    print("Decoy message: Sum is even.")

else:
    # Rule3:
    # Multiplying the 3rd digit by the 2nd digit and subtracting the 1st digit, then determining the rescue day and storing it in the variable "date", and if it is not a valid day, then the program will stop and print the message "Decoy Message: Invalid rescue day." and set the variable "valid" to False, which will be used to run the next rule.
    valid = True
    third_rule = code[2]*code[1]-code[0]
    if third_rule == 1:
        date = "Rescued on Monday"
    elif third_rule == 2:
        date = "Rescued on Tuesday"
    elif third_rule == 3:
        date = "Rescued on Wednesday"
    elif third_rule == 4:
        date = "Rescued on Thursday"
    elif third_rule == 5:
        date = "Rescued on Friday"
    elif third_rule == 6:
        date = "Rescued on Saturday"
    elif third_rule == 7:
        date = "Rescued on Sunday"
    else:
        print("Decoy message: Invalid rescue day.")
        valid = False

    # Rule4:
    # Calculating the value of the 3rd digit to the power of the 2nd digit, then determining the rendezvous point and storing it in the variable "point".
    if valid:
        fourth_rule = code[2] ** code[1]
        if fourth_rule % 3 == 0:
            point_as_num = code[5]-code[4]
        else:
            point_as_num = code[4]-code[5]

        if point_as_num == 1:
            point = "bridge"
        elif point_as_num == 2:
            point = "library"
        elif point_as_num == 3:
            point = "river crossing"
        elif point_as_num == 4:
            point = "airport"
        elif point_as_num == 5:
            point = "bus terminal"
        elif point_as_num == 6:
            point = "hospital"
        elif point_as_num == 7:
            point = "railway station"
        else:
            print("Decoy message: Invalid rendezvous point.")

            # Setting the condition to False to prevent the next print statement from executing.
            valid = False

    if valid:
        # Printing the rescue day and the rendezvous point.
        print(date, "at the", point)
