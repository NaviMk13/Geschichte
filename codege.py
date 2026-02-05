# main.py
import streamlit as st
import json
import random

# ========================
# Utils
# ========================
def load_epoche(epoche_name):
    with open(f"data/{epoche_name}.json", encoding="utf-8") as f:
        return json.load(f)

def ask_question(question_data):
    st.write(f"**{question_data['frage']}**")
    options = question_data["antworten"]
    user_answer = st.radio("Wähle die richtige Antwort:", options)
    if st.button("Antwort prüfen"):
        if user_answer == question_data["richtige_antwort"]:
            st.success("✅ Richtig!")
            return True
        else:
            st.error(f"❌ Falsch! Richtige Antwort: {question_data['richtige_antwort']}")
            return False

# ========================
# Session State Setup
# ========================
if "epoche_index" not in st.session_state:
    st.session_state.epoche_index = 0
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# ========================
# Epochen
# ========================
epochen = ["steinzeit", "antike", "mittelalter"]
current_epoche = epochen[st.session_state.epoche_index]
content = load_epoche(current_epoche)

st.title("🌍 Geschichtsreise – Zeitreise durch die Weltgeschichte")

st.header(f"Epoche: {content['epoche_name']}")
st.image(f"assets/images/{current_epoche}.jpg", use_column_width=True)

# Story
st.markdown(content["story"])

# Quiz
if st.session_state.quiz_index < len(content["quiz"]):
    question_data = content["quiz"][st.session_state.quiz_index]
    if ask_question(question_data):
        st.session_state.score += 1
        st.session_state.quiz_index += 1
else:
    st.success(f"Du hast die Epoche '{content['epoche_name']}' abgeschlossen! ✅")
    if st.session_state.epoche_index + 1 < len(epochen):
        if st.button("Zur nächsten Epoche reisen"):
            st.session_state.epoche_index += 1
            st.session_state.quiz_index = 0
    else:
        st.balloons()
        st.success(f"🎉 Herzlichen Glückwunsch! Du hast alle Epochen abgeschlossen. Punkte: {st.session_state.score}")

st.sidebar.title("Spielstatus")
st.sidebar.write(f"Aktueller Punktestand: {st.session_state.score}")
st.sidebar.write(f"Epoche: {current_epoche.capitalize()}")
