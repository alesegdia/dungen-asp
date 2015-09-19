
import re

def build_data(programstr):
    programdata = {}
    r = re.compile(r'([a-zA-Z_]+)\(([\-a-zA-Z,\(\)0-9]+)\)\.')
    for fact in programstr.split():
        gs = r.match(fact).groups()
        predicate = gs[0]
        args = gs[1]
        if predicate not in programdata:
            programdata[predicate] = []
        programdata[predicate].append(args)
        # programdata[predicate].append([arg for arg in args.split(",")])
    return programdata

