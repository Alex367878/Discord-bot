import requests
import os

RAIDERIO_API_KEY = os.getenv("RAIDERIO_API_KEY")

#functia care returneaza scorul pentru sezonul 1 din dragonflight, primind ca argument linkul de la raiderio al jucatorului
def get_season1df_score(player_key):
    region, realm, name = extract_player_info(player_key)
    r = requests.get("https://raider.io/api/v1/characters/profile?region={region}&realm={realm}&name={name}&fields=mythic_plus_scores_by_season:season-df-1&access_key={RAIDERIO_API_KEY}"
                     .format(region=region, 
                             realm=realm, 
                             name=name, 
                             RAIDERIO_API_KEY=RAIDERIO_API_KEY))
    score = only_score(r)
    return score

#citesc linkul si extrag regiunea, realmul si numele jucatorului din linkul de la raiderio, pentru a le folosi in cererea catre API
def extract_player_info(link):
    try:
        parts = link.strip().split("/")
        region = parts[4]
        realm = parts[5]
        name = parts[6]
        return region, realm, name
    except IndexError:
        return None
#ofer doar scorul, fara alte informatii
def only_score(response):
    scores = response.json()["mythic_plus_scores_by_season"][0]["scores"]
    return "\n Scorul pe all = {all} \n Scorul pe dps = {dps} \n Scorul pe healer = {healer} \n Scorul pe tank = {tank}".format(all=scores["all"], 
                                                                                                                                dps=scores["dps"], 
                                                                                                                                healer=scores["healer"], 
                                                                                                                                tank=scores["tank"])
    

