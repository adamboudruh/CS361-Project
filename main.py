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
    {'option': 'team <[blue]name[/blue]>', 'desc': 'view a current team\'s season statistics'},
    {'option': 'player <[blue]player name[/blue]>', 'desc': 'view a player\'s current season stats'},
    {'option': 'compare', 'desc': 'view a comparison between two NBA players of your choosing'},
    {'option': 'help', 'desc': 'ask an AI helper a question about basketball and its rules or history'},
    {'option': 'team <[blue]name[/blue]>', 'desc': 'view a current team\'s season statistics'},
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
    'compare': None,
    'help': None,
    'back': None,
    'exit': None,
})

options_completer_r = NestedCompleter.from_nested_dict({
    'roster': None,
    'standings': None,
    'compare': None,
    'home': None,
    'team': team_completer_dict,   # loads all city and team names
    'player': None,
    'compare': None,
    'help': None,
    'back': None,
    'exit': None,
})

def print_options():
    console = Console()
    console.print('\n[b][purple]Options:[/purple][/b]')
    for option in options:
        console.print(f"\t[b]{option['option']}:[/b] {option['desc']}")

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

    print()
    console.print(table_west)
    
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)

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

def display_player_data(player):
    stats = playerprofilev2.PlayerProfileV2(player_id=player['id'], per_mode36='PerGame')
    totals = stats.season_totals_regular_season.get_dict()
    rankings = stats.season_rankings_regular_season.get_dict()
    if stats:
        total_indices = ['PTS', 'REB', 'AST', 'MIN', 'FG3_PCT', 'FG3A', 'STL', 'BLK', 'TOV']
        rank_indices = ['RANK_PG_PTS', 'RANK_PG_REB', 'RANK_PG_AST', 'RANK_PG_MIN', 'RANK_FG3_PCT', 'RANK_PG_FG3A', 'RANK_PG_STL', 'RANK_PG_BLK', 'RANK_PG_TOV']
        #index_names = ['Points Per Game', 'Rebounds Per Game', 'Assists Per Game', 'Minutes Per Game', 'Three-Point Percentage', 'Three-Point Attempts', 'Steals Per Game', 'Blocks Per Game', 'Turnovers Per Game']
        stats_table = Table(title=f"{player['full_name']} Current Season Stats")
        stats_table.add_column("Stat", justify="left", style="white")
        stats_table.add_column("#", justify="right", style="white")
        stats_table.add_column("Rank", justify="right", style="white")
        for i in range(len(total_indices)):
            # add a row containing the data point under each of the three indices
            total_index = totals['headers'].index(total_indices[i])
            rank_index = rankings['headers'].index(rank_indices[i])
            stat_name = total_indices[i]
            stat_value = totals['data'][-1][total_index]
            stat_rank = rankings['data'][-1][rank_index]
            if stat_rank:
                rank_style = "green" if stat_rank < 10 else "white"
            else:
                stat_rank = "Unranked"
            stats_table.add_row(stat_name, str(stat_value), f"[{rank_style}]{stat_rank}[/{rank_style}]")
        
        # make a get request to microservice B and print whatever is returned
        response = requests.get(f'http://127.0.0.1:3001/player/{player['id']}')
        if response.status_code == 200:
            print(response.json())
            console = Console()
            print("\n")
            console.print(stats_table)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    else:
        print("No data available")
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)
   
# styles each of the colors depending on which plater has the higher stat
def color_stat(stat1, stat2):
    if stat1 > stat2:
        return ("[green]" + str(stat1) + "[/green]", "[red]" + str(stat2) + "[/red]")
    else:
        return ("[red]" + str(stat1) + "[/red]", "[green]" + str(stat2) + "[/green]")
    
def display_ai_help():
    question = prompt("\nPlease enter your basketball question below and I'll do my best to answer it!\nQuestion: ")
    response = requests.post('http://127.0.0.1:3003/help', json={'question': question})
    console = Console()
    if response.status_code == 200:
        answer = response.json().get('answer', 'Sorry, I could not find an answer to your question.')
        console.print(f"\n[b]Answer:[/b] {answer}")
    else:
        print(f"Failed to retrieve answer: {response.status_code}")
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)
    
def display_comparison():
    player1 = None
    player2 = None
    while player1 is None:
        player1_name = prompt("\nPlease enter the first player: ")
        player1 = find_player(player1_name)
        if player1 is None: print("Player with that name not found.")
    print(f"Player1: {player1['full_name']}")
    while player2 is None:
        player2_name = prompt("\nPlease enter the second player: ")
        player2 = find_player(player2_name)
        if player2 is None: print("Player with that name not found.")
    print(f"Player2: {player2['full_name']}")
    comp_path = f"http://127.0.0.1:3002/player/comp?id_1={player1['id']}&id_2={player2['id']}"
    response = requests.get(comp_path)
    if response.status_code == 200:
        totals1 = response.json()['totals1']
        totals2 = response.json()['totals2']
        table = Table(title=f"{player1['full_name']} vs. {player2['full_name']}")
        table.add_column("Stat", justify="left", style="white")
        table.add_column(f"{player1['full_name']}", justify="right", style="white")
        table.add_column(f"{player2['full_name']}", justify="right", style="white")
        
        total_indices = ['PTS', 'REB', 'AST', 'MIN', 'FG3_PCT', 'FG3A', 'STL', 'BLK', 'TOV']

        for i in range(len(total_indices)):
            index = totals1['headers'].index(total_indices[i])
            stat1 = totals1['data'][-1][index]
            stat2 = totals2['data'][-1][index]
            colored_stat1, colored_stat2 = color_stat(stat1, stat2)
            table.add_row(total_indices[i], colored_stat1, colored_stat2)
        
        console = Console()
        print()
        console.print(table)
    else:
        print(f"Failed to retrieve comparison data: {response.status_code}")
    print_options()
    return prompt("Enter your choice: ", completer=options_completer)
    
def display_invalid():
    print("Invalid input. Please try again.")
    return prompt("Enter your choice: ", completer=options_completer)

prev_pages = []
current_page = 'home'
user_input = display_home()

def find_player(player_name):
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
        return playerlist[0]
    else: return None

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
        
        player = find_player(player_name)
        print(player)
        if player: 
            user_input = display_player_data(player)
        else:
            user_input = display_invalid()
    
    elif user_input == "compare":
        prev_pages.append(current_page)
        user_input = display_comparison()
        
    elif user_input == "help":
        prev_pages.append(current_page)
        user_input = display_ai_help()
    
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
