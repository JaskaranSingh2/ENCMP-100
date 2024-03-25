## PERIHELION  Mercury's perihelion precession and general relativity
#
# In this lab assignment, a student completes a Python program to test with
# data an accurate prediction of Einstein’s theory, namely the perihelion
# precession of Mercury. Mercury’s orbit around the Sun is not a stationary
# ellipse, as Newton’s theory predicts when there are no other bodies. With
# Einstein’s theory, the relative angle of Mercury’s perihelion (position
# nearest the Sun) varies by about 575.31 arcseconds per century.
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
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def main():
    data = loaddata('horizons_results')  # Load data from the 'horizons_results' file
    data = locate(data)  # Locate the perihelia in the data
    data = select(data, 25, ('Jan', 'Feb', 'Mar'))  # Select data based on year and month
    makeplot(data, 'horizons_results')  # Make a plot of the data

def loaddata(filename):
    """
    Load data from a text file.

    Args:
        filename (str): The name of the file to load.

    Returns:
        list: A list of dictionaries containing the loaded data.
    """
    file = open(filename+'.txt','r')  # Open the file for reading
    lines = file.readlines()  # Read all lines from the file
    file.close()  # Close the file
    noSOE = True  # Flag to indicate if the start of the data section has been reached
    num = 0  # Counter for the number of lines read
    data = []  # List to store the loaded data
    for line in lines:
        if noSOE:
            if line.rstrip() == "$$SOE":  # Check if the start of the data section is reached
                noSOE = False  # Set the flag to False to indicate the start of the data section
        elif line.rstrip() != "$$EOE":  # Check if the end of the data section is reached
            num = num+1  # Increment the line counter
            if num % 10000 == 0:
                print(filename,":",num,"line(s)")  # Print the progress every 10000 lines
            datum = str2dict(line)  # Convert the line of text into a dictionary
            data.append(datum)  # Add the dictionary to the data list
        else:
            break  # Exit the loop if the end of the data section is reached
    if noSOE:
        print(filename,": no $$SOE line")  # Print a message if the start of the data section is not found
    else:
        print(filename,":",num,"line(s)")  # Print the total number of lines read
    return data  # Return the loaded data

def str2dict(line):
    """
    Convert a line of text into a dictionary.

    Args:
        line (str): The line of text to convert.

    Returns:
        dict: A dictionary containing the converted data.
    """
    parts = line.split(',')  # Split the line of text by comma
    numdate = int(float(parts[0]))  # Convert the first part to a float and then to an integer
    strdate = parts[1][6:17]  # Extract the date string from the second part
    coord = tuple(map(float, parts[2:-1]))  # Convert the remaining parts to floats and create a tuple
    return {'numdate': numdate, 'strdate': strdate, 'coord': coord}  # Return a dictionary with the converted data

def locate(data1):
    """
    Locate the perihelia in the data.

    Args:
        data1 (list): The input data.

    Returns:
        list: A list of dictionaries containing the located perihelia.
    """
    dist = []  # List to store the vector lengths
    for datum in data1:
        coord = np.array(datum['coord'])  # Convert the coordinate tuple to a numpy array
        dot = np.dot(coord,coord)  # Calculate the dot product of the coordinate array with itself
        dist.append(np.sqrt(dot))  # Calculate the vector length and add it to the list
    data2 = []  # List to store the located perihelia
    for k in range(1,len(dist)-1):
        if dist[k] < dist[k-1] and dist[k] < dist[k+1]:  # Check if the current distance is smaller than the previous and next distances
            data2.append(data1[k])  # Add the corresponding datum to the located perihelia list
    return data2  # Return the located perihelia

def select(data, ystep, month):
    """
    Select data based on year and month.

    Args:
        data (list): The input data.
        ystep (int): The year step.
        month (tuple): The months to select.

    Returns:
        list: A list of dictionaries containing the selected data.
    """
    selected_data = []  # List to store the selected data
    for datum in data:
        year = int((datum['strdate'].split('-')[0])[0:4])  # Extract the year from the date string
        month_str = datum['strdate'].split('-')[1]  # Extract the month from the date string
        if year % ystep == 0 and month_str in month:  # Check if the year is divisible by ystep and the month is in the specified list
            selected_data.append(datum)  # Add the datum to the selected data list
    return selected_data  # Return the selected data

def makeplot(data, filename):
    """
    Make a plot of the data.

    Args:
        data (list): The input data.
        filename (str): The name of the output file.
    """
    (numdate, strdate, arcsec) = precess(data)  # Calculate the precession angles
    plt.plot(numdate, arcsec, 'bo')  # Plot the precession angles
    strdate = [datum['strdate'] for datum in data]  # Extract the date strings from the data
    plt.xticks(numdate, strdate, rotation=45)  # Set the x-axis ticks to the date strings
    add2plot(numdate, arcsec)  # Add the best fit line to the plot
    plt.xlabel('Perihelion date')  # Set the x-axis label
    plt.ylabel('Precession (arcsec)')  # Set the y-axis label
    plt.savefig(filename+'.png', bbox_inches='tight')  # Save the plot to a file
    plt.show()  # Display the plot

def precess(data):
    numdate = []  # List to store the numerical dates
    strdate = []  # List to store the date strings
    arcsec = []  # List to store the precession angles
    v = np.array(data[0]['coord'])  # Reference (3D) coordinate array
    for datum in data:
        u = np.array(datum['coord'])  # Perihelion (3D) coordinate array
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v))  # Calculate the dot product ratio
        if np.abs(ratio) <= 1:  # Check if the ratio is within the valid range
            angle = 3600*np.degrees(np.arccos(ratio))  # Calculate the precession angle in arcseconds
            numdate.append(datum['numdate'])  # Add the numerical date to the list
            strdate.append(datum['strdate'])  # Add the date string to the list
            arcsec.append(angle)  # Add the precession angle to the list
    return (numdate, strdate, arcsec)  # Return the numerical dates, date strings, and precession angles

def add2plot(numdate, actual):
    r = stats.linregress(numdate, actual)  # Perform linear regression on the data
    bestfit = []  # List to store the best fit line
    for k in range(len(numdate)):
        bestfit.append(r[0]*numdate[k]+r[1])  # Calculate the best fit line values
    plt.plot(numdate, bestfit, 'b-')  # Plot the best fit line
    plt.legend(["Actual data", "Best fit line"], loc="upper left")  # Add a legend to the plot

main()  # Call the main function to start the program
