from urllib.request import urlopen
import json
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from scipy import stats
from datetime import datetime, timedelta

rawAddress = "https://rsbuddy.com/exchange/summary.json"

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="testPass",
	database="OSRSGE"
)

mycursor = mydb.cursor()

sql = "INSERT INTO itemquery (datetime, itemname, members, buyaverage, buyquantity, sellaverage, sellquantity, overallaverage, overallquantity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

now = datetime.now()
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

def mean(dataset, *args):
    mean = 0.
    for x in dataset:
        mean = mean + x
    mean = mean/len(dataset)
    return mean

def stdDev (mean, dataset, *args):
    stdDev = 0.
    for x in dataset:
        stdDev = stdDev + (x-mean)**2
    stdDev = stdDev/(len(dataset)-1)
    stdDev = np.sqrt(stdDev)
    return stdDev


totalMarketBought = 0
totalMarketSold = 0

totalBoughtQuant = 0
totalSoldQuant = 0

pricelog = []
quantlog = []
bulkQuant = []
    
page = urlopen(rawAddress)

jsonData = json.load(page)
    
for key in jsonData.keys():
	totalMarketBought = totalMarketBought + jsonData[str(key)][u'buy_average']*jsonData[str(key)][u'buy_quantity']
	totalMarketSold = totalMarketSold + jsonData[str(key)][u'sell_average']*jsonData[str(key)][u'sell_quantity']
	totalBoughtQuant = totalBoughtQuant + jsonData[str(key)][u'buy_quantity']
	totalSoldQuant = totalSoldQuant + jsonData[str(key)][u'sell_quantity']
	if jsonData[str(key)][u'buy_average'] > 0 and jsonData[str(key)][u'buy_quantity'] > 0 and jsonData[str(key)][u'sell_quantity'] > 0:
		pricelog.append(jsonData[str(key)][u'buy_average'])
		quantlog.append(jsonData[str(key)][u'buy_quantity'])
		bulkQuant.append((jsonData[str(key)][u'buy_average']-jsonData[str(key)][u'sell_average'])*(jsonData[str(key)][u'buy_quantity']+jsonData[str(key)][u'sell_quantity']))

	val = (formatted_date, jsonData[str(key)][u'name'], jsonData[str(key)][u'members'], jsonData[str(key)][u'buy_average'], jsonData[str(key)][u'buy_quantity'], jsonData[str(key)][u'sell_average'], jsonData[str(key)][u'sell_quantity'], jsonData[str(key)][u'overall_average'], jsonData[str(key)][u'overall_quantity'])
	mycursor.execute(sql, val)
	mydb.commit()

pMean = mean(bulkQuant)
pStdDev = stdDev(pMean, bulkQuant)
pMode = stats.mode(bulkQuant)

with open("stats.txt", 'a') as myfile:
	myfile.write(str(datetime.now()) + "," + str(pMean) + "," + str(pStdDev)  + "," + str(totalMarketBought) + "," + str(totalMarketSold) + "," + str(totalBoughtQuant) + "," + str(totalSoldQuant))

#print("Mean value of goods: " + str(pMean))
#print("Std deviation of goods: " + str(pStdDev))
#print("Mode of goods: " + str(pMode))

#plt.hist(bulkQuant, bins=1000, density=True)
#plt.xlabel("Price brackets")
#plt.ylabel("Quantity of items at price")
#plt.show()

for x in range(0, len(bulkQuant)):
	bulkQuant[x] = (bulkQuant[x]-pMean)/pStdDev

sMean = mean(bulkQuant)
sStdDev = stdDev(sMean, bulkQuant)
sMode = stats.mode(bulkQuant)
    
#print("Standardized mean: " + str(sMean))
#print("Standardized std deviation: " + str(sStdDev))
#print("Standardized mode: " + str(sMode))
            
#print("Total market value of bought goods:" + str("{:,}".format(totalMarketBought)))
#print("Total market value of sold goods:" + str("{:,}".format(totalMarketSold)))
#print("Total quantity of bought goods:" + str("{:,}".format(totalBoughtQuant)))
#print("Total quantity of sold goods:" + str("{:,}".format(totalSoldQuant)))
    
#plt.hist(bulkQuant, bins=1000, density=True)
#plt.xlabel("Price brackets")
#plt.ylabel("Quantity of items at price")
#plt.show()