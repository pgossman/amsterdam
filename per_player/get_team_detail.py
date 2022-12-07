import requests
import sys
import time
from bs4 import BeautifulSoup


headers = {"Cookie": "redacted cookie"}
print(
    "game_name,game_date,player_name,player_hcp,player_games,player_opponent,player_opponent_hcp,player_opponent_games"
)
team_id = 1
for team_id in range(200, 1000):
    time.sleep(0.1)
    page = requests.get(
        "https://leagues2.amsterdambilliards.com/8ball/abc/team_scouting_report.php?season_nameid=211&team_id="
        + str(team_id),
        headers=headers,
    )

    if page.status_code == 200:
        None
    else:
        continue

    # Proceed with parsing the data
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find_all("td", {"colspan": "4"})

    # print("division,team_name,player_name,player_name,player_class,player_th,player_dbs,player_game_wins,player_game_losses,player_game_total,player_match_wins,player_match_losses,player_match_total,team_match_score")
    if len(results) < 1:
        continue

    parent_tables = results[0].find_parent("center").find_all_next("table")
    total_tables = len(parent_tables)
    if total_tables < 2:
        continue
    for table in parent_tables:
        header = table.find_next("tr").find_all("td")
        game_name = header[0].text.strip()
        game_date = header[1].text.strip()
        player_start = table.find_next("tr").find_next("tr").find_next_siblings("tr")
        for players in player_start:
            player_details = players.find_all("td")
            player_name = player_details[0].text.strip()
            player_hcp = player_details[1].text.strip()
            player_games = player_details[2].text.strip()
            player_opponent = player_details[3].text.strip()
            player_opponent_hcp = player_details[4].text.strip()
            player_opponent_games = player_details[5].text.strip()
            print(
                game_name
                + ","
                + game_date
                + ","
                + player_name
                + ","
                + player_hcp
                + ","
                + player_games
                + ","
                + player_opponent
                + ","
                + player_opponent_hcp
                + ","
                + player_opponent_games
            )
