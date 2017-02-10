# DFSA_exercise
An exercise for implemention of deterministic finite state automaton in python
<br>
<br>
<br>
This is a python module for deterministic finite state automaton.<br>
It is coded in python 2.7.2.with UTF-8 under windows 7.<br>

The options and argument should be as follows:

    cat automaton.fsa  |  fsa_gao_zihao_44141519.py  string

or:

    fsa_gao_zihao_44141519.py  string  <  automaton.fsa

The program will read the standard input.<br>
Here the file automaton.fsa becomes the standard input.<br>
The standard input will contain an automaton in the format described below.<br>
The program will output True or False depending on whether string is accepted by the automaton or not.<br>
<br>
The format of the file standard input should be as illustrated in the following example:
<br>
<br>
initial: q0<br>
final: q0, q1<br>
q0 -- a --> q1<br>
q0 -- b --> q1<br>
q1 -- b --> q1<br>
<br>
The lines may be in any order.
