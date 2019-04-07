from flask import Flask,jsonify
import bs4 as bs
import sys
import urllib.request
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        
    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()

#url = input('Enter the URL: ')
def getDetails(page):
	soup = bs.BeautifulSoup(page.html, 'html.parser')

	divs_bank  = soup.find("div",{"class":"bank_info"})

	companyName = divs_bank.find("div",{"class":"left_info"}).find("span",{"id":"companyName"}).text
	print ("Name of Company ",companyName)#Name of Company

	symbol = divs_bank.find("div",{"class":"left_info"}).find("span",{"id":"symbol"}).text
	print("Symbol " , symbol)#Symbol

	series = divs_bank.find("a",{"class":"sel"}).text
	print("Series " ,series)#Series

	isin = divs_bank.find("div",{"class":"left_info"}).find_all("ul")[1].find_all("li")[1].text
	print (isin)#ISIN

	divs_lt = soup.find("div",{"class":"details"}).find_all("div",{"class":"leftTableData"})

	for item in divs_lt:
	    lists_lt = item.find_all("li")

	show_hide = soup.find_all("div",{"class":"show_hide_content"})[1]
	applicableMargin = show_hide.find("span",{"id":"applicableMargin"}).text
	print("Applicable Margin Rate: ",applicableMargin)


	vwap = lists_lt[1].text 
	print(vwap)#Volume Weighted Average Price

	stock_items = soup.find("ul",{"class":"stock"})

	lastPrice = stock_items.find("span",{"id":"lastPrice"}).text
	print("Last Price: ",lastPrice)

	try:
	    change = stock_items.find("span",{"class":"up"}).text
	    print("Change " ,change )
	except:
	    change = stock_items.find("span",{"class":"down"}).text
	    print("Change " ,change )

	perChange = stock_items.find("a",{"id":"pChange"}).text
	print("Percentage Change ",perChange)

	dayOpen = stock_items.find("div",{"id":"open"}).text
	print("Day Open ",dayOpen)

	dayHigh = stock_items.find("div",{"id":"dayHigh"}).text
	print("Day High ",dayHigh)

	dayLow = stock_items.find("div",{"id":"dayLow"}).text
	print("Day Low ",dayLow)

	closePrice =  stock_items.find("div",{"id":"closePrice"}).text
	print("Close Price ",closePrice)


	return ({"Name of Company":companyName,"Symbol" : symbol,"Series" :series,"Applicable Margin Rate":applicableMargin,"Last Price":lastPrice,"Change" :change,"Day Open":dayOpen,"Day High":dayHigh,"Day Low":dayLow,"Close Price":closePrice})

flaskapp = Flask(__name__)
@flaskapp.route('/')

def createJson():
	return jsonify(data)
if __name__ == '__main__':
	#inpSym = input("Enter the symbol if the company: ")
	data = dict()
	inpSym='TECHM'
	url ='https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+ inpSym
	page = Page(url)
	data = getDetails(page)
	flaskapp.run(debug = True)
