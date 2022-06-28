"""
In this project, we will be importing a csv reader once again to be able to read the csv files. We will then
use a series of country codes associated with data to each country in regards to the World Tourist Organization.
This organization is interested in the inbound and outbound travels of tourists as well as the expenses made
in the inbound and outbound travels. This program will show the yearly number of arrivals, departures, 
total receipts, and total expenses from each country between 2009 and 2017.The program will to read
 two files: one containing the international travel data between 2009 to 2017 and another with the codes
 for each country which international travel data is recorded. The data from the first file will be 
 stored into a list of yearly data, where each year will have its own list of tuples with the required
 values for the program to extract and process the information. The program will then display a table 
 with the information of each country within a single year, as well as the yearly information for a 
 single country. Also, we will plot the top 20 countries with the highest average expenses and
 receipts and another plot for the yearly average expenses and receipts for a country.
"""

import matplotlib.pyplot as plt
import csv
from operator import itemgetter
import numpy as np


MIN_YEAR = 2009
MAX_YEAR = 2017

VALID_YEARS=['2009','2010','2011','2012','2013','2014','2015','2016','2017']

def open_file(inputstring):
    '''This open file function receives a string in the form of a user input and searches
    the computer for the file. If the file is not found, the user will be prompted that the file is not found,
    then reprompted to try inputting a file again.'''
    FileFound=False

    filename=input(inputstring)
  
    while (FileFound==False):
            
        try:
           fp = open(filename, encoding="utf-8")
           return fp
       #try-except for the filenotfound error incase the file does not exist
        except FileNotFoundError:
           print("File not found. Try Again")
           filename = input(inputstring)





def read_travel_file(fp):
    '''This function receives a file pointer for the data file, and will then read it using the csv reader.
    We will be using the variables to return a list of lists with tuples for each year between 2009 and 2017.
    Each list of countries per year contains tuples with the data for a single country for a single year.
    '''
    reader=csv.reader(fp)
    next(reader, None)
    #This is where we skip the header line

    data_list=[[],[],[],[],[],[],[],[],[]]
    #list of lists
    
    for line in reader:
                    
        year=0
        country_name=line[1][:20]
        country_code=line[2]
        num_departures=0
        num_arrivals=0
        expenditures=0
        receipts=0
        avg_expenditures=0
        avg_receipts=0
        #these are our variables
       
        try:
            year = int(line[0])
            num_departures = int(line[3])/1000
            num_arrivals = int(line[4])/1000
            expenditures = float(line[5])/1000000
            receipts = float(line[6])/1000000
            #This is where we do the calculations for the averages

      
        except:
            pass
        #Pass the values through
        try:
            
            avg_expenditures=(expenditures/num_departures)* 1000

        except:
            avg_expenditures=0
            #If the calculation does not work, we set the avergae equal to zero
            #We can also use a try-except zerodivision error here
        try:
            
            avg_receipts=(receipts/num_arrivals)*1000

        except:
            avg_receipts=0
        avg_expenditures=round(avg_expenditures,2)
        avg_receipts=round(avg_receipts,2)        
            
        tup=(year,country_name,country_code,num_arrivals,num_departures,expenditures,receipts,avg_expenditures,avg_receipts)

        year_index=year-2009
        data_list[year_index].append(tup)
        #setting the index for the year
    
    for item in data_list:
        item.sort(key=itemgetter(1))
        #sort the data
    return data_list
    
def read_country_code_file(fp):
    '''This function will read the file for the country code by creating an empty list, and for 
    each line, appending the data to a new list, which we then append to a tuple. We will pass in the fp
    so the data in the file is used here'''
    country_list=[]
    line_number=0
    for line in fp:
        if line_number>0:
           temp=line.split('\n')
           temp=temp[0].split('/')
           code=temp[0]
           country=temp[1]
           country_tuple=(code,country)
           #creating the new location for the data
           country_list.append(country_tuple) 


        line_number=line_number+1
        #each line
    country_list.sort(key=itemgetter(0))
    return country_list
        
    return country_list

def get_country_code_data(country_code,DataList):
    '''This function will receive the datalist parameter which is the same list returned by 
    the read_travel_file function and a country code.  It returns a list with the tuples
    from a single country. It then will iterate through each year in datalist for the tuples whose code
    is equal to the country_code parameter. The function will sort this data in ascending order.  '''

    Country_Data_List=[]

    for List in DataList:
             
        for value in List:
            if value[2]==country_code:
               Country_Data_List.append(value)
               #we append onto the list for the country code, automatically does this in ascending order
         
    return Country_Data_List

def get_year_data(year,DataList):
    '''This function will receive the data for each year from the datalist,
    try to return it as an integer, then append it to the new list we create for 
    the year data.'''
    Year_Data_List=[]

    for List in DataList:
        if List[0][0]==int(year):
            #we make integer, for value in year
           for value in List:
               #we append the data to our new list for the year
               Year_Data_List.append(value)
        
    return Year_Data_List
  

def display_country_codes(country_codes):
    '''This function is used to display the country codes as seen in our menu,
    when the user enters this, the code will output all of the country codes in the proper format.'''
    print('Country Code Reference')
    print('{:10s}{:>15s}'.format('Country Code','Country Name'))
    for value in country_codes:
        country_code=value[0]
        country_name=value[1]
        #we format the data for the country code reference
        print('{:10s}{:>15s}'.format(country_code,country_name))
        

def display_data_by_year(data_list,year):
    '''This function receives a list of travel data for all countries within a year and  displays the travel
    data for all countries in a single year between 2009 and 2017. It also displays the total of each column in
    the proper formatting'''
  
    # Get the country name from the list
    country_name = data_list[0][1]
    
    # Print table title
    title = "Travel Data for {}".format(year)
    print("\n{:^80s}".format(title))
    
    # Table headers
     
    print('{:20s}{:>15s}{:>20s}{:>25s}{:>30s}'.format('Country Name','Departure','Arrivals','Expenditures','Receipts'))
    print('{:20s}{:>15s}{:>20s}{:>25s}{:>30s}'.format('','(thousands)','(thousands)','(millions)','(millions'))
    print()

    # Country(1), Departures(3), Arrivials(4), Expenditures(5), Receipts(6)
    #proper indices
    country=''
    tot_departures=0
    tot_arrivals=0
    tot_expenditures=0
    tot_receipts=0
    #set variables for the totals
        
    for value in data_list:
        country=value[1]
        departures=value[3]
        arrivals=value[4]
        expenditures=value[5]
        receipts=value[6]
        #we use the indices for the values
       
      
        print('{:20s}{:>15,.2f}{:>20,.2f}{:>25,.2f}{:>30,.2f}'.format(country,departures,arrivals,expenditures,receipts))
        tot_departures=tot_departures+departures
        tot_arrivals=tot_arrivals+arrivals
        tot_expenditures=tot_expenditures+expenditures
        tot_receipts=tot_receipts+receipts
        #format for the totals then print the totals
    print()
    print('{:20s}{:>15,.2f}{:>20,.2f}{:>25,.2f}{:>30,.2f}'.format('Total',tot_departures,tot_arrivals,tot_expenditures,tot_receipts))                 
    


def display_data_by_country(data_list,country_name):
    '''This function receives a list of travel data for a single country between 2009 and 2017. It will display
    the data for one country in the years between 2009 and 2017. It also displays the total of each column in
    the proper formatting '''
  
    title = "Travel Data for {}".format(country_name)
    #printing table title
    print("\n{:^80s}".format(title))
    
    # Table headers     
    print('{:20s}{:>15s}{:>20s}{:>25s}{:>30s}'.format('Year','Departure','Arrivals','Expenditures','Receipts'))
    print('{:20s}{:>15s}{:>20s}{:>25s}{:>30s}'.format('','(thousands)','(thousands)','(millions)','(millions'))
    print()
    #printing the titles
    year=''
    tot_departures=0
    tot_arrivals=0
    tot_expenditures=0
    tot_receipts=0
        #setting our variables
    for value in data_list:
        year=value[0]
        departures=value[3]
        arrivals=value[4]
        expenditures=value[5]
        receipts=value[6]
       #setting the indicies for the list
      
        print('{:20d}{:>15,.2f}{:>20,.2f}{:>25,.2f}{:>30,.2f}'.format(year,departures,arrivals,expenditures,receipts))
        tot_departures=tot_departures+departures
        tot_arrivals=tot_arrivals+arrivals
        tot_expenditures=tot_expenditures+expenditures
        tot_receipts=tot_receipts+receipts
        #setting up the totals before printing them
    print()
    print('{:20s}{:>15,.2f}{:>20,.2f}{:>25,.2f}{:>30,.2f}'.format('Total',tot_departures,tot_arrivals,tot_expenditures,tot_receipts))         
    #printing the totals


def prepare_bar_plot(year_list):
    '''This function will receive a list of travel data for all countries within a single year. 
    It returns two lists: the top 20 countries by average expenditures and the top 20 countries by 
    average receipts. The list of average expenditures will contain tuples with the country
    name and the average expenditure for each country. The list of average receipts will contain tuples 
    with the country name and the average receipt for each country.'''

    expenditure_list=[]
    receipt_list=[]
    #creating the two empty lists
    year_list.sort(key=itemgetter(7),reverse=True)
    #sorting the items using itemgetter
    top_twenty_countries=year_list[:20]
    #top 20 countries

    for value in top_twenty_countries:
        country=value[1]
        avg_expenditure=value[7]
        #setting the indices
        data_tuple=(country,avg_expenditure)
        expenditure_list.append(data_tuple)
        #appending the data to the list


    year_list.sort(key=itemgetter(8),reverse=True)
    #sorting using the itemgetter
    top_twenty_countries=year_list[:20]
    for value in top_twenty_countries:
        country=value[1]
        avg_receipt=value[8]
        #indices for receipt avg and country
        data_tuple=(country,avg_receipt)
        expenditure_list.append(data_tuple)
        receipt_list.append(data_tuple)
        #appending the data to the list

      
    return expenditure_list,receipt_list
#we return the two lists, now appended
    



def prepare_line_plot(country_list):
    '''This function receives a list of the travel data for a single country between 2009 and 2017. The
    countrylist parameter is the same list returned by the get_country_code_data function.  This function
    will return two lists in the order of expenditures then receipts (avg). The function will return lists
    of values, not of tuples.'''
    
    avg_expediture_list=[]
    avg_receipt_list=[]
    #creating our empty lists
    for value in country_list:
        avg_expediture_list.append(value[7])
        avg_receipt_list.append(value[8])
        #the indices for the averages
    return avg_expediture_list,avg_receipt_list
#we return the expenditure first then the receipts


def plot_bar_data(expenditure_list, receipt_list, year):
    '''This function we will build the plot using a plt.show and our x and y values. This will be ran 
    when the user prompts that they do want a plot to be included with the data. This will simplify our code
    and give us a place to put the data for the expenditures and receipts. This will return the 
    plot for the averages for a year, not just the country.'''
    
    title_expenditures="Top 20 countries with highest average expenditures {:4s}".format(year)
    title_receipts="Top 20 countries with highest average receipts {:4s}".format(year)
    print(title_expenditures)
    #printing the plot titles

    X1=[]
    Y1=[]
    #setting up our empty list values for x and y
    for value in expenditure_list:
        x_coordinate=value[0]
        y_coordinate=value[1]
        X1.append(x_coordinate)
        Y1.append(y_coordinate)
        #appending our data to our x and y using the proper indices for expenditures
        
    X2=[]
    Y2=[]

    for value in receipt_list:
        x_coordinate=value[0]
        y_coordinate=value[1]
        X2.append(x_coordinate)
        Y2.append(y_coordinate)
        #appending our data to our x and y using the proper indices for receipts
    fig, axs = plt.subplots(2, 1,figsize=(7,8))
    #creating our plot

    axs[0].set_title(title_expenditures)
    axs[0].bar(X1,Y1, width=0.4, color='b')
    axs[0].set_ylabel("Avg. Expenditures (US dollar)")
    axs[0].set_xticks(X1)
    axs[0].set_xticklabels(X1 , rotation='90')
    #setting up our labels for expenditures
    

    axs[1].set_title(title_receipts)
    axs[1].set_ylabel("Avg. Receipts (US dollar)")
    axs[1].bar(X2,Y2, width=0.4, color='b')
    axs[1].set_xticks(X2)
    axs[1].set_xticklabels(X2 , rotation='90')
    #setting up our labels for receipts
    fig.tight_layout()
    #commanding our layout
    plt.show()
    #using the plt.show command to show the plot when prompted
  
    
    
def plot_line_data(country_code, expenditure_list, receipt_list):
    '''This function will take the data from our preparation function for the single country in the
    years 2009-2017 and then put the data into a plot when called. This function will be called when
    the user inputs for plot. This plot is for the averages and their costs according to the
    country data, not the year data.'''
    title = "Average expenditures and receipts for {} between 2009 and 2017".format(CountryName)
    #title
    X=[]
    for i in range(MIN_YEAR, MAX_YEAR+1):
        #we append the year for each time the year goes up
        X.append(i)

    
    title = "Average expenditures and receipts for {} between 2009 and 2017".format(country_code)
    #title
    fig, axs = plt.subplots(figsize=(7,5))
    #creating our plot requirements
    axs.set_title(title)
    axs.set_ylabel("Cost (US dollar)")
    #ylabel title
    axs.plot(X,expenditure_list)
    #passing our expenditure data to the X
    axs.plot(X,receipt_list)
    #passing our receipt data to the X
    axs.legend(['Expenditures','Receipt'])

    plt.show()
    #using plt.show to show the plot when prompted

def CheckYear(Year):
    '''This function is used to simplify our code and allow us to check if the year entered
    is in our variable for Valid Years, and if not then we return false.'''
    Validchoice=False
    if Year in VALID_YEARS:
       Validchoice=True
       #if the year entered is in validyears
    return Validchoice


def CheckCountry(country_code,country_list):
    '''This function will make it easier for our code to check the country using both
    its country code and the list of countries.'''
    Validchoice=False
    for value in country_list:
        #if the country entered is in our list of countries
        #we return true and use the proper index
        if country_code==value[0]:
           return True,value[1]
    return Validchoice,''



def GetDataForGraphing(data_list,index1,index2):
    '''This function will take the data from datalist in order to use it in our plots '''
    X=[]
    Y=[]
    #creating our empty lists
    for value in data_list:
        X.append(value[index1])
        Y.append(value[index2])
        #we append to either the x or y value

    return X,Y
#return our x and y

def user_selection():
    ''' The purpose of this function is to make it easier to re-loop the function after an individual
    calculation in the main function.'''
    validchoice=False
    while (validchoice==False):
        #we print our menu here
        OPTION = "Menu\
    \n\t1: Display data by year\
    \n\t2: Display data by country\
    \n\t3: Display country codes\
    \n\t4: Stop the Program "
        print(OPTION)
        print()
        choice=input('\n\tEnter Option Number: ')
        if choice not in ('1','2','3','4'):
           print('Invalid Option. Try again!') 
           #we print invalid option if the user does not enter a valid option
        else:
           Validchoice=True   
           #return the choice if it is a valid option
           return choice


def main():
    '''
Our main function begins with the banner we print. We then prompt for the option. We allow choice to be 
inputted for, then create our parameters. We then prompt the user to enter the travel data file, and try 
to open it. Then, we prompt fot the country code file, and try to open it. For either of these options, if
entered incorrectly we will prompt the user to try again. Our four choices consist of displaying the data by
year, country, country codes, or quitting. The function will create if statements for each parameter and
run the corresponding function for each of them. If the user prompts to create the plot, then we will
run the plot creating fucntions above. Otherwise, if the user chooses 4, we break the program by printing
our goodbye message.
    '''
    
    BANNER = "International Travel Data Viewer\
    \n\nThis program reads and displays departures, arrivals, expenditures,"\
    " and receipts for international travels made between 2009 and 2017."
    
    # Prompt for option
    OPTION = "Menu\
    \n\t1: Display data by year\
    \n\t2: Display data by country\
    \n\t3: Display country codes\
    \n\t4: Stop the Program\
    \n\n\tEnter option number: "
    
    
    print(BANNER)
    #our opening banner

    choice=0   

    travel_string="Enter the travel data file: "
    fp_travel=open_file(travel_string)
    country_string="Enter the country code file: "
    fp_country=open_file(country_string)
    data_list=read_travel_file(fp_travel)
    country_list=read_country_code_file(fp_country)
    #we call on our user choice function here which will print our menu
    choice=user_selection()
       
    while(choice!='4'):
            
        if (choice=='1'):
            year=''
            valid_year=False
            year=input('Enter Year: ')
            while valid_year==False:
                  valid_year=CheckYear(year)
                  if valid_year==False:
                     print('Year needs to be between 2009 and 2017. Try Again!')
                     year=input('Enter Year: ')
                     #for choice 1, we check if their responses are valid, and if not we reprompt them

                  
            year_data_list=get_year_data(year,data_list)
            display_data_by_year(year_data_list,year)
            choice_plot=input('Do you want to plot (yes/no)? ')
            if choice_plot in ('yes','Y','y'):
                #we then pass our get year data function and ask if they want a plot
             
                expenditure_list,receipt_list=prepare_bar_plot(year_data_list)
                plot_bar_data(expenditure_list,receipt_list,year)
                #if they choose to plot, we pass function to create the plot.

                
        if (choice=='2'):
            valid_code=False
            country_code=''
            country_name=''
            country_code=input('Enter Country Code: ')
            while valid_code==False:
                  valid_code,country_name=CheckCountry(country_code.upper(),country_list)
                  if valid_code==False:
                     print('Country code is not found! Try Again!')
                     country_code=input('Enter Country Code: ')
                  #prompts for choice 2 and reprompt if invalid
              
            country_data_list=get_country_code_data(country_code.upper(),data_list) 
            #we use a .upper here because all the country code file data is uppercase
            display_data_by_country(country_data_list,country_name)
            choice_plot=input('Do you want to plot (yes/no)?')
            if choice_plot in ('yes','Y','y'):
                #prompt for the plot, and if the choice is yes, we create the plot
               Year,Avg_Expenditures=GetDataForGraphing(country_data_list[:20],0,7)
               Year,Avg_Receipts=GetDataForGraphing(country_data_list[:20],0,8)
               plot_line_data(Year,Avg_Expenditures,Avg_Receipts,country_name)
               


       
        if (choice=='3'):
            display_country_codes(country_list)
            #choice 3 simply calls our display country codes from our country list
            #to allow the user to see these values.


        choice=user_selection()
        #we reprompt for the choice after each time the user gets an output, until they want to quit
 
        #if the choice is outside the loop, aka while it is 4, we break the code
        #and print our thank you message
    print("\nThanks for using this program!")
            
if __name__ == "__main__":
    main()
