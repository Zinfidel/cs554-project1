#!/usr/bin/env python

from automata import *
from regex import *

'''
General notes for Thompson's construction:

There is always just one start and accept state for any nfa. That means that whenever nfas are combined
that start/accept states are cleared and set to new, single states appropriate to the kind of combination.

When combining nfas, instead of creating an all new automaton, the "left" automata will just inherit all
of the "right" automata's states and the right automata will be discarded. The left automata then acts as
the new combined nfa.
'''


EPSILON = '\0'
__next_node_id = 0


def __nextName():
    """Returns a unique state name (i.e.: s0, s1, etc.)."""
    global __next_node_id
    __next_node_id += 1
    return 's' + str(__next_node_id)


def constructCharacter(character):
    """Constructs a character transition automaton.
       :param str character: Transition character.
       :rtype: Automata
    """

    # Create two states with transition between them.
    s0, s1 = AutomataNode(__nextName()), AutomataNode(__nextName())
    s0.addTransition(s1.name, character)

    # Install the states into an nfa.
    nfa = Automata()
    nfa.addNodes([s0, s1])
    nfa.start = s0.name
    nfa.accepts = [s1.name]
    nfa.alphabet.add(character)

    return nfa


def constructConcatenation(left, right):
    """Constructs a concatenation automaton from two other automata.
       :param Automata left: Left side automaton to concatenate.
       :param Automata right: Right side automaton to concatenate.
       :rtype: Automata
    """

    # Merge the right automata into the left.
    left.addNodes(right.nodes.values())
    left.accepts = right.accepts
    left.alphabet |= right.alphabet

    # Add an epsilon transition from the accept state of left to the start state of the right.
    for node in left.accepts:
        left.nodes[node].addTransition(right.start, EPSILON)

    return left


def constructAlternative(left, right):
    """Constructs an alternative automaton from two other automata.
       :param Automata left: Left side automaton to alternate.
       :param Automata right: Right side automaton to alternate.
       :rtype: Automata
    """

    # Merge the right automata into the left.
    left.addNodes(right.nodes.values())
    left.alphabet |= right.alphabet

    # New start and accept states
    newStart, newAccept = AutomataNode(__nextName()), AutomataNode(__nextName())
    left.addNodes([newStart, newAccept])

    # Epsilon transitions from the new start state to the start states of the combined automata,
    # and epsilon transitions from the combined automata accept states to the new accept state.
    newStart.addTransition(left.start, EPSILON)
    newStart.addTransition(right.start, EPSILON)
    left.nodes[left.accepts[0]].addTransition(newAccept.name, EPSILON)
    left.nodes[right.accepts[0]].addTransition(newAccept.name, EPSILON)

    # Set combined automaton start/accept states.
    left.start = newStart.name
    left.accepts = [newAccept.name]

    return left


def constructRepetition(left):
    """Constructs an alternative automaton from two other automata.
       :param Automata left: Left side automaton to alternate.
       :rtype: Automata
    """

    # New start and accept states
    newStart, newAccept = AutomataNode(__nextName()), AutomataNode(__nextName())
    left.addNodes([newStart, newAccept])

    # Epsilon transitions from the new start to the original start and to the new accept.
    newStart.addTransition(left.start, EPSILON)
    newStart.addTransition(newAccept.name, EPSILON)

    # Epsilon transition from the original accept to the new accept and original start.
    left.nodes[left.accepts[0]].addTransition(newAccept.name, EPSILON)
    left.nodes[left.accepts[0]].addTransition(left.start, EPSILON)

    # Set automaton's new start and accept states.
    left.start = newStart.name
    left.accept = [newAccept.name]

    return left


def convertRegexToNFA(node):
    """Constructs an NFA from a supplied regular expression tree.
       :param Production node: The current node of the regular expression tree being evaluated.
       :rtype: Automata
    """

    if isinstance(node, Sigma):
        return constructCharacter(node.sigma)
    elif isinstance(node, Repetition):
        expr = convertRegexToNFA(node.expr)
        return constructRepetition(expr)
    elif isinstance(node, Alternative):
        left = convertRegexToNFA(node.left)
        right = convertRegexToNFA(node.right)
        return constructAlternative(left, right)
    elif isinstance(node, Concatenation):
        left = convertRegexToNFA(node.left)
        right = convertRegexToNFA(node.right)
        return constructConcatenation(left, right)
    else:
        pass
