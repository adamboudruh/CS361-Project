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
from basketball_reference_web_scraper.data import Team
from basketball_reference_web_scraper.data import Conference
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from rich.table import Table
from rich.console import Console
from bs4 import BeautifulSoup
import requests


# Load team aliases from teams.json
with open('teams.json', 'r') as f:
    teams = json.load(f)

options = [
    {'option': 'standings', 'desc': 'view current eastern and western conference standings'},
    {'option': 'home', 'desc': 'return to homepage'},
    {'option': 'team <name>', 'desc': 'view a current team\'s season statistics'},
    {'option': 'back', 'desc': 'return to the previous page'},
    {'option': 'exit', 'desc': 'quit the program'}
]

# print(teams['teams'])
team_completer_dict = {team: None for team in teams['teams']}
options_completer = NestedCompleter.from_nested_dict({
    'standings': None,
    'home': None,
    'team': team_completer_dict,   # loads all city and team names
    'back': None,
    'exit': None,
})

options_completer_r = NestedCompleter.from_nested_dict({
    'roster': None,
    'standings': None,
    'home': None,
    'team': team_completer_dict,   # loads all city and team names
    'back': None,
    'exit': None,
})

def print_options():
    print('\nOptions:')
    for option in options:
        print(f"\t{option['option']}: {option['desc']}")

def get_team_name(alias):
    for team in teams['aliases']:
        if alias in team['aliases']:
            return team['team']
    return None

def display_home():
    print("Welcome to the NBA Fast stats!")
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)

def display_standings():
    standings = client.standings(season_end_year=2025)
    
    #sort teams by least losses to most losses
    standings.sort(key=lambda x: x['losses'])
    
    console = Console()
    # Use rich to format into table with name, wins, losses, and pct(loss divided by win rounded to 3 decimals) columns and each team
    
    table_east = Table(title="Eastern Conference Standings")
    
    table_east.add_column("Team", justify="left", style="white", no_wrap=True)
    table_east.add_column("Wins", justify="right", style="green")
    table_east.add_column("Losses", justify="right", style="red")
    table_east.add_column("Pct", justify="right", style="magenta")
    
    for team in standings:
        if (team['conference'].value == 'EASTERN'):
            team_name = team['team'].value
            wins = team['wins']
            losses = team['losses']
            pct = round(wins / (wins + losses), 3)
            table_east.add_row(team_name, str(wins), str(losses), str(pct))

    print('\n')
    console.print(table_east)
    
    table_west = Table(title="Western Conference Standings")
    
    table_west.add_column("Team", justify="left", style="cyan", no_wrap=True)
    table_west.add_column("Wins", justify="right", style="green")
    table_west.add_column("Losses", justify="right", style="red")
    table_west.add_column("Pct", justify="right", style="magenta")
    
    for team in standings:
        if (team['conference'].value == 'WESTERN'):
            team_name = team['team'].value
            wins = team['wins']
            losses = team['losses']
            pct = round(wins / (wins + losses), 3)
            table_west.add_row(team_name, str(wins), str(losses), str(pct))

    print('\n')
    console.print(table_west)
    
    print("Options: \n\thome: return to homepage \n\tstandings: view current team standings \n\tteam <team_name>: view a current team's season statistics \n\texit: exit the program")
    return prompt("Enter your choice: ")

def display_team_info(team_name):
    print(f"Displaying information for {team_name}")
    # Add logic to display team information
    abr = team_name.upper()
    url = f'https://www.basketball-reference.com/teams/{abr}/2025.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.prettify())
    name = soup.find('h1').find_all('span')[1].text
    
    stats = soup.find('div', id='meta').find('div', {'data-template': 'Partials/Teams/Summary'}).find_all('p')
    record = stats[0].text.strip().replace('\n', ' ').replace('  ', ' ')
    pts = stats[5].text.strip().replace('\n', ' ').replace('  ', ' ')
    rtg = stats[7].text.strip().replace('\n', ' ').replace('  ', ' ')
    
    console = Console()
    console.print(f"[bold]Team Name:[/bold] {name}")
    console.print(f"[bold]Record:[/bold] {record}")
    console.print(f"[bold]Off and Def Ratings:[/bold] {rtg}")
    
    print_options()
    options.pop()
    return prompt("Enter your choice: ", completer=options_completer_r)

def display_roster_names(team_name):
    print("Displaying roster names")
    # Add logic to display roster names
    abr = team_name.upper()
    url = f'https://www.basketball-reference.com/teams/{abr}/2025.html'
    """
    name = text field of second span of only h1 tag in document
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    name = soup.find('h1').find_all('span')[1].text
    
    print(name)
    table_roster = Table(title=f"{name} Roster")
    
    table_roster.add_column("Number", justify="left", style="white",)
    table_roster.add_column("Name", justify="left", style="white")
    table_roster.add_column("Height", justify="right", style="white")
    table_roster.add_column("Position", justify="right", style="blue")
    
    page_roster = soup.find('table', id='roster')
    for row in page_roster.find('tbody').find_all('tr'):
        number = row.find('th', {'data-stat': 'number'}).text
        name = row.find('td', {'data-stat': 'player'}).text
        position = row.find('td', {'data-stat': 'pos'}).text
        height = row.find('td', {'data-stat': 'height'}).text
        table_roster.add_row(number, name, height, position)
    
    console = Console()
    console.print(table_roster)
    """
        use beautiful soup, find <table> with id="roster"
            for each row, make a row in the table
            number: text field of data-stat="number"
            name: text field of data-stat="player"
            position: text field of data-stat="pos"
            height: text field of data-stat"height"
            
        
    """
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)

def display_invalid():
    print("Invalid input. Please try again.")
    return prompt("Enter your choice: ", completer=options_completer)

prev_page = ''
current_page = 'home'
user_input = display_home()

while user_input:
    print(f"Current page: {current_page}, Previous page: {prev_page}\n")
    
    if prev_page.startswith('team'): options.pop()
    
    if user_input == 'home':
        user_input = display_home()
        prev_page = current_page
        current_page = 'home'
        
    elif user_input == 'standings':
        user_input = display_standings()
        prev_page = current_page
        current_page = 'standings'
        
    elif user_input.split(' ', 1)[0] == 'team':
        # gets the 3 letter abbreviation for team to look them up
        team_alias = ' '.join(user_input.split(' ')[1:])
        team_name = get_team_name(team_alias)
        if team_name:
            # roster is now available as an option
            options.append({'option': 'roster', 'desc': 'view team\'s current roster'})
            user_input = display_team_info(team_name)
            prev_page = current_page
            current_page = 'team ' + team_name
        else:
            user_input = display_invalid()
            
    elif current_page.split(' ', 1)[0] == 'team' and user_input == 'roster':
        # split page and grab second word, pass into display roster
        team_name = current_page.split(' ', 1)[1]
        user_input = display_roster_names(team_name)
    
    elif user_input == 'back':    
        print(f"Returning to {prev_page}")
        user_input = prev_page
        temp = current_page
        current_page = prev_page
        prev_page = temp
        
    elif user_input == 'exit':
        result = yes_no_dialog(
            title='Confirm exit',
            text='Are you sure you would like to quit the program?',
            style=Style.from_dict({
                'dialog':             'bg:black',
                # 'dialog frame.label': 'bg:green',
                # 'dialog.body':        'bg:white whitte',
                # 'dialog shadow':      'bg:gray',
                
                })
            ).run()
        if result: exit()
        else: user_input = current_page
        
    else:
        user_input = display_invalid()