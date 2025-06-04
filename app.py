import streamlit as st
import datetime
import pytz

# Aufgabenlisten KTW und RTW
aufgaben_ktw = {
    "Montag": ["Fächerdesi 1-3", "Fächerdesi 4-6"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-11"],
    "Mittwoch": ["Innenraumdesi KTW"],
    "Donnerstag": ["Auto waschen (KTW)", "Garage reinigen"],
    "Freitag": ["Fach 12-15 desinfizieren", "Betriebsmittelkontrolle"],
    "Samstag": ["Fach 20-21 desinfizieren"],
    "Sonntag": ["Küche reinigen (KTW)"]
}

aufgaben_rtw = {
    "Montag": ["Fächerdesi RTW 1-6"],
    "Dienstag": ["RTW Ausstattung prüfen", "O2 Flasche checken"],
    "Mittwoch": ["Innenraumdesi RTW"],
    "Donnerstag": ["Auto waschen (RTW)", "Garage reinigen RTW"],
    "Freitag": ["Fach 16-18 desinfizieren", "O2 Schlauch + Fingertipp wechseln"],
    "Samstag": ["Fach 22 desinfizieren"],
    "Sonntag": ["Küche reinigen (RTW)"]
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

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Sonneninfos (optional statisch)
sonnenaufgang = "05:17"
sonnenuntergang = "21:43"

# Streamlit Page Setup
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")
st.title("🚑 RTW Tagesaufgaben")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Aufgabenbereich für den aktuellen Tag
st.markdown("## ✅ Aufgaben für heute")

# KTW Aufgaben
st.write("### 🧾 Aufgaben KTW")
for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
    st.checkbox(f"{aufgabe}", key=f"ktw_{heute_deutsch}_{aufgabe}")

# RTW Aufgaben
st.write("### 🚑 Aufgaben RTW")
for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
    st.checkbox(f"{aufgabe}", key=f"rtw_{heute_deutsch}_{aufgabe}")

# Auswahl anderer Tage
st.markdown("---")
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag zur Ansicht:", list(tage_uebersetzung.values()))

if tag_auswahl != heute_deutsch:
    st.markdown(f"## 🔄 Aufgaben für {tag_auswahl}")
    st.write("### 🧾 Aufgaben KTW")
    for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
        st.checkbox(f"{aufgabe}", key=f"ktw_{tag_auswahl}_{aufgabe}")

    st.write("### 🚑 Aufgaben RTW")
    for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
        st.checkbox(f"{aufgabe}", key=f"rtw_{tag_auswahl}_{aufgabe}")

# Zusatzinfos
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🕒 Uhrzeit", get_current_time())
col2.metric("🌅 Sonnenaufgang", sonnenaufgang)
col3.metric("🌇 Sonnenuntergang", sonnenuntergang)
col4.metric("🎉 Feiertag", feiertag_heute if feiertag_heute else "—")
