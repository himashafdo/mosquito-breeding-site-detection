import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Mosquito Site Monitor", layout="wide")
st.title("🦟 Mosquito Breeding Site Detection Dashboard")

# 1. Initialize Firebase from Streamlit Cloud Secrets
if not firebase_admin._apps:
    if "textkey" in st.secrets:
        key_dict = dict(st.secrets["textkey"])
        cred = credentials.Certificate(key_dict)
    elif os.path.exists("firebase_key.json"):
        cred = credentials.Certificate("firebase_key.json")
    else:
        st.error("Missing Firebase Credentials in Secrets!")
        st.stop()
        
    firebase_admin.initialize_app(cred)

db = firestore.client()

st.subheader("Live Detection Feed")

# 2. Fetch and display alerts
try:
    docs = db.collection("mosquito_alerts").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(12).stream()
    alerts = [doc.to_dict() for doc in docs]

    if not alerts:
        st.info("No detection alerts uploaded yet. Run your model on a test image!")
    else:
        cols = st.columns(3)
        for idx, alert in enumerate(alerts):
            with cols[idx % 3]:
                st.image(alert["image_url"], use_container_width=True)
                st.warning(f"Detected: {alert['class_detected']}")
                st.caption(f"Time: {alert['timestamp']}")
except Exception as e:
    st.error(f"Error fetching alerts: {e}")