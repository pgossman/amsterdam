import requests
import sys
from bs4 import BeautifulSoup
from lxml import etree


headers = {"Cookie": "redacted cookie"}
page = requests.get(
    "https://leagues2.amsterdambilliards.com/8ball/abc/individual_standings.php",
    headers=headers,
)

if page.status_code == 200:
    print("Successfully obtained data from site")
else:
    sys.exit(0)

# Proceed with parsing the data
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("td", {"colspan": "13"})
division = {}

print(
    "division,team_name,player_name,player_class,player_th,player_dbs,player_game_wins,player_game_losses,player_game_total,player_match_wins,player_match_losses,player_match_total,team_match_score"
)
for result in results:
    h3_children = result.find("h3")
    if h3_children != None:
        division = h3_children.text.strip()
        # 		print('Found division: ' + division)
        parent_table = h3_children.parent.parent.parent
        next_team_table = parent_table.find_next_sibling("table")
        while next_team_table != None:
            team_name = next_team_table.find_next("tr").text.strip()
            if team_name.endswith("Division"):
                next_team_table = None
            else:
                # 				print('Found team: ' + team_name)
                total_wins = (
                    next_team_table.find_next("tr")
                    .find_next("tr")
                    .find_next("tr")
                    .find_next("tr")
                    .find_all("td")
                )
                # 				print('Total Wins/Losses: ' + total_wins[11].text + '/' + total_wins[12].text)
                total_win = total_wins[11].text
                total_loss = total_wins[12].text
                player_stats = (
                    next_team_table.find_next("tr")
                    .find_next("tr")
                    .find_next("tr")
                    .find_next_siblings("tr")
                )
                for player in player_stats:
                    player_breakdown = player.find_all("td")
                    if player_breakdown[0].text == "Totals":
                        team_game_wins = player_breakdown[1].text
                        team_game_losses = player_breakdown[2].text
                        team_game_total = player_breakdown[3].text
                        team_match_wins = player_breakdown[4].text
                        team_match_losses = player_breakdown[5].text
                        team_match_total = player_breakdown[6].text
                        team_match_score = player_breakdown[7].text
                        print(
                            division
                            + ","
                            + team_name
                            + ",Total,,,,"
                            + team_game_wins
                            + ","
                            + team_game_losses
                            + ","
                            + team_game_total
                            + ","
                            + team_match_wins
                            + ","
                            + team_match_losses
                            + ","
                            + team_match_total
                            + ","
                            + team_match_score
                        )
                        continue
                    player_name = player_breakdown[1].text
                    player_class = player_breakdown[2].text
                    player_th = player_breakdown[3].text
                    player_dbs = player_breakdown[4].text
                    player_game_wins = player_breakdown[5].text
                    player_game_losses = player_breakdown[6].text
                    player_game_total = player_breakdown[7].text
                    player_match_wins = player_breakdown[8].text
                    player_match_losses = player_breakdown[9].text
                    player_match_total = player_breakdown[10].text
                    print(
                        division
                        + ","
                        + team_name
                        + ","
                        + player_name
                        + ","
                        + player_class
                        + ","
                        + player_th
                        + ","
                        + player_dbs
                        + ","
                        + player_game_wins
                        + ","
                        + player_game_losses
                        + ","
                        + player_game_total
                        + ","
                        + player_match_wins
                        + ","
                        + player_match_losses
                        + ","
                        + player_match_total
                        + ","
                    )
                try:
                    next_team_table = (
                        next_team_table.find_previous("center")
                        .find_next("center")
                        .find_next("table")
                    )
                except:
                    next_team_table = None
# 		while team_table != None:
# 			print('Found team: ' + team_table.text.strip())
# 			team_table = team_table.find_next_sibling('td', {"class": "data_level_1_nobg"})
