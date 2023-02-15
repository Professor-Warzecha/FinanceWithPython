# Peter Warzecha Homework IX (Final Project)
# Python Retirement Saving Program

### Import our nesseccary packages

import quandl
quandl.ApiConfig.api_key = 'BNy_ZPWsiEbwMz_BT8sL'

### Created my own portfolios based on timeframe available for investments to compound value
### Shorter time frames will be assigned a less risky portfolio
### Longer time frames will be assigned a more risky portfolio
### ESG preferences overrule all

growthStocks = ["AMZN","GOOG","JNJ","CRM","FB"]
blueChipStocks = ["WMT","PEP","KO","NKE","AXP"]
ESGStocks = ["CSCO","VZ","MSFT","PYPL","EXC"]

### Create lists of options for Yes and No

Yes = ["Yes", "yes", "YES", "yea", "sure", "ok", "Ok", "OK", "Fine", "fine"]
No = ["No", "no", "nope"]

getStarted = input("Do you want to start creating your retirement portfolio?\n>> ")

### Convince the user to use my code

while getStarted not in Yes:
    print("\n")
    if getStarted in Yes:
        print("Ok, lets go!")
        print("\n")
    elif getStarted in No:
        print("Oh come on, try it out. It's free!")
        print("\n")
        getStarted = input("Do you want to start creating your retirement portfolio?\n>> ")
        print("\n")
    else:
        print("Hm, not sure what you mean, try again")
        print("\n")
        getStarted = input("Do you want to start creating your retirement portfolio?\n>> ")
        print("\n")
        
print("Ok, lets go!")
print("\n")

### Ask some basic questions to determine which portfolio is suitable

userStartingAmount = input("How much can you currently invest? (Should be over $1000) \n>> ")
print("\n")
userAge = input("What is your current age?\n>> ")
print("\n")
userRetirementAge = input("At what age do you think you'll retire by? (Estimate)\n>> ")
print("\n")

### Use error handling incase one of the previous inputs could not be used

try:
    timeTillRetirement = int(userRetirementAge) - int(userAge)
except:
    print("Uh oh, one of the values you entered for either your age or anticipated age of retirement is not a number, please re-enter them")
    print("\n")
    userAge = input("What is your current age?\n>> ")
    print("\n")
    userRetirementAge = input("At what age do you think you'll retire by? (Estimate)\n>> ")
    print("\n")

timeTillRetirement = int(userRetirementAge) - int(userAge)

userESGPreference = input("Are you interested in ESG? These companies focus on sustainable and ethical impacts (Yes or No)\n>> ")
print("\n")

### Determine portfolio based on inputs

if timeTillRetirement >= 10 and userESGPreference in No:
    stocks = growthStocks
elif timeTillRetirement <= 10 and userESGPreference in No:
    stocks = blueChipStocks
elif timeTillRetirement >= 10 and userESGPreference in Yes:
    stocks = ESGStocks
elif timeTillRetirement <= 10 and userESGPreference in Yes:
    stocks = ESGStocks

### Took this function from the following website
### (https://medium.com/python-data/quandl-getting-end-of-day-stock-data-with-python-8652671d6661)

data = quandl.get_table('WIKI/PRICES', ticker = stocks, 
                        qopts = { 'columns': ['ticker', 'date', 'adj_close'] }, 
                        date = { 'gte': '2015-12-31', 'lte': '2016-12-31' }, 
                        paginate=True)

newData = data.set_index('date')

### I set the date to December 30th, 2016 because I couldn't figure out how to get the latest closing price using quandl
### Whenver I change the date prameters to something more recent it didn't pull the stock prices
### Please don't be dissapointed 

df = (newData.loc['2016-12-30'])

closePrices = df['adj_close'].tolist()

### Calcualte maximum of each stock we can buy

eachStockLimit = float(userStartingAmount) / 5

newList = []

for x in closePrices:
    stocksBought = eachStockLimit // x
    newList.append(stocksBought)
    
### Calculate amount of stocks bought for each stock in the portfolio

stock1Worth = newList[0] * closePrices[0]
stock2Worth = newList[1] * closePrices[1]
stock3Worth = newList[2] * closePrices[2]
stock4Worth = newList[3] * closePrices[3]
stock5Worth = newList[4] * closePrices[4]

portfolioValues = [stock1Worth, stock2Worth, stock3Worth, stock4Worth, stock5Worth]

### These 10 year annual average return values were taken from this website
### https://www.averageannualreturn.com/
### You can input each ticker symbol and it will show you each stock's 10 year annual average return

ESGAnnualAverageReturns = [18.25, 2.88, 26.97, 9.84, 10.79]
growthStockAnnualAverageReturns = [21.67, 14.83, 12.26, 12.26, 15.27]
blueChipStockAnnualAverageReturns = [9.85, 13.23, 8.61, 17.27, 12.02]

### Create if statement to change value for average return for each stock based on portfolio

if stocks == ESGStocks:
    averageReturn = ESGAnnualAverageReturns
    finalPortfolio = ESGStocks
elif stocks == growthStocks:
    averageReturn = growthStockAnnualAverageReturns
    finalPortfolio = growthStocks
elif stocks == blueChipStocks:
    averageReturn = blueChipStockAnnualAverageReturns
    finalPortfolio = blueChipStocks

def futureValue():
    totalAmount1 = int(stock1Worth) * ((1+(0.01*averageReturn[0])) ** int(timeTillRetirement))
    totalAmount2 = int(stock2Worth) * ((1+(0.01*averageReturn[1])) ** int(timeTillRetirement))
    totalAmount3 = int(stock3Worth) * ((1+(0.01*averageReturn[2])) ** int(timeTillRetirement))
    totalAmount4 = int(stock4Worth) * ((1+(0.01*averageReturn[3])) ** int(timeTillRetirement))
    totalAmount5 = int(stock5Worth) * ((1+(0.01*averageReturn[4])) ** int(timeTillRetirement))
    totalAmount = totalAmount1 + totalAmount2 + totalAmount3 + totalAmount4 + totalAmount5
    return totalAmount

### Call function to determine final dollar amount of our portfolio

finalValue = futureValue()

### Create variable and assign how much the portfolio grew in percent 

totalReturn = ((int(finalValue) - int(userStartingAmount)) / int(userStartingAmount) * 100)

### Create a final list to show which stocks the user is invested in

finalPortfolioList = []

for allStocks in finalPortfolio:
    finalPortfolioList.append(allStocks)

print("Nice job, based on your answers here is your following portfolio.")
print("\n")
print("The stocks you are invested in are " + str(finalPortfolioList))
print("\n")
print("The total value of your portfolio in " + str(timeTillRetirement) + " years is estimated to be $" + str(finalValue))
print("\n")
print("That is a return of " + str(totalReturn) + "%! Well done!")

stocksPriceAllocationList = '/Users/peterwarzecha/Desktop/Portfolio.csv'

### Record the portfolio information in a csv

with open(stocksPriceAllocationList, 'w', encoding = 'utf8') as output:
    output.write("Stock Tickers" + "," + str(finalPortfolioList))
    output.write("\n")
    output.write("Original Investment in Stock" + "," + str(portfolioValues))
    output.write("\n")
    output.write("Amount of Each Stock Held" + "," + str(newList))
    
print("\n")
print("Your portfolio has been recorded in a csv file.")