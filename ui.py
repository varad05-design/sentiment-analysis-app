import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/predict"
st.title("Sentiment analysis of Text Reviews")
user_input=st.text_area(
    label="Enter the Review Text below", 
    placeholder="This movie was fantastic!!!",
    height=150
)

analyze_button=st.button("Analyze Sentiment")

if analyze_button:
    if user_input.strip():
        payload={
            'review':user_input
        }
        try:
            with st.spinner("Analyzing...."):
                response=requests.post(API_URL,json=payload)
            if response.status_code==200:
                response_data=response.json()
                sentiment=response_data.get('sentiment')
                if sentiment=='Positive':
                    st.success(f"Prediction: Positive 👍")
                elif sentiment=='Negative':
                    st.error(f"Prediction: Negative 👎")
                else:
                    st.warning("Could not determine the sentiment. Please try another review.")
            else:
                try:
                    error_details=response.json()
                    st.error(f"API error {error_details.get('error','Unknown error occured')}")
                except requests.exceptions.JSONDecodeError:
                    st.error(f"API Error: Status code {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"Connection error. Could not able to connect to API at {API_URL}. Please check if Flask is running")
        except Exception as e:
            print("Unknown error occured")
    else:
        st.warning("Enter a review to analyze")
