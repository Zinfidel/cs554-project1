def dfa_valid_string(automata, testing_string, current_state=None, current_step=0):
    if current_state is None:
        current_state = automata.start

    if current_step == len(testing_string):
        # for x in automata.accepts:
        #     if current_state == x: return True
        # return False
        return current_state in automata.accepts
    else:
        next_state = automata.nodes[current_state]\
            .getTransitionState(testing_string[current_step])
        if next_state is None:
            return False
        else:
            next_state = next_state[0].name  # DFA - should only be one state.
            return dfa_valid_string(automata, testing_string,
                                    next_state, current_step + 1)
