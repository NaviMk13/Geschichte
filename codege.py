import streamlit as st
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Deutsche Geschichte Timeline", layout="centered")
st.title("🇩🇪 Deutsche Geschichte Timeline")
st.write(
    "Diese App zeigt historische Ereignisse in Deutschland für ein ausgewähltes Jahr. "
    "Daten werden dynamisch von Wikipedia abgerufen."
)

# ----------------- USER INPUT -----------------
year = st.slider("Wähle ein Jahr", 1900, 2025, 1945)

# ----------------- WIKIPEDIA -----------------
wikipedia.set_lang("de")

@st.cache_data
def fetch_events(year: int):
    """
    Ruft Wikipedia-Seite für das Jahr ab und filtert nach Deutschland-bezogenen Ereignissen.
    """
    try:
        page = wikipedia.page(str(year))
        content = page.content

        keywords = [
            "Deutschland", "deutsch", "Berlin", "Bundesrepublik", "DDR",
            "NS", "Kaiserreich", "Weimar", "Nazi"
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

# ----------------- FETCH DATA -----------------
with st.spinner("Lade Ereignisse von Wikipedia …"):
    events = fetch_events(year)

# ----------------- DISPLAY -----------------
st.subheader(f"Ereignisse in Deutschland im Jahr {year}")

if not events:
    st.info("Keine Deutschland-bezogenen Ereignisse gefunden.")
else:
    # Alles zu einem Fließtext zusammenfassen
    text = f"Im Jahr {year} gab es in Deutschland folgende Ereignisse: " + " ".join(events[:15])
    # Optional: Text kürzen
    MAX_CHARS = 1500
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + " …"
    st.write(text)

# ----------------- FOOTER -----------------
st.divider()
st.caption("Datenquelle: Wikipedia · Demo-App mit Streamlit & Python")
