import streamlit as st
import sqlite3
import streamlit as st
# import plotly.express as px
import pandas as pd
import numpy as np
import pickle as pkl

import matplotlib.pyplot as plt
# create database connection
      
conn = sqlite3.connect('users.db')
c = conn.cursor()

# create table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username text, password text)''')
conn.commit()

# define function to check if user exists in the database
def user_exists(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# define function to add user to the database
def add_user(username, password):
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()

# define function to verify user credentials
def verify_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# define Streamlit app
def app():



    st.set_page_config(page_title="Price Predictor", page_icon=":laptop:" )

    #st.title("Login/Signup")

    # check if user is logged in
    if not st.session_state.get("logged_in"):
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.success("Logged in!")
                st.experimental_rerun()

            else:
                st.error("Invalid username or password")

        st.subheader("Signup")
        username = st.text_input("Username", key="signup_username")

        if user_exists(username):
            st.error("Username already taken")
        else:
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

            if password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password should be at least 6 characters long")
            else:
                if st.button("Signup"):
                    add_user(username, password)
                    st.success("User created!")

    # show content if user is logged in
    if st.session_state.get("logged_in"):
        #st.title("Welcome! You are logged in.")

        

        page_bg_img = f"""
                        <style>
                        [data-testid="stAppViewContainer"] > .main {{
                        background-image: url("https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=820&q=80");
                        background-size: 150%;

                        background-repeat: no-repeat;
                        background-attachment: local;
                        }}
                        </style>

                        """





        st.markdown(page_bg_img, unsafe_allow_html=True)

        
        # Define the main function
        st.write("# Welcome to Laptop Price Predictor 👨‍💻")

        
        
        # Define the main function
        def main():


            # Create the tabbed interface
            tabs = ["HOME", "Predictor"]
            tab = st.selectbox("", tabs)
            if tab == "HOME":
                infopage1 = f'''
                    <p style = "color:#8BF5FA"> Are you tired of browsing endless pages online trying to find the perfect laptop that fits your budget? Look no further! Our price predictor will help you find the best laptop for your budget. </p>
                    <p style = "color:#8BF5FA"> Simply enter your favourite brand and desired specifications, such as screen size, RAM, storage, and processor speed, and our algorithm will predict the best laptop for you. </p>
                    <p style = "color:#8BF5FA"> We constantly update our database with the latest laptops on the market, so you can be sure that our predictions are accurate and up-to-date. </p>
                    <p style = "color:#8BF5FA"> Our goal is to help you save time and money by providing you with personalized recommendations based on your preferences and budget.</p>
                    <p style = "color:#8BF5FA"> Start predicting now and find your dream laptop!</p>
                    <p style = "color:#8BF5FA"> Note :- This prediction is purely based on various Data and Algorithms</p>

     

        '''
                st.markdown(infopage1, unsafe_allow_html=True)




            elif tab == "Predictor":
                with st.form("tab2_form"):





                        # Define the main function


                        # Security
                        #passlib,hashlib,bcrypt,scrypt


                        # import the model
                        pipe = pkl.load(open('pipe.pkl','rb'))
                        df = pkl.load(open('df.pkl','rb'))




                        st.title("Laptop Predictor")

                        # brand
                        company = st.selectbox('Brand',df['Company'].unique())

                        # type of laptop
                        type = st.selectbox('Type',df['TypeName'].unique())

                        # Ram
                        ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

                        # weight
                        weight = st.number_input('Weight of the Laptop')

                        # Touchscreen
                        touchscreen = st.selectbox('Touchscreen',['No','Yes'])

                        # IPS
                        ips = st.selectbox('IPS',['No','Yes'])
                
                        # screen size
                        screen_size = st.number_input('Screen Size')

                        # resolution
                        resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

                        #cpu
                        cpu = st.selectbox('CPU',df['Cpu brand'].unique())

                        hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

                        ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

                        gpu = st.selectbox('GPU',df['Gpu brand'].unique())

                        os = st.selectbox('OS',df['os'].unique())



                        submit_button = st.form_submit_button("Submit")

                        if submit_button:

                                                        #st.form_submit_button('Submit')
                                ppi = None
                                if touchscreen == 'Yes':
                                        touchscreen = 1
                                else:
                                        touchscreen = 0

                                if ips == 'Yes':
                                        ips = 1
                                else:
                                        ips = 0

                                X_res = int(resolution.split('x')[0])
                                Y_res = int(resolution.split('x')[1])
                                ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size 
                                query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os])

                                query = query.reshape(1,12)
                            
                                st.title("The predicted price of this configuration is " + str(int(np.exp(pipe.predict(query)[0]))))




                        

            

        # Call the main function
        main()




# run the app
if __name__ == '__main__':
    app()
