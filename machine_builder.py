
import random

from action import Action
from machine import Machine


class MachineBuilder:
    colour_list = [(255,0,0),(0,0,255)]
    machine_name_iterator = 0


    def __init__(self, board_width: int):
         self.board_width = board_width
         self.colour_iteration = 0

    def random_machine(self):
        states = self.pick_random_states()
        name = self.pick_name()

        self.print_machine(name, states)
        return Machine(
             name,
             self.board_width // 2,
             self.board_width // 2,
             states,
             self.pick_colour()
        )

    def machine_from_string_input(self, string: str):
        """
        Receives a string and outputs a machine.
        platypus(1475986,[t(y,k,y,w,gg),t(g,k,y,p,gg),t(y,e,y,e,wa),t(g,e,y,k,gg),t(y,w,y,k,gg),t(g,w,y,w,gg),t(y,p,y,p,wa)]).
        """

        if string == '': return False
        name_start_index = string.find('(')
        name_end_index = string.find(',')
        name = string[name_start_index+1:name_end_index]
        state_start_index = string.find('[')
        state_end_index = string.find(']')
        state_string = string[state_start_index+1:state_end_index]
        states_list = state_string.split('),t(')
        states_list[0] = states_list[0][2:]
        states_list[-1] = states_list[-1][:-1]
        states = {}
        for state in states_list:
            state_items = state.split(',')
            states[(state_items[0], state_items[1])] = Action(state_items[2], state_items[3], state_items[4])

        self.print_machine(name, states)
        return Machine(name, self.board_width // 2, self.board_width // 2, states, self.pick_colour())
    
    def pick_colour(self):
        if len(self.colour_list) > self.colour_iteration:
            self.colour_iteration += 1
            return self.colour_list[self.colour_iteration-1]
        else:
             return (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        
    def pick_name(self):
        self.machine_name_iterator += 1
        return 'random' + str(self.machine_name_iterator)
        
    def pick_random_states(self):
        return {
            ('y','k'):random_action(),
            ('g','k'):random_action(),
            ('y','e'):random_action(),
            ('g','e'):random_action(),
            ('y','w'):random_action(),
            ('g','w'):random_action(),
            ('y','p'):random_action(),
        }

    def print_machine(self, name, states):
        print("\nNew Machine", name)
        for state, action in states.items():
            print('('+state[0]+','+state[1]+','+str(action)+')')
        print("\n")

def random_action():
        random_colour = random.choice(['y','g'])
        random_animal = random.choice(['k', 'e', 'w', 'p'])
        random_tree = random.choice(['gg', 'wa'])
        return Action(random_colour, random_animal, random_tree)

