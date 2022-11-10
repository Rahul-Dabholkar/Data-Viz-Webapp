import numpy as np
import pandas as pd
import streamlit as st
import plotly_express as px
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# FONT THEME AND ALIGNMENT
st.set_page_config(layout="wide")
st.markdown("""
<style>
.header {
    font-size:60px;text-align:center; !important;
}

.paragraph{
    font-size:20px;text-align:center;
}

.highlight{
    background-color:#BAD7DF;
}
</style>
""", unsafe_allow_html=True)


# HEADER AND TITLE 
st.markdown(
    "<h1 class = 'header'> VISUAL DATA INSIGHTS </h1>"
    "<p class = 'paragraph'> An EDA APP created in Streamlit where you can make  <b>CUSTOM CHARTS</b> or get visualizations generated through <b>Pandas_Profiling</b> library.</p>"
    "<p style = 'text-align:center;'> App Built Using : \
        <mark class = 'highlight'> Python </mark> + \
        <mark class = 'highlight'> Streamlit </mark> + \
            <mark class = 'highlight'> pandas_profiling </mark> + \
            <mark class = 'highlight'> streamlit_pandas_profiling </mark> \
    </p>",
    unsafe_allow_html=True)


# SIDEBAR
# ---Header
st.sidebar.header("Upload CSV or EXCEL Data File")
# ---Upload Files 
uploaded_file = st.sidebar.file_uploader('📁 UPLOAD YOUR DATA FILE HERE :')
# ---Select Chart Type 
st.sidebar.write('---')
custom_or_pdrep = st.sidebar.selectbox(
    label= '📊 DATA VIZUALISATION TYPE :',
    options=['Custom Chart','Pandas Profile Visualization']
)

# PANDAS PROFILING REPORT
#---if file is uploaded
if uploaded_file is not None:
    @st.cache
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    def load_excel():
        excel = pd.read_excel(uploaded_file)
        return excel
    
    try:
        df = load_csv()
    except Exception as e:
        print(e)
        df = load_excel()

    st.header('**DataFrame Insights**')
    try:
        st.write(df)
        numeric_columns = list(df.select_dtypes(['float','int']).columns)
    except Exception as e:
        print(e)
    
    #---if file is uploaded and **custom charts** is selected
    if custom_or_pdrep == 'Custom Chart':
        st.write('---')
        st.header('Your Custom Chart')
        chart_select = st.sidebar.selectbox(
        label= 'Make your own CUSTOM CHART',
        options=['Scatter','Line','Histogram','Heatmap']
        )

        # PC : Tried to make this a function -was facing problem with px.plot_type (e:px has no attribute named plot_type)
        if chart_select == 'Scatter':
            st.sidebar.subheader('Scatter Plot Settings')
            try:
                x_values = st.sidebar.selectbox(label='X AXIS', options=numeric_columns)
                y_values = st.sidebar.selectbox(label='Y AXIS', options=numeric_columns)
                plot = px.scatter(data_frame=df, x=x_values, y=y_values)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)
        elif chart_select == 'Line':
            st.sidebar.subheader('Line Plot Settings')
            try:
                x_values = st.sidebar.selectbox(label='X AXIS', options=numeric_columns)
                y_values = st.sidebar.selectbox(label='Y AXIS', options=numeric_columns)
                plot = px.line(data_frame=df, x=x_values, y=y_values)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)
        elif chart_select == 'Histogram':
            st.sidebar.subheader('Histogram Settings')
            try:
                x_values = st.sidebar.selectbox(label='X AXIS', options=numeric_columns)
                y_values = st.sidebar.selectbox(label='Y AXIS', options=numeric_columns)
                plot = px.histogram(data_frame=df, x=x_values, y=y_values)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)
        elif chart_select == 'Heatmap':
            st.sidebar.subheader('Box Plot Settings')
            try:
                x_values = st.sidebar.selectbox(label='X AXIS', options=numeric_columns)
                y_values = st.sidebar.selectbox(label='Y AXIS', options=numeric_columns)
                plot = px.density_heatmap(data_frame=df, x=x_values, y=y_values)
                st.plotly_chart(plot)
            except Exception as e:
                print(e)

    #---if file is uploaded and **pandas profile** is selected
    elif custom_or_pdrep == 'Pandas Profile Visualization':
        pr = ProfileReport(df, explorative=True)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)

#---if file is not uploaded
else:
    st.write('---')
    st.info('Awaiting for CSV file to be uploaded.')
    
    #---example dataset button 
    if st.button('Press to use Example Dataset'):  
        @st.cache
        def load_data():
            a = pd.DataFrame(
                np.random.rand(100, 5),
                columns=['a', 'b', 'c', 'd', 'e']
            )
            return a
        df = load_data()
        pr = ProfileReport(df, explorative=True)
        st.header('**Input DataFrame**')
        st.write(df)
        st.write('---')
        st.header('**Pandas Profiling Report**')
        st_profile_report(pr)

    # Recommendations
    st.write('---')
    st.markdown("<p class = 'paragraph'> <b> 🔍 Some Important Things to Note : </b></p>",unsafe_allow_html=True)
    st.write('> Selecting A Data Visualisation option before uploading data file is recommended')
    st.write("> Example CSV is made using Numpy's np.random.rand attribute, which generates a random number data for calulation.")
    st.write('> Custom Charts Option is not available for example dataset.')

#
#THEMES = [
#primaryColor="#ff2e63"
#backgroundColor="#eaeaea"
#secondaryBackgroundColor="#08d9d6"
#textColor="#252a34"]
#'''
#