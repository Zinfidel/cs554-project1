from automata import Automata
import scanner

def dfa_valid_string(automata, testing_string, current_state, current_step):
    if(current_step == len(testing_string)):
        for x in automata.accepts:
            if(current_state == x): return True
        return False
    else:
        next_state = dfa.nodes[current_state].getTransitionState(testing_string[current_step])
        if (next_state == None): return False
        else: return dfa_valid_string(automata,testing_string,next_state,current_step+1)

dfa = scanner.ConstructAutomata("testdata/dfa2.txt")
start = dfa.getStartStates()[0];
string = "aaaaaaaa";
print dfa_valid_string(dfa,string,start,0);