import json
from os.path import join, dirname
from textx import metamodel_from_file
import requests
import base64
import json
import pathlib

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
        with open("config.json", "r") as f:
            config = json.load(f)
    
        isJiraEnabled = config["enableTrackingSystem"]["Jira"]
        isTrelloEnabled = config["enableTrackingSystem"]["Trello"]

        for sprint_model in model.sprints:
            if(isTrelloEnabled):
                created_sprint_on_trello = self.create_new_sprint_on_trello(sprint_model, config)
                self.create_sprint_user_stories_trello(sprint_model.userStories, created_sprint_on_trello, config)
            if(isJiraEnabled):
                self.create_sprint_user_stories_jira(sprint_model.userStories, config)


    def create_sprint_user_stories_trello(self, sprint_user_stories_model, created_sprint, config):   
        # TODO: Move this get call to one logical higher level (call it once, not for each sprint!)
        all_board_members = self.get_all_board_members(config)
        all_board_labels = self.get_all_board_labels(config)
      
        for user_story_model in sprint_user_stories_model: 
            story_member_ids = self.get_story_member_ids(user_story_model, all_board_members)
            story_label_ids = self.get_story_label_ids(user_story_model, all_board_labels)
            story_payload_trello = {
                    'idList': created_sprint['id'],
                    'key': config["apiSecurity"]["trelloKey"],
                    'token': config["apiSecurity"]["trelloToken"],
                    'name': '(' + str(user_story_model.userStoryDetails.storyPoints) + ') ' + user_story_model.name,
                    'desc': user_story_model.userStoryBody.storyDescription.value,
                    'idMembers': story_member_ids,
                    'idLabels': story_label_ids
                }
            self.create_new_ticket_on_trello(story_payload_trello)
            

    def create_sprint_user_stories_jira(self, sprint_user_stories_model, config):
    
        for user_story_model in sprint_user_stories_model: 
            story_payload_jira = {
                "fields":{
                    "project":{
                        "key":config["boardsInfo"]["jiraProjectKey"],
                    },
                    "summary":'(' + str(user_story_model.userStoryDetails.storyPoints) + ') ' + user_story_model.name,
                    "description": user_story_model.userStoryBody.storyDescription.value,
                    "issuetype":{
                        "name":"Story"
                    },
                    "assignee": {
                         "id": config["boardsInfo"]["assignJiraMemberToTickets"]
                     },
                    "labels": self.get_story_label_names(user_story_model)
                }
            }
            self.create_new_ticket_on_jira(story_payload_jira, config)  

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

    def get_story_label_names(self, user_story_model):
        story_label_names = []
       
        for user_story_label_model in user_story_model.userStoryDetails.storyLabels:
            story_label_names.append(user_story_label_model.name.lower() )

        return story_label_names

    def get_all_board_members(self, config):
        url = f'https://api.trello.com/1/boards/{config["boardsInfo"]["idTrelloBoard"]}/members'

        headers = {"Accept": "application/json"}

        payload = {
            'key': config["apiSecurity"]["trelloKey"],
            'token': config["apiSecurity"]["trelloToken"],
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=payload
        )

        return json.loads(response.text)


    def get_all_board_labels(self, config):
        url = f'https://api.trello.com/1/boards/{config["boardsInfo"]["idTrelloBoard"]}/labels'

        payload = {
            'key': config["apiSecurity"]["trelloKey"],
            'token': config["apiSecurity"]["trelloToken"],
        }

        response = requests.request(
            "GET",
            url,
            params=payload
        )

        return json.loads(response.text)


    def create_new_sprint_on_trello(self, sprint, config):

        sprint_payload = {
                'idBoard': config["boardsInfo"]["idTrelloBoard"],
                'key': config["apiSecurity"]["trelloKey"],
                'token': config["apiSecurity"]["trelloToken"],
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

    def create_new_ticket_on_jira(self, story_payload_jira, config):
        # Base encode email and api token
        loginConfig = f'{config["apiSecurity"]["jiraUserMail"]}:{config["apiSecurity"]["jiraToken"]}'
        cred =  "Basic " + base64.b64encode(loginConfig.encode('ascii')).decode("utf-8") 

        # Update your site url 
        url = f'https://{config["apiSecurity"]["jiraUserSite"]}.atlassian.net/rest/api/2/issue/'

        # Set header parameters
        headers = {
            "Content-Type": "application/json",
            "Authorization" : cred
        }

        response = requests.request(
                "POST",
                url,
                headers=headers,
                json=story_payload_jira
        )
            
        print('Jira', json.loads(response.text))
        
    def get_all_board_members_jira(self, projectKey, config):
        # Base encode email and api token
        loginConfig = f'{config["apiSecurity"]["jiraUserMail"]}:{config["apiSecurity"]["jiraToken"]}'
        cred =  "Basic " + base64.b64encode(loginConfig.encode('ascii')).decode("utf-8") 

        url = f'https://{config["apiSecurity"]["jiraUserSite"]}.atlassian.net/rest/api/3/user/assignable/multiProjectSearch'

        # Set header parameters
        headers = {
            "Content-Type": "application/json",
            "Authorization" : cred
        }

        query = {
            'query': 'query',
            'projectKeys': config["boardsInfo"]["jiraProjectKey"]
        }

        response = requests.request(
                "GET",
                url,
                headers=headers,
                params=query,
        )
        return response.text
        

def connect_with_jira_and_dispaly_all_issues(config):
    # Base encode email and api token
    loginConfig = f'{config["apiSecurity"]["jiraUserMail"]}:{config["apiSecurity"]["jiraToken"]}'
    cred =  "Basic " + base64.b64encode(loginConfig.encode('ascii')).decode("utf-8") 
    # Set header parameters
    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization" : cred
    }

    url = f'https://{config["apiSecurity"]["jiraUserSite"]}.atlassian.net/rest/api/3/search?jql=project=' + config["boardsInfo"]["jiraProjectKey"]

    # Send request and get response
    response = requests.request(
    "GET", 
    url,
    headers=headers
    )

    # Decode Json string to Python
    json_data = json.loads(response.text)

    # Display issues
    for item in json_data["issues"]:
        print(item["id"] + "\t" + item["key"] + "\t" +
            item["fields"]["issuetype"]["name"] + "\t" +
            item["fields"]["created"]+ "\t" +
            item["fields"]["creator"]["displayName"] + "\t" +
            item["fields"]["status"]["name"] + "\t" +
            item["fields"]["summary"] + "\t" 
            )

# Extracting all the cards in all boards FROM TRELLO:
def extracte_all_cards_from_all_boards(config):
    url_member = "https://api.trello.com/1/members/malibajojszd"
    querystring = {"key":config["apiSecurity"]["trelloKey"],"token":config["apiSecurity"]["trelloToken"],}
    response_member = requests.request("GET", url_member, params=querystring)

    data_member = json.loads(response_member.text)
    board_ids = data_member['idBoards']
  
    for board_id in board_ids:
        url_board_cards = "https://api.trello.com/1/boards/" + board_id +"/cards"
        response_board_cards = requests.request("GET", url_board_cards, params=querystring)
        data_board_cards = json.loads(response_board_cards.text)

def main():

    this_folder = dirname(__file__)

    scrum_mm = metamodel_from_file(join(this_folder, 'scrum.tx'), debug=False)
    scrum_model = scrum_mm.model_from_file(join(this_folder, 'sprintOne.scrum'))

    scrum = Scrum()

    #extracte_all_cards_from_all_boards()
    #connect_with_jira_and_dispaly_all_issues()

    if(scrum.is_model_semantically_valid(scrum_model)):
        scrum.interpret(scrum_model)

if __name__ == "__main__":
    main()