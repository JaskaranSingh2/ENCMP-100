## TSPANALYZE  Geomatics and the Travelling Sales[person] Problem
#
# According to the ISO/TC 211, geomatics is the "discipline concerned
# with the collection, distribution, storage, analysis, processing, [and]
# presentation of geographic data or geographic information." Geomatics
# is associated with the travelling salesman problem (TSP), a fundamental
# computing problem. In this lab assignment, a University of Alberta
# student completes a Python program to analyze, process, and present
# entries, stored in a binary data file, of the TSPLIB, a database
# collected and distributed by the University of Heidelberg.
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
#

import scipy.io as io  # Importing the scipy.io module for input/output operations
import matplotlib.pyplot as plt  # Importing the matplotlib.pyplot module for plotting
import numpy as np  # Importing the numpy module for numerical operations

def plotEuc2D(coord, comment, name):
    """
    Function to plot 2D Euclidean coordinates.

    Parameters:
    - coord: numpy array of shape (N, 2) representing the x and y coordinates
    - comment: string representing the plot comment
    - name: string representing the plot name
    """
    x = coord[:, 0]  # Extracting the x-coordinates from the coord array
    y = coord[:, 1]  # Extracting the y-coordinates from the coord array
    plt.plot(x, y, 'bo-')  # Plotting the coordinates as blue dots connected by lines
    plt.plot([x[0], x[-1]], [y[0], y[-1]], 'r-')  # Plotting a red line connecting the first and last coordinates
    plt.xlabel('x-Coordinate')  # Setting the x-axis label
    plt.ylabel('y-Coordinate')  # Setting the y-axis label
    plt.title(comment)  # Setting the plot title
    plt.savefig('tspPlot.png')  # Saving the plot as an image file
    plt.legend([name], loc='upper right')  # Adding a legend to the plot
    plt.show()  # Displaying the plot

def tspPrint(tsp):
    """
    Function to print information about the TSP data.

    Parameters:
    - tsp: list of lists representing the TSP data
    """
    print()
    print("NUM  FILE NAME  EDGE TYPE  DIMENSION  COMMENT")
    for k in range(1, len(tsp)):
        name = tsp[k][0]  # Extracting the file name from the tsp data
        edge = tsp[k][5]  # Extracting the edge type from the tsp data
        dimension = tsp[k][3]  # Extracting the dimension from the tsp data
        comment = tsp[k][2]  # Extracting the comment from the tsp data
        print("%3d  %-9.9s  %-9.9s  %9d  %s"
              % (k, name, edge, dimension, comment))  # Printing the information in a formatted manner

def tspPlot(tsp):
    """
    Function to plot a tour from the TSP data.

    Parameters:
    - tsp: list of lists representing the TSP data
    """
    num = int(input("Number (EUC_2D)? "))  # Getting the user input for the tour number
    tsp1 = tsp[num]  # Selecting the tour from the tsp data
    edge = tsp1[5]  # Extracting the edge type of the selected tour
    if edge == 'EUC_2D':  # Checking if the edge type is 'EUC_2D'
        print("Valid (%s)!!!" % edge)  # Printing a validation message
        plotEuc2D(tsp1[10], tsp1[2], tsp1[0])  # Plotting the tour using the plotEuc2D function
    else:
        print("Invalid (%s)!!!" % edge)  # Printing an invalid message

def menu():
    """
    Function to display the main menu and get user choice.

    Parameters:
    None

    Returns:
    - choice: integer representing the user's choice
    """
    print()
    print("MAIN MENU")
    print("0. Exit program")
    print("1. Print database")
    print("2. Limit dimension")
    print("3. Plot one tour")
    print()
    choice = int(input("Choice (0-3)? "))  # Getting the user input for the choice
    while not (0 <= choice <= 3):  # Validating the choice
        choice = int(input("Choice (0-3)? "))  # Getting the user input again if the choice is invalid
    return choice  # Returning the user's choice

def main():
    tsp = io.loadmat('tspData.mat', squeeze_me=True)  # Loading the TSP data from a binary file
    tsp = np.ndarray.tolist(tsp['tsp'])  # Converting the TSP data to a list of lists
    file = open('tspAbout.txt', 'r')  # Opening the tspAbout.txt file for reading
    print(file.read())  # Printing the contents of the file
    file.close()  # Closing the file

    choice = menu()  # Getting the user's choice from the menu
    while choice != 0:  # Looping until the user chooses to exit
        if choice == 1:  # If the user chooses to print the database
            tspPrint(tsp)  # Call the tspPrint function to print the TSP data
        elif choice == 3:  # If the user chooses to plot a tour
            tspPlot(tsp)  # Call the tspPlot function to plot the tour

        choice = menu()  # Getting the user's choice again from the menu

if __name__ == "__main__":
    main()  # Calling the main function when the script is run directly
