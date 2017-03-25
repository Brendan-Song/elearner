import requests
from bs4 import BeautifulSoup
from python_utils import converters

def get_parsed_page(url):
    return BeautifulSoup(requests.get(url).text, "lxml")

def get_results():
    results = get_parsed_page("http://www.hltv.org/results/")
    resultslist = results.find_all("div", {"class": ["matchListBox", "matchListDateBox"]})
    datestring = ""
    results_list = []
    for result in resultslist:
        if result['class'][0] == "matchListDateBox":
            # TODO possibly change this into a real date object
            datestring = result.text.strip()
        else:
            #What does resultd mean?
            resultd = {}
            #This page uses the time box to show map played
            resultd['date'] = datestring
            resultd['map'] = result.find("div", {"class": "matchTimeCell"}).text.strip()
            scores = result.find("div", {"class": "matchScoreCell"}).text.strip()

            #Team 1 info
            team1div = result.find("div", {"class": "matchTeam1Cell"})
            team1 = {}
            team1['name'] = team1div.text.strip()
            #I seem to get the ID slightly differently, still works fine though
            team1href = team1div.select('a')[0].get('href')
            team1['id'] = converters.to_int(team1href.split("=")[-1], regexp=True)
            team1['score'] = converters.to_int(scores.split("-")[0].strip(), regexp=True)
            resultd['team1'] = team1

            #Team 2 info
            team2div = result.find("div", {"class": "matchTeam2Cell"})
            team2 = {}
            team2['name'] = team2div.text.strip()
            team2href = team2div.select('a')[0].get('href')
            team2['id'] = converters.to_int(team2href.split("=")[-1], regexp=True)
            team2['score'] = converters.to_int(scores.split("-")[1].strip(), regexp=True)
            resultd['team2'] = team2

            resultd['matchid'] = result.find("div", {"class": "matchActionCell"}).find("a").get('href') #What a fucking mess lmao
                                                    
            results_list.append(resultd)
    return(results_list)

def main():
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(get_results())

main()
