import streamlit as st
import datetime
import pytz
import json
import os
import hashlib

# Passwortabfrage
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

check_password()

st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="wide")

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

# Quiz mit 20 Fragen
quiz_fragen = [
    {"frage": "Was ist die Hauptstadt von Deutschland?", "optionen": ["Berlin", "München", "Köln", "Hamburg"], "korrekt": "Berlin"},
    {"frage": "Wie viele Kontinente gibt es?", "optionen": ["5", "6", "7", "8"], "korrekt": "7"},
    {"frage": "Wer schrieb 'Faust'?", "optionen": ["Goethe", "Schiller", "Heine", "Lessing"], "korrekt": "Goethe"},
    {"frage": "Was ist das chemische Symbol für Wasser?", "optionen": ["H2O", "O2", "CO2", "NaCl"], "korrekt": "H2O"},
    {"frage": "Wie viele Planeten hat unser Sonnensystem?", "optionen": ["7", "8", "9", "10"], "korrekt": "8"},
    {"frage": "Wer malte die Mona Lisa?", "optionen": ["Michelangelo", "Leonardo da Vinci", "Raphael", "Rembrandt"], "korrekt": "Leonardo da Vinci"},
    {"frage": "Was ist die größte Wüste der Welt?", "optionen": ["Sahara", "Arabische Wüste", "Gobi", "Antarktische Wüste"], "korrekt": "Antarktische Wüste"},
    {"frage": "Wie viele Bundesländer hat Deutschland?", "optionen": ["14", "15", "16", "17"], "korrekt": "16"},
    {"frage": "Wer war der erste Mensch auf dem Mond?", "optionen": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"], "korrekt": "Neil Armstrong"},
    {"frage": "Welche Sprache hat die meisten Muttersprachler?", "optionen": ["Englisch", "Mandarin", "Spanisch", "Hindi"], "korrekt": "Mandarin"},
    {"frage": "Wie heißt das kleinste Knochen im menschlichen Körper?", "optionen": ["Steigbügel", "Hammer", "Amboss", "Elle"], "korrekt": "Steigbügel"},
    {"frage": "Welcher Planet ist der heißeste in unserem Sonnensystem?", "optionen": ["Venus", "Merkur", "Mars", "Jupiter"], "korrekt": "Venus"},
    {"frage": "Wie viele Tage hat ein Schaltjahr?", "optionen": ["365", "366", "367", "364"], "korrekt": "366"},
    {"frage": "Wer entdeckte die Relativitätstheorie?", "optionen": ["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"], "korrekt": "Albert Einstein"},
    {"frage": "Was ist die Währung in Japan?", "optionen": ["Yen", "Won", "Dollar", "Euro"], "korrekt": "Yen"},
    {"frage": "Welches Land gewann die Fußball-Weltmeisterschaft 2014?", "optionen": ["Brasilien", "Deutschland", "Argentinien", "Spanien"], "korrekt": "Deutschland"},
    {"frage": "Welches Tier ist das größte Landsäugetier?", "optionen": ["Giraffe", "Elefant", "Nashorn", "Nilpferd"], "korrekt": "Elefant"},
    {"frage": "Wie viele Tasten hat ein klassisches Klavier?", "optionen": ["88", "76", "61", "100"], "korrekt": "88"},
    {"frage": "Was bedeutet das lateinische Wort 'Aqua'?", "optionen": ["Feuer", "Erde", "Wasser", "Luft"], "korrekt": "Wasser"},
    {"frage": "In welchem Jahr fiel die Berliner Mauer?", "optionen": ["1987", "1989", "1991", "1993"], "korrekt": "1989"},
]

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "quiz_beendet" not in st.session_state:
    st.session_state.quiz_beendet = False
if "quiz_name" not in st.session_state:
    st.session_state.quiz_name = ""

def quiz_start():
    fragen_index = st.session_state.quiz_index
    frage = quiz_fragen[fragen_index]
    st.markdown(f"**Frage {fragen_index + 1} von {len(quiz_fragen)}:** {frage['frage']}")
    antwort = st.radio("Wähle deine Antwort:", frage["optionen"], key=f"frage_{fragen_index}")

    if st.button("Antwort bestätigen"):
        if antwort == frage["korrekt"]:
            if fragen_index + 1 == len(quiz_fragen):
                st.success("🎉 Herzlichen Glückwunsch! Du hast alle Fragen richtig beantwortet!")
                st.session_state.quiz_beendet = True
            else:
                st.session_state.quiz_index += 1
                st.experimental_rerun()
        else:
            st.error(f"❌ Falsch! Die richtige Antwort wäre: {frage['korrekt']}")
            st.session_state.quiz_beendet = True
            st.experimental_rerun()

def scoreboard_eingabe():
    st.markdown("## Das Quiz ist beendet.")
    name = st.text_input("Bitte gib deinen Namen für das Scoreboard ein:", value=st.session_state.quiz_name)
    st.session_state.quiz_name = name
    if st.button("Name speichern"):
        if name.strip():
            st.success(f"Vielen Dank, {name}! Dein Ergebnis wurde gespeichert.")
            # Hier könnte man Scoreboard speichern, z.B. in eine Datei oder DB
        else:
            st.error("Bitte gib einen gültigen Namen ein.")

# Aktuelles Datum und Wochentag
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")
heute_str = datetime.datetime.now().strftime('%d.%m.%Y')
feiertag_heute = feiertage_2025.get(heute_str)

# Lade gespeicherten Status
status_dict = lade_status()

# Seitentitel & Header
st.title("✔ Rettungswache Südlohn Tagesaufgaben ✔")
st.subheader(f"📅 Heute ist {heute_deutsch} ({heute_str})")

# Vier Kästchen (2 Reihen x 2 Spalten)
col1, col2 = st.columns(2)

# 1. Kasten: KTW Aufgaben (grün)
with col1:
    st.markdown("""
    <div style="
        background-color:#e8f5e9; 
        border:2px solid #2e7d32; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(46, 125, 50, 0.15);
        margin-bottom: 10px;
    ">
        <h3 style='color:#2e7d32; margin-bottom:12px;'>🧾 Aufgaben KTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_ktw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="KTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. Kasten: RTW Aufgaben (rot)
with col2:
    st.markdown("""
    <div style="
        background-color:#ffebee; 
        border:2px solid #c62828; 
        border-radius:12px; 
        padding:20px; 
        box-shadow: 2px 3px 8px rgba(198, 40, 40, 0.15);
        margin-bottom: 10px;
    ">
        <h3 style='color:#c62828; margin-bottom:12px;'>🚑 Aufgaben RTW</h3>
    """, unsafe_allow_html=True)
    for aufgabe in aufgaben_rtw.get(heute_deutsch, []):
        aufgabe_mit_feedback(aufgabe, heute_deutsch, status_dict, fahrzeug="RTW", readonly=False)
    st.markdown("</div>", unsafe_allow_html=True)

# 3. Kasten: Feiertag / Info (grau)
with col1:
    st.markdown("""
    <div style="
        background-color:#f5f5f5;
        border:2px solid #b0bec5;
        border-radius:12px;
        padding:20px;
        box-shadow: 2px 3px 8px rgba(176, 190, 197, 0.15);
    ">
        <h3 style='color:#37474f; margin-bottom:12px;'>ℹ️ Info</h3>
    """, unsafe_allow_html=True)
    if feiertag_heute:
        st.success(f"Heute ist Feiertag: {feiertag_heute} 🎉")
    else:
        st.info("Heute ist kein Feiertag.")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. Kasten: Quiz (blau) - hier wird das Quiz eingebaut
with col2:
    st.markdown("""
    <div style="
        background-color:#e3f2fd;
        border:2px solid #1565c0;
        border-radius:12px;
        padding:20px;
        box-shadow: 2px 3px 8px rgba(21, 101, 192, 0.15);
    ">
        <h3 style='color:#1565c0; margin-bottom:12px;'>❓ Quiz Allgemeinwissen</h3>
    """, unsafe_allow_html=True)
    if not st.session_state.quiz_beendet:
        quiz_start()
    else:
        scoreboard_eingabe()
    st.markdown("</div>", unsafe_allow_html=True)

# Dropdown zur Ansicht anderer Wochentage (readonly)
st.markdown("---")
tag_auswahl = st.selectbox(
    "📌 Wähle einen anderen Wochentag zur Ansicht:",
    ["—"] + list(tage_uebersetzung.values())
)

if tag_auswahl and tag_auswahl != "—":
    st.markdown(f"### Aufgaben am {tag_auswahl}")

    col1_other, col2_other = st.columns(2)
    with col1_other:
        st.markdown(f"**🧾 KTW Aufgaben am {tag_auswahl}:**")
        for aufgabe in aufgaben_ktw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="KTW", readonly=True)
    with col2_other:
        st.markdown(f"**🚑 RTW Aufgaben am {tag_auswahl}:**")
        for aufgabe in aufgaben_rtw.get(tag_auswahl, []):
            aufgabe_mit_feedback(aufgabe, tag_auswahl, status_dict, fahrzeug="RTW", readonly=True)
