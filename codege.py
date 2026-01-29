import streamlit as st
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="Deutsche Geschichte Timeline",
    page_icon="🇩🇪",
    layout="centered"
)

wikipedia.set_lang("de")

# ----------------- UI -----------------
st.title("🇩🇪 Deutsche Geschichte – Timeline (1900–2025)")
st.write(
    "Diese App lädt Ereignisse **dynamisch von Wikipedia** "
    "und filtert sie nach **Deutschland-Bezug**."
)

year = st.slider(
    "Wähle ein Jahr",
    min_value=1900,
    max_value=2025,
    value=1945,
    step=1
)

# ----------------- DATA FETCHING -----------------
@st.cache_data(show_spinner=False)
def fetch_wikipedia_events(year: int) -> list[str]:
    """
    Holt den Wikipedia-Artikel für ein Jahr
    und filtert nach Deutschland-bezogenen Ereignissen.
    """
    try:
        page = wikipedia.page(str(year))
        content = page.content

        # Schlüsselwörter für Deutschland-Bezug
        keywords = [
            "Deutschland", "deutsch", "Deutsches Reich",
            "Bundesrepublik", "DDR", "Berlin",
            "Kaiserreich", "Weimar", "NS", "Nazi"
        ]

        events = []
        for line in content.split("\n"):
            if any(keyword.lower() in line.lower() for keyword in keywords):
                if len(line.strip()) > 30:
                    events.append(line.strip())

        return events

    except DisambiguationError:
        return ["⚠️ Mehrdeutiger Wikipedia-Eintrag für dieses Jahr."]
    except PageError:
        return []
    except Exception as e:
        return [f"❌ Fehler beim Laden der Daten: {e}"]

# ----------------- LOGIC -----------------
with st.spinner("Lade Daten von Wikipedia …"):
    events = fetch_wikipedia_events(year)

# ----------------- OUTPUT -----------------
st.subheader(f"Ereignisse in Deutschland im Jahr {year}")

if not events:
    st.info("Keine Deutschland-bezogenen Ereignisse gefunden.")
else:
    for i, event in enumerate(events[:15], start=1):
        with st.expander(f"Ereignis {i}"):
            st.write(event)

# ----------------- FOOTER -----------------
st.divider()
st.caption(
    "Datenquelle: Wikipedia (automatisch abgerufen) · "
    "Demo-App mit Streamlit & Python"
)
