from os.path import join, dirname
from textx import metamodel_from_file

class Scrum(object):


    def interpret(self, model):
            print(model)


def main():

    this_folder = dirname(__file__)

    scrum_mm = metamodel_from_file(join(this_folder, 'scrum.tx'), debug=False)
    scrum_model = scrum_mm.model_from_file(join(this_folder, 'sprintOne.scrum'))

    scrum = Scrum()
    scrum.interpret(scrum_model)


if __name__ == "__main__":
    main()