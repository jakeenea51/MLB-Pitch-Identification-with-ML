
############################################################################
# IMPORTS AND SETUP
############################################################################

import streamlit as st
import pandas as pd
from sklearn.svm import SVC
from PIL import Image


############################################################################
# MACHINE LEARNING
############################################################################

# create the ML model
model = SVC()

# fix pitch names to match training set
def reformatTrainSet(df):
    # combine first and last names
    df['last_name'] = df['first_name'] + ' ' + df['last_name']
    df = df.rename(columns = {'last_name':'name'})
    df = df.rename(columns = {'avg_speed':'Pitch Vel (MPH)'})
    df = df.rename(columns = {'pitcher_break_z':'VBreak (In.)'})
    df = df.rename(columns = {'pitcher_break_x':'HBreak (In.)'})
    df = df.drop(columns = 'first_name')
    for i in df:
        df = df.replace(to_replace = '4-Seam Fastball', value = '4-Seamer')
        df = df.replace(to_replace = 'Knuckle Curve', value = 'Curveball')
    return df


# general ML model
def generalModel():

    # take in train data
    df = pd.read_csv('web app/pitchTrainSet2021.csv')
    df = reformatTrainSet(df)
    
    # prepare train data
    df_train = df.drop(columns = ['name', 'pitcher_id'])

    X_train = df_train.drop(columns = 'pitch_type_name')
    y_train = df_train['pitch_type_name']

    # train the ML model
    model.fit(X_train, y_train)

    # input widgets
    a, b, c = st.columns([1, 1, 1])
    velo = round(a.number_input("Pitch velocity"), 1)
    vbreak = round(b.number_input("Vertical break (inches)"), 0)
    hbreak = round(c.number_input("Horizontal break (inches)"), 0)
    predictButton = st.button("Identify")

    if predictButton:
        prediction = model.predict([[velo, vbreak, hbreak]])
        st.write("_________________________________________________________")
        st.write("Pitch prediction:")
        st.header(prediction[0])


# pitcher-specific ML model
def pitcherSpecificModel():

    # take in train data
    if season == 2021:
        df = pd.read_csv('web app/pitchTrainSet2021.csv')
        df = reformatTrainSet(df)
    elif season == 2022:
        df = pd.read_csv('web app/pitchTrainSet2022.csv')
        df = reformatTrainSet(df)

    # name input box
    nameInput = st.text_input("Enter a pitcher's name")

    # prepare train data
    df_train = df.drop(columns = ['pitcher_id'])

    found = True
    if nameInput in df_train['name'].tolist():
        df_train = df_train.loc[df_train['name'] == nameInput]
    elif ' ' in nameInput:
        nameInput = nameInput.replace(' ', '')
        if nameInput in df_train['name'].tolist():
            df_train = df_train.loc[df_train['name'] == nameInput]
        else: found = False
    else:
        found = False

    if not found:
        st.write("Player not available.")
        return
    else:
        df_train = df_train.drop(columns = 'name')

        X_train = df_train.drop(columns = 'pitch_type_name')
        y_train = df_train['pitch_type_name']

        # train the ML model
        try:
            model.fit(X_train, y_train)
        except ValueError as e:
            found = False
            st.write("Player not available.") 

        if found:
            # input widgets
            a, b, c = st.columns([1, 1, 1])
            velo = round(a.number_input("Pitch velocity"), 1)
            vbreak = round(b.number_input("Vertical break (inches)"), 0)
            hbreak = round(c.number_input("Horizontal break (inches)"), 0)
            predictButton = st.button("Identify")

            if predictButton:
                prediction = model.predict([[velo, vbreak, hbreak]])
                st.write("_________________________________________________________")
                st.write("Pitch prediction:")
                st.header(prediction[0])


############################################################################
# STREAMLIT DASHBOARD
############################################################################

# setup page configuration settings
icon = "web app/baseball_icon.png"
st.set_page_config(page_title="MLB Pitch Identifier", page_icon=icon, layout="centered")

# header
mlbLogo = Image.open('web app/mlb.png')
a, b = st.columns([1, 8])
a.image(mlbLogo)
b.title("MLB Pitch Identifier")
st.write("A machine learning model that identifies MLB pitches based on pitch velocity and movement.")
st.write("Created by: **Jake Enea**")
st.write("_________________________________________________________")

modelType = st.selectbox("Select which model to use", ["General", "Pitcher-Specific"])
if modelType == "General":
    st.subheader("Accuracy: 88%")
elif modelType == "Pitcher-Specific":
    st.subheader("Accuracy: 97%")
    season = st.selectbox("Select season", [2021, 2022])
    st.write("Notes:")
    st.write(" - Only pitchers from season selected with enough sample size")
    st.write(" - Case sensitive")
    st.write(" - Omit any special characters or spaces in first or last name of pitcher (ex. Lance McCullersJr.)")
st.write("_________________________________________________________")

if modelType == "General":
    generalModel()
elif modelType == "Pitcher-Specific":
    pitcherSpecificModel()

