import streamlit as st
import datetime
import pytz
import json
import os

# ---------- Daten & Styling ----------

aufgaben_ktw = {
    "Montag": ["Fächerdesi 1-6", "Umkleide Bad SW-Bereich reinigen"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-8", "BZ Messung"],
    "Mittwoch": ["Innenraumdesi KTW"],
    "Donnerstag": ["Auto waschen (KTW)", "Garage reinigen"],
    "Freitag": ["Betriebsmittelkontrolle", "O2 Schlauch + Fingertipp wechseln"],
    "Samstag": ["Wäsche gemacht?"],
    "Sonntag": ["Küche reinigen alle Fronten"]
}

aufgaben_rtw = {
    "Montag": ["Fächerdesi 1-6", "Umkleide Bad SW-Bereich reinigen"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-11"],
    "Mittwoch": ["Innenraumdesi RTW"],
    "Donnerstag": ["Auto waschen (RTW)", "Garage reinigen", "Betriebsmittelkontrolle"],
    "Freitag": ["Fach 12-18 desinfizieren", "O2 Schlauch + Fingertipp wechseln", "Betriebsmittel Kontrolle"],
    "Samstag": ["Fach 20-22 desinfizieren"],
    "Sonntag": ["Küche reinigen alle Fronten"]
}

tage_uebersetzung = {
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Sunday": "Sonntag"
}

quiz_fragen = [
    ("Was ist die Hauptstadt von Deutschland?", ["Berlin", "München", "Frankfurt", "Hamburg"], 0),
    ("Welcher Planet ist der dritte von der Sonne?", ["Mars", "Venus", "Erde", "Jupiter"], 2),
    # ... alle 20 Fragen ...
]

# ---------- Status laden/speichern ----------

STATUS_DATEI = "status.json"

def lade_status():
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status):
    with open(STATUS_DATEI, "w") as f:
        json.dump(status, f)

# ---------- Styling als CSS ----------

def lade_css():
    st.markdown("""
    <style>
    .aufgabe-rtw {
        background-color: #ffdddd;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
    .aufgabe-ktw {
        background-color: #ddffdd;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 5px;
    }
    .quiz-box {
        background-color: #ddeeff;
        padding: 15px;
        border-radius: 10px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- Hauptfunktion ----------

def main():
    st.title("🚑 RTW & KTW Aufgaben + Quiz 🚑")

    lade_css()

    if "status_dict" not in st.session_state:
        st.session_state["status_dict"] = lade_status()

    if "quiz_active" not in st.session_state:
        st.session_state["quiz_active"] = False
    if "quiz_index" not in st.session_state:
        st.session_state["quiz_index"] = 0
    if "score" not in st.session_state:
        st.session_state["score"] = 0
    if "player_name" not in st.session_state:
        st.session_state["player_name"] = ""
    if "scoreboard" not in st.session_state:
        st.session_state["scoreboard"] = {}

    if not st.session_state["quiz_active"]:
        if st.sidebar.button("▶️ Quiz starten"):
            st.session_state["quiz_active"] = True
            st.session_state["quiz_index"] = 0
            st.session_state["score"] = 0
            st.session_state["player_name"] = ""

    if st.session_state["quiz_active"]:
        with st.container():
            st.markdown('<div class="quiz-box">', unsafe_allow_html=True)
            st.header("🎯 Quiz")
            if not st.session_state["player_name"]:
                name = st.text_input("Bitte gib deinen Namen ein:", key="eingabe_name")
                if name:
                    st.session_state["player_name"] = name
                else:
                    st.info("Bitte Namen eingeben, um das Quiz zu starten.")
                    st.stop()

            idx = st.session_state["quiz_index"]
            frage, antworten, korrekt = quiz_fragen[idx]

            st.write(f"**Frage {idx+1} von {len(quiz_fragen)}:** {frage}")
            antwort = st.radio("Antwort auswählen:", antworten, key=f"frage_{idx}")

            if st.button("Antwort prüfen"):
                if antwort == antworten[korrekt]:
                    st.success("Richtig! 🎉")
                    st.session_state["score"] += 1
                    st.session_state["quiz_index"] += 1
                    if st.session_state["quiz_index"] >= len(quiz_fragen):
                        st.balloons()
                        st.success(f"Herzlichen Glückwunsch {st.session_state['player_name']}! Alle Fragen richtig.")
                        beende_quiz()
                else:
                    st.error(f"Falsch! Quiz beendet. Deine Punktzahl: {st.session_state['score']}")
                    beende_quiz()

            st.write(f"📊 Aktueller Punktestand: {st.session_state['score']}")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        heute = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
        heute_en = heute.strftime("%A")
        heute_de = tage_uebersetzung.get(heute_en, heute_en)
        datum = heute.strftime("%d.%m.%Y")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="aufgabe-rtw">', unsafe_allow_html=True)
            st.header("🚑 RTW Aufgaben")
            for aufgabe in aufgaben_rtw.get(heute_de, []):
                key = f"rtw_{heute_de}_{aufgabe}"
                checked = st.session_state["status_dict"].get(key, False)
                neu = st.checkbox(aufgabe, value=checked, key=key)
                if neu != checked:
                    st.session_state["status_dict"][key] = neu
                    speichere_status(st.session_state["status_dict"])
                    if neu:
                        st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="aufgabe-ktw">', unsafe_allow_html=True)
            st.header("🚐 KTW Aufgaben")
            for aufgabe in aufgaben_ktw.get(heute_de, []):
                key = f"ktw_{heute_de}_{aufgabe}"
                checked = st.session_state["status_dict"].get(key, False)
                neu = st.checkbox(aufgabe, value=checked, key=key)
                if neu != checked:
                    st.session_state["status_dict"][key] = neu
                    speichere_status(st.session_state["status_dict"])
                    if neu:
                        st.balloons()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        zeige_scoreboard()

def beende_quiz():
    name = st.session_state["player_name"] or "Unbekannt"
    punkte = st.session_state["score"]
    if name in st.session_state["scoreboard"]:
        if punkte > st.session_state["scoreboard"][name]:
            st.session_state["scoreboard"][name] = punkte
    else:
        st.session_state["scoreboard"][name] = punkte

    st.session_state["quiz_active"] = False

def zeige_scoreboard():
    st.subheader("🏆 Scoreboard")
    if not st.session_state["scoreboard"]:
        st.write("Noch keine Einträge.")
        return
    sortiert = sorted(st.session_state["scoreboard"].items(), key=lambda x: x[1], reverse=True)
    for name, score in sortiert:
        st.write(f"**{name}**: {score} Punkte")

if __name__ == "__main__":
    main()
