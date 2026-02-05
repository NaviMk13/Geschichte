import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import wikipedia
from wikipedia.exceptions import PageError, DisambiguationError
import random

st.set_page_config(page_title="History Dash", layout="wide")
st.title("🚀 History Dash – Springe durch die deutsche Geschichte!")

# ---------------- SETTINGS ----------------
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 400
PLAYER_SIZE = 30
GRAVITY = 2
JUMP_STRENGTH = -15
FPS = 30
SCROLL_SPEED = 10

wikipedia.set_lang("de")

# ---------------- SESSION STATE ----------------
if "player_y" not in st.session_state:
    st.session_state.player_y = CANVAS_HEIGHT - PLAYER_SIZE - 50
    st.session_state.vel_y = 0
    st.session_state.scroll_x = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.events = []
    st.session_state.event_platforms = []

# ---------------- FETCH WIKIPEDIA EVENTS ----------------
@st.cache_data
def fetch_events(years):
    events_list = []
    platforms = []
    x_pos = 400
    for y in years:
        try:
            page = wikipedia.page(str(y))
            content = page.content
            keywords = ["Deutschland", "deutsch", "Berlin", "Bundesrepublik", "DDR",
                        "NS", "Kaiserreich", "Weimar", "Nazi"]
            for line in content.split("\n"):
                if any(k.lower() in line.lower() for k in keywords):
                    if len(line.strip()) > 30:
                        events_list.append((y, line.strip()))
                        # Plattformen werden im Canvas platziert
                        platforms.append({"x": x_pos, "y": random.randint(250, 350), "text": line.strip()})
                        x_pos += 300  # Abstand zwischen Plattformen
                        break
        except (PageError, DisambiguationError):
            continue
    return events_list, platforms

# Lade Events beim Start
if not st.session_state.events:
    years = range(1900, 2026, 5)
    st.session_state.events, st.session_state.event_platforms = fetch_events(years)

# ---------------- GAME INPUT ----------------
jump = st.button("Springen (Space)")

# ---------------- GAME LOGIC ----------------
if not st.session_state.game_over:
    # Spieler springt
    if jump and st.session_state.player_y + PLAYER_SIZE >= CANVAS_HEIGHT - 50:
        st.session_state.vel_y = JUMP_STRENGTH

    # Physik
    st.session_state.vel_y += GRAVITY
    st.session_state.player_y += st.session_state.vel_y

    # Boden
    if st.session_state.player_y + PLAYER_SIZE >= CANVAS_HEIGHT - 50:
        st.session_state.player_y = CANVAS_HEIGHT - PLAYER_SIZE - 50
        st.session_state.vel_y = 0

    # Scroll
    st.session_state.scroll_x += SCROLL_SPEED

    # Kollision mit Plattformen / Punkte
    player_rect = (100, st.session_state.player_y, PLAYER_SIZE, PLAYER_SIZE)
    for plat in st.session_state.event_platforms:
        plat_rect = (plat["x"] - st.session_state.scroll_x, plat["y"], 100, 20)
        px, py, pw, ph = player_rect
        ox, oy, ow, oh = plat_rect
        if px + pw > ox and px < ox + ow and py + ph > oy and py < oy + oh:
            st.session_state.score += 1
            # Info-Card anzeigen
            with st.expander(f"Ereignis {st.session_state.score} ({plat['x']}):"):
                st.write(plat["text"])
            # Plattform nach vorne verschieben, damit sie nicht erneut Punkte gibt
            plat["x"] += 10000

    # Game Over: falls Spieler unter Canvas fällt
    if st.session_state.player_y > CANVAS_HEIGHT:
        st.session_state.game_over = True

# ---------------- DRAW ----------------
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, CANVAS_WIDTH)
ax.set_ylim(0, CANVAS_HEIGHT)
ax.set_facecolor("skyblue")
ax.invert_yaxis()

# Boden
ax.add_patch(patches.Rectangle((0, CANVAS_HEIGHT-50), CANVAS_WIDTH, 50, color="gray"))

# Spieler
ax.add_patch(patches.Rectangle((100, st.session_state.player_y), PLAYER_SIZE, PLAYER_SIZE, color="green"))

# Plattformen
for plat in st.session_state.event_platforms:
    px = plat["x"] - st.session_state.scroll_x
    if -100 < px < CANVAS_WIDTH:
        ax.add_patch(patches.Rectangle((px, plat["y"]), 100, 20, color=random.choice(["red","orange","yellow","blue","purple"])))

# Score
ax.text(10, 20, f"Score: {st.session_state.score}", fontsize=12, color="white")

ax.axis("off")
st.pyplot(fig)

# ---------------- GAME OVER ----------------
if st.session_state.game_over:
    st.warning("GAME OVER! F5 drücken zum Neustarten")
