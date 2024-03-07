# HSPECTRUM  Quantum Chemistry and the Hydrogen Emission Spectrum
#
# The periodic table is central to chemistry. According to Britannica,
# "Detailed understanding of the periodic system has developed along with
# the quantum theory of spectra and the electronic structure of atoms,
# beginning with the work of Bohr in 1913." In this lab assignment, a
# University of Alberta student explores the Bohr model's accuracy in
# predicting the hydrogen emission spectrum, using observed wavelengths
# from a US National Institute of Standards and Technology database.
#
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
# numbers, adding to 100%, follow-up questions will be asked.
#
# For anonymous sources, enter pseudonyms in uppercase, e.g., SAURON,
# followed by percentages as above. Email a link to or a copy of the
# source to the lab instructor before the assignment is due.

# VERSION 2

# Importing the libraries necessary for this program (numpy allows us to do a variety of mathematical operations, matplotlib.pyplot allows us to plot graphs)
import numpy as np
import matplotlib.pyplot as plt

# EXPERIMENT DATA
# The 'data' object is converted into a NumPy array and then stored in 'nist' then its length is reported in 'n'
data = [656.460, 486.271, 434.1692, 410.2892,
        397.1198, 389.0166, 383.6485]  # nm
nist = np.array(data)
n = len(nist)

# MODEL SETUP
# The values for the variables used in the first equation in the Lab Instructions are rounded to 8 significant figures, as suggested in the Lab Instructions
rydbergPrevious = 1.0973732e7  # 1/m

electron_mass = 9.1093837e-31  # kg
proton_mass = 1.6726219e-27  # kg
fundamental_charge = 1.6021766e-19  # C
free_space_permittivity = 8.8541878e-12  # F/m
planck = 6.6260702e-34  # J*s
speed_light = 2.9979246e8  # m/s

# Calculating the rydberg constant by utilizing the values of the variables above
rydberg = (electron_mass * fundamental_charge**4) / \
    (8 * free_space_permittivity**2 * planck**3 * speed_light)  # 1/m

# Restating the rydberg variable so that it equals the hydrogen rydberg constant:
rydberg = rydberg * (proton_mass / (proton_mass + electron_mass))
print("Rydberg constant:", f"{int(rydberg)}m"+chr(8315)+chr(185))

# SIMULATION DATA
# Getting nf from the user, converting it to an integer then creating an array of ni values, then plotting it with a grid in the back
nf = input("Final state (nf): ")
nf = int(nf)
ni = np.arange(nf+1, nf+n+1)
plt.plot(ni, nist, 'bx', label='NIST Data')
plt.grid(True)

# Compute Bohr model data points and converting to nm
wavelength = 1/(rydberg * ((1 / nf**2) - (1 / ni**2)))
wavelength_nm = wavelength * 1e9

# Plot Bohr model data points and annotating the graph
plt.plot(ni, wavelength_nm, 'r.', label='Bohr Model')
plt.xlabel('Initial State (ni)')
plt.ylabel('Wavelength (nm)')
plt.title('Hydrogen Emission Spectrum')
plt.legend()

plt.show()

# ERROR ANALYSIS
# Compute the wavelength difference between observed and predicted wavelengths
wavelength_difference = nist - wavelength_nm
# Compute the worst-case error by taking the absolute value of all the wavelength_difference values in the list using np.abs, and then finding the maximum value using np.max
worst_case_error = np.max(np.abs(wavelength_difference))

# Print the worst-case error rounded
print("Worst-case error:", f"{worst_case_error:.3f} nm")
# Plot the wavelength difference
plt.bar(ni, wavelength_difference, color='#bf00bf', label='NIST-Bohr')
plt.xlabel('Initial State (ni)')
plt.ylabel('Wavelength (nm)')
plt.title('Hydrogen Emission Spectrum')
plt.legend()
plt.show()
