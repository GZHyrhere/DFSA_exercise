# DFSA_exercise
an exercise for implemention of deterministic finite state automaton in python

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
