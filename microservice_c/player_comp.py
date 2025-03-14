from flask import Flask, request, jsonify
from nba_api.stats.endpoints import playerprofilev2
from rich.table import Table
from rich.console import Console
from nba_api.stats.static import players

app = Flask(__name__)

@app.route('/player/comp', methods=['GET'])
def get_player_comp():
    id_1 = request.args.get('id_1')
    id_2 = request.args.get('id_2')
    
    player_1_name = players.find_player_by_id(id_1)['full_name']
    player_2_name = players.find_player_by_id(id_2)['full_name']
    
    if not id_1 or not id_2:
        return jsonify({"error": "Missing player IDs"}), 400
    
    stats1 = playerprofilev2.PlayerProfileV2(player_id=id_1, per_mode36='PerGame')
    totals1 = stats1.season_totals_regular_season.get_dict()
    
    stats2 = playerprofilev2.PlayerProfileV2(player_id=id_2, per_mode36='PerGame')
    totals2 = stats2.season_totals_regular_season.get_dict()
    
    return jsonify({"totals1": totals1, "totals2": totals2})
    
    # table = Table(title=f"{player_1_name} vs. {player_2_name}")
    # table.add_column("Stat", justify="left", style="white")
    # table.add_column(f"{player_1_name}", justify="right", style="white")
    # table.add_column(f"{player_2_name}", justify="right", style="white")
    
    # total_indices = ['PTS', 'REB', 'AST', 'MIN', 'FG3_PCT', 'FG3A', 'STL', 'BLK', 'TOV']
    
    # # styles each of the colors depending on which plater has the higher stat
    # def color_stat(stat1, stat2):
    #     if stat1 > stat2:
    #         return ("[green]" + str(stat1) + "[/green]", "[red]" + str(stat2) + "[/red]")
    #     else:
    #         return ("[red]" + str(stat1) + "[/red]", "[green]" + str(stat2) + "[/green]")

    # for i in range(len(total_indices)):
    #     index = totals1['headers'].index(total_indices[i])
    #     stat1 = totals1['data'][-1][index]
    #     stat2 = totals2['data'][-1][index]
    #     colored_stat1, colored_stat2 = color_stat(stat1, stat2)
    #     table.add_row(total_indices[i], colored_stat1, colored_stat2)
    
    # console = Console(record=True)
    # console.print(table)
    # table_str = console.export_text()
    # return jsonify({"table": table_str})

if __name__ == '__main__':
    app.run(debug=True, port=3002)