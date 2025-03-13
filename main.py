import json
from basketball_reference_web_scraper import client
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from rich.table import Table
from rich.console import Console
from bs4 import BeautifulSoup
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerprofilev2
import requests


# Load team aliases from teams.json
with open('teams.json', 'r') as f:
    teams = json.load(f)

options = [
    {'option': 'standings', 'desc': 'view current eastern and western conference standings'},
    {'option': 'home', 'desc': 'return to homepage'},
    {'option': 'team <name>', 'desc': 'view a current team\'s season statistics'},
    {'option': 'player <player first name> <player last name>', 'desc': 'view a player\'s current season stats'},
    {'option': 'compare', 'desc': 'view a comparison between two NBA players of your choosing'},
    {'option': 'team <name>', 'desc': 'view a current team\'s season statistics'},
    {'option': 'back', 'desc': 'return to the previous page'},
    {'option': 'exit', 'desc': 'quit the program'}
]

# print(teams['teams'])
team_completer_dict = {team: None for team in teams['teams']}

options_completer = NestedCompleter.from_nested_dict({
    'standings': None,
    'compare': None,
    'home': None,
    'team': team_completer_dict,   # loads all city and team names
    'player': None,
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
    with open(f'./ascii_art/nba.txt', 'r') as art_file:
        art = art_file.read()
    print(art)
    print("\nWelcome to the NBA Fast stats!")
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
    
    table_west.add_column("Team", justify="left", style="white", no_wrap=True)
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
    
    print_options()
    return prompt("Enter your choice: ")

def display_team_info(team_name):
    print("\n\n")
    # Add logic to display team information
    abr = team_name.upper()
    url = f'https://www.basketball-reference.com/teams/{abr}/2025.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    name = soup.find('h1').find_all('span')[1].text
    
    # get team ascii art
    with open(f'./ascii_art/{team_name}.txt', 'r') as art_file:
        art = art_file.read()
    
    stats = soup.find('div', id='meta').find('div', {'data-template': 'Partials/Teams/Summary'}).find_all('p')
    record = stats[0].text.strip().replace('\n', ' ').replace('  ', ' ')
    rtg = stats[7].text.strip().replace('\n', ' ').replace('  ', ' ')
    
    console = Console()
    console.print(f"{art}\n\n")
    console.print(f"[bold]Team Name:[/bold] {name}\n")
    console.print(f"{record}\n")
    console.print(f"{rtg}\n")
    
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
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)

def display_player_data(id):
    stats = playerprofilev2.PlayerProfileV2(player_id=id, per_mode36='PerGame')
    totals = stats.season_totals_regular_season.get_dict()
    data = totals['data']
    if data:
        # make a get request to http://127.0.0.1:5000/player/{player_id} and print whatever is returned
        response = requests.get(f'http://127.0.0.1:5000/player/{id}')
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Failed to retrieve data: {response.status_code}")
        print(json.dumps(data[-1], indent=4))
    else:
        print("No data available")
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)
    
def display_invalid():
    print("Invalid input. Please try again.")
    return prompt("Enter your choice: ", completer=options_completer)

prev_pages = []
current_page = 'home'
user_input = display_home()

while user_input:
    
    if user_input == 'home':
        prev_pages.append(current_page)
        user_input = display_home()
        current_page = 'home'
        
    elif user_input == 'standings':
        prev_pages.append(current_page)
        user_input = display_standings()
        current_page = 'standings'
        
    elif user_input.split(' ', 1)[0] == 'team':
        team_alias = ' '.join(user_input.split(' ')[1:])
        team_name = get_team_name(team_alias)
        if team_name:
            options.append({'option': 'roster', 'desc': 'view team\'s current roster'})
            prev_pages.append(current_page)
            user_input = display_team_info(team_name)
            current_page = 'team ' + team_name
        else:
            user_input = display_invalid()
            
    elif current_page.split(' ', 1)[0] == 'team' and user_input == 'roster':
        team_name = current_page.split(' ', 1)[1]
        prev_pages.append(current_page)
        user_input = display_roster_names(team_name)
        
    elif user_input.split(' ', 1)[0] == 'player':
        player_name = ' '.join(user_input.split(' ')[1:])
        prev_pages.append(current_page)
        
        # gather all players with matching name
        playerlist = [player for player in players.find_players_by_full_name(player_name) if player['is_active']]
        
        # if more than one player, ask user to specify
        while len(playerlist) > 1:
            print("\nYour request brought up multiple players: \n")
            playerlist_names = []
            for player in playerlist:
                print(player['full_name'])
                playerlist_names.append(player['full_name'])
            player_completer = WordCompleter(playerlist_names, ignore_case=True)
            player_name = prompt("\nPlease specify one of the above: ", completer=player_completer)
            playerlist = [player for player in players.find_players_by_full_name(player_name) if player['is_active']]
        if len(playerlist) == 1:
            user_input = display_player_data(playerlist[0]['id'])
        else:
            display_invalid()
    
    elif user_input == 'back':
        if prev_pages:
            current_page = prev_pages.pop()
            user_input = current_page
        else:
            user_input = display_invalid()
        
    elif user_input == 'exit':
        result = yes_no_dialog(
            title='Confirm exit',
            text='Are you sure you would like to quit the program?',
            style=Style.from_dict({
                'dialog': 'bg:black'
            })
        ).run()
        if result:
            exit()
        else:
            user_input = current_page
        
    else:
        user_input = display_invalid()
