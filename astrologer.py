import streamlit as st
import anthropic
import json
from datetime import date, datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🔮 Celestial Soul Reader",
    page_icon="🔮",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Raleway:wght@300;400;500;600&display=swap');

/* ---- Global ---- */
html, body, [class*="css"] {
    font-family: 'Raleway', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0015 0%, #0d0030 40%, #100020 70%, #0a0015 100%);
    min-height: 100vh;
}

/* Stars animation */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 50% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 90% 30%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 90%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 60% 50%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 80% 70%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 40%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 15% 55%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 15%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 55% 85%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 35%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 45%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(2px 2px at 45% 75%, rgba(255,255,255,0.4) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* Nebula glows */
.stApp::after {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(120,0,200,0.15) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ---- Header ---- */
.cosmic-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
}

.cosmic-title {
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 2.2rem;
    background: linear-gradient(135deg, #ffd700, #ff9ff3, #a29bfe, #74b9ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.4rem;
}

.cosmic-subtitle {
    color: rgba(255,255,255,0.45);
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    font-weight: 300;
}

/* ---- Cards ---- */
.cosmic-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 1.8rem;
    margin: 1rem 0;
    backdrop-filter: blur(20px);
}

/* ---- Section titles ---- */
.section-title {
    font-family: 'Cinzel Decorative', serif;
    font-size: 0.75rem;
    color: #a855f7;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    text-align: center;
    margin: 1.5rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::before, .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, transparent, rgba(168,85,247,0.4), transparent);
}

/* ---- Person name result ---- */
.result-name {
    font-family: 'Cinzel Decorative', serif;
    font-size: 2rem;
    background: linear-gradient(135deg, #ffd700, #ff9ff3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.5rem;
}

.zodiac-pill {
    display: inline-block;
    background: rgba(168,85,247,0.2);
    border: 1px solid rgba(168,85,247,0.4);
    border-radius: 999px;
    padding: 0.3rem 1.2rem;
    color: #c4b5fd;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.08em;
}

/* ---- Lucky grid ---- */
.lucky-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-top: 0.5rem;
}

.lucky-item {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 1rem 0.8rem;
    text-align: center;
}

.lucky-label {
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.38);
    margin-bottom: 0.4rem;
    font-weight: 600;
}

.lucky-value {
    font-size: 1rem;
    font-weight: 600;
    color: white;
}

.colour-swatch {
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-block;
    margin-top: 0.35rem;
    border: 2px solid rgba(255,255,255,0.2);
}

/* ---- Reading text ---- */
.reading-text {
    color: rgba(255,255,255,0.82);
    font-size: 0.93rem;
    line-height: 1.95;
    font-weight: 300;
}

/* ---- Streamlit overrides ---- */
.stTextInput > div > div > input,
.stDateInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Raleway', sans-serif !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus {
    border-color: rgba(162,155,254,0.6) !important;
    box-shadow: 0 0 0 3px rgba(162,155,254,0.15) !important;
}

.stTextInput label, .stDateInput label {
    color: rgba(255,255,255,0.55) !important;
    font-family: 'Raleway', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}

.stButton > button {
    width: 100%;
    padding: 0.9rem 1rem;
    border: none;
    border-radius: 14px;
    background: linear-gradient(135deg, #7c3aed, #a855f7, #ec4899) !important;
    color: white !important;
    font-family: 'Cinzel Decorative', serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(168,85,247,0.4) !important;
}

.stSpinner > div {
    border-top-color: #a855f7 !important;
}

div[data-testid="stMarkdownContainer"] p {
    color: rgba(255,255,255,0.82);
}

.stAlert {
    background: rgba(168,85,247,0.1) !important;
    border: 1px solid rgba(168,85,247,0.3) !important;
    color: rgba(255,255,255,0.8) !important;
    border-radius: 14px !important;
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_zodiac(dob: date) -> str:
    m, d = dob.month, dob.day
    if (m == 3 and d >= 21) or (m == 4 and d <= 19): return "♈ Aries"
    if (m == 4 and d >= 20) or (m == 5 and d <= 20): return "♉ Taurus"
    if (m == 5 and d >= 21) or (m == 6 and d <= 20): return "♊ Gemini"
    if (m == 6 and d >= 21) or (m == 7 and d <= 22): return "♋ Cancer"
    if (m == 7 and d >= 23) or (m == 8 and d <= 22): return "♌ Leo"
    if (m == 8 and d >= 23) or (m == 9 and d <= 22): return "♍ Virgo"
    if (m == 9 and d >= 23) or (m == 10 and d <= 22): return "♎ Libra"
    if (m == 10 and d >= 23) or (m == 11 and d <= 21): return "♏ Scorpio"
    if (m == 11 and d >= 22) or (m == 12 and d <= 21): return "♐ Sagittarius"
    if (m == 12 and d >= 22) or (m == 1 and d <= 19): return "♑ Capricorn"
    if (m == 1 and d >= 20) or (m == 2 and d <= 18): return "♒ Aquarius"
    return "♓ Pisces"


def get_age(dob: date) -> int:
    today = date.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


COLOR_MAP = {
    "red": "#e74c3c", "rose": "#e91e63", "pink": "#f06292", "coral": "#ff7043",
    "orange": "#ff9800", "amber": "#ffc107", "gold": "#ffd700", "yellow": "#ffeb3b",
    "green": "#4caf50", "teal": "#009688", "cyan": "#00bcd4", "blue": "#2196f3",
    "indigo": "#3f51b5", "violet": "#9c27b0", "purple": "#673ab7", "lavender": "#b39ddb",
    "white": "#f5f5f5", "silver": "#bdbdbd", "grey": "#9e9e9e", "gray": "#9e9e9e",
    "black": "#424242", "brown": "#795548", "maroon": "#880e4f", "navy": "#1a237e",
    "sky": "#29b6f6", "jade": "#00897b", "emerald": "#26a69a", "sapphire": "#1565c0",
    "ruby": "#c62828", "cream": "#fff8e1", "peach": "#ffab91", "turquoise": "#26c6da",
}


def colour_hex(name: str) -> str:
    lower = name.lower()
    for k, v in COLOR_MAP.items():
        if k in lower:
            return v
    return "#a855f7"


def call_claude(name: str, dob: date) -> dict:
    client = anthropic.Anthropic()
    zodiac = get_zodiac(dob)
    age = get_age(dob)
    dob_fmt = dob.strftime("%-d %B %Y")

    prompt = f"""You are a mystical astrologer, numerologist, and name meaning expert. Analyze the following person and give a comprehensive cosmic reading.

Name: {name}
Date of Birth: {dob_fmt}
Age: {age} years
Zodiac Sign: {zodiac}

Respond ONLY in valid JSON with this exact structure (no markdown, no code blocks, no extra text):

{{
  "lucky_number": "a single or double digit number",
  "lucky_colour": "one specific color name (e.g. Deep Violet, Rose Gold, Emerald Green)",
  "lucky_day": "one day of the week",
  "lucky_stone": "one gemstone name",
  "lucky_metal": "one metal name",
  "name_meaning": "3-4 paragraphs about what the first name means, its cultural/historical origins, linguistic roots, famous people with this name, and what kind of energy this name carries. Be poetic and detailed.",
  "personality": "3-4 paragraphs describing this person's personality based on their name numerology and zodiac. Include strengths, weaknesses, how they behave in love, friendships, and work. Make it feel personal.",
  "astro_reading": "3-4 paragraphs of deep astrological reading - their planetary ruler, element, modality, birth chart energy, what their zodiac says about their soul, chakras, and cosmic purpose.",
  "future": "3-4 paragraphs of future predictions - career, love life, finances, health, major life events they can expect. Be optimistic yet realistic. Include specific time periods.",
  "star_message": "a beautiful, poetic, personalized message from the universe/stars addressed directly to this person. 2-3 paragraphs. Inspire them, acknowledge their struggles, give hope."
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = "".join(b.text for b in response.content if hasattr(b, "text"))
    clean = text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ── UI ────────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="cosmic-header">
    <div style="font-size:3.5rem; margin-bottom:0.4rem; filter: drop-shadow(0 0 25px rgba(255,220,100,0.7));">🔮</div>
    <div class="cosmic-title">Celestial Soul Reader</div>
    <div class="cosmic-subtitle">✦ Name Meaning · Astrology · Destiny · Lucky Charms ✦</div>
</div>
""", unsafe_allow_html=True)

# Input form
with st.container():
    st.markdown('<div class="cosmic-card">', unsafe_allow_html=True)

    name_input = st.text_input("✨ Your Full Name", placeholder="e.g. Priya Sharma")
    dob_input = st.date_input(
        "🗓 Date of Birth",
        value=date(1995, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today(),
    )

    reveal = st.button("✦ Reveal My Destiny ✦")
    st.markdown("</div>", unsafe_allow_html=True)

# Result
if reveal:
    if not name_input.strip():
        st.warning("Please enter your full name 🌙")
    else:
        with st.spinner("Reading the stars for you... ✨"):
            try:
                data = call_claude(name_input.strip(), dob_input)

                zodiac = get_zodiac(dob_input)
                dob_fmt = dob_input.strftime("%-d %B %Y")

                # ── Result header ─────────────────────────────────────────
                st.markdown(f"""
                <div class="cosmic-card" style="text-align:center; margin-top:1.5rem;">
                    <div class="result-name">{name_input.strip()}</div>
                    <span class="zodiac-pill">{zodiac} · Born {dob_fmt}</span>
                </div>
                """, unsafe_allow_html=True)

                # ── Lucky charms ──────────────────────────────────────────
                hex_col = colour_hex(data.get("lucky_colour", ""))
                st.markdown(f"""
                <div class="section-title">✨ Lucky Charms ✨</div>
                <div class="cosmic-card">
                  <div class="lucky-grid">
                    <div class="lucky-item">
                      <div class="lucky-label">Lucky Colour</div>
                      <div class="lucky-value">{data.get('lucky_colour','—')}</div>
                      <div class="colour-swatch" style="background:{hex_col};"></div>
                    </div>
                    <div class="lucky-item">
                      <div class="lucky-label">Lucky Number</div>
                      <div class="lucky-value">🔢 {data.get('lucky_number','—')}</div>
                    </div>
                    <div class="lucky-item">
                      <div class="lucky-label">Lucky Day</div>
                      <div class="lucky-value">📅 {data.get('lucky_day','—')}</div>
                    </div>
                    <div class="lucky-item">
                      <div class="lucky-label">Lucky Stone</div>
                      <div class="lucky-value">💎 {data.get('lucky_stone','—')}</div>
                    </div>
                    <div class="lucky-item">
                      <div class="lucky-label">Lucky Metal</div>
                      <div class="lucky-value">⚙️ {data.get('lucky_metal','—')}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Sections ──────────────────────────────────────────────
                sections = [
                    ("🌟 Name Meaning", "name_meaning"),
                    ("♈ Personality", "personality"),
                    ("💫 Astrological Reading", "astro_reading"),
                    ("🔮 Your Future", "future"),
                    ("💌 Message from the Stars", "star_message"),
                ]

                for title, key in sections:
                    content = data.get(key, "")
                    st.markdown(f"""
                    <div class="section-title">{title}</div>
                    <div class="cosmic-card">
                        <div class="reading-text">{content}</div>
                    </div>
                    """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("🌙 The cosmic signals got confused. Please try again!")
            except Exception as e:
                st.error(f"✦ The stars are misaligned right now. Error: {str(e)}")
