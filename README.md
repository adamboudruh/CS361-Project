# NBA Fast Stats

This is the repository for my final project in CS361.

## Overview

This project is a Python-based application with a text-based UI that compiles information about your favorite NBA teams or Players and converts NBA Player Portraits to ASCII art.

## Screenshots
<img width="1310" height="859" alt="image" src="https://github.com/user-attachments/assets/38acaa59-81ba-42c6-b96a-e741017d417c" />
<img width="654" height="455" alt="image" src="https://github.com/user-attachments/assets/48e3a55b-53fc-46db-bd81-86208af56e19" />
<img width="653" height="453" alt="image" src="https://github.com/user-attachments/assets/8106a12e-73d9-4920-a8ae-c6c65fd6e510" />


## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/adamboudruh/CS361-Project.git
   cd CS361-Project
   ```

2. **(Recommended) Set up a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   - For Linux:
     ```bash
     pip install lxml-5.3.1-pp310-pypy310_pp73-manylinux_2_28_x86_64.whl
     ```
   - For Windows:
     ```bash
     pip install lxml-5.3.1-pp310-pypy310_pp73-win_amd64.whl
     ```

4. **Run the project:**
   ```bash
   py main.py
   ```

## Video demo
Demo video: https://docs.google.com/videos/d/1ncFtcWUWwMg3pWQ9aXLAbm3NFeoqj_eriJBceLJ39V8/edit?usp=sharing

## Dependencies
Key libraries used across the project:
- Flask
- nba_api
- beautifulsoup4
- prompt_toolkit
- rich

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
