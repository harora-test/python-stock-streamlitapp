import pickle
import streamlit as st
import datetime, time
import numpy as np
import plotly.graph_objects as go
import pandas_datareader as pdr
import pandas as pd

df = pd.DataFrame()

@st.cache
def load_data():
    startdate = datetime.datetime(2002,1,1)
    enddate = datetime.date.today()
    df = pdr.get_data_yahoo('HDFC.NS', startdate, enddate)
    return df
    
def predict(loaded_data, stock, ldays, fdays):
    st.write(stock)
    st.write(ldays)
    st.write(fdays)


#Setup Page
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('STOCK FORECAST')
current_status = st.empty()
current_status.write("Current Status: Data App Loaded")

#Store Data Loaded in Session State
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False

#Set Sidebar
controller = st.sidebar.container() 
controller.subheader("Controller") 
menu = ['None','Load Model', 'Forecast']
task = controller.selectbox("Select Task", menu)

if task=='Load Model':
    current_status.write('Loading The Data ...')
    time.sleep(0.1)
    if(st.session_state['data_loaded']):
        current_status.write('Data Already Loded Please Forecast')
    else:
        df = load_data()
        current_status.write('Data Loaded!')
        st.session_state['data_loaded'] = True
        st.write(df)
elif task=='Forecast':
    if(not(st.session_state['data_loaded'])):
        current_status.write('Please Load the data before Forecasting')
    else:
        trained_stocks = np.array([ "GOOG", "GME", "FB","AAPL",'TSLA']) 
        #Set Session Variable If Not Present
        if 'stock' not in st.session_state:
            st.session_state['stock'] = 'GOOG'
        if 'ldays' not in st.session_state:
            st.session_state['ldays'] = 30
        if 'fdays' not in st.session_state:
            st.session_state['fdays'] = 5
        controller.selectbox("Select Stock", trained_stocks, key='stock')
        controller.slider("Last Known Days", 10, 200, 30, key='ldays')
        controller.slider("Forecast Days", 1, 10, 5, key='fdays')
        if controller.button('Run Model'):
            predict(df, st.session_state['stock'], st.session_state['ldays'], st.session_state['fdays'])
else:
    pass