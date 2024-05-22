# @author: Dor Gaon 315873844
# import this libraries for data and functions
import pandas as pd
import numpy as np
import yahoofinancials as yf
from matplotlib import pyplot as plt
import statsmodels.api as sm
from datetime import datetime

date_format = "%Y-%m-%d"
opt_signs = {'A': 'QQQ', 'B': 'SPY', 'C': 'IWM'}


def take_main_choice():
    """
    :return: user's main choice
    """
    opt = None
    while opt not in ['A', 'B', 'C', 'D']:
        opt = input("Welcome to our program! Please choose one option: \nA:  see NASDAQ 100 \nB:  see S&P500 \nC:  see RUSSELL200 \nD:  exit")
        if opt not in ['A', 'B', 'C', 'D']:
            print('Sorry not an option\n')
    return opt


def take_dates_choice():
    """
    :return: user's start and end choices
    """
    while True:
        # take start date
        while True:
            try:
                start_s = input("Please enter the start date in YYYY-MM-DD format: ")
                start_d = datetime.strptime(start_s, date_format)
                break
            except ValueError:
                print("incorrect date format. It should be YYYY-MM-DD.\n")

        # take end date
        while True:
            try:
                end_s = input("Please enter the end date in YYYY-MM-DD format: ")
                end_d = datetime.strptime(end_s, date_format)
                break
            except ValueError:
                print("incorrect date format. It should be YYYY-MM-DD.\n")

        # ensure end is after start
        if end_d > start_d:
            break
        else:
            print("end is before start\n")

    return start_s, end_s


if __name__ == "__main__":
    # take user's choice of option, exit if that's the choice, take dates otherwise
    opt = take_main_choice()
    if opt == 'D':
        print("See you next time")
        exit()
    d_start, d_end = take_dates_choice()


    yahoo_f = yf.YahooFinancials(opt_signs[opt])
    # you can continue still without ifs




if opt == 'A':
    yahoo_f = yf.YahooFinancials("QQQ")
    data = yahoo_f.get_historical_price_data(start_date=d_start, end_date=d_end, time_interval='daily')
    df = pd.DataFrame(data['QQQ']['prices'])
    df = df.drop('date', axis=1).set_index('formatted_date')
    df.head()
    # Calculating returns:
    df["returns"] = df["adjclose"] / df["adjclose"].shift(1) - 1
    df.head()
    df["leg_returns"] = df["returns"].shift(1)
    df["returns_pos"] = np.where(df['returns'] > 0, 1, 0)
    df.head()
    print(df)

elif opt == 'B':
    yahoo_f = yf.YahooFinancials("SPY")
    data = yahoo_f.get_historical_price_data(start_date=d_start, end_date=d_end, time_interval='daily')
    df = pd.DataFrame(data['SPY']['prices'])
    df = df.drop('date', axis=1).set_index('formatted_date')
    df.head()
    # Calculating returns:
    df["returns"] = df["adjclose"] / df["adjclose"].shift(1) - 1
    df.head()
    df["leg_returns"] = df["returns"].shift(1)
    df.head()
    df["returns_pos"] = 0
    df["returns_pos"] = np.where(df['returns'] > 0, 1, 0)

elif opt == 'C':
    yahoo_f = yf.YahooFinancials("IWM")
    data = yahoo_f.get_historical_price_data(start_date=d_start, end_date=d_end, time_interval='daily')
    df = pd.DataFrame(data['IWM']['prices'])
    df = df.drop('date', axis=1).set_index('formatted_date')
    df.head()
    # Calculating returns:
    df["returns"] = df["adjclose"] / df["adjclose"].shift(1) - 1
    df.head()
    df["leg_returns"] = df["returns"].shift(1)
    df.head()
    df["returns_pos"] = 0
    df["returns_pos"] = np.where(df['returns'] > 0, 1, 0)

elif opt == 'D':
    print("See you next time")
    exit()

# use this temp to know which option the user press
temp = int(input(
    "Press 1 to plot a timeseries of the prices\n2 to plot the timeseries of returns\n3 to plot a histogram of the positive returns\n4 to plot a scatter plot: returns vs. lagged returns\n5 to observe the mean, standard deviation and the coefficient of variation of the returns\n6 to Estimate a regression of the returns. Independent variable: pos returns\n7 to Check the % of correct predictions\n8 to return to choosing the data: "))
if temp == 1:
    # Setting the size of the figure
    plt.figure(figsize=(15, 10))
    # Choosing the number of days between observations (major ticks)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(120))
    # Setting the size of the fonts of the x- and y- ticks
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    # Drawing a figure of the adjusted closing price. The color of the line is green
    plt.plot(df["adjclose"], color="green")
    # Setting the y and x - titles
    plt.ylabel("Price", fontsize=16)
    plt.xlabel("Date", fontsize=16)
    # Setting the figure's title
    plt.title("The Adjusted Closing Price", fontsize=20)
    plt.show()
elif temp == 2:
    # Setting the size of the figure
    plt.figure(figsize=(15, 10))
    # Choosing the number of days between observations (major ticks)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(120))
    # Setting the size of the fonts of the x- and y- ticks
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    # Drawing a figure of the returns. The color of the line is green
    plt.plot(df["returns"], color="green")
    # Setting the y and x - titles
    plt.ylabel("Returns", fontsize=16)
    plt.xlabel("Date", fontsize=16)
    # Setting the figure's title
    plt.title("The Adjusted Closing Price", fontsize=20)
    plt.show()
elif temp == 3:
    # Histogram of the returns:
    plt.figure(figsize=(15, 10))
    # Setting the size of the fonts of the x- and y- ticks
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    # Drawing a histogram of the returns. The color of the line is blue.
    # The number of bins is 50
    plt.hist(df["returns_pos"], color="blue", bins=50)
    # Setting the y and x - titles
    plt.ylabel("Frequency", fontsize=16)
    plt.xlabel("Positive Returns", fontsize=16)
    # Setting the figure's title
    plt.title("Histogram of the  positive returns", fontsize=20)
    plt.show()
elif temp == 4:
    # Scatter plot: returns vs. lagged returns:
    plt.figure(figsize=(15, 10))
    # Setting the size of the fonts of the x- and y- ticks
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    # Drawing a scatter plot: returns vs. lagged returns. Color = purple
    plt.scatter(df["returns"], df["leg_returns"], color="purple")
    # Setting the y and x - titles
    plt.ylabel("Returns", fontsize=16)
    plt.xlabel("Lagged returns", fontsize=16)
    # Setting the figure's title
    plt.title("Returns vs. Lagged returns", fontsize=20)
    plt.show()
elif temp == 5:
    # get the mean, standard deviation and coefficient of variation
    avg = df["returns"].mean()
    stiya = df["returns"].std()
    cov = stiya / avg
    print("The average daily returns: " + str(avg) + "\nThe average daily returns standard deviation: " + str(stiya) + "\nThe coefficient of variation of the returns: " + str(cov))
elif temp == 6:
    # Regression:
    x = df["leg_returns"]  # independent variable number 1
    y = df["returns_pos"]  # dependent variable
    x = sm.add_constant(x)  # let's add an intercept (beta_0) to our model
    model = sm.ols(y, x).fit()
    predictions = model.predict(X)
    # Print out the statistics
    model.summary()
else:
    print("eee")
