import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# ===========================
# ✅ RTW/KTW Aufgaben-App + Quiz
# ===========================

st.set_page_config(page_title="RTW Aufgabenplan + Quiz", page_icon="🚑", layout="wide")

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

def get_current_time():
    timezone = pytz.timezone('Europe/Berlin')
    return datetime.datetime.now(timezone).strftime('%H:%M:%S')

def lade_status():
    if os.path.exists(STATUS_DATEI):
        with open(STATUS_DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_status(status_dict):
    with open(STATUS_DATEI, "w") as f:
        json.dump(status_dict, f)

def aufgabe_mit_feedback(aufgabe, wochentag, status_dict, fahrzeug, readonly=False):
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    raw_key = f"{fahrzeug}_{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"
    key_hash = hashlib.md5(raw_key.encode()).hexdigest()
    checked = status_dict.get(key_hash, False)

    if readonly:
        if checked:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)
    else:
        neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()

        if neu_gesetzt:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)


# ----------------------
# Quiz Fragen: (Frage, [Antworten], Index korrekte Antwort)
# ----------------------
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

# ----------------------
# Session State Initialisierung
# ----------------------
if "quiz_active" not in st.session_state:
    st.session_state["quiz_active"] = False
if "quiz_index" not in st.session_state:
    st.session_state["quiz_index"] = 0
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "player_name" not in st.session_state:
    st.session_state["player_name"] = ""
if "status_dict" not in st.session_state:
    st.session_state["status_dict"] = lade_status()

# ----------------------
# Quiz Start Funktion
# ----------------------
def quiz_starten():
    st.session_state["quiz_active"] = True
    st.session_state["quiz_index"] = 0
    st.session_state["score"] = 0
    st.session_state["player_name"] = ""

# ----------------------
# Quiz Stop Funktion (z.B. bei Fehler oder Ende)
# ----------------------
def quiz_stoppen():
    st.session_state["quiz_active"] = False
    # Speichere Score im Scoreboard (optional, hier lokal)
    scoreboard = st.session_state.get("scoreboard", {})
    name = st.session_state["player_name"] or "Unbekannt"
    scoreboard[name] = max(scoreboard.get(name, 0), st.session_state["score"])
    st.session_state["scoreboard"] = scoreboard

# ----------------------
# Anzeige der Quiz-Scoreboard
# ----------------------
def zeige_scoreboard():
    st.write("### 🏆 Scoreboard")
    scoreboard = st.session_state.get("scoreboard", {})
    if not scoreboard:
        st.write("Noch keine Einträge.")
        return
    sorted_scores = sorted(scoreboard.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_scores:
        st.write(f"**{name}**: {score} Punkte")

# ----------------------
# Haupt-App Logik
# ----------------------

st.title("✔ Rettungswache Südlohn Tagesaufgaben + Quiz ✔")

# Quiz Start/Stop Steuerung
if not st.session_state["quiz_active"]:
    st.sidebar.button("▶️ Quiz starten", on_click=quiz_starten)
else:
    st.sidebar.button("✖ Quiz abbrechen", on_click=quiz_stoppen)

# ----------------------
# Wenn Quiz aktiv ist, zeige Quiz
# ----------------------
if st.session_state["quiz_active"]:
    st.header("🎯 Quiz")

    if not st.session_state["player_name"]:
        name = st.text_input("Bitte gib deinen Namen ein:", key="player_name")
        if not name:
            st.info("Bitte gib deinen Namen ein, um zu starten.")
            st.stop()
        else:
            st.session_state["player_name"] = name

    frage_idx = st.session_state["quiz_index"]
    frage, antworten, korrekt_idx = quiz_fragen[frage_idx]

    st.write(f"**Frage {frage_idx + 1} von {len(quiz_fragen)}:** {frage}")
    auswahl = st.radio("Wähle die richtige Antwort:", antworten, key=f"frage_{frage_idx}")

    if st.button("Antwort prüfen"):
        if auswahl == antworten[korrekt_idx]:
            st.success("Richtig! 🎉")
            st.session_state["score"] += 1
            st.session_state["quiz_index"] += 1
            if st.session_state["quiz_index"] >= len(quiz_fragen):
                st.balloons()
                st.success(f"Gratulation {st.session_state['player_name']}! Du hast alle Fragen richtig beantwortet.")
                quiz_stoppen()
        else:
            st.error(f"Falsch! Das Quiz ist beendet. Deine Punktzahl: {st.session_state['score']}")
            quiz_stoppen()

    st.write(f"📝 Aktueller Punktestand: {st.session_state['score']}")

# ----------------------
# Wenn Quiz nicht aktiv, zeige Aufgabenplaner
# ----------------------
if not st.session_state["quiz_active"]:
    # Aktuelles Datum und Wochentag
    heute_en = datetime.datetime.now().strftime('%A')
    heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
    heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
    feiertag_heute = feiertage_2025.get(heute_str)

    status_dict = st.session_state["status_dict"]

    st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

    col_ktw, col_rtw = st.columns(2)

    with col_ktw:
        st.markdown("""
        <div style="
            background-color
