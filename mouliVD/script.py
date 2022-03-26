import sys
import os
from moulitek.moulitek import *

data = ["BAD"]
poll = Category("Poll", "Test on poll Dockerfile")
result = Category("Result", "Test on Result Dockerfile")
worker = Category("Worker", "Test on Worker Dockerfile")
compose = Category("Docker-compose", "Test on your Docker-compose file")

def get_trace(txt):
    data = []
    txt = txt + " > trace"
    os.system(txt)
    try:
        text_file = open("trace", "r")
        data = text_file.read()
        data = [e for e in data.split('\n') if len(e) > 0]
        text_file.close()
    except:
        data = []
        data.append("BAD")
    os.system("rm trace")
    return data

def get_elem(lst, to_find):
    for elem in lst:
        if to_find in elem:
            return elem
    return "Oups"

## POLL TESTS ##

data = get_trace("python poll.py")

poll_name = ["VERSION", "COPY", "WORKDIR","EXPOSE", "RUN", "LAUNCH"]

for elem in poll_name:
    poll_seq = 0
    poll_seq = poll.add_sequence(elem)
    poll_seq.add_test(elem)
    if elem in data or "BAD" in data:
        poll_seq.set_status(elem, False, BADOUTPUT, expected="OK", got="KO")
    else:
        poll_seq.set_status(elem, True)


data = get_trace("python result.py")

result_name = ["IGNORE", "VERSION", "COPY", "WORKDIR","EXPOSE", "RUN", "LAUNCH"]

for elem in result_name:
    result_seq = 0
    result_seq = result.add_sequence(elem)
    result_seq.add_test(elem)
    if elem in data or "BAD" in data:
        result_seq.set_status(elem, False, BADOUTPUT, expected="OK", got="KO")
    else:
        result_seq.set_status(elem, True)


data = get_trace("python worker.py")

worker_name = ["MAVEN VERSION", "MAVEN COPY", "MAVEN WORKDIR", "MAVEN RUN DEPEDENCY","MAVEN RUN PACKAGE", "OPEN VERSION", "OPEN EXPOSE", "OPEN COPY", "OPEN WORKDIR", "OPEN LAUNCH"]

for elem in worker_name:
    worker_seq = 0
    worker_seq = worker.add_sequence(elem)
    worker_seq.add_test(elem)
    if elem in data or "BAD" in data:
        worker_seq.set_status(elem, False, BADOUTPUT, expected="OK", got="KO")
    else:
        worker_seq.set_status(elem, True)


data = get_trace("python compose.py")

## version compose
compose_seq = compose.add_sequence("version")
compose_seq.add_test("version")
if any("version" in s for s in data):
    compose_seq.set_status("version", False, BADOUTPUT, expected="OK", got="KO")
else:
    compose_seq.set_status("VERSION", True)


## POLL compose

compose_seq = compose.add_sequence("Poll service")
compose_seq.add_test("Poll service")
if any("poll" in s for s in data):
    compose_seq.set_status("Poll service", False, BADOUTPUT, expected="OK", got=get_elem(data, "poll"))
else:
    compose_seq.set_status("Poll service", True)

## WORKER compose

compose_seq = compose.add_sequence("worker service")
compose_seq.add_test("worker service")
if any("worker" in s for s in data):
    compose_seq.set_status("worker service", False, BADOUTPUT, expected="OK", got=get_elem(data, "worker"))
else:
    compose_seq.set_status("worker service", True)

## RESULT compose

compose_seq = compose.add_sequence("result service")
compose_seq.add_test("result service")
if any("result" in s for s in data):
    compose_seq.set_status("result service", False, BADOUTPUT, expected="OK", got=get_elem(data, "result"))
else:
    compose_seq.set_status("result service", True)

## REDIS compose

compose_seq = compose.add_sequence("redis service")
compose_seq.add_test("redis service")
if any("redis" in s for s in data):
    compose_seq.set_status("redis service", False, BADOUTPUT, expected="OK", got=get_elem(data, "redis"))
else:
    compose_seq.set_status("redis service", True)

## DB compose

compose_seq = compose.add_sequence("db service")
compose_seq.add_test("db service")
if any("db" in s for s in data):
    compose_seq.set_status("db service", False, BADOUTPUT, expected="OK", got=get_elem(data, "db"))
else:
    compose_seq.set_status("db service", True)

## VOLUMES compose

compose_seq = compose.add_sequence("volumes")
compose_seq.add_test("volumes")
if any("volumes" in s for s in data):
    compose_seq.set_status("volumes", False, BADOUTPUT, expected="OK", got="KO")
else:
    compose_seq.set_status("volumes", True)

## NETWORKS compose

compose_seq = compose.add_sequence("networks")
compose_seq.add_test("networks")
if any("networks" in s for s in data):
    compose_seq.set_status("networks", False, BADOUTPUT, expected="OK", got="KO")
else:
    compose_seq.set_status("networks", True)

gen_trace()