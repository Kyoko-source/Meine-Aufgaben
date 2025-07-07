import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# 🔒 Verbesserte Passwortabfrage – zentriert & gestylt
def check_password():
    def password_entered():
        if st.session_state["password"] == "RettSüd15":
            st.session_state["passwort_akzeptiert"] = True
        else:
            st.session_state["passwort_akzeptiert"] = False
            st.error("❌ Falsches Passwort. Bitte versuche es erneut.")

    if "passwort_akzeptiert" not in st.session_state or not st.session_state["passwort_akzeptiert"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 🔐 Zugriff geschützt")
            st.markdown("Bitte Passwort eingeben, um fortzufahren.")
            st.text_input("Passwort", type="password", on_change=password_entered, key="password")
        st.stop()

# Passwortprüfung zuerst ausführen
check_password()

# ===========================
# ✅ RTW/KTW Aufgaben-App
# ===========================

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

STATUS_DATEI = "status.json"

aufgaben_ktw = {
    "Montag": ["Fächerdesi 1-6", "Umkleide Bad SW-Bereich reinigen"],
    "Dienstag": ["BZ Kontrolle", "Fächerdesi 7-8"],
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
    "Donnerstag": ["Auto waschen (RTW)", "Garage reinigen"],
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

# =============================
# Monatsaufgaben 1-31 als Platzhalter
# =============================
aufgaben_monat = {
    1: ["Verfallsdaten Verbrauchsmaterialien Fzg"],
    2: ["Reinigung Rucksäcke und tausch mit reserve"],
    3: ["Keine Monatsaufgabe"],
    4: ["Desi-Raum, Desi Spender, Türgriffe desi"],
    5: ["Reinigung Fensterbänke, Schreibtisch, Sofa"],
    6: ["Reinigung Checken Fach 23"],
    7: ["Reinigung Checken Außenfach 24"],
    8: ["Reinigung Checken Außenfach 25 und Rettungsboa plus KED System"],
    9: ["Reinigung Checken Kindernotfallkoffer"],
    10: ["Trage Desinfizieren und Gurte Wechseln"],
    11: ["Reinigung der Schränke in der Fahrzeughalle"],
    12: ["Reinigung Terasse"],
    13: ["Vakuumschienen und Matratze prüfen"],
    14: ["Wurflicher aufladen"],
    15: ["Keine Monatsaufgabe"],
    16: ["Keine Monatsaufgabe"],
    17: ["Keine Monatsaufgabe"],
    18: ["Reinigung Fensterbänke, Schreibtisch, Sofa"],
    19: ["Keine Monatsaufgabe"],
    20: ["Keine Monatsaufgabe"],
    21: ["Keine Monatsaufgabe"],
    22: ["Keine Monatsaufgabe"],
    23: ["Keine Monatsaufgabe"],
    24: ["Martinanlage prüfen und ölen"],
    25: ["Keine Monatsaufgabe"],
    26: ["Keine Monatsaufgabe"],
    27: ["Monatliche Kontrolle C3 C1"],
    28: ["Reinigung Aussenstahlschrank"],
    29: ["Reinigung Wachenvorplatz"],
    30: ["Keine Monatsaufgabe"],
    31: ["Keine Monatsaufgabe"]
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
        # Nur Text anzeigen, keine interaktive Checkbox
        if checked:
            st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)
    else:
        col_cb, col_text = st.columns([1, 20])
        with col_cb:
            neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        with col_text:
            if neu_gesetzt:
                st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:red;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)

        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Aktueller Tag im Monat
heute_tag = datetime.datetime.now().day

# Lade gespeicherten Status
status_dict = lade_status()

# Seitentitel & Header
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Aufgabenbereiche in Boxen mit Farben & Überschrift und Liste
col_ktw, col_rtw = st.columns(2)

with col_ktw:
    st.markdown("""
    <div style="
        background-color:#e8f5e9; 
        border:2px solid #2e7d32; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(46, 125, 50, 0.15);
    ">
        <h3 style='color:#2e7d32; margin-bottom:12px;'>🧾 Aufgaben KTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="KTW")
    st.markdown("</div>", unsafe_allow_html=True)

with col_rtw:
    st.markdown("""
    <div style="
        background-color:#e3f2fd; 
        border:2px solid #1976d2; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(25, 118, 210, 0.15);
    ">
        <h3 style='color:#1976d2; margin-bottom:12px;'>🧾 Aufgaben RTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="RTW")
    st.markdown("</div>", unsafe_allow_html=True)

# Feiertagsanzeige
if feiertag_heute:
    st.markdown(f"### 🎉 Heute ist Feiertag: **{feiertag_heute}** 🎉")

# Anzeige der Monatsaufgaben für den heutigen Tag (einmal, da gleich für KTW und RTW)
st.markdown("---")
st.markdown("## 📅 Monatsaufgaben")

aufgaben_heute = aufgaben_monat.get(heute_tag, [])
if aufgaben_heute and not (len(aufgaben_heute) == 1 and aufgaben_heute[0].lower() == "keine monatsaufgabe"):
    st.markdown(f"""
    <div style="
        background-color:#fff3e0; 
        border:2px solid #fb8c00; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 10px rgba(251, 140, 0, 0.3);
        margin-bottom: 20px;
    ">
        <h4 style='color:#ef6c00;'>📌 Monatsaufgaben für den {heute_tag}.</h4>
    """, unsafe_allow_html=True)

    # Status für die Monatsaufgaben anzeigen (alle in einer Liste mit Checkboxen)
    for aufgabe in aufgaben_heute:
        jahr = datetime.datetime.now().year
        raw_key = f"Monat_{heute_tag}_{jahr}_{aufgabe}"
        key_hash = hashlib.md5(raw_key.encode()).hexdigest()
        checked = status_dict.get(key_hash, False)

        col_cb, col_text = st.columns([1, 20])
        with col_cb:
            neu_gesetzt = st.checkbox("", value=checked, key=key_hash)
        with col_text:
            if neu_gesetzt:
                st.markdown(f"<span style='color:green; text-decoration: line-through;'>✅ {aufgabe}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:#bf360c;'>⏳ {aufgabe}</span>", unsafe_allow_html=True)

        if neu_gesetzt != checked:
            status_dict[key_hash] = neu_gesetzt
            speichere_status(status_dict)
            if neu_gesetzt:
                st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Heute keine Monatsaufgaben geplant.")

# Footer mit Uhrzeit
st.markdown("---")
st.markdown(f"⏰ Aktuelle Uhrzeit: {get_current_time()}")

# Hinweis:
# Möchtest du Monatsaufgaben befüllen, trage einfach z.B.:
# aufgaben_monat[1] = ["Monatscheck Batteriezustand", "Lüftungsfilter prüfen"]
