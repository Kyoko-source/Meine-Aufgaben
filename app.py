import streamlit as st
import datetime
import pytz
import json
import os

# Datei zum Speichern der Checkbox-Zustände
STATUS_DATEI = "status.json"

# Aufgabenlisten KTW und RTW
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

def aufgabe_mit_feedback(aufgabe, wochentag, status_dict):
    jahr, kalenderwoche, _ = datetime.datetime.now().isocalendar()
    key = f"{wochentag}_{jahr}_{kalenderwoche}_{aufgabe}"

    checked = status_dict.get(key, False)
    neu_gesetzt = st.checkbox("", value=checked, key=key)

    if neu_gesetzt != checked:
        status_dict[key] = neu_gesetzt
        speichere_status(status_dict)
        if neu_gesetzt:
            st.balloons()

    if neu_gesetzt:
        st.markdown(f"<span style='color:green; text-decoration: line-through;'>{aufgabe} ✅</span>", unsafe_allow_html=True)
    else:
        st.markdown(aufgabe)

# Streamlit Setup
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

# Aktuelles Datum & Tag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Sonneninfos statisch
sonnenaufgang = "05:17"
sonnenuntergang = "21:43"

# Status laden
status_dict = lade_status()

st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Aufgaben für heute nebeneinander
st.markdown("## ✅ Aufgaben für heute")
col_ktw, col_rtw = st.columns(2)
with col_ktw:
    st.write("### 🚑 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict)
with col_rtw:
    st.write("### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict)

# Auswahl anderer Tag
st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", ["—"] + list(tage_uebersetzung.values()))

if tag_auswahl != "—" and tag_auswahl != heute_deutsch:
    st.markdown(f"## 🔄 Aufgaben für {tag_auswahl}")
    col_ktw_alt, col_rtw_alt = st.columns(2)
    with col_ktw_alt:
        st.write("### 🚑 Aufgaben KTW")
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict)
    with col_rtw_alt:
        st.write("### 🚑 Aufgaben RTW")
        for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict)

# Zusatzinfos
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕒 Uhrzeit", get_current_time())
col2.metric("🌅 Sonnenaufgang", sonnenaufgang)
col3.metric("🌇 Sonnenuntergang", sonnenuntergang)
col4.metric("🎉 Feiertag", feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟")

# Chatfunktion mit Name und aufklappbarem Chatfenster
if 'chat_name' not in st.session_state:
    st.session_state.chat_name = ""

if st.session_state.chat_name == "":
    if st.button("💬 Chat starten"):
        st.session_state.show_chat_input = True

if st.session_state.get("show_chat_input", False) and st.session_state.chat_name == "":
    name = st.text_input("Bitte gib deinen Namen für den Chat ein (frei erfunden):", max_chars=20)
    if st.button("Name bestätigen"):
        if name.strip():
            st.session_state.chat_name = name.strip()
            st.session_state.show_chat_input = False

if st.session_state.chat_name != "":
    if st.button("💬 Chat öffnen/schließen"):
        st.session_state.show_chat = not st.session_state.get("show_chat", False)

    if st.session_state.get("show_chat", False):
        st.markdown(f"### Chat mit {st.session_state.chat_name}")
        chat_placeholder = st.empty()

        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []

        with st.form(key="chat_form", clear_on_submit=True):
            user_msg = st.text_input("Deine Nachricht:")
            submit = st.form_submit_button("Senden")

            if submit and user_msg.strip():
                st.session_state.chat_messages.append((st.session_state.chat_name, user_msg.strip()))

        for sender, msg in st.session_state.chat_messages:
            st.markdown(f"**{sender}:** {msg}")

