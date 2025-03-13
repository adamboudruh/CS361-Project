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