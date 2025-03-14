from flask import Flask, request, jsonify
from ascii_magic import AsciiArt, Back

app = Flask(__name__)

@app.route('/player/<int:player_id>', methods=['GET'])
def get_player_data(player_id):
    img_path = f'https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png'
    
    # convert to ascii and return
    try:
        my_art = AsciiArt.from_url(img_path)
        output = my_art.to_ascii(columns=100, width_ratio=2.5)
    except OSError as e:
        print(f'Could not load the image, server said: {e.code} {e.msg}')
    print(output)
    
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, port=3001)