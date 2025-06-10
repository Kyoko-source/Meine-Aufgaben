import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# -----------------------
# Konstanten und Daten
# -----------------------

STATUS_DATEI = "status.json"

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

feiertage_2025 = {
    "01.01.2025": "Neujahrstag",
    "06.01.2025": "Heilige Drei Könige",
    "08.03.2025": "Internationaler Frauentag",
    "18.04.2025": "Karfreitag",
    "21.04.2025": "Ostermontag",
    "01.05.2025": "Tag der Arbeit",
    "29.05.2025": "Christi Himmelfahrt",
    "09.06.2025": "Pfingstmontag",
    "19.06.2025": "Fronleichnam",
    "03.10.2025": "Tag der Deutschen Einheit",
    "31.10.2025": "Reformationstag",
    "01.11.2025": "Allerheiligen",
    "19.11.2025": "Buß- und Bettag",
    "25.12.2025": "1. Weihnachtstag",
    "26.12.2025": "2. Weihnachtstag"
}

quiz_fragen = [
    ("Was ist die Hauptstadt von Deutschland?", ["Berlin", "München", "Frankfurt", "Hamburg"], 0),
    ("Welcher Planet ist der dritte von der Sonne?", ["Mars", "Venus", "Erde", "Jupiter"], 2),
    ("Wie viele Bundesländer hat Deutschland?", ["14", "16", "18", "20"], 1),
    ("Welcher Kontinent ist am größten?", ["Afrika", "Asien", "Europa", "Antarktika"], 1),
    ("Wer schrieb 'Faust'?", ["Goethe", "Schiller", "Heine", "Kafka"], 0),
    ("In welchem Jahr begann der Zweite Weltkrieg?", ["1939", "1945", "1914", "1923"], 0),
    ("Was bedeutet 'RTW'?", ["Rettungswagen", "Rettungstransportwagen", "Rettungstaxi", "Rettungsdienst"], 0),
    ("Welches Gas atmen wir hauptsächlich ein?", ["Sauerstoff", "Kohlenstoffdioxid", "Stickstoff", "Helium"], 2),
    ("Wie viele Knochen hat ein erwachsener Mensch?", ["206", "201", "210", "215"], 0),
    ("Welcher Fluss fließt durch Berlin?", ["Elbe", "Donau", "Spree", "Rhein"], 2),
    ("Was ist die chemische Formel von Wasser?", ["CO2", "H2O", "O2", "NaCl"], 1),
    ("Wie viele Stunden hat ein Tag?", ["12", "24", "48", "36"], 1),
    ("Wer malte die Mona Lisa?", ["Michelangelo", "Leonardo da Vinci", "Raphael", "Donatello"], 1),
    ("Was ist das größte Land der Welt?", ["Kanada", "China", "USA", "Russland"], 3),
    ("Welches Element hat das Symbol 'Fe'?", ["Fluor", "Eisen", "Kupfer", "Gold"], 1),
    ("Wie viele Planeten hat unser Sonnensystem?", ["7", "8", "9", "10"], 1),
    ("Was ist der längste Fluss der Welt?", ["Amazonas", "Nil", "Yangtze", "Mississippi"], 1),
    ("Welche Sprache hat die meisten Muttersprachler?", ["Englisch", "Spanisch", "Mandarin", "Hindi"], 2),
    ("Wie viele Zähne hat ein Erwachsener normalerweise?", ["28", "30", "32", "34"], 2),
    ("Wer entdeckte die Schwerkraft?", ["Newton", "Einstein", "Galilei", "Tesla"], 0)
]

# -----------------------
# Hilfsfunktionen
# -----------------------

def lade_status():
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status_dict):
    with open(STATUS_DATEI, "w") as f:
        json.dump(status_dict, f)

def aufgabe_key(fahrzeug, wochentag, aufgabe):
    jahr, kw, _ = datetime.datetime.now().isocalendar()
    raw_key = f"{fahrzeug}_{wochentag}_{jahr}_{kw}_{aufgabe}"
    return hashlib.md5(raw_key.encode()).hexdigest()

def aufgabe_checkbox(aufgabe, fahrzeug, wochentag, status_dict):
    key = aufgabe_key(fahrzeug, wochentag, aufgabe)
    checked = status_dict.get(key, False)
    neu = st.checkbox(aufgabe, value=checked, key=key)
    if neu != checked:
        status_dict[key] = neu
        speichere_status(status_dict)
        if neu:
            st.balloons()

# -----------------------
# Session State Setup
# -----------------------

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

# -----------------------
# Quiz Funktionen
# -----------------------

def quiz_starten():
    st.session_state["quiz_active"] = True
    st.session_state["quiz_index"] = 0
    st.session_state["score"] = 0
    st.session_state["player_name"] = ""

def quiz_beenden():
    st.session_state["quiz_active"] = False
    name = st.session_state["player_name"] or "Unbekannt"
    punkte = st.session_state["score"]
    if name in st.session_state["scoreboard"]:
        if punkte > st.session_state["scoreboard"][name]:
            st.session_state["scoreboard"][name] = punkte
    else:
        st.session_state["scoreboard"][name] = punkte

def zeige_scoreboard():
    st.write("### 🏆 Scoreboard")
    if not st.session_state["scoreboard"]:
        st.write("Noch keine Einträge.")
        return
    sortiert = sorted(st.session_state["scoreboard"].items(), key=lambda x: x[1], reverse=True)
    for name, score in sortiert:
        st.write(f"**{name}**: {score} Punkte")

# -----------------------
# Haupt UI
# -----------------------

st.title("🚑 RTW & KTW Aufgaben + Quiz 🚑")

if not st.session_state["quiz_active"]:
    if st.sidebar.button("▶️ Quiz starten"):
        quiz_starten()

if st.session_state["quiz_active"]:
    st.header("🎯 Quiz")
    if not st.session_state["player_name"]:
        name_input = st.text_input("Bitte gib deinen Namen ein:", key="eingabe_name")
        if name_input:
            st.session_state["player_name"] = name_input
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
                st.success(f"Herzlichen Glückwunsch {st.session_state['player_name']}! Du hast alle Fragen richtig beantwortet.")
                quiz_beenden()
        else:
            st.error(f"Falsch! Quiz beendet. Deine Punktzahl: {st.session_state['score']}")
            quiz_beenden()

    st.write(f"📊 Aktueller Punktestand: {st.session_state['score']}")

else:
    # Aufgabenplaner

    heute = datetime.datetime.now(pytz.timezone('Europe/Berlin'))
    heute_en = heute.strftime("%A")
    heute_de = tage_uebersetzung.get(heute_en, heute_en)
    datum = heute.strftime("%d.%m.%Y")
    feiertag = feiertage_2025.get(datum)

    st.subheader(f"Heute ist {heute_de} ({datum})")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚑 RTW Aufgaben")
        for aufgabe in aufgaben_rtw.get(heute_de, []):
            aufgabe_checkbox(aufgabe, "RTW", heute_de, st.session_state["status_dict"])

    with col2:
        st.markdown("### 🚐 KTW Aufgaben")
        for aufgabe in aufgaben_ktw.get(heute_de, []):
            aufgabe_checkbox(aufgabe, "KTW", heute_de, st.session_state["status_dict"])

    if feiertag:
        st.info(f"Heute ist Feiertag: {feiertag}")

    st.markdown("---")
    zeige_scoreboard()
