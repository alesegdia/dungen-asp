from subprocess import Popen, PIPE, STDOUT

def clingo_spawn(*sources):
	source = ''.join(sources)
	clingo_process = Popen(['clingo-3.0.5', '--asp09'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	clingo_stdout = clingo_process.communicate( input = b'' + source )[0]
	return clingo_stdout
