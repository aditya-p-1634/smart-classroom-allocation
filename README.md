# Smart Room Booking — Prototype MARK-1

A Streamlit app that helps students and administrators find and book available
classrooms, labs, and halls. It checks the selected time against the weekly
Odd/Even semester timetables and existing bookings, then lists only rooms that
match the requested type, capacity, and projector requirements.

## Why this project

Manual room allocation can lead to double bookings, overcrowded rooms, or
spaces without required facilities. This project demonstrates how timetable
data, room requirements, and saved reservations can be combined to make room
search and booking clearer.

## Short presentation

“Smart Room Booking Prototype MARK-1 is a Python and Streamlit app that finds
suitable rooms for a requested date and time. It checks the weekly Odd/Even
timetable and previous reservations, then shows only rooms that are available
and meet the capacity and facility needs. A final conflict check runs before a
booking is saved. Administrators can also manage student access. This
prototype uses local CSV storage, so it demonstrates the workflow but is not
designed for simultaneous production use.”

## Features

- Search for currently available classrooms, labs, and halls.
- Filter by semester timetable, date, time, duration, capacity, and projector.
- Avoid conflicts with scheduled classes and saved reservations.
- Student and administrator booking histories.
- Student view of today's schedule from the supplied Odd/Even timetable PDFs.
- Admin tools to block or unblock student accounts.
- Save bookings and student access status locally as CSV files.
- Blue-accented interface with 12-hour time labels.

## Run locally

Requirements: Git, Python 3.10+, and Windows PowerShell.

```powershell
git clone https://github.com/aditya-p-1634/smart-classroom-allocation.git
cd smart-classroom-allocation
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run src\app.py
```

Open <http://localhost:8501>. These commands do not require activating the
virtual environment, avoiding PowerShell execution-policy issues. Alternatively,
download the repository as a ZIP from GitHub, extract it, and run the commands
from its folder. Each person creates their own local `.venv` and booking CSV
files; these are not included in the repository.

See [RUN_INSTRUCTIONS.txt](RUN_INSTRUCTIONS.txt) for complete installation,
usage, and troubleshooting steps.

## Demo accounts

These built-in accounts are for demonstration only—not real credentials:

| Role | ID | Password |
|---|---|---|
| Student | `21CS001` | `1234` |
| Student | `21CS015` | `1234` |
| Student | `21CS032` | `1234` |
| Admin | `ADM001` | `admin123` |
| Admin | `ADM002` | `admin123` |

## How it works

1. The user signs in as a student or admin.
2. Students can open Today's timetable. The app uses the computer's local
   date to choose the weekday and displays the selected Odd/Even program
   schedule from the timetable PDFs.
3. For a room search, the user selects a date, start time, number of periods,
   room type, and optional capacity/projector requirements.
4. The app checks the matching weekday from the selected timetable and saved
   reservations for overlapping periods.
5. It lists rooms that are both free and suitable.
6. When a room is booked, availability is checked again before the booking is
   saved.

## Project structure

```text
.
├── src/
│   └── app.py
├── data/
│   └── timetables/
│       ├── Odd_Semester_Timetables_With_Rooms.pdf
│       └── Even_Semester_Timetables_With_Rooms.pdf
├── docs/
│   ├── PROJECT_GUIDE.txt
│   └── ROOM_AND_FACILITY_NOTES.txt
├── requirements.txt
├── .gitignore
├── README.md
└── RUN_INSTRUCTIONS.txt
```

## Technology

- Python
- Streamlit for the web interface
- pandas for CSV-backed booking data
- pdfplumber for extracting timetable information from PDFs

## Current limitations

- Demo users and passwords are stored in the source code.
- Student accounts are not linked to a semester or program, so students select
  which supplied schedule to view; the timetable is not personalized.
- CSV storage is suitable for a local demonstration, not concurrent production
  use.
- Timetable parsing depends on the supplied PDF layout.
- Room capacity and facility details should be verified before real use.

See [docs/PROJECT_GUIDE.txt](docs/PROJECT_GUIDE.txt) for detailed behavior,
architecture, and setup notes.
