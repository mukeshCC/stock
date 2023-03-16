import streamlit as st, pandas as pd, numpy as np
import matplotlib.pyplot as plt, plotly.express as px,plotly.graph_objects as go
from nsepy import get_history,get_index_pe_history
from nsetools import Nse
from datetime import date
import requests
from bs4 import BeautifulSoup

nse = Nse()
#nse
st.title("Stock ka Search Engine ")
adv_dec = nse.get_advances_declines()
df = pd.DataFrame(adv_dec)
#df

nifty_50 = nse.get_index_quote("nifty 50")
currprice = nifty_50['lastPrice']
idxchg = nifty_50['change']
#st.title("nifty 50")

nifty_bank = nse.get_index_quote("nifty bank")
currtprice = nifty_bank['lastPrice']
idchg = nifty_bank['change']
#st.title("nifty_bank")
col1,col2 = st.columns(2)
with col1:
    st.title("Nifty 50")
    st.metric("Current Price",currprice,idxchg)
with col2:
    st.title("Nifty Bank")
    st.metric("Current Price",currtprice,idchg)
      
top_gain = nse.get_top_gainers()
dftopg = pd.DataFrame(top_gain)
dftopg = dftopg.drop(["series","tradedQuantity", "turnoverInLakhs","lastCorpAnnouncementDate","lastCorpAnnouncement"],axis=1)
change = ((dftopg['ltp'] - dftopg['previousPrice']))
# Add the change percentage as a new column
dftopg['Change'] = change

top_loss = nse.get_top_losers()
dftopl = pd.DataFrame(top_loss)
dftopl = dftopl.drop(["series", "tradedQuantity", "turnoverInLakhs","lastCorpAnnouncementDate","lastCorpAnnouncement"],axis=1)
change = ((dftopl['ltp'] - dftopl['previousPrice']))
# Add the change percentage as a new column
dftopl['Change'] = change

tab1,tab2 = st.tabs(["Indices","Stocks"])
with tab1:
         selectedindex = st.selectbox('Select Index',nse.get_index_list())
         df1 = df[df['indice'] == selectedindex]
         currprice = nse.get_index_quote(selectedindex)['lastPrice']
         idxchg = nse.get_index_quote(selectedindex)['change']
         st.title(selectedindex)
         col1, col2, col3 = st.columns(3)
         col1.metric("Current Price", currprice,idxchg)
         col2.metric("Advances", df1["advances"])
         col3.metric("Declines", df1["declines"])
#col3.metric("52 week high",yrHigh)
#col3.metric("52 week low",yrLow)
#with col2:
    #st.title("CandleStick Chart")
    #st.plotly_chart(fig)

         start_date = date(2019,1,1)
         end_date = date.today()
         idata  = get_history(symbol=selectedindex,start=start_date,end=end_date,index=True)
#index_data = pd.DataFrame(index)
         dfid = pd.DataFrame(idata)
         #st.write(dfid)
         fig_index = px.line(dfid,x=dfid.index,y='Close',title=selectedindex)
         st.plotly_chart(fig_index)
         fig_i = go.Figure(data=[go.Candlestick(x=dfid.index,
                open=dfid['Open'], high=dfid['High'],
                low=dfid['Low'], close=dfid['Close']),
                     ])

         fig_i.update_layout(xaxis_rangeslider_visible=False)
         st.title("CandleStick Chart")
         st.plotly_chart(fig_i)
         


with tab2:
        tab1, tab2 = st.tabs(["Gainer", "Losers"])
        with tab1:
           st.header("Top Gainers")
           st.dataframe(dftopg)    
        with tab2:
           st.header("Top Losers")
           st.dataframe(dftopl)

        fig_barG = px.bar(dftopg['symbol'],x=dftopg['symbol'],y=dftopg['netPrice'])
        fig_barL = px.bar(dftopl['symbol'],x=dftopl['symbol'],y=dftopl['netPrice'])
        col1,col2 = st.columns(2)
        with col1:
             st.plotly_chart(fig_barG)
        with col2:
             st.plotly_chart(fig_barL)


        st.header('Stock Dashboard')
        qt =  pd.DataFrame(nse.get_stock_codes().items(), columns=['SYMBOL', 'NAME OF COMPANY'])
        qt = qt.iloc[1:]

        selectedstock = st.selectbox('Select Stock',qt["SYMBOL"])
#selectedstock = str(selectedstock)
        stockst_date = st.date_input("Start Date")
        stocked_date = st.date_input("End Date")
        #marketcap = nse.get_quote(selectedstock)['marketCap']
        stkchg = nse.get_quote(selectedstock)['change']
        compnm = nse.get_quote(selectedstock)['companyName']
        currprice = nse.get_quote(selectedstock)['lastPrice']
        dayHigh = nse.get_quote(selectedstock)['dayHigh']
        dayLow = nse.get_quote(selectedstock)['dayLow']
        yrHigh =nse.get_quote(selectedstock)['high52']
        yrLow = nse.get_quote(selectedstock)['low52']

# Row A
        st.title(compnm)
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", currprice,stkchg)
        col2.metric("Day High", dayHigh )
        col2.metric("Day Low", dayLow )
        col3.metric("52 week high", yrHigh)
        col3.metric("52 week low",yrLow)
        #col3.metric("Market Cap ",marketcap)

        dfstk = get_history(symbol=selectedstock,
                   start=stockst_date,
                   end=stocked_date)

        fig = go.Figure(data=[go.Candlestick(x=dfstk.index,
                open=dfstk['Open'], high=dfstk['High'],
                low=dfstk['Low'], close=dfstk['Close'])
                     ])

        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)
        sdata  = get_history(symbol=selectedstock,start=stockst_date,end=stocked_date)
        sdf = pd.DataFrame(sdata)
        sdf = sdf.drop(["Series","Volume","Turnover","Trades","Deliverable Volume","%Deliverble"],axis=1)
        change_v = ((sdf['Last'] - sdf['Prev Close']))
        change_per = ((sdf['Last'] - sdf['Prev Close'])/sdf['Prev Close'])*100
# Add the change percentage as a new column
        sdf["Chng"]  = change_v
        sdf['%Chng'] = change_per
        sdf












        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        #url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=(selectedstock)&apikey=7FYQ2CXFCMYVMHOS'
        #r = requests.get(url)
        #data = r.json()

        #print(data)
        #st.write(data)

        #symbol = st.text_input("Enter Stock Symbol", "AAPL")

       # Set Alpha Vantage API key
        #ALPHAVANTAGE_API_KEY = "7FYQ2CXFCMYVMHOS"
        

# Create function to fetch stock overview data from Alpha Vantage
        #def fetch_stock_overview(symbol):
         #url =  f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={'7FYQ2CXFCMYVMHOS'}"
         #response = requests.get(url)
         #data = response.json()
         #return data

        #data = fetch_stock_overview(symbol)


# Create Streamlit app
        #st.title("NSE Stock Overview")
# Get stock symbol from user input
# Fetch stock overview data from Alpha Vantage
# Display stock overview data
        #if data:
         #st.subheader(f"Overview of {data['Name']} ({symbol})")
         #overview = pd.DataFrame(data.items(), columns=["Attribute", "Value"])
         #st.write(overview)
        #else:
          #st.warning("No data found. Please enter a valid stock symbol.")



        #key = '7FYQ2CXFCMYVMHOS'
        #url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={selectedstock}&apikey={'7FYQ2CXFCMYVMHOS'}"
        #response = requests.get(url)
        #data = response.json()
        #data
        # Retrieve the balance sheet data as a dictionary of key-value pairs
        #balance_sheet_data = data["balanceSheetAnnual"]

    # Convert the dictionary to a pandas DataFrame
        #balance_sheet_df = pd.DataFrame.from_dict(balance_sheet_data, orient="index").transpose()

        #fd = FundamentalData(key,output_format = 'pandas')
        #baln_sheet = fd.get_balance_sheet_annual(selectedstock)[0]
        #bs = baln_sheet.T[2:]
        #bs.columns = list(baln_sheet.T.iloc[0])
        #st.write(balance_sheet_df)
        #st.title('Balance Sheet Data')

        #symbol = st.text_input('Enter the stock symbol of the company (e.g. RELIANCE.NS):')

        #if selectedstock:
           # url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={selectedstock}&apikey=7FYQ2CXFCMYVMHOS'
    
          #  response = requests.get(url)
    
        #if response.ok:
         #data = response.json()
         #annual_reports = data['annualReports']
        
        #for report in annual_reports:
            #fiscal_year = report['fiscalDateEnding']
            #total_assets = report['totalAssets']
            #total_liabilities = report['totalLiabilities']
            #shareholder_equity = report['shareholderEquity']
            
            #st.write(f'Fiscal Year: {fiscal_year}')
            #st.write(f'Total Assets: {total_assets}')
            #st.write(f'Total Liabilities: {total_liabilities}')
            #st.write(f'Shareholder Equity: {shareholder_equity}')
        #else:
         #st.write('Error fetching data. Please try again later.')
        #response.status_code
#data = yf.download(Ticker,start=start_date,end=end_date)
#data
#stock_data = get_history(symbol=Ticker, start=start_date, end=end_date)
#stock_data
#fig = px.line(stock_data,x=stock_data.index,y=stock_data['Close'],title=Ticker)
#st.plotly_chart(fig)
#fig1 = go.Figure(data=[go.Candlestick(x=stock_data.index,open=stock_data['Open'],high=stock_data['High'],
#                                      low=stock_data['Low'],close=stock_data['Close'])]
#)

#fig1.show()
# Create the candlestick chart using Plotly
#fig = go.Figure(data=[go.Candlestick(x=stock_data.index,
                                     # open=stock_data['Open'],
                                     # high=stock_data['High'],
                                     # low=stock_data['Low'],
                                     # close=stock_data['Close'])])
#fig.update_layout(title=f'{Ticker} Stock Price',
                  #xaxis_title='Date',
                  #yaxis_title='Price (INR)')
#st.plotly_chart(fig)
# Create the visualizations
#fig1 = go.Figure(data=go.Scatter(x=stock_data.index, y=stock_data['Close']))
#fig1.update_layout(title=f'{Ticker} Stock Price', xaxis_title='Date', yaxis_title='Price (INR)')
# Add interactivity
#st.sidebar.write('Select the visualization:')
#visualization = st.sidebar.selectbox('', ['Historical Prices', 'Candlestick Chart'])

# Display the visualizations
#if visualization == 'Historical Prices':
    #st.plotly_chart(fig1)
#elif visualization == 'Candlestick Chart':
    #st.plotly_chart(fig)


# Fetch the data
#nifty_pe = get_index_pe_history(index='NIFTY 50', start='01-01-2022', end='12-03-2023')
#nifty_close = get_history(symbol='NIFTY 50', start='01-01-2022', end='12-03-2023')
#sensex_close = get_history(symbol='SENSEX', start='01-01-2022', end='12-03-2023')

# Display the data
#st.subheader('Indices')
#st.write(f'Nifty 50 PE Ratio: {nifty_pe.iloc[-1]["P/E"]}')
#st.write(f'Nifty 50 Close: {nifty_close.iloc[-1]["Close"]}')
#st.write(f'Sensex Close: {sensex_close.iloc[-1]["Close"]}')
#indices = nse.get_index_list()
#s_index = st.selectbox("Select an Indice",indices)

# Define the web application
#st.set_page_config(page_title='Stock Market Dashboard', page_icon=':chart_with_upwards_trend:')
#st.title('Stock Market Dashboard')
#Ticker = st.sidebar.text_input('Ticker')
#start_date = st.sidebar.date_input('Start Date')
#end_date = st.sidebar.date_input('End Date')

#left_column,right_column = st.columns(2)

#indices = st.text_input("Select the indices")
#index_data = yf.download('indices',start='2010-01-01')
    #index = get_index_pe_history
#nifty_df = yf.download("^NSEI", start="2010-01-01")
    #nifty_df
    #sensex_df = yf.download("^BSESN", start="2010-01-01")
    #niftybank_df = yf.download("^NSEBANK", start="2010-01-01")
    
#index_data = pd.DataFrame(index_data)
#nifty_data = pd.DataFrame(nifty_df)
    #sensex_data = pd.DataFrame(sensex_df)
    #niftybank_data = pd.DataFrame(niftybank_df)
    
#fig_index = px.line(index_data,x=index_data.index,y='Close',title=indices)
#fig_nifty = px.line(nifty_data, x=nifty_data.index, y='Close', title='Nifty Index')
    #fig_sensex = px.line(sensex_data, x=sensex_data.index, y='Close', title='Sensex Index')
    #fig_niftybank = px.line(niftybank_data, x=niftybank_data.index, y='Close', title='Nifty Bank Index')
    
#st.plotly_chart(fig_index)
#st.plotly_chart(fig_nifty)
    #st.plotly_chart(fig_sensex)
    #st.plotly_chart(fig_niftybank)
    
#if __name__ == '__main__':
    #main()
# Ticker symbol for the NIFTY 50 index on NSE
#symbol = 'NIFTY 50'

# Fetch data for the NIFTY 50 index from NSE
#nse = Nse()
#quote = nse.get_quote("nifty 50")
#data = get_history(symbol=quote,
                    #start='2010-01-01',
                    #end='2022-03-14',
                    #index=True)

# Create a candlestick chart using plotly
#fig = go.Figure(data=[go.Candlestick(x=data.index,
                                     #open=data['Open'],
                                     #high=data['High'],
                                     #low=data['Low'],
                                     #close=data['Close'])])

# Set the chart title
#fig.update_layout(title='NIFTY 50 Candlestick Chart')

# Display the chart in Streamlit
#st.plotly_chart(fig)

#dfi = pd.DataFrame(id)
#dfind = get_history(symbol=dfi,
                   #start=date(2023,1,15),
                   #end=date(2023,2,3))
#fig = go.Figure(data=[go.Candlestick(x=dfind.index,
                #open=dfind['Open'], high=dfind['High'],
                #low=dfind['Low'], close=dfind['Close'])
                 #    ])

#fig.update_layout(xaxis_rangeslider_visible=False)
#st.plotly_chart(fig)
#fig_line = px.line(dfi, x=dfi.index, y='Close', title=selectedindex)

#yrHigh =nse.get_index_quote(selectedindex)['high52']
#yrLow = nse.get_index_quote(selectedindex)['low52']

