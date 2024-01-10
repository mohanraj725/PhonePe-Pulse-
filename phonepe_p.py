# Importing Libraries
import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo
#<------------------------------------------------------------------------------------------------------------------------------------.>
# requried image imported 

icon_logo = Image.open("D:\VS_Code\Project\Phonepe\project\PhonePe.png")
icon = Image.open("D:\VS_Code\Project\Phonepe\project\phonepe-logo-icon.webp")
map_img = Image.open("D:\VS_Code\Project\Phonepe\project\india_map.jpg")

#<-------------------------------------------------------------------------------------------------------------------------------------------->


# Setting up page configuration

st.set_page_config(page_title= "Phonepe Pulse Data Visualization by MJ 🃏",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by Mohanraj
                                        Data has been cloned from Phonepe Pulse Github """})
with st.sidebar:
    icon_logo_resized = icon_logo.resize((750,400))
    st.image(icon_logo_resized)
    st.header(":violet[**Hello! Welcome to the dashboard**]")

#<-------------------------------------------------------------------------------------------------------------------------------------------->


# Reference Syntax - Repo.clone_from("Clone Url", "Your working directory")
# Repo.clone_from("https://github.com/PhonePe/pulse.git", "Project_3_PhonepePulse/Phonepe_data/data")

#<-------------------------------------------------------------------------------------------------------------------------------------------->

# connection to pyscopg 

mydb = psycopg2.connect( host = "localhost", 
                         user = "postgres",
                         password = "Mj@2590",
                         database = "phonepe_pluse",
                         port ="5432"
                         )
cursor = mydb.cursor()


#<-------------------------------------------------------------------------------------------------------------------------------------------->

# Creating option menu in the side bar
with st.sidebar:
    
    selected = option_menu("Menu", ["Home","Report","Explore Data","Data API"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=-1,
                styles={"nav-link": {"font-size": "16px", "text-align": "left", "margin": "1.8px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if selected == "Home":
    #st.image("img.png")
    st.header(" :violet[**Data Visualization and Exploration**]")
    st.write("#### :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        #st.markdown("### :violet[Domain :] Fintech")
        st.markdown("""#### :violet[Technologies used :] 
Github Cloning, Python, Pandas, psycopg2, Streamlit, Plotly 
        
                                                """)
        st.write("""##### :violet[**Overview :**]
In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions,
number of users, top 10 state, district, pincode and which brand has most number of users and so on.
Bar charts, Pie charts and Geo map visualization are used to get some insights.
                  """)
    
    with col2:
        
        st.image(map_img,clamp=False, use_column_width= "always")

#<-------------------------------------------------------------------------------------------------------------------------------------------->

# MENU 2 - Report
if selected == "Report":
    st.markdown("## :violet[Report]")
    col1,col2 = st.columns(2)
    with col1:
            Type = st.selectbox("**Type**", ("Transactions", "Users"),
                                index=None,
                                placeholder="Select the Type...")
    with col2:
        st.write("")
    st.write(" \n ")
    colum1,colum2= st.columns([1,1.5],gap="medium")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """#,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2= st.columns([2,2],gap="large")
        
        if Year == 2023 and Quarter == [4]:
            st.markdown(" ###### Data for 4th Quater of year 2023 is not updated")     
        else:      
            with col1:
                st.markdown("### :violet[State]")            
                cursor.execute(f"select State, sum(Trans_count) as Total_Transactions_Count, sum(Trans_amount) as Total from aggre_trans1 where Year = {Year} and Quater = {Quarter} group by State order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            with col2:
                st.write("")
            
            col3,col4 = st.columns([2,2],gap="large")
        
            with col3:
                st.markdown("### :violet[District]")
                cursor.execute(f"select District , sum(Transcation_count) as Total_Count, sum(Transcation_amount) as Total from map_trans where Year = {Year} and Quater = {Quarter} group by District order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label') 
                st.plotly_chart(fig,use_container_width=True)
                
            with col4:
                st.markdown("### :violet[Pincode]")
                cursor.execute(f"select Pincode, sum(Count) as Total_Transactions_Count, sum(Amount) as Total from top_trans_pincode  where Year = {Year} and Quater = {Quarter} group by Pincode order by Total desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
#<-------------------------------------------------------------------------------------------------------------------------------------------->
# Top Charts - USERS          
    if Type == "Users":
        col1,col2 = st.columns([2,2],gap="medium")
        
        with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 4")
            else:
                cursor.execute(f"select Brands, sum(Transcation_counts) as Total_Count, avg(Percentage)*100 as Avg_Percentage from Aggre_user where Year = {Year} and Quater = {Quarter} group by Brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Brand",
                             y="Total_Users",
                             orientation='v',
                             
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            cursor.execute(f"select District, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens from map_user1 where Year = {Year} and Quater = {Quarter} group by District order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="District",
                         y="Total_Users",
                         orientation='v',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
        
        col3,col4 = st.columns([2,2],gap="medium")    
              
        with col3:
            st.markdown("### :violet[Pincode]")
            cursor.execute(f"select Pincode, sum(Reg_User) as Total_Users from top_user_pincode where Year = {Year} and Quater = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            cursor.execute(f"select State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens from map_user1 where Year = {Year} and Quater = {Quarter} group by State order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->
# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    c1,c2 = st.columns(2)
    with c1:
        Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    with c2:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    col1,col2 = st.columns(2)
    
#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------->
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select State, sum(Transcation_count) as Total_Transactions, sum(Transcation_amount) as Total_amount from map_trans where Year = {Year} and Quater = {Quarter} group by State order by State")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(f"select State, sum(Transcation_count) as Total_Transactions, sum(Transcation_amount) as Total_amount from map_trans where Year = {Year} and Quater = {Quarter} group by State order by State")
            df1 = pd.DataFrame(cursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(f"select Transcation_type, sum(Trans_count) as Total_Transactions, sum(Trans_amount) as Total_amount from aggre_trans1 where Year= {Year} and Quater = {Quarter} group by Transcation_type order by Transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        cursor.execute(f"select State, District,Year,Quater, sum(Transcation_count) as Total_Transactions, sum(Transcation_amount) as Total_amount from map_trans where Year = {Year} and Quater = {Quarter} and State = '{selected_state}' group by State, District,Year,Quater order by State,District")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        cursor.execute(f"select State, sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens from map_user1 where Year = {Year} and Quater = {Quarter} group by State order by State")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv('Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        cursor.execute(f"select State,Year,Quater,District,sum(Registered_Users) as Total_Users, sum(App_Opens) as Total_Appopens from map_user1 where Year = {Year} and Quater = {Quarter} and state = '{selected_state}' group by State, District,Year,Quater order by State,District")
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Year', 'Quater', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    