import streamlit as st
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError

# ----------------- CONFIG -----------------
st.set_page_config(
    page_title="Deutsche Geschichte Timeline",
    page_icon="🇩🇪",
    layout="centered"
)

st.title("🇩🇪 Deutsche Geschichte (1900–2025)")
st.write(
    "Diese App zeigt historische Ereignisse in Deutschland für ein ausgewähltes Jahr. "
    "Die Daten werden **dynamisch von Wikipedia** abgerufen."
)

# ----------------- UI: Jahr auswählen -----------------
year = st.slider(
    "Wähle ein Jahr",
    min_value=1900,
    max_value=2025,
    value=1945,
    step=1
)

# ----------------- WIKIPEDIA CONFIG -----------------
wikipedia.set_lang("de")

# ----------------- DATEN ABRUFEN -----------------
@st.cache_data(show_spinner=False)
def fetch_events(year: int) -> list[str]:
    """
    Ruft Wikipedia-Seite für das Jahr ab und filtert Deutschland-bezogene Ereignisse.
    """
    try:
        page = wikipedia.page(str(year))
        content = page.content

        # Keywords für Deutschland-Bezug
        keywords = [
            "Deutschland", "deutsch", "Deutsches Reich",
            "Bundesrepublik", "DDR", "Berlin",
            "Kaiserreich", "Weimar", "NS", "Nazi"
        ]

        events = []
        for line in content.split("\n"):
            if any(k.lower() in line.lower() for k in keywords):
                if len(line.strip()) > 30:
                    events.append(line.strip())

        return events

    except DisambiguationError:
        return ["⚠️ Mehrdeutiger Wikipedia-Eintrag für dieses Jahr."]
    except PageError:
        return []
    except Exception as e:
        return [f"❌ Fehler beim Laden der Daten: {e}"]

# ----------------- LOGIK -----------------
with st.spinner("Lade Daten von Wikipedia …"):
    events = fetch_events(year)

# ----------------- AUSGABE -----------------
st.subheader(f"Ereignisse in Deutschland im Jahr {year}")

if not events:
    st.info("Keine Deutschland-bezogenen Ereignisse gefunden.")
else:
    # Alle Ereignisse zu einem Text zusammenfassen
    text = f"Im Jahr {year} gab es in Deutschland folgende bedeutende Ereignisse: " + " ".join(events[:15])
    # Optional: Text auf max. Länge kürzen
    MAX_CHARS = 1500
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + " …"
    st.write(text)

# ----------------- FOOTER -----------------
st.divider()
st.caption(
    "Datenquelle: Wikipedia (automatisch abgerufen) · "
    "Demo-App mit Streamlit & Python"
)
