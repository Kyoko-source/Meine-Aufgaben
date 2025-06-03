import streamlit as st
import datetime
import pytz

# --- Aufgabenplan ---
wochentag_saetze = {
    "Montag": "Heute ist die Fächerdesi dran! 1-6",
    "Dienstag": "Heute ist die BZ Kontrolle + Fächerdesi 7-11 dran",
    "Mittwoch": "Heute ist die Innenraumdesi dran",
    "Donnerstag": "Heute wird das Auto gewaschen und die Garage gereinigt",
    "Freitag": "Heute wird Fach 12-18 desinfiziert, Zusätzlich Betriebsmittelkontrolle und O2 Schlauch + Fingertipp gewechselt",
    "Samstag": "Heute wird Fach 20-22 desinfiziert",
    "Sonntag": "Heute wird die Küche gereinigt"
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

# --- Feiertage 2025 in Deutschland ---
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

# --- Streamlit Setup ---
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")
st.title("🚑 RTW Tagesaufgaben")

# --- Aktuelle Uhrzeit ---
def get_current_time():
    timezone = pytz.timezone('Europe/Berlin')
    current_time = datetime.datetime.now(timezone).strftime('%H:%M:%S')
    return current_time

# --- Heute bestimmen ---
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")

# --- Feiertag prüfen ---
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str, None)

# --- Sonnenaufgang und Sonnenuntergang für heute ---
# (Daten manuell eingetragen oder aus einer zuverlässigen Quelle entnommen)
sonnenaufgang = "05:17"
sonnenuntergang = "21:43"

# --- Sidebar mit Tabelle ---
st.sidebar.header("📅 Aktuelle Informationen")
st.sidebar.table({
    "Aktuelle Uhrzeit": [get_current_time()],
    "Sonnenaufgang": [sonnenaufgang],
    "Sonnenuntergang": [sonnenuntergang],
    "Feiertag": [feiertag_heute if feiertag_heute else "Kein Feiertag"]
})

# --- Aufgabenübersicht ---
st.subheader(f"Heute ist {heute_deutsch}:")
st.success(wochentag_saetze.get(heute_deutsch, "Kein Satz für heute definiert."))

# --- Auswahl anderer Tag ---
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag:", list(wochentag_saetze.keys()))
st.write(f"📝 Aufgabe für **{tag_auswahl}**:")
st.info(wochentag_saetze[tag_auswahl])

# --- Zusatzinfos unten anzeigen ---
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")

info_col1, info_col2, info_col3, info_col4 = st.columns(4)
info_col1.metric("Aktuelle Uhrzeit", get_current_time())
info_col2.metric("Sonnenaufgang", sonnenaufgang)
info_col3.metric("Sonnenuntergang", sonnenuntergang)
info_col4.metric("Feiertag", feiertag_heute if feiertag_heute else "—")
