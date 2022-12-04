# MLB Pitch Identification with ML

This project demonstrates one of the many uses of machine learning in baseball by creating a machine learning model capable of identifying which pitch is being thrown when given the pitcher, velocity, and movement of the pitch.

Data used is taken from [Baseball Savant](https://baseballsavant.mlb.com/).


## ML Model Notebook

The notebook file walks through the creation of both a general and pitcher-specific machine learning model, as well as an analysis of the accuracy of both models. 


## Pitch Identifier Web App

The machine learning model can be interacted with via a Streamlit web app dashboard. A user can select either the general or pitcher-specific model and by entering the pitcher (*pitcher-specific model only*), pitch velocity and movement, the model will identify and display what pitch was thrown. 

Check out the web app [here](https://jakeenea51-mlb-pitch-identifica-pitch-identification-app-ykdusi.streamlit.app/).
