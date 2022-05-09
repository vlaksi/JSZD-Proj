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
            payload={'title': 'foo','body': 'bar','userId': 1}
            r = requests.post('https://jsonplaceholder.typicode.com/posts', data=payload)
            print(r.status_code)
            print(r.text)
            print(r.ok)
            print(r.url)
            print(r.json())


def main():

    this_folder = dirname(__file__)

    scrum_mm = metamodel_from_file(join(this_folder, 'scrum.tx'), debug=False)
    scrum_model = scrum_mm.model_from_file(join(this_folder, 'sprintOne.scrum'))

    scrum = Scrum()
    scrum.interpret(scrum_model)


if __name__ == "__main__":
    main()