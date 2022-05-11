import json
from os.path import join, dirname
from textx import metamodel_from_file
import requests

class Scrum(object):
    def interpret(self, model):
        for sprint in model.sprints:
            #print(model.__dict__)
            print(sprint)
            for user_story in sprint.userStories:
                print(user_story.userStoryBody.storyAcceptanceCriteria.value)
            #example of post request using requests library
            payload={'title':user_story.name,'body': user_story.userStoryBody.storyAcceptanceCriteria.value,'userId': 1}
            r = requests.post('https://jsonplaceholder.typicode.com/posts', data=payload)
            print(r.status_code)
            print(r.text)
            print(r.ok)
            print(r.url)
            print(r.json())

#Extracting all the cards in all boards FROM TRELLO:
def extracte_all_cards_from_all_boards():
    url_member = "https://api.trello.com/1/members/malibajojszd"
    querystring = {"key":"9519ec4ca00591297f8bb4e7e184a841","token":"013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82"}
    response_member = requests.request("GET", url_member, params=querystring)

    data_member = json.loads(response_member.text)
    board_ids = data_member['idBoards']
  
    for board_id in board_ids:
        url_board_cards = "https://api.trello.com/1/boards/" + board_id +"/cards"
        response_board_cards = requests.request("GET", url_board_cards, params=querystring)
        data_board_cards = json.loads(response_board_cards.text)
        print(data_board_cards)


def main():

    this_folder = dirname(__file__)

    scrum_mm = metamodel_from_file(join(this_folder, 'scrum.tx'), debug=False)
    scrum_model = scrum_mm.model_from_file(join(this_folder, 'sprintOne.scrum'))

    scrum = Scrum()
    scrum.interpret(scrum_model)
    extracte_all_cards_from_all_boards()



if __name__ == "__main__":
    main()