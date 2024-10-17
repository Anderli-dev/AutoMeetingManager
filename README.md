# AutoMeetingManager

AutoMeetingManager is a Python script, for my education, that automates joining and exiting Google Classroom meetings based on a schedule. It uses `pyautogui` to handle mouse and keyboard actions and `schedule` for task scheduling.

## Features

- **Automated Meeting Join:** The script automatically clicks "Join", "Mute Video" and "Mute Mic" buttons to quickly join a meeting.
- **Automated Meeting Exit:** Automatically leaves the meeting at a scheduled time.
- **Task Scheduling:** Joins and exits meetings at specified times using the `schedule` library.
- **Automatic Shutdown:** Shuts down the computer once the defined end time is reached.

## Requirements

- **Python 3.x**
- Python Libraries:
  - `pyautogui`
  - `schedule`

Install the required libraries via pip:
```bash
pip install pyautogui schedule
