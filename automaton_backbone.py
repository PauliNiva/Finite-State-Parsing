  # !/usr/bin/env python
# -*- coding: utf-8 -*-

# Running:   python automaton_backbone.py
# This code should do four things:
#   - visualize
#   - test string membership
#   - enumerate a slice of the language
#   - print the automaton in the ATT column format


# We represent an automaton as a list of arcs and finals states, assuming that the initial state is 0
fstates = [2]
arcs = [[0, 1, "a:0"],
        [1, 1, "b"],
        [1, 2, "c:0"],
        [0, 3, "a"],
        [3, 2, "c"],
        [3, 4, "0:d"],
        [4, 4, "b"],
        [4, 2, "c:d"],
        [3, 5, "b"],
        [5, 5, "b"],
        [5, 2, "c"]]


def extract_states(arcs, fstates):
    # collect the set of states
    states = fstates
    for [s, t, a] in arcs:
        if s not in states:
            states = states + [s]
        if t not in states:
            states = states + [t]
    return states


# prints the FSM for dot programing in Graphiviz.  Copy and paste the output to a file.dot and save
# then compile with command: dot -Tpdf file.dot >file.pdf
def viz(arcs, fstates):
    # print the header
    print "--cut here--"
    print "digraph A { font = \"Courier\"; margin = 0; rankdir = LR; ranksep=0; nodesep = .2;"
    # print states
    for s in extract_states(arcs, fstates):
        if s not in fstates:
            print("node [fixedsize = false, width = 0.2, fontsize = 16, shape = circle, style = solid] {:d};".format(s))
        else:
            print("node [fixedsize = false, width = 0.2, fontsize = 16, shape = doublecircle, style =s olid] {:d};".format(s))
    # print arcs
    for [s, t, a] in arcs:
        print("{:d} -> {:d} [arrowsize = .65, fontsize = 16,label = \"{:s}\"];".format(s, t, a))
    # print the arrow to the state 0 that is now considered as the only initial state
    print "node [width = 0.04, style = invis, fontsize = 1, fixedsize = true, shape = circle] 00;"
    print "00 -> 0 [arrowsize = .65, fontsize = 10];"
    # print the trailer
    print "}"
    print "--cut here--"


# prints successful and non-successful paths for the argument string:
# arguments: path = "", curr = 0, string = the string, arcs/fstates = fsm
def member(path, curr, string, arcs, fstates):
    if string == []:
        if curr in fstates:
            print path, "successful"
        else:
            print path, "unsuccessful"
        return
    block = 1
    for [s, t, a] in arcs:
        if (curr == s) and (string[0] == a):
            block = 0
            member(path + " {:s}->{:d}".format(a, t), t, string[1:], arcs, fstates)
    if block == 1:
        print path, "unsuccessful"
        return


# enumerates all strings of length "length"
# arguments: path = "", curr = 0, length = the length, arcs/fstates = fsm
def enum(path, curr, length, arcs, fstates):
    if length == 0:
        print path
    if length > 0:
        for [s, t, a] in arcs:
            if curr == s:
                formattedarc = " {:s} ({:d})".format(a, t)
                enum(path + formattedarc, t, length - 1, arcs, fstates)


# print the automaton in the column format:
def print_att(arcs, fstates):
    for [s, t, a] in arcs:
        print("{:d}\t{:d}\t{:s}".format(s, t, a))
    for s in fstates:
        print s

# MAIN PROGRAM:
# call the function to visualize
viz(arcs, fstates)

# call the function to match a string
member("", 0, ["a", "b", "b", "c:0"], arcs, fstates)
member("", 0, ["a:0", "b", "b", "c:0"], arcs, fstates)

# call the function to enumerate all strings of a given length
print "0:"
enum("", 0, 0, arcs, fstates)
print "1:"
enum("", 0, 1, arcs, fstates)
print "2:"
enum("", 0, 2, arcs, fstates)
print "3:"
enum("", 0, 3, arcs, fstates)
print "4:"
enum("", 0, 4, arcs, fstates)

print_att(arcs, fstates)



