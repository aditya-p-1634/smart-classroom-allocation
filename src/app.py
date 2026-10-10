import os
import re
from datetime import date, datetime

import pandas as pd
import pdfplumber
import streamlit as st

st.set_page_config(page_title="Smart Room Booking", page_icon="SRB", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --ink: #16202a;
        --muted: #687586;
        --line: #dbe3ea;
        --surface: #ffffff;
        --surface-soft: #f7f9fc;
        --surface-tint: #edf7f4;
        --primary: #0f766e;
        --primary-dark: #115e59;
        --accent: #d97706;
        --danger: #b91c1c;
        --shadow: 0 18px 45px rgba(22, 32, 42, 0.08);
    }

    .stApp {
        color: var(--ink);
        background: linear-gradient(180deg, #f7f9fc 0%, #eef5f1 46%, #f9fafb 100%);
    }

    [data-testid="stHeader"] {
        background: rgba(247, 249, 252, 0.88);
        border-bottom: 1px solid rgba(219, 227, 234, 0.8);
        backdrop-filter: blur(12px);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        color: var(--ink) !important;
        letter-spacing: 0;
    }

    h1 {
        font-size: clamp(2.1rem, 5vw, 4.1rem) !important;
        line-height: 1.02 !important;
        margin-bottom: 0.65rem !important;
    }

    p, label, [data-testid="stMarkdownContainer"] {
        color: var(--ink);
    }

    [data-testid="stCaptionContainer"], small {
        color: var(--muted) !important;
    }

    .app-hero {
        display: grid;
        grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
        gap: 1rem;
        align-items: stretch;
        margin-bottom: 1.25rem;
    }

    .hero-copy,
    .summary-panel,
    .modern-card,
    .section-shell {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: var(--shadow);
    }

    .hero-copy {
        padding: clamp(1.25rem, 3vw, 2rem);
        background: linear-gradient(135deg, #ffffff 0%, #edf7f4 100%);
    }

    .hero-kicker {
        width: fit-content;
        margin-bottom: 1rem;
        padding: 0.35rem 0.65rem;
        border: 1px solid rgba(15, 118, 110, 0.22);
        border-radius: 999px;
        color: var(--primary-dark);
        background: rgba(15, 118, 110, 0.08);
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .hero-copy p {
        max-width: 54rem;
        margin: 0;
        color: #405164;
        font-size: 1.03rem;
        line-height: 1.7;
    }

    .summary-panel {
        padding: 1.25rem;
        background: #16202a;
        color: #f8fafc;
    }

    .summary-panel .label {
        color: #b7c6d6;
        font-size: 0.78rem;
        text-transform: uppercase;
        font-weight: 700;
    }

    .summary-panel .value {
        margin-top: 0.35rem;
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
    }

    .summary-panel .hint {
        margin-top: 0.7rem;
        color: #c9d6e2;
        line-height: 1.55;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.75rem 0 1.25rem;
    }

    .modern-card {
        padding: 1rem;
    }

    .modern-card .metric-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .modern-card .metric-value {
        margin-top: 0.45rem;
        color: var(--ink);
        font-size: 1.75rem;
        font-weight: 800;
    }

    .modern-card .metric-note {
        margin-top: 0.3rem;
        color: var(--muted);
        font-size: 0.9rem;
    }

    .account-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.7rem;
        align-items: center;
        justify-content: space-between;
        padding: 1rem;
        margin: 0.65rem 0 1.25rem;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #ffffff;
        box-shadow: var(--shadow);
    }

    .account-title {
        color: var(--ink);
        font-size: 1.15rem;
        font-weight: 800;
    }

    .account-meta {
        color: var(--muted);
        font-size: 0.94rem;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    .pill {
        padding: 0.4rem 0.65rem;
        border-radius: 999px;
        border: 1px solid rgba(15, 118, 110, 0.2);
        color: var(--primary-dark);
        background: rgba(15, 118, 110, 0.08);
        font-size: 0.86rem;
        font-weight: 700;
    }

    .section-shell {
        padding: 1.1rem;
    }

    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stForm"],
    [data-testid="stExpander"],
    [data-testid="stDataFrame"],
    [data-testid="stAlert"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #ffffff;
        box-shadow: var(--shadow);
    }

    [data-testid="stForm"] {
        padding: 1rem 1.1rem;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        color: var(--ink);
        background-color: #ffffff;
        border-color: #cfd9e3;
        border-radius: 8px;
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.12);
    }

    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="menu"] {
        color: var(--ink);
        background: #ffffff;
        border: 1px solid var(--line);
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgba(15, 118, 110, 0.08);
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] > button {
        color: #ffffff;
        font-weight: 700;
        border: 1px solid var(--primary);
        border-radius: 8px;
        background: var(--primary);
        box-shadow: 0 10px 24px rgba(15, 118, 110, 0.18);
        transition: transform 140ms ease, box-shadow 140ms ease, filter 140ms ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        color: #ffffff;
        border-color: var(--primary-dark);
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 14px 32px rgba(15, 118, 110, 0.24);
    }

    [data-testid="stDataFrame"] {
        overflow: hidden;
    }

    [data-testid="stDataFrame"] [role="grid"] {
        background: #ffffff;
    }

    [data-testid="stMetric"] {
        padding: 1rem;
        border: 1px solid var(--line);
        border-radius: 8px;
        background: #ffffff;
    }

    [data-testid="stAlert"] {
        color: var(--ink);
    }

    hr {
        border-color: var(--line);
    }

    a {
        color: var(--primary) !important;
    }

    div[data-testid="stInfo"] {
        background: #eff6ff;
    }

    div[data-testid="stWarning"] {
        background: #fffbeb;
    }

    @media (max-width: 900px) {
        .app-hero,
        .metric-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 700px) {
        .block-container {
            padding: 1.5rem 1rem 2rem;
        }

        [data-testid="stForm"] {
            padding: 1rem;
        }
    }

    :root {
        --ink: #e6f1ff;
        --muted: #91a5bd;
        --line: rgba(105, 153, 204, 0.2);
        --surface: #0c1524;
        --surface-soft: #111e30;
        --surface-tint: #10243a;
        --primary: #38bdf8;
        --primary-dark: #1683c2;
        --accent: #f0b85b;
        --danger: #fb7185;
        --shadow: 0 20px 56px rgba(0, 0, 0, 0.3);
    }

    .stApp {
        color: var(--ink);
        background:
            radial-gradient(ellipse at 8% 0%, rgba(14, 116, 195, 0.2), transparent 36%),
            radial-gradient(ellipse at 100% 12%, rgba(37, 99, 235, 0.13), transparent 34%),
            #070b14;
    }

    [data-testid="stHeader"] {
        background: rgba(7, 11, 20, 0.78);
        border-bottom-color: rgba(105, 153, 204, 0.12);
        backdrop-filter: blur(14px);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c1422 0%, #090f1b 100%);
        border-right-color: rgba(56, 189, 248, 0.18);
    }

    h1, h2, h3, p, label, [data-testid="stMarkdownContainer"],
    [data-testid="stWidgetLabel"] p {
        color: var(--ink) !important;
    }

    h1 {
        text-shadow: 0 0 28px rgba(56, 189, 248, 0.27);
    }

    [data-testid="stCaptionContainer"], small,
    .account-meta, .modern-card .metric-note,
    .modern-card .metric-label {
        color: var(--muted) !important;
    }

    .hero-copy, .modern-card, .section-shell, .account-strip,
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stForm"], [data-testid="stExpander"],
    [data-testid="stDataFrame"], [data-testid="stAlert"],
    [data-testid="stMetric"] {
        color: var(--ink);
        border-color: var(--line);
        background: rgba(12, 21, 36, 0.9);
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
    }

    .hero-copy {
        background: linear-gradient(145deg, rgba(15, 29, 48, 0.97), rgba(12, 21, 36, 0.91));
    }

    .hero-copy p {
        color: #b5c7dc !important;
    }

    .hero-kicker, .pill {
        color: #7dd3fc;
        border-color: rgba(56, 189, 248, 0.27);
        background: rgba(56, 189, 248, 0.09);
    }

    .summary-panel {
        border-color: rgba(56, 189, 248, 0.3);
        background: linear-gradient(145deg, #10243a, #0c1728);
        box-shadow: 0 0 34px rgba(56, 189, 248, 0.1), var(--shadow);
    }

    .summary-panel .label, .summary-panel .hint {
        color: #a9c1d8;
    }

    .summary-panel .value, .modern-card .metric-value, .account-title {
        color: #f1f7ff;
    }

    [data-testid="stForm"] {
        background: rgba(12, 21, 36, 0.8);
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stDateInput"] input,
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        color: var(--ink);
        background-color: #0b1626;
        border-color: rgba(125, 170, 220, 0.24);
    }

    [data-testid="stTextInput"] input:focus,
    [data-testid="stNumberInput"] input:focus,
    [data-testid="stDateInput"] input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 1px var(--primary), 0 0 18px rgba(56, 189, 248, 0.22);
    }

    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="menu"] {
        color: var(--ink);
        background: #101b2c;
        border-color: var(--line);
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgba(56, 189, 248, 0.14);
    }

    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        color: #03111d;
        border-color: rgba(125, 211, 252, 0.8);
        background: linear-gradient(115deg, #38bdf8, #60a5fa);
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.2);
        transition: transform 260ms cubic-bezier(0.2, 0.75, 0.25, 1),
                    box-shadow 260ms ease, filter 260ms ease;
    }

    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        color: #03111d;
        border-color: #bae6fd;
        background: linear-gradient(115deg, #7dd3fc, #93c5fd);
        transform: translateX(4px);
        box-shadow: 0 0 24px rgba(56, 189, 248, 0.4);
    }

    @keyframes slide-in-content {
        from {
            opacity: 0.65;
            transform: translateX(22px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .block-container {
        animation: slide-in-content 360ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    [data-testid="stSelectbox"] > div,
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {
        transition: border-color 220ms ease, background-color 220ms ease,
                    box-shadow 220ms ease, color 220ms ease;
    }

    [data-testid="stSelectbox"] > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 1px var(--primary), 0 0 16px rgba(56, 189, 248, 0.18);
    }

    @keyframes dropdown-slide-in {
        from {
            opacity: 0;
            transform: translateY(-9px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="menu"] {
        transform-origin: top center;
        animation: dropdown-slide-in 190ms cubic-bezier(0.2, 0.75, 0.25, 1) both;
    }

    @media (prefers-reduced-motion: reduce) {
        .block-container,
        [data-baseweb="popover"] [role="listbox"],
        [data-baseweb="menu"] {
            animation: none;
        }

        .stButton > button,
        [data-testid="stFormSubmitButton"] > button,
        [data-testid="stSelectbox"] > div,
        [data-testid="stRadio"] label,
        [data-testid="stCheckbox"] label {
            transition: none;
        }
    }

    [data-testid="stDataFrame"] [role="grid"] {
        background: #0b1422;
    }

    div[data-testid="stInfo"] {
        background: rgba(14, 116, 195, 0.13);
    }

    div[data-testid="stWarning"] {
        background: rgba(180, 100, 20, 0.14);
    }

    hr {
        border-color: var(--line);
    }

    a {
        color: #7dd3fc !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
TIMETABLE_DIR = os.path.join(DATA_DIR, "timetables")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.csv")
BLOCKED_USERS_FILE = os.path.join(DATA_DIR, "blocked_users.csv")
os.makedirs(DATA_DIR, exist_ok=True)

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIME_SLOTS = [
    "8:30 AM",
    "9:20 AM",
    "10:30 AM",
    "11:20 AM",
    "1:40 PM",
    "2:30 PM",
    "3:30 PM",
    "4:20 PM",
]
PERIOD_END_TIMES = [
    "9:20 AM",
    "10:10 AM",
    "11:20 AM",
    "12:10 PM",
    "2:30 PM",
    "3:20 PM",
    "4:20 PM",
    "5:10 PM",
]
LEGACY_TIME_SLOTS = ["08:30", "09:20", "10:30", "11:20", "13:40", "14:30", "15:30", "16:20"]
PERIOD_LABELS = [f"P{i}" for i in range(1, 9)]
DAY_ABBREVIATIONS = {
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
}

STUDENTS = [
    {"roll_number": "21CS001", "name": "Aarav Sharma", "password": "1234", "subjects": ["CS101", "CS102", "CS104"]},
    {"roll_number": "21CS015", "name": "Meera Nair", "password": "1234", "subjects": ["CS101", "CS201", "CS205"]},
    {"roll_number": "21CS032", "name": "Rahul Verma", "password": "1234", "subjects": ["CS102", "CS203", "CS204"]},
]

ADMINS = [
    {"admin_id": "ADM001", "name": "Admin One", "password": "admin123"},
    {"admin_id": "ADM002", "name": "Admin Two", "password": "admin123"},
]

COURSE_CODES = {
    "CS101": "Data Structures",
    "CS102": "Operating Systems",
    "CS104": "Discrete Mathematics",
    "CS201": "DBMS",
    "CS203": "Computer Networks",
    "CS204": "Software Engineering",
    "CS205": "Algorithms",
    "CS301": "Machine Learning",
    "CS302": "Big Data",
}

CLASSROOMS = [
    {"room_id": "M201", "type": "Classroom", "capacity": 60, "projector": True, "building": "M"},
    {"room_id": "M202", "type": "Classroom", "capacity": 60, "projector": True, "building": "M"},
    {"room_id": "M501", "type": "Classroom", "capacity": 40, "projector": True, "building": "M"},
    {"room_id": "M502", "type": "Classroom", "capacity": 40, "projector": True, "building": "M"},
    {"room_id": "M505", "type": "Classroom", "capacity": 40, "projector": True, "building": "M"},
    {"room_id": "M506", "type": "Classroom", "capacity": 40, "projector": True, "building": "M"},
    {"room_id": "M507", "type": "Classroom", "capacity": 60, "projector": True, "building": "M"},
    {"room_id": "J501", "type": "Classroom", "capacity": 40, "projector": True, "building": "J"},
    {"room_id": "J502", "type": "Classroom", "capacity": 40, "projector": True, "building": "J"},
    {"room_id": "J514", "type": "Classroom", "capacity": 80, "projector": True, "building": "J"},
    {"room_id": "J517", "type": "Classroom", "capacity": 60, "projector": False, "building": "J"},
    {"room_id": "J518", "type": "Classroom", "capacity": 60, "projector": False, "building": "J"},
    {"room_id": "K503", "type": "Classroom", "capacity": 80, "projector": False, "building": "K"},
    {"room_id": "K504", "type": "Classroom", "capacity": 60, "projector": False, "building": "K"},
    {"room_id": "K505", "type": "Classroom", "capacity": 40, "projector": False, "building": "K"},
    {"room_id": "A105", "type": "Classroom", "capacity": 60, "projector": True, "building": "A"},
    {"room_id": "A106", "type": "Classroom", "capacity": 60, "projector": True, "building": "A"},
    {"room_id": "A108", "type": "Classroom", "capacity": 60, "projector": True, "building": "A"},
    {"room_id": "A109", "type": "Classroom", "capacity": 80, "projector": True, "building": "A"},
    {"room_id": "A110", "type": "Classroom", "capacity": 60, "projector": True, "building": "A"},
    {"room_id": "A111", "type": "Classroom", "capacity": 80, "projector": True, "building": "A"},
    {"room_id": "A112", "type": "Classroom", "capacity": 60, "projector": False, "building": "A"},
]

LABS = [
    {"room_id": "M601", "type": "Lab", "capacity": 100, "projector": True, "building": "M"},
    {"room_id": "M701", "type": "Lab", "capacity": 100, "projector": True, "building": "M"},
    {"room_id": "M801", "type": "Lab", "capacity": 100, "projector": True, "building": "M"},
    {"room_id": "J601", "type": "Lab", "capacity": 100, "projector": True, "building": "J"},
    {"room_id": "J701", "type": "Lab", "capacity": 100, "projector": True, "building": "J"},
    {"room_id": "J801", "type": "Lab", "capacity": 100, "projector": True, "building": "J"},
    {"room_id": "K601", "type": "Lab", "capacity": 100, "projector": True, "building": "K"},
    {"room_id": "K701", "type": "Lab", "capacity": 100, "projector": True, "building": "K"},
    {"room_id": "K801", "type": "Lab", "capacity": 100, "projector": True, "building": "K"},
    {"room_id": "A601", "type": "Lab", "capacity": 100, "projector": True, "building": "A"},
    {"room_id": "A701", "type": "Lab", "capacity": 100, "projector": True, "building": "A"},
    {"room_id": "A801", "type": "Lab", "capacity": 100, "projector": True, "building": "A"},
]

HALLS = [
    {
        "room_id": room_id,
        "type": "Hall",
        "capacity": capacity,
        "projector": True,
        "building": room_id.rstrip("0123456789"),
    }
    for room_id, capacity in [
        ("A150", 150), ("B200", 200), ("C250", 250),
        ("D150", 150), ("E200", 200), ("F250", 250),
        ("G150", 150), ("H200", 200), ("I250", 250),
        ("J150", 150), ("K200", 200), ("L250", 250),
        ("M150", 150), ("N200", 200), ("O250", 250),
        ("P150", 150), ("Q200", 200), ("R250", 250),
        ("S150", 150), ("T200", 200), ("U250", 250),
        ("V150", 150), ("W200", 200), ("X250", 250),
        ("Y150", 150), ("Z200", 200), ("AA250", 250),
        ("AB150", 150), ("AC200", 200), ("AD250", 250),
    ]
]

ROOM_OPTIONS = {"Classroom": CLASSROOMS, "Lab": LABS, "Hall": HALLS}


@st.cache_data
def load_timetable_data():
    timetable_events = []
    daily_schedule = []
    lab_room_ids = set()

    for semester in ("Odd", "Even"):
        pdf_path = os.path.join(
            TIMETABLE_DIR, f"{semester}_Semester_Timetables_With_Rooms.pdf"
        )
        if not os.path.isfile(pdf_path):
            raise FileNotFoundError(f"Required timetable PDF not found: {pdf_path}")

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                program = text.splitlines()[0] if text.splitlines() else "Program not identified"
                lab_match = re.search(r"Lab room:\s*([A-Z]\d{3})", text)
                if lab_match:
                    lab_room_ids.add(lab_match.group(1))

                words = page.extract_words()
                period_centers = {
                    int(word["text"][1:]): (word["x0"] + word["x1"]) / 2
                    for word in words
                    if re.fullmatch(r"P[1-8]", word["text"])
                }
                day_rows = [
                    (
                        DAY_ABBREVIATIONS[word["text"]],
                        (word["top"] + word["bottom"]) / 2,
                    )
                    for word in words
                    if word["text"] in DAY_ABBREVIATIONS
                ]
                if len(period_centers) != 8 or not day_rows:
                    continue

                period_pair_centers = [
                    ((period_centers[first] + period_centers[first + 1]) / 2, first)
                    for first in range(1, 8)
                ]
                period_width = period_centers[2] - period_centers[1]
                for word in words:
                    room_match = re.fullmatch(r"([A-Z]\d{3})\*?", word["text"])
                    if not room_match:
                        continue

                    word_y = (word["top"] + word["bottom"]) / 2
                    day, day_y = min(day_rows, key=lambda row: abs(row[1] - word_y))
                    if abs(day_y - word_y) > 38:
                        continue

                    room_x = (word["x0"] + word["x1"]) / 2
                    nearest_period = min(
                        period_centers,
                        key=lambda period: abs(period_centers[period] - room_x),
                    )
                    nearest_period_distance = abs(period_centers[nearest_period] - room_x)
                    pair_center, first_period = min(
                        period_pair_centers,
                        key=lambda pair: abs(pair[0] - room_x),
                    )
                    if (
                        abs(pair_center - room_x) < 14
                        and abs(pair_center - room_x) < nearest_period_distance
                    ):
                        occupied_periods = (first_period, first_period + 1)
                    else:
                        occupied_periods = (nearest_period,)

                    first_occupied = occupied_periods[0]
                    last_occupied = occupied_periods[-1]
                    cell_left = period_centers[first_occupied] - period_width / 2
                    cell_right = period_centers[last_occupied] + period_width / 2
                    subject_words = [
                        cell_word
                        for cell_word in words
                        if cell_left
                        <= (cell_word["x0"] + cell_word["x1"]) / 2
                        <= cell_right
                        and abs(
                            (cell_word["top"] + cell_word["bottom"]) / 2 - day_y
                        ) <= 30
                        and not re.fullmatch(r"[A-Z]\d{3}\*?", cell_word["text"])
                        and cell_word["text"] not in DAY_ABBREVIATIONS
                    ]
                    subject = " ".join(
                        cell_word["text"]
                        for cell_word in sorted(
                            subject_words,
                            key=lambda item: (item["top"], item["x0"]),
                        )
                    ).strip()
                    daily_schedule.append(
                        {
                            "semester": semester,
                            "program": program,
                            "day": day,
                            "period_start": first_occupied,
                            "period_end": last_occupied,
                            "subject": subject,
                            "room_id": room_match.group(1),
                        }
                    )

                    for period in occupied_periods:
                        timetable_events.append(
                            {
                                "semester": semester,
                                "day": day,
                                "period": period,
                                "room_id": room_match.group(1),
                            }
                        )

    if not timetable_events:
        raise ValueError("No class room assignments could be read from the timetable PDFs.")
    return timetable_events, sorted(lab_room_ids), daily_schedule


TIMETABLE_EVENTS, TIMETABLE_LAB_IDS, TIMETABLE_SCHEDULE = load_timetable_data()


def ensure_bookings_file():
    if not os.path.exists(BOOKINGS_FILE):
        pd.DataFrame(
            columns=[
                "booking_id",
                "user_type",
                "user_id",
                "course_code",
                "semester",
                "resource_type",
                "resource_id",
                "booking_date",
                "start_time",
                "periods",
                "status",
                "booking_timestamp",
                "created_by",
            ]
        ).to_csv(BOOKINGS_FILE, index=False)


ensure_bookings_file()


def ensure_blocked_users_file():
    if not os.path.exists(BLOCKED_USERS_FILE):
        pd.DataFrame(
            columns=[
                "user_id",
                "blocked",
                "reason",
                "updated_by",
                "updated_at",
            ]
        ).to_csv(BLOCKED_USERS_FILE, index=False)


ensure_blocked_users_file()


def load_user_access():
    df = pd.read_csv(BLOCKED_USERS_FILE, dtype={"user_id": str})
    if df.empty:
        return {}
    return {
        str(row["user_id"]): {
            "blocked": str(row["blocked"]).strip().lower() in {"true", "1", "yes"},
            "reason": "" if pd.isna(row["reason"]) else str(row["reason"]),
            "updated_by": "" if pd.isna(row["updated_by"]) else str(row["updated_by"]),
            "updated_at": "" if pd.isna(row["updated_at"]) else str(row["updated_at"]),
        }
        for _, row in df.iterrows()
    }


def save_user_access(access_records):
    rows = [
        {
            "user_id": user_id,
            "blocked": details["blocked"],
            "reason": details["reason"],
            "updated_by": details["updated_by"],
            "updated_at": details["updated_at"],
        }
        for user_id, details in sorted(access_records.items())
    ]
    pd.DataFrame(
        rows,
        columns=["user_id", "blocked", "reason", "updated_by", "updated_at"],
    ).to_csv(BLOCKED_USERS_FILE, index=False)


def is_student_blocked(roll_number):
    record = load_user_access().get(roll_number)
    return bool(record and record["blocked"])


def set_student_blocked(roll_number, blocked, admin_id, reason=""):
    if not any(student["roll_number"] == roll_number for student in STUDENTS):
        raise ValueError(f"Unknown student roll number: {roll_number}")

    access_records = load_user_access()
    access_records[roll_number] = {
        "blocked": blocked,
        "reason": reason.strip() if blocked else "",
        "updated_by": admin_id,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
    }
    save_user_access(access_records)


def load_bookings():
    df = pd.read_csv(BOOKINGS_FILE)
    if df.empty:
        return []
    return df.to_dict("records")


def save_bookings(bookings):
    pd.DataFrame(bookings).to_csv(BOOKINGS_FILE, index=False)


def room_choices(resource_type):
    ids = {room["room_id"] for room in ROOM_OPTIONS[resource_type]}
    if resource_type == "Lab":
        ids.update(TIMETABLE_LAB_IDS)
    elif resource_type == "Classroom":
        scheduled_rooms = {event["room_id"] for event in TIMETABLE_EVENTS}
        ids.update(scheduled_rooms - set(TIMETABLE_LAB_IDS))
    return sorted(ids)


def room_catalog():
    catalog = {
        room["room_id"]: dict(room)
        for rooms in ROOM_OPTIONS.values()
        for room in rooms
    }
    for room_id in {event["room_id"] for event in TIMETABLE_EVENTS}:
        if room_id not in catalog:
            catalog[room_id] = {
                "room_id": room_id,
                "type": "Lab" if room_id in TIMETABLE_LAB_IDS else "Classroom",
                "capacity": None,
                "projector": None,
                "building": room_id[0],
            }
    for room_id in TIMETABLE_LAB_IDS:
        if room_id not in catalog:
            catalog[room_id] = {
                "room_id": room_id,
                "type": "Lab",
                "capacity": None,
                "projector": None,
                "building": room_id[0],
            }
    return sorted(catalog.values(), key=lambda room: room["room_id"])


def is_room_conflict(resource_id, booking_date, start_time, periods, semester, bookings=None):
    day = DAYS[booking_date.weekday()] if booking_date.weekday() < len(DAYS) else None
    start_period = time_slot_index(start_time) + 1
    requested_periods = set(range(start_period, start_period + int(periods)))
    if day:
        for event in TIMETABLE_EVENTS:
            if (
                event["semester"] == semester
                and event["day"] == day
                and event["room_id"] == resource_id
                and event["period"] in requested_periods
            ):
                return True, {
                    "source": "timetable",
                    "resource_id": resource_id,
                    "booking_date": str(booking_date),
                    "start_time": TIME_SLOTS[event["period"] - 1],
                }

    if bookings is None:
        bookings = load_bookings()
    for booking in bookings:
        if booking.get("resource_id") != resource_id:
            continue
        if booking.get("booking_date") != str(booking_date):
            continue
        other_start_period = time_slot_index(booking["start_time"]) + 1
        other_periods = set(
            range(other_start_period, other_start_period + int(booking["periods"]))
        )
        if requested_periods.intersection(other_periods):
            booking["source"] = "booking"
            return True, booking
    return False, None


def time_slot_index(value):
    value = str(value).strip()
    if value in TIME_SLOTS:
        return TIME_SLOTS.index(value)
    if value in LEGACY_TIME_SLOTS:
        return LEGACY_TIME_SLOTS.index(value)
    raise ValueError(f"Unsupported booking time: {value}")


def booking_history_frame(bookings):
    history = pd.DataFrame(bookings)
    if not history.empty and "start_time" in history:
        start_indices = history["start_time"].map(time_slot_index)
        history["time"] = [
            f"{TIME_SLOTS[start]} - {PERIOD_END_TIMES[min(start + int(periods) - 1, 7)]}"
            for start, periods in zip(start_indices, history["periods"])
        ]
        history["day"] = pd.to_datetime(history["booking_date"]).dt.day_name()
        history["course"] = history["course_code"].map(COURSE_CODES).fillna(history["course_code"])
        history = history.drop(columns=["start_time"])
    return history


def get_daily_timetable(semester, selected_date, program=None):
    day = DAYS[selected_date.weekday()] if selected_date.weekday() < len(DAYS) else None
    if day is None:
        return []

    return [
        event
        for event in TIMETABLE_SCHEDULE
        if event["semester"] == semester
        and event["day"] == day
        and (program is None or event["program"] == program)
    ]


def get_room_availability(semester, booking_date, start_time, periods, resource_type, capacity, requires_projector):
    records = []
    bookings = load_bookings()
    for room in room_catalog():
        if resource_type != "All" and room["type"] != resource_type:
            continue

        conflict, conflict_details = is_room_conflict(
            room["room_id"],
            booking_date,
            start_time,
            periods,
            semester,
            bookings=bookings,
        )
        reasons = []
        capacity_known = room["capacity"] is not None
        projector_known = room["projector"] is not None
        if not capacity_known:
            reasons.append("Capacity not listed")
        elif room["capacity"] < capacity:
            reasons.append("Too small")
        if requires_projector:
            if not projector_known:
                reasons.append("Projector details not listed")
            elif not room["projector"]:
                reasons.append("No projector")

        requirements_met = not reasons
        records.append(
            {
                "Room": room["room_id"],
                "Type": room["type"],
                "Capacity": room["capacity"] if capacity_known else "Not listed",
                "Projector": (
                    "Yes" if room["projector"] is True
                    else "No" if room["projector"] is False
                    else "Not listed"
                ),
                "Building": room["building"],
                "Availability": "Occupied" if conflict else "Available",
                "Requirements": "Meets" if requirements_met else "; ".join(reasons),
                "_eligible": not conflict and requirements_met,
                "_conflict": conflict_details,
            }
        )
    return records


def render_booking_panel(user_type, user_id, course_code, key_prefix):
    st.markdown("### Find a room")
    with st.form(f"{key_prefix}_availability_form"):
        semester = st.selectbox("Semester timetable", ["Odd", "Even"], key=f"{key_prefix}_semester")
        resource_type = st.selectbox(
            "Room type",
            ["All", "Classroom", "Lab", "Hall"],
            index=1,
            key=f"{key_prefix}_type",
        )
        booking_date = st.date_input("Date", key=f"{key_prefix}_date")
        start_time = st.selectbox("Start time", TIME_SLOTS, key=f"{key_prefix}_time")
        periods = st.number_input(
            "Number of periods",
            min_value=1,
            max_value=len(TIME_SLOTS) - time_slot_index(start_time),
            value=1,
            key=f"{key_prefix}_periods",
        )
        capacity = st.number_input(
            "Minimum capacity needed",
            min_value=1,
            max_value=300,
            value=40,
            step=5,
            key=f"{key_prefix}_capacity",
        )
        requires_projector = st.checkbox("Projector required", key=f"{key_prefix}_projector")
        find_rooms = st.form_submit_button("Show all room availability")

    query_key = f"{key_prefix}_availability_query"
    if find_rooms:
        st.session_state[query_key] = {
            "semester": semester,
            "resource_type": resource_type,
            "booking_date": booking_date,
            "start_time": start_time,
            "periods": int(periods),
            "capacity": int(capacity),
            "requires_projector": requires_projector,
        }

    query = st.session_state.get(query_key)
    if not query:
        return

    records = get_room_availability(
        semester=query["semester"],
        booking_date=query["booking_date"],
        start_time=query["start_time"],
        periods=query["periods"],
        resource_type=query["resource_type"],
        capacity=query["capacity"],
        requires_projector=query["requires_projector"],
    )
    eligible_records = [record for record in records if record["_eligible"]]
    eligible_rooms = [record["Room"] for record in eligible_records]
    if not eligible_rooms:
        st.warning("No available rooms meet these requirements. Adjust the time or room requirements and check again.")
        return

    display_records = [
        {key: value for key, value in record.items() if not key.startswith("_")}
        for record in eligible_records
    ]
    st.caption(f"Showing {len(display_records)} available room(s) that meet the requested features.")
    st.dataframe(pd.DataFrame(display_records), use_container_width=True, hide_index=True)

    selected_room = st.selectbox(
        "Choose an available matching room",
        eligible_rooms,
        key=f"{key_prefix}_selected_room",
    )
    if st.button("Confirm Booking", key=f"{key_prefix}_confirm_booking"):
        conflict, _ = is_room_conflict(
            selected_room,
            query["booking_date"],
            query["start_time"],
            query["periods"],
            query["semester"],
        )
        if conflict:
            st.error("Conflict Error: This room became occupied. Refresh availability and choose another room.")
            return

        room_details = next(room for room in room_catalog() if room["room_id"] == selected_room)
        booking_entry = {
            "booking_id": f"BK-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "user_type": user_type,
            "user_id": user_id,
            "course_code": course_code,
            "semester": query["semester"],
            "resource_type": room_details["type"],
            "resource_id": selected_room,
            "booking_date": str(query["booking_date"]),
            "start_time": query["start_time"],
            "periods": query["periods"],
            "status": "Confirmed",
            "booking_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "created_by": user_id,
        }
        bookings = load_bookings()
        bookings.append(booking_entry)
        save_bookings(bookings)
        st.session_state.pop(query_key, None)
        st.success(f"Booking confirmed: {selected_room} on {query['booking_date']} at {query['start_time']}.")
        st.rerun()


def get_student_by_roll(roll_number):
    for student in STUDENTS:
        if student["roll_number"].lower() == roll_number.lower():
            return student
    return None


def get_admin_by_id(admin_id):
    for admin in ADMINS:
        if admin["admin_id"].lower() == admin_id.lower():
            return admin
    return None


def get_student_subjects(roll_number):
    student = get_student_by_roll(roll_number)
    return student["subjects"] if student else []


def get_booking_history(user_type, user_id):
    bookings = load_bookings()
    return [b for b in bookings if b.get("user_type") == user_type and b.get("user_id") == user_id]


def get_admin_history(course_code=None, resource_id=None, date_from=None, date_to=None):
    bookings = load_bookings()
    filtered = []
    for booking in bookings:
        if course_code and booking.get("course_code") != course_code:
            continue
        if resource_id and booking.get("resource_id") != resource_id:
            continue
        if date_from and pd.to_datetime(booking["booking_date"]) < pd.to_datetime(date_from):
            continue
        if date_to and pd.to_datetime(booking["booking_date"]) > pd.to_datetime(date_to):
            continue
        filtered.append(booking)
    return filtered


st.title("Smart Room Booking")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if (
    st.session_state.logged_in
    and st.session_state.role == "Student"
    and is_student_blocked(st.session_state.user_id)
):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.user_id = ""
    st.session_state["access_revoked"] = True


with st.sidebar:
    if st.session_state.logged_in and st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.user_id = ""
        st.rerun()

if not st.session_state.logged_in:
    if st.session_state.pop("access_revoked", False):
        st.error("Your account access has been blocked by an administrator.")

    left, login_column, right = st.columns([1, 0.9, 1])
    with login_column:
        with st.container(border=True):
            st.subheader("Sign in to continue")
            with st.form("login_form"):
                selected_role = st.selectbox("Login as", ["Student", "Admin"])
                login_id = st.text_input("Roll Number" if selected_role == "Student" else "Admin ID")
                password = st.text_input("Password", type="password")
                login_submitted = st.form_submit_button("Login", use_container_width=True)

    if login_submitted:
        if selected_role == "Student":
            account = get_student_by_roll(login_id)
            if account and account["password"] == password:
                if is_student_blocked(account["roll_number"]):
                    st.error("This student account has been blocked. Contact an administrator.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.role = "Student"
                    st.session_state.user_id = account["roll_number"]
                    st.rerun()
            else:
                st.error("Invalid student credentials.")
        else:
            account = get_admin_by_id(login_id)
            if account and account["password"] == password:
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
                st.session_state.user_id = account["admin_id"]
                st.rerun()
            else:
                st.error("Invalid admin credentials.")

else:
    if st.session_state.role == "Student":
        student = get_student_by_roll(st.session_state.user_id)
        history = get_booking_history("Student", student["roll_number"])
        st.subheader(f"{student['name']} · {student['roll_number']}")

        booking_tab, timetable_tab, history_tab = st.tabs(
            ["Book space", "Today's timetable", "Booking history"]
        )
        with booking_tab:
            render_booking_panel(
                user_type="Student",
                user_id=student["roll_number"],
                course_code="General",
                key_prefix="student",
            )

        with timetable_tab:
            today = date.today()
            st.subheader(f"Today's timetable · {today.strftime('%A, %d %B %Y')}")
            st.caption(
                "The date is taken from this computer's local system clock. "
                "Select the semester timetable and program to view."
            )
            semester = st.selectbox(
                "Semester timetable",
                ["Odd", "Even"],
                key="student_timetable_semester",
            )
            programs = sorted(
                {
                    event["program"]
                    for event in TIMETABLE_SCHEDULE
                    if event["semester"] == semester
                }
            )
            selected_program = st.selectbox(
                "Program",
                ["Select a program"] + programs,
                key=f"student_timetable_program_{semester.lower()}",
            )
            day_schedule = get_daily_timetable(
                semester,
                today,
                program=None if selected_program == "Select a program" else selected_program,
            )
            if today.weekday() >= len(DAYS):
                st.info("The provided timetable PDFs do not include weekend classes.")
            elif selected_program == "Select a program":
                st.info("Select your program to view its timetable.")
            elif not day_schedule:
                st.info("No scheduled classes were found for this day and selection.")
            else:
                timetable_rows = []
                for event in day_schedule:
                    first_period = event["period_start"]
                    last_period = event["period_end"]
                    period_label = (
                        f"P{first_period}"
                        if first_period == last_period
                        else f"P{first_period}-P{last_period}"
                    )
                    timetable_rows.append(
                        {
                            "Program": event["program"],
                            "_period_start": first_period,
                            "Period": period_label,
                            "Time": (
                                f"{TIME_SLOTS[first_period - 1]} - "
                                f"{PERIOD_END_TIMES[last_period - 1]}"
                            ),
                            "Class": event["subject"] or "Activity not identified",
                            "Room": event["room_id"],
                        }
                    )
                timetable_frame = pd.DataFrame(timetable_rows).sort_values(
                    ["_period_start", "Program"]
                ).drop(columns=["_period_start"])
                st.dataframe(
                    timetable_frame,
                    use_container_width=True,
                    hide_index=True,
                )
                st.caption(
                    "The timetable PDFs contain schedules for multiple programs "
                    "and are not linked to individual student accounts."
                )

        with history_tab:
            st.markdown("### Booking History")
            if history:
                st.dataframe(
                    booking_history_frame(history),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No bookings yet.")

    elif st.session_state.role == "Admin":
        admin = get_admin_by_id(st.session_state.user_id)
        st.subheader(f"{admin['name']} · {admin['admin_id']}")

        booking_tab, history_tab, access_tab = st.tabs(
            ["Book space", "Booking history", "Manage student access"]
        )
        with booking_tab:
            course_code = st.selectbox("Course Code", list(COURSE_CODES.keys()))
            render_booking_panel(
                user_type="Admin",
                user_id=admin["admin_id"],
                course_code=course_code,
                key_prefix="admin",
            )

        with history_tab:
            st.subheader("All Booking History")
            with st.expander("Filter bookings", expanded=False):
                colA, colB = st.columns(2)
                with colA:
                    filter_course = st.selectbox(
                        "Course",
                        ["All"] + list(COURSE_CODES.keys()) + ["General"],
                    )
                    filter_room = st.selectbox(
                        "Room",
                        ["All"] + [room["room_id"] for room in room_catalog()],
                    )
                with colB:
                    filter_by_date = st.checkbox("Filter by date range")
                    if filter_by_date:
                        filter_date_from = st.date_input("From date")
                        filter_date_to = st.date_input("To date")
                    else:
                        filter_date_from = None
                        filter_date_to = None

            if filter_by_date and filter_date_from > filter_date_to:
                st.error("The start date must be on or before the end date.")
                admin_history = []
            else:
                admin_history = get_admin_history(
                    course_code=None if filter_course == "All" else filter_course,
                    resource_id=None if filter_room == "All" else filter_room,
                    date_from=filter_date_from,
                    date_to=filter_date_to,
                )

            if admin_history:
                st.dataframe(booking_history_frame(admin_history), use_container_width=True, hide_index=True)
            else:
                st.info("No bookings match the selected filters.")

        with access_tab:
            st.subheader("Manage Student Access")
            st.caption("Blocked students cannot sign in. Active student sessions are ended on their next interaction.")
            access_records = load_user_access()
            with st.form("manage_student_access_form"):
                target_student = st.selectbox(
                    "Student account",
                    [student["roll_number"] for student in STUDENTS],
                    format_func=lambda roll: (
                        f"{get_student_by_roll(roll)['name']} · {roll}"
                    ),
                )
                action = st.selectbox("Action", ["Block access", "Unblock access"])
                block_reason = st.text_input(
                    "Reason (optional)",
                    disabled=action == "Unblock access",
                )
                update_access = st.form_submit_button("Update access")

            if update_access:
                should_block = action == "Block access"
                set_student_blocked(
                    roll_number=target_student,
                    blocked=should_block,
                    admin_id=admin["admin_id"],
                    reason=block_reason,
                )
                st.success(
                    f"{target_student} access "
                    f"{'blocked' if should_block else 'unblocked'}."
                )
                st.rerun()

            access_records = load_user_access()
            access_rows = []
            for student in STUDENTS:
                access = access_records.get(student["roll_number"], {})
                access_rows.append(
                    {
                        "Student": student["name"],
                        "Roll Number": student["roll_number"],
                        "Access": "Blocked" if access.get("blocked", False) else "Active",
                        "Reason": access.get("reason", ""),
                        "Updated By": access.get("updated_by", ""),
                        "Updated At": access.get("updated_at", ""),
                    }
                )
            st.dataframe(pd.DataFrame(access_rows), use_container_width=True, hide_index=True)
