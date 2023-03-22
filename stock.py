import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import matplotlib.pyplot as plt, plotly.express as px,plotly.graph_objects as go
from nsepy import get_history,get_index_pe_history
from nsetools import Nse
from datetime import date
#from alpha_vantage.fundamentaldata import FundamentalData
#import requests
import pandas_ta as ta

st.set_page_config(layout='wide', initial_sidebar_state='expanded')


nse = Nse()
#nse
st.title("Stocks ka Search Engine ")
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
      
with st.sidebar:
    add_radio = st.radio(
        "Select option",
        ("Stocks", "Indices")
    )
#tab1,tab2 = st.tabs(["Indices","Stocks"])
#with tab1:
if add_radio=="Indices":
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

         top_gain = nse.get_top_gainers(selectedindex) 

         dftopg = pd.DataFrame(top_gain)
         dftopg = dftopg.drop(["series","tradedQuantity", "turnoverInLakhs","lastCorpAnnouncementDate","lastCorpAnnouncement"],axis=1)
         change = ((dftopg['ltp'] - dftopg['previousPrice']))
# Add the change percentage as a new column
         dftopg['Change'] = change
         top_loss = nse.get_top_losers(selectedindex)
         dftopl = pd.DataFrame(top_loss)
         dftopl = dftopl.drop(["series", "tradedQuantity", "turnoverInLakhs","lastCorpAnnouncementDate","lastCorpAnnouncement"],axis=1)
         change = ((dftopl['ltp'] - dftopl['previousPrice']))
# Add the change percentage as a new column
         dftopl['Change'] = change
         tab1, tab2 = st.tabs(["Gainer", "Losers"])
         with tab1:
                st.header("Top Gainers")
                fig_barG = px.bar(dftopg['symbol'],x=dftopg['symbol'],y=dftopg['netPrice'])
                st.plotly_chart(fig_barG)  
                st.dataframe(dftopg)
         with tab2:
                st.header("Top Losers")
                fig_barL = px.bar(dftopl['symbol'],x=dftopl['symbol'],y=dftopl['netPrice'])
                st.plotly_chart(fig_barL)
                st.dataframe(dftopl)
         #fig_barG = px.bar(dftopg['symbol'],x=dftopg['symbol'],y=dftopg['netPrice'])
         #fig_barL = px.bar(dftopl['symbol'],x=dftopl['symbol'],y=dftopl['netPrice'])
           #col1,col2 = st.columns(2)
          # with col1:
           #          st.plotly_chart(fig_barG)
           #with col2:
            #         st.plotly_chart(fig_barL)




#with tab2:
#        
#        
if add_radio=="Stocks":
           
           st.header('Stock Dashboard')
           qt =  pd.DataFrame(nse.get_stock_codes().items(), columns=['SYMBOL', 'NAME OF COMPANY'])
           qt = qt.iloc[1:]

           selectedstock = st.selectbox('Select Stock',qt["SYMBOL"])
#selectedstock = str(selectedstock)
           stockst_date = st.date_input("Start Date")
           stocked_date = date.today()
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
           #pddfstk = pd.DataFrame(dfstk)
           #st.write(pddfstk)

           fig = go.Figure(data=[go.Candlestick(x=dfstk.index,
                open=dfstk['Open'], high=dfstk['High'],
                low=dfstk['Low'], close=dfstk['Close'])
                     ])
           fig.update_layout(xaxis_rangeslider_visible=False)
           st.plotly_chart(fig)
           sdata  = get_history(symbol=selectedstock,start=stockst_date,end=stocked_date)
           sdf = pd.DataFrame(sdata)
           sdf = sdf.drop(["Series","Turnover","Trades","Deliverable Volume","%Deliverble"],axis=1)
           change_v = ((sdf['Last'] - sdf['Prev Close']))
           change_per = ((sdf['Last'] - sdf['Prev Close'])/sdf['Prev Close'])*100
# Add the change percentage as a new column
           sdf["Chng"]  = change_v
           sdf['%Chng'] = change_per
           sdf
           #annual_returns = sdf['%Chng'].mean()*252
           #st.write("Annual Return is",annual_returns,"%")
           dfi = pd.DataFrame()
           ind_lis = dfi.ta.indicators(as_list = True)
           tech_ind = st.selectbox("Technical Indicators",options = ind_lis)
           method = tech_ind
           indicator = pd.DataFrame(getattr(ta,method)(open=dfstk['Open'], high=dfstk['High'],
                low=dfstk['Low'], close=dfstk['Close'],volume=dfstk['VWAP']))
           indicator['Close']=dfstk['Close']
           fig_line = px.line(indicator)
           st.plotly_chart(fig_line)
           st.write(indicator)
           #fig_indic = px.candle
           #fig_ind = go.Figure(data=[go.Candlestick(indicator.index)])
           #fig_ind.update_layout(xaxis_rangeslider_visible=False)
           #fig_ind = go.Figure(data=[go.Candlestick(x=indicator.index,
           #     open=dfstk['Open'], high=dfstk['High'],
           #     low=dfstk['Low'], close=dfstk['Close'])
            #         ])
           #st.plotly_chart(fig_ind)

