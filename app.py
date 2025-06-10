# Tagesinfos schön gestaltet mit 4 farbigen Boxen
st.markdown("---")
st.markdown("### 🌤️ Zusätzliche Tagesinfos")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
    <div style="
        background:#e8f5e9; 
        border:1.5px solid #2e7d32; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#2e7d32;
        box-shadow: 1px 1px 4px rgba(46, 125, 50, 0.15);
    ">
        🕒 Uhrzeit<br><span style='font-size:24px;'>{get_current_time()}</span>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style="
        background:#ffebee; 
        border:1.5px solid #c62828; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#c62828;
        box-shadow: 1px 1px 4px rgba(198, 40, 40, 0.15);
    ">
        🎉 Feiertag<br><span style='font-size:20px;'>{feiertag_heute if feiertag_heute else "Kein Feiertag heute 😟"}</span>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style="
        background:#e3f2fd; 
        border:1.5px solid #1565c0; 
        border-radius:8px; 
        padding:12px; 
        text-align:center;
        font-weight:bold;
        color:#1565c0;
        box-shadow: 1px 1px 4px rgba(21, 101, 192, 0.15);
    ">
        📅 Wochentag<br><span style='font-size:24px;'>{heute_deutsch}</span>
    </div>
""", unsafe_allow_html=True)

# 4. Box mit Quiz
with col4:
    st.markdown("""
    <div style="
        background:#fff3e0;
        border:1.5px solid #ef6c00;
        border-radius:8px;
        padding:12px;
        text-align:center;
        font-weight:bold;
        color:#ef6c00;
        box-shadow: 1px 1px 4px rgba(239, 108, 0, 0.15);
    ">
        🧠 Quizzeit!
    </div>
    """, unsafe_allow_html=True)

    frage = "Wie viele Tage hat eine Woche?"
    optionen = ["5", "6", "7", "8"]
    antwort = st.radio(frage, optionen, key="quiz_antwort")

    if st.button("Antwort überprüfen"):
        if antwort == "7":
            st.success("✅ Richtig! Eine Woche hat 7 Tage.")
        else:
            st.error("❌ Falsch, versuche es nochmal.")
