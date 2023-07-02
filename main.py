import re
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from dataclasses import dataclass
import sqlite3


@dataclass
class Player():
    name: str
    id_: int
    overall: int
    max_overall: int
    first_name: str
    last_name: str
    team_name: str
    team_location: str
    height_inches: int
    weightPounds: int
    acceleration: int
    agility: int
    awareness: int
    ballCarrierVision: int
    blockShedding: int
    breakSack: int
    breakTackle: int
    carrying: int
    catchInTraffic: int
    catching: int
    changeOfDirection: int
    deepRouteRunning: int
    deepThrowAccuracy: int
    finesseMoves: int
    hitPower: int
    impactBlocking: int
    injury: int
    jukeMove: int
    jumping: int
    kickAccuracy: int
    kickPower: int
    kickReturn: int
    leadBlock: int
    manCoverage: int
    mediumRouteRunning: int
    mediumThrowAccuracy: int
    passBlock: int
    passBlockFinesse: int
    passBlockPower: int
    playAction: int
    playRecognition: int
    powerMoves: int
    press: int
    pursuit: int
    release: int
    runBlock: int
    runBlockFinesse: int
    runBlockPower: int
    shortRouteRunning: int
    shortThrowAccuracy: int
    spectacularCatch: int
    speed: int
    spinMove: int
    stamina: int
    stiffArm: int
    strength: int
    tackle: int
    throwAccuracy: int
    throwPower: int
    throwUnderPressure: int
    throwingOnTheRun: int
    toughness: int
    trucking: int
    zoneCoverage: int


def create_db():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('player_stats.db')

        # Create a new cursor
        c = conn.cursor()

        # Create a new table named "players"
        c.execute('''
            CREATE TABLE players (
                id INTEGER PRIMARY KEY,
                name TEXT,
                overall INTEGER,
                max_overall INTEGER,
                first_name TEXT,
                last_name TEXT,
                team_name TEXT,
                team_location TEXT,
                height_inches INTEGER,
                weightPounds INTEGER,
                acceleration INTEGER,
                agility INTEGER,
                awareness INTEGER,
                ballCarrierVision INTEGER,
                blockShedding INTEGER,
                breakSack INTEGER,
                breakTackle INTEGER,
                carrying INTEGER,
                catchInTraffic INTEGER,
                catching INTEGER,
                changeOfDirection INTEGER,
                deepRouteRunning INTEGER,
                deepThrowAccuracy INTEGER,
                finesseMoves INTEGER,
                hitPower INTEGER,
                impactBlocking INTEGER,
                injury INTEGER,
                jukeMove INTEGER,
                jumping INTEGER,
                kickAccuracy INTEGER,
                kickPower INTEGER,
                kickReturn INTEGER,
                leadBlock INTEGER,
                manCoverage INTEGER,
                mediumRouteRunning INTEGER,
                mediumThrowAccuracy INTEGER,
                passBlock INTEGER,
                passBlockFinesse INTEGER,
                passBlockPower INTEGER,
                playAction INTEGER,
                playRecognition INTEGER,
                powerMoves INTEGER,
                press INTEGER,
                pursuit INTEGER,
                release INTEGER,
                runBlock INTEGER,
                runBlockFinesse INTEGER,
                runBlockPower INTEGER,
                shortRouteRunning INTEGER,
                shortThrowAccuracy INTEGER,
                spectacularCatch INTEGER,
                speed INTEGER,
                spinMove INTEGER,
                stamina INTEGER,
                stiffArm INTEGER,
                strength INTEGER,
                tackle INTEGER,
                throwAccuracy INTEGER,
                throwPower INTEGER,
                throwUnderPressure INTEGER,
                throwingOnTheRun INTEGER,
                toughness INTEGER,
                trucking INTEGER,
                zoneCoverage INTEGER
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    except Exception:
        pass


def insert_into_db(player: Player):
    # Reconnect to the SQLite database
    conn = sqlite3.connect('player_stats.db')

    # Create a new cursor
    c = conn.cursor()

    # Insert the Player object's data into the "players" table
    c.execute('''
        INSERT INTO players VALUES (
            :id_, :name, :overall, :max_overall, :first_name, :last_name, :team_name,
            :team_location, :height_inches, :weightPounds, :acceleration, :agility,
            :awareness, :ballCarrierVision, :blockShedding, :breakSack, :breakTackle,
            :carrying, :catchInTraffic, :catching, :changeOfDirection, :deepRouteRunning,
            :deepThrowAccuracy, :finesseMoves, :hitPower, :impactBlocking, :injury,
            :jukeMove, :jumping, :kickAccuracy, :kickPower, :kickReturn, :leadBlock,
            :manCoverage, :mediumRouteRunning, :mediumThrowAccuracy, :passBlock,
            :passBlockFinesse, :passBlockPower, :playAction, :playRecognition, :powerMoves,
            :press, :pursuit, :release, :runBlock, :runBlockFinesse, :runBlockPower,
            :shortRouteRunning, :shortThrowAccuracy, :spectacularCatch, :speed, :spinMove,
            :stamina, :stiffArm, :strength, :tackle, :throwAccuracy, :throwPower,
            :throwUnderPressure, :throwingOnTheRun, :toughness, :trucking, :zoneCoverage
        )
    ''', player.__dict__)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def main():
    player_ids = []
    s = HTMLSession()

    header = {
        "Host": "www.mut.gg",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.mut.gg/upgrades/",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    i = 1
    pages = 401
    while i <= pages:
        get_player_ids = s.get(url=f"https://www.mut.gg/players/?page={i}", headers=header)
        i += 1
        if get_player_ids.status_code == 200:
            get_player_ids.html.render(sleep=1)

            soup = BeautifulSoup(get_player_ids.html.html, 'html.parser')

            # Find all script tags
            items = soup.find_all(class_='player-list-item')

            for item in items:
                href = item.contents[1].attrs['href']
                id_prep = re.split("/", href)[-2]
                id_ = re.split("-", id_prep)[-1]
                player_ids.append(id_)

    for player_id in player_ids:
        get_upgrade_values_url = f"https://www.mut.gg/api/23/player-items/?ids={player_id}"
        get_player_stats = s.get(url=get_upgrade_values_url, headers=header)
        if get_player_stats.status_code == 200:
            stats_json = get_player_stats.json()
            player_data = stats_json["data"][0]
            player = Player(
                name=f'{player_data["firstName"]} {player_data["lastName"]}',
                id_=player_data["externalId"],
                overall=player_data["overall"],
                max_overall=player_data["maxOverall"],
                first_name=player_data["firstName"],
                last_name=player_data["lastName"],
                team_name=player_data["team"]["name"],
                team_location=player_data["team"]["location"],
                height_inches=player_data["heightInches"],
                weightPounds=player_data["weightPounds"],
                acceleration=player_data["acceleration"],
                agility=player_data["agility"],
                awareness=player_data["awareness"],
                ballCarrierVision=player_data["ballCarrierVision"],
                blockShedding=player_data["blockShedding"],
                breakSack=player_data["breakSack"],
                breakTackle=player_data["breakTackle"],
                carrying=player_data["carrying"],
                catchInTraffic=player_data["catchInTraffic"],
                catching=player_data["catching"],
                changeOfDirection=player_data["changeOfDirection"],
                deepRouteRunning=player_data["deepRouteRunning"],
                deepThrowAccuracy=player_data["deepThrowAccuracy"],
                finesseMoves=player_data["finesseMoves"],
                hitPower=player_data["hitPower"],
                impactBlocking=player_data["impactBlocking"],
                injury=player_data["injury"],
                jukeMove=player_data["jukeMove"],
                jumping=player_data["jumping"],
                kickAccuracy=player_data["kickAccuracy"],
                kickPower=player_data["kickPower"],
                kickReturn=player_data["kickReturn"],
                leadBlock=player_data["leadBlock"],
                manCoverage=player_data["manCoverage"],
                mediumRouteRunning=player_data["mediumRouteRunning"],
                mediumThrowAccuracy=player_data["mediumThrowAccuracy"],
                passBlock=player_data["passBlock"],
                passBlockFinesse=player_data["passBlockFinesse"],
                passBlockPower=player_data["passBlockPower"],
                playAction=player_data["playAction"],
                playRecognition=player_data["playRecognition"],
                powerMoves=player_data["powerMoves"],
                press=player_data["press"],
                pursuit=player_data["pursuit"],
                release=player_data["release"],
                runBlock=player_data["runBlock"],
                runBlockFinesse=player_data["runBlockFinesse"],
                runBlockPower=player_data["runBlockPower"],
                shortRouteRunning=player_data["shortRouteRunning"],
                shortThrowAccuracy=player_data["shortThrowAccuracy"],
                spectacularCatch=player_data["spectacularCatch"],
                speed=player_data["speed"],
                spinMove=player_data["spinMove"],
                stamina=player_data["stamina"],
                stiffArm=player_data["stiffArm"],
                strength=player_data["strength"],
                tackle=player_data["tackle"],
                throwAccuracy=player_data["throwAccuracy"],
                throwPower=player_data["throwPower"],
                throwUnderPressure=player_data["throwUnderPressure"],
                throwingOnTheRun=player_data["throwingOnTheRun"],
                toughness=player_data["toughness"],
                trucking=player_data["trucking"],
                zoneCoverage=player_data["zoneCoverage"]
            )
            insert_into_db(player)


if __name__ == '__main__':
    create_db()
    main()
