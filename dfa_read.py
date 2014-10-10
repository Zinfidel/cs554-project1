import scanner


def dfa_valid_string(automata, testing_string, current_state, current_step):
    if current_step == len(testing_string):
        for x in automata.accepts:
            if current_state == x: return True
        return False
    else:
        next_state = dfa.nodes[current_state].getTransitionState(testing_string[current_step])
        if next_state is None: return False
        else: return dfa_valid_string(automata, testing_string, next_state, current_step + 1)

if __name__ == "__main__":
    dfa = scanner.ConstructAutomata("testdata/dfa2.txt")
    start = dfa.getStartState()[0]
    string = "aaaaaaaa"
    print dfa_valid_string(dfa, string, start, 0)