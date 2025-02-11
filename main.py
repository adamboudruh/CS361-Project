"""
pseudo code:
import basketball_reference_web_scraper client
import teams
import display standings from standings.py
import display team from team.py
import display home from home.py

prev_page = ''
current_page = 'home'
input = ""

while input != "exit":
    print(welcome page)
    
    
    
    call display options("page")
    
    if input == 'home':
        call display_home()
        prev_page = current_page
        current_page = 'home'
    elif input == 'standings':
        call display_standings()
        prev_page = current_page
        current_page = 'standings'
    elif input.startswith('team'):
        team_alias = input.split(' ', 1)[1]
        check if team_alias is within team aliases
        if found:
            team_name = team.name of object that the found alias is under
            call display_team_info(team_name)
        else:
            display_invalid()
    elif current_page == 'team' and input == 'roster':
        call display_roster_names()
    elif input == 'back':
        call handle_back(prev_page)
        temp = current_page
        current_page = prev_page
        prev_page = temp
    elif input != 'exit':
        display_invalid()
"""
import json
from basketball_reference_web_scraper import client

# Load team aliases from teams.json
with open('teams.json', 'r') as f:
    teams = json.load(f)

def get_team_name(alias):
    for team in teams:
        if alias in team['aliases']:
            return team['team']
    return None

def display_home():
    print("Welcome to the NBA Stats Viewer!")
    print("Options: home, standings, team <team_alias>, exit")
    return input("Enter your choice: ")

def display_standings():
    standings = client.standings(season_end_year=2025)
    for team in standings:
        print(f"{team['team']} - {team['wins']} wins, {team['losses']} losses")
    return input("Enter your choice: ")

def display_team_info(team_name):
    print(f"Displaying information for {team_name}")
    # Add logic to display team information
    return input("Enter your choice: ")

def display_roster_names():
    print("Displaying roster names")
    # Add logic to display roster names
    return input("Enter your choice: ")

def handle_back(prev_page):
    print(f"Returning to {prev_page}")
    return prev_page

def display_invalid():
    print("Invalid input. Please try again.")
    return input("Enter your choice: ")

prev_page = ''
current_page = 'home'
user_input = ""

while user_input != "exit":
    if current_page == 'home':
        user_input = display_home()
        prev_page = current_page
        current_page = 'home'
    elif current_page == 'standings':
        user_input = display_standings()
        prev_page = current_page
        current_page = 'standings'
    elif user_input.startswith('team'):
        team_alias = user_input.split(' ', 1)[1]
        team_name = get_team_name(team_alias)
        if team_name:
            user_input = display_team_info(team_name)
            prev_page = current_page
            current_page = 'team'
        else:
            user_input = display_invalid()
    elif current_page == 'team' and user_input == 'roster':
        user_input = display_roster_names()
    elif user_input == 'back':
        user_input = handle_back(prev_page)
        temp = current_page
        current_page = prev_page
        prev_page = temp
    elif user_input != 'exit':
        user_input = display_invalid()