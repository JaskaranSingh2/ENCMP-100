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

import matplotlib.pyplot as plt
import numpy as np

print('Version 1')

# ------------Students edit/write their code below here--------------------------

# Saving Calculation

# Number of months
months = 18 * 12
# Monthly contribution
monthly_contribution = 200
# Interest rate
interest_rate = 0.0625
# Old balance, which initially serves as the initial balance
old_balance = 2000
# List to store monthly balances
monthly_balance = [old_balance]
# New balance
new_balance = 0

# Calculate monthly balances
for i in range(1, months):
    new_balance = old_balance * (1 + interest_rate / 12) + monthly_contribution
    monthly_balance.append(new_balance)
    old_balance = new_balance

# Print the final savings amount
print(f"The savings amount is ${monthly_balance[-1]:.2f}")

# Tuition Calculation

# List to store tuition costs for arts program
arts = [5550]
# List to store tuition costs for science program
science = [6150]
# List to store tuition costs for engineering program
engineering = [6550]
# Rate of increase for tuition costs
rate_of_increase = 7 / 100

# Calculate tuition costs for 22 years

for i in range(1, 22):
    arts.append(arts[-1] * (1 + rate_of_increase))
    science.append(science[-1] * (1 + rate_of_increase))
    engineering.append(engineering[-1] * (1 + rate_of_increase))

# Calculate total tuition costs for four years

arts_four_years = sum(arts[-4:])
science_four_years = sum(science[-4:])
engineering_four_years = sum(engineering[-4:])

# Print the cost of each program for four years

print(f"The cost of the arts program is ${arts_four_years:.2f}")
print(f"The cost of the science program is ${science_four_years:.2f}")
print(f"The cost of the engg program is ${engineering_four_years:.2f}")

# Plot

# x-axis values
x_values = np.arange(19)  # Extend the range to include age 18
# y-axis values (monthly balances at the end of each year)
y_values = [monthly_balance[12 * i]
            for i in range(18)]
# Extend the range to include final balance
y_values.append(monthly_balance[-1])
# Plot the savings balance
plt.plot(x_values, y_values, label='Saving Balance')
# Plot horizontal lines for tuition costs
plt.axhline(y=science_four_years, color='green', label='Science')
plt.axhline(y=arts_four_years, color='orange', label='Arts')
plt.axhline(y=engineering_four_years, color='red', label='Engineering')
# Set plot title, labels, and legend
plt.title('Savings vs Tuition')
plt.xlabel('Years')
plt.xticks(np.arange(0, 19, 1))  # Set x-axis to go up by increments of 1
plt.ylabel('Amount ($)')
plt.xlim(0, 18)
plt.ylim(0, 100000)
plt.legend()
# Display the plot
plt.show()
