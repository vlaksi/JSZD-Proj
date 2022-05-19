import json
from os.path import join, dirname
from textx import metamodel_from_file
import requests

# INFO: This grammar & interpreter is based on the fact that user
# ie. member that is assignee or reporter is already member of
# the used board !!! 
# INFO: It's the same for the labels, ie. assigned labels to the story
# must already exist on the board, otherwise it will be not added to the
# story

# TODO: Implement checker for position, ie. we need to have at least one
# fe_dev, be_dev & qa in the team (board)

# Right now, we have a methods in this class that can create new sprint
# on the Trello & also we can create tickets/stories in the new column
# ie. list (and that represent a sprint)
# TODO: Improve a class to support many tracking system
class Scrum(object):

    def is_model_semantically_valid(self, model):
        # If any checker fail, we will print error that ocurred + return false to indicate not valid model
        
        for sprint_model in model.sprints:
            if(not self.is_min_number_of_user_story_per_sprint_valid(sprint_model)): return False
            if(not self.is_max_number_of_user_story_per_sprint_valid(sprint_model)): return False


        return True


    def is_min_number_of_user_story_per_sprint_valid(self, sprint_model):

        min_number_of_user_story_per_sprint = sprint_model.sprintRules.minNumberOfUSPerSprint
        total_number_of_user_stories = len(sprint_model.userStories)

        if(total_number_of_user_stories < min_number_of_user_story_per_sprint):
            print("\n[Checker][Semantic error]: Minimal number of user story for the sprint " + sprint_model.name + " is not valid, should be at least " + str(min_number_of_user_story_per_sprint))
            return False

        return True


    def is_max_number_of_user_story_per_sprint_valid(self, sprint_model):

        max_number_of_user_story_per_sprint = sprint_model.sprintRules.maxNumberOfUSPerSprint
        total_number_of_user_stories = len(sprint_model.userStories)

        if(total_number_of_user_stories > max_number_of_user_story_per_sprint):
            print("\n[Checker][Semantic error]: Max number of user story for the sprint " + sprint_model.name + " is not valid, should be at most " + str(max_number_of_user_story_per_sprint))
            return False

        return True


    def interpret(self, model):
        for sprint_model in model.sprints:
            #print(model.__dict__)

            created_sprint_on_trello = self.create_new_sprint_on_trello(sprint_model)
            self.create_sprint_user_stories(sprint_model.userStories, created_sprint_on_trello)


    def create_sprint_user_stories(self, sprint_user_stories_model, created_sprint):
        # TODO: Move this get call to one logical higher level (call it once, not for each sprint!)
        all_board_members = self.get_all_board_members()
        all_board_labels = self.get_all_board_labels()
        for user_story_model in sprint_user_stories_model: 
            story_member_ids = self.get_story_member_ids(user_story_model, all_board_members)
            story_label_ids = self.get_story_label_ids(user_story_model, all_board_labels)
            story_payload = {
                    'idList': created_sprint['id'],
                    'key': "9519ec4ca00591297f8bb4e7e184a841",
                    'token': "013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82",
                    'name': '(' + str(user_story_model.userStoryDetails.storyPoints) + ') ' + user_story_model.name,
                    'desc': user_story_model.userStoryBody.storyDescription.value,
                    'idMembers': story_member_ids,
                    'idLabels': story_label_ids
                }
                
            self.create_new_ticket_on_trello(story_payload)


    def get_story_member_ids(self, user_story_model, all_board_members):
        story_member_ids = []

        for member in all_board_members:
            try: # INFO: We have this try/catch because assigne is not required (and we will break program otherwise)
                if user_story_model.userStoryDetails.assigne.person.name.lower() in member['fullName'].lower():
                    story_member_ids.append(member['id'])
            except:
                print("Warning: There is no assigne for " + user_story_model.name + " story")

            if user_story_model.userStoryDetails.reporter.person.name.lower() in member['fullName'].lower():
                story_member_ids.append(member['id'])

        return story_member_ids


    def get_story_label_ids(self, user_story_model, all_board_labels):
        story_label_ids = []

        for label in all_board_labels:
            try: 
                for user_story_label_model in user_story_model.userStoryDetails.storyLabels:
                    if user_story_label_model.name.lower() in label['name'].lower():
                        story_label_ids.append(label['id'])
            except:
                print("Warning: There is no label for " + user_story_model.name + " story")

        return story_label_ids


    def get_all_board_members(self):
        url = "https://api.trello.com/1/boards/627c210aa0ed4a48c3dd069c/members"

        headers = {"Accept": "application/json"}

        payload = {
            'key': '9519ec4ca00591297f8bb4e7e184a841',
            'token': '013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82'
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=payload
        )

        return json.loads(response.text)


    def get_all_board_labels(self):
        url = "https://api.trello.com/1/boards/627c210aa0ed4a48c3dd069c/labels"

        payload = {
            'key': '9519ec4ca00591297f8bb4e7e184a841',
            'token': '013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82'
        }

        response = requests.request(
            "GET",
            url,
            params=payload
        )

        return json.loads(response.text)


    def create_new_sprint_on_trello(self, sprint):

        sprint_payload = {
                'idBoard':'627c210aa0ed4a48c3dd069c',
                'key': "9519ec4ca00591297f8bb4e7e184a841",
                'token': "013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82",
                'name': sprint.name, 
        }
        
        url="https://api.trello.com/1/lists"
        
        headers= {
            "Accept":"application/json"
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            params=sprint_payload
        )

        return json.loads(response.text)


    def create_new_ticket_on_trello(self, story_payload):
        url = "https://api.trello.com/1/cards"

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            params=story_payload
        )

        return json.loads(response.text)




# Extracting all the cards in all boards FROM TRELLO:
def extracte_all_cards_from_all_boards():
    url_member = "https://api.trello.com/1/members/malibajojszd"
    querystring = {"key":"9519ec4ca00591297f8bb4e7e184a841","token":"013c3b97e0290d108573fb6d150a8bf32982b84150c20a4d372bf701dabe8d82"}
    response_member = requests.request("GET", url_member, params=querystring)

    data_member = json.loads(response_member.text)
    board_ids = data_member['idBoards']
    print(board_ids)
    for board_id in board_ids:
        url_board_cards = "https://api.trello.com/1/boards/" + board_id +"/cards"
        response_board_cards = requests.request("GET", url_board_cards, params=querystring)
        data_board_cards = json.loads(response_board_cards.text)
        #print(data_board_cards)


def main():

    this_folder = dirname(__file__)

    scrum_mm = metamodel_from_file(join(this_folder, 'scrum.tx'), debug=False)
    scrum_model = scrum_mm.model_from_file(join(this_folder, 'sprintOne.scrum'))

    scrum = Scrum()
    scrum.interpret(scrum_model)


if __name__ == "__main__":
    main()