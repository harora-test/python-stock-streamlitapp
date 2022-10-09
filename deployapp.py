import pickle
import streamlit as st
import datetime, time
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas_datareader as pdr
import pandas as pd
import joblib
import s3fs


@st.experimental_memo
def load_data():
    if st.secrets['USEAWS']=="TRUE":
        fs = s3fs.S3FileSystem(anon=False)
        with fs.open('appliedroot-project-stock/testdict.sav') as f:
            loaddict = joblib.load(f)
        return loaddict 
    else:
        loaddict = joblib.load('testdict.sav')
        return loaddict
    
def predict(loaded_data, stock, ldays, fdays):
    lkey = stock+'_ldays'
    fkey = stock+'_fdays'
    lstock = loaded_data[lkey]
    fstock = loaded_data[fkey]
    lstock = lstock.tail(ldays)
    fstock = fstock.head(fdays)  
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=lstock.index, y=lstock['Close'], name='Actual', fillcolor='blue', mode='lines'))
    fig.add_trace(go.Scatter(x=fstock.index, y=fstock['Close'], name='Forecasted', fillcolor='red', mode='lines+markers'))
    fig.update_layout(title=stock.title() + " Price Forecast", xaxis_title="Date", yaxis_title="Closing Price", height=500, width=800)
    graph.plotly_chart(fig, height=500, width=800)
    


#Setup Page
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
st.title('STOCK FORECAST')
current_status = st.empty()
current_status.write("Current Status: Data App Loaded")
graph = st.empty()

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
        data = load_data()
        st.session_state['extracted_data'] = data
        st.session_state['last_update'] = data['last_update']
        st.session_state['stock_list'] = data['stock_list']
        current_status.write('Finished Loading the Data!')
        st.session_state['data_loaded'] = True

elif task=='Forecast':
    if(not(st.session_state['data_loaded'])):
        current_status.write('Please Load the data before Forecasting')
    else:
        data = st.session_state['extracted_data']
        stock_list = st.session_state['stock_list']
        #Set Session Variable If Not Present
        if 'stock' not in st.session_state:
            st.session_state['stock'] = stock_list[0]
        if 'ldays' not in st.session_state:
            st.session_state['ldays'] = 30
        if 'fdays' not in st.session_state:
            st.session_state['fdays'] = 5
        pforecast = controller.container()
        pforecast.selectbox("Select Stock", stock_list, key='stock')
        pforecast.slider("Last Known Days", 10, 200, 30, key='ldays')
        pforecast.slider("Forecast Days", 1, 10, 5, key='fdays')
        with pforecast:
            predict(data, st.session_state['stock'], st.session_state['ldays'], st.session_state['fdays'])
else:
    pass