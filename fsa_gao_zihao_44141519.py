"""
This is a python module for deterministic finite state automaton.
It is coded in python 2.7.2.with UTF-8 under windows 7.

The options and argument should be as follows:

    cat automaton.fsa  |  fsa_gao_zihao_44141519.py  string

or:

    fsa_gao_zihao_44141519.py  string  <  automaton.fsa

The program will read the standard input.
Here the file automaton.fsa becomes the standard input.
The standard input will contain an automaton in the format described below.
The program will output True or False depending on whether string is accepted by the automaton or not.

The format of the file standard input should be as illustrated in the following example:
---------------------------------------------------
initial: q0
final: q0, q1
q0 -- a --> q1
q0 -- b --> q1
q1 -- b --> q1
--------------------------------------------------
The lines may be in any order.
"""


__author__ = 'GAO_ZIHAO_44141519'
import sys

class DFSA:
    """The deterministic finite state automaton.

    Read start state, final states and transitions from file.
    Output the result True or False for one input sequence each time.
    The method for removing unreachable states and minimizing is also provided.
    """
    def __init__(self):
        self.transitions = {}   # Use dict() to store the transitions of this automaton
        self.final_states = {}
        self.start_state = None
        self.current_state = None
        self.states = []    # All the states in the automaton
        self.vocabulary = []    # vocabulary of the language recognized

    def add_transition(self,state,symbol,next_state):
        """Add a new transition to the automaton."""
        self.transitions[(state,symbol)] = next_state

    def set_initial_state(self,state):
        """Set the start state of the automaton."""
        self.start_state = state

    def set_final_states(self,state):
        """Set the final states of the automaton."""
        self.final_states[state] = True

    def set_states(self):
        """Collect all the states as a list in the automaton.

        Invoked by minimize() when minimizing the automaton.
        """
        self.states = list(set(self.transitions.values()+list([self.start_state])))

    def reset_final_states(self):
        """Clear the final states."""
        self.final_states.clear()

    def reset_transitions(self):
        """Clear the transitions."""
        self.transitions.clear()

    def get_states(self):
        """Return the list of all the states in the automaton.

        Invoked by minimize() when minimizing the automaton.
        """
        return self.states

    def set_vocabulary(self):
        """Collect all the input symbol as a list for the automaton.

        Invoked by minimize() when minimizing the automaton.
        """
        transition_pairs = self.transitions.keys()
        for i in range(len(transition_pairs)):
                self.vocabulary.append(transition_pairs[i][1])
        self.vocabulary = list(set(self.vocabulary))

    def get_vocabulary(self):
        """Return the list of all the input symbol for the automaton.

        Invoked by minimize() when minimizing the automaton.
        """
        return self.vocabulary

    def delta(self,state,symbol):
        """Delta function of the automaton

        For each tuple of (state,symbol) return next state.
        """
        current_pair = (state,symbol)
        new_state = 'fail'
        if self.transitions.has_key(current_pair):
            new_state = self.transitions[current_pair]
        return new_state

    def is_final(self,state):
        """Return the result whether the input state is a final state."""
        return self.final_states.get(state,False)

    def accept(self,sequence):
        """Decide if a string of sequence is acceptable by this automaton.

        Return True for acceptable and False for not.
        """
        self.current_state = self.start_state
        for i in range(len(sequence)):
            self.current_state = self.delta(self.current_state,sequence[i])
            if self.current_state == 'fail':
                return False    # Skip the rest of loop to save time
        if self.is_final(self.current_state):
            return True
        else:
            return False

    def trim(self):
        """Remove unreachable states in this automaton.

        Delete corresponding items in transitions.
        """
        state_and_symbol = self.transitions.keys()
        next_state = list(set(self.transitions.values()))
        for i in range(len(state_and_symbol)):
            if state_and_symbol[i][0] not in next_state:
                if state_and_symbol[i][0] != self.start_state:  # Ignore start state
                    del self.transitions[state_and_symbol[i]]

    def minimize(self):
        """Minimize the automaton.

        Using Moore's algorithm to minimize the automaton.
        trim() is supposed to be invoked in advance.
        Reset the start state, final state and transitions of this automaton.
        """
        self.set_states()
        self.set_vocabulary()
        n = 1   # Previous number of classes
        classes = {}
        states = self.get_states()
        vocabulary = self.get_vocabulary()
        for q in states:
            classes[q] = (0,) if q in self.final_states else (1,)
        # Separate the non-final states and final states
        new_classes = classes.copy() # Temporary dictionary
        # Compare the number of previous classes and current ones
        while len(set(classes.values())) != n:
            n = len(set(classes.values()))
            for q in states:
                for v in vocabulary:
                    if self.transitions.has_key((q,v)):
                        new_classes[q] = classes[q] + tuple([classes[self.delta(q,v)]])
                        # Divide the classes
            classes = new_classes
        reversed_classes = dict([(classes[q],q) for q in states])
        new_states = reversed_classes.keys()    # Get new states
        # Get new final states
        new_final_states = set()
        for q in self.final_states:
            new_final_states.add(classes[q])
        self.reset_final_states()
        for q in new_final_states:
            self.set_final_states(q)
        # Get new transitions for automaton
        temp_transitions = self.transitions.copy()
        self.reset_transitions()
        for q in new_states:
            for v in vocabulary:
                if temp_transitions.has_key((reversed_classes[q],v)):
                    self.add_transition(q,v,classes[temp_transitions[(reversed_classes[q],v)]])
        # Get new start state
        self.set_initial_state(classes[self.start_state])


def read_states(line):
    """Read the states from input line.

    Return the list of states.
    """
    str = line.replace(' ','')
    str = str.replace('initial:','')
    str = str.replace('final:','')
    return str.split(',')

def read_transition(line):
    """Read the transitions from input line.

    return the list of states and symbol.
    """
    str = line.replace(' ','')
    str = str.replace('>','')
    return str.split('--')

if __name__ == "__main__":
    if len(sys.argv)<2:
        print 'No action specified.'
        sys.exit()
    else:
            #f = file(sys.argv[2])
            sequence = sys.argv[1]
            dfsa = DFSA()
            while True:
                line = sys.stdin.readline().strip('\n')
                if len(line) == 0:
                    break
                elif line.startswith('initial'): # Read start states
                    initial_state = read_states(line)
                    dfsa.set_initial_state(initial_state[0])
                elif line.startswith('final'): # Read final states
                    final_states = read_states(line)
                    for i in range(len(final_states)):
                        dfsa.set_final_states(final_states[i])
                else:   # Read transitions
                    transition = read_transition(line)
                    dfsa.add_transition(transition[0],transition[1],transition[2])
            # The following two functions can be skipped
            dfsa.trim() # Remove the unreachable states
            dfsa.minimize() # Minimize the automaton
            
            if dfsa.accept(sequence):
                print 'true'
            else:
                print 'false'



        