import csv
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from selenium import webdriver

now_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

USERNAME = "user"
PASSWORD = "pass"
USERNAME = "pgossman"
PASSWORD = "3J7Q3KTRNppJw5Q"
OUTPUT_FILE = f"/home/paul/amsterdam_billiards_team_stats_{now_string}.csv"
print(OUTPUT_FILE)

BASE_SITE = "http://leagues2.amsterdambilliards.com"
INDIVIDUAL_STANDINGS_PAGE = f"{BASE_SITE}/8ball/abc/individual_standings.php\?foo\=bar"

service = Service(executable_path="/home/paul/dev/chromedriver")
driver = webdriver.Chrome(service=service)


def login():
    driver.get(INDIVIDUAL_STANDINGS_PAGE)
    username_input = driver.find_element(by=By.NAME, value="user")
    password_input = driver.find_element(by=By.NAME, value="pwd")
    login_button_locator = locate_with(By.TAG_NAME, "input").below(password_input)
    login_button = driver.find_element(by=login_button_locator)

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    login_button.click()


def get_team_tables():
    # this list contains all the team tables plus the division headers, like
    # "Lassiter Division," so we need to filter those out
    tables = driver.find_elements(by=By.CLASS_NAME, value="tableteir2")

    def filter_tables_with_one_row(table):
        rows = table.find_elements(by=By.XPATH, value="./tbody/tr")
        return len(rows) > 1

    return list(filter(filter_tables_with_one_row, tables))


# TODO: would be nice to get team name too
def parse_team_table(index_and_table):
    i, table = index_and_table
    team_id = i + 1
    print(f"Parsing team {team_id}...")
    rows = table.find_elements(by=By.XPATH, value="./tbody/tr")

    # drop first 3 and last 1 rows
    players = rows[3:-1]

    def parse_player_from_row(row):
        row = row.find_elements(by=By.XPATH, value="./td")
        return {
            "team_id": team_id,
            "name": row[1].text,
            "handicap": row[2].text,
            "t_h": row[3].text,
            "dbs": row[4].text,
            "game_wins": row[5].text,
            "game_losses": row[6].text,
            "match_wins": row[8].text,
            "match_losses": row[9].text,
        }

    return list(map(parse_player_from_row, players))


login()
print("Getting team tables...")
team_tables = get_team_tables()
print(f"Found {len(team_tables)} teams")
teams = list(map(parse_team_table, enumerate(team_tables)))

print("Done parsing teams, writing results to disk...")
with open(OUTPUT_FILE, "w") as f:
    w = csv.DictWriter(f, teams[0][0].keys())
    w.writeheader()
    for team in teams:
        for player in team:
            w.writerow(player)

print("Done")
