import streamlit as st
import datetime

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

# --- Datum ---
heute_en = datetime.datetime.now().strftime('%A')
heute_deutsch = tage_uebersetzung.get(heute_en, "Unbekannt")

# --- Streamlit Setup ---
st.set_page_config(page_title="RTW Aufgabenplan", page_icon="🚑", layout="centered")
st.markdown("<h1 style='text-align: center; color: #d11f1f;'>🚑 RTW Tagesaufgaben</h1>", unsafe_allow_html=True)

st.subheader(f"📅 Heute ist **{heute_deutsch}**:")
st.success(wochentag_saetze.get(heute_deutsch, "Kein Satz für heute definiert."))

# --- Auswahl anderer Tag ---
tag_auswahl = st.selectbox("📌 Wähle einen anderen Wochentag:", list(wochentag_saetze.keys()))
st.write(f"📝 Aufgabe für **{tag_auswahl}**:")
st.info(wochentag_saetze[tag_auswahl])

# --- RTW + Gras Animation ---
rtw_img_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Rettungswagen-BF-Bochum.jpg/320px-Rettungswagen-BF-Bochum.jpg"  # Beispielbild

animation_html = f"""
<div style="position: fixed; bottom: 0; width: 100%; height: 130px; z-index: -1;">
    <!-- Gras -->
    <div style="position: absolute; bottom: 0; width: 100%; height: 50px; background: linear-gradient(to top, #228B22, #7CFC00); border-top: 2px solid #004d00;"></div>

    <!-- RTW -->
    <img src="{rtw_img_url}" style="position: absolute; height: 80px; bottom: 50px; animation: moveRtw 10s linear infinite;">
</div>

<style>
@keyframes moveRtw {{
    0% {{ left: -250px; }}
    100% {{ left: 100%; }}
}}
</style>
"""

st.markdown(animation_html, unsafe_allow_html=True)
