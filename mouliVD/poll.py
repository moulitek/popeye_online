test_passed = []
test_failed = []
try:
    text_file = open("poll/Dockerfile", "r")
    data = text_file.read().split('\n')
    text_file.close()
except:
    print("FILE")
    exit(84)

poll_obj = {
    "img_version": None,
    "cpy": None,
    "run": None,
    "expose": None,
    "cmd": None,
    "locate": None,
    "workdir": None
}


def check_launch():
    founded = 0
    txt = poll_obj["cmd"]
    txt = txt.replace(',', ' ')
    txt = txt.replace(']', ' ')
    txt = txt.replace('[', ' ')
    txt = txt.replace('"', ' ')
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "flask":
            founded += 1
        if elem == "run":
            founded += 1
        if elem == "--host=0.0.0.0":
            founded += 1
    return founded == 3

def check_run():
    founded = 0
    txt = poll_obj["run"]
    txt = txt.replace(',', ' ')
    txt = txt.replace(']', ' ')
    txt = txt.replace('[', ' ')
    txt = txt.replace('"', ' ')
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "pip3":
            founded += 1
        if elem == "install":
            founded += 1
        if elem == "-r":
            founded += 1
        if elem == "requirements.txt":
            founded += 1
    return founded == 4

def check_expose():
    txt = poll_obj["expose"]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    if len(tmp) != 2:
        return 0
    if tmp[0] == "EXPOSE" and tmp[1] == "80":
        return 1
    return 0

def init_dict():
    for i in data:
        if "FROM" in i:
            poll_obj["img_version"] = i
        if "COPY" in i:
            poll_obj["cpy"] = i
        if "RUN" in i:
            poll_obj["run"] = i
        if "EXPOSE" in i:
            poll_obj["expose"] = i
        if "CMD" in i:
            poll_obj["cmd"] = i
        if "WORKDIR" in i:
            poll_obj["workdir"] = i
    if (poll_obj["cpy"] != None):
        poll_obj["locate"] = poll_obj["cpy"][7:]
    else:
        poll_obj["locate"] = "."

init_dict()

# TEST PYTHON VERSION
if (poll_obj["img_version"] == None):
    test_failed.append("VERSION")
else:
    if poll_obj["img_version"].startswith("FROM python:"):
        test_passed.append("VERSION")
    else:
        test_failed.append("VERSION")

# TEST DE COPY
if (poll_obj["cpy"] == None):
    test_failed.append("COPY")
else:
    if poll_obj["cpy"].startswith("COPY . ") and len(poll_obj["cpy"]) > 7:
        test_passed.append("COPY")
    else:
        test_failed.append("COPY")

# TEST WORKDIR TP IF NOT IN THE ROOT
if (poll_obj["locate"] != "." and poll_obj["workdir"] == None):
    test_failed.append("WORKDIR")

if (poll_obj["workdir"] != None):
    if not poll_obj["workdir"].endswith(str(poll_obj["locate"])):
        test_failed.append("WORKDIR")

# TEST THE RUN CMD
if (poll_obj["run"] == None):
    test_failed.append("RUN")
else:
    if check_run():
        test_passed.append("RUN")
    else:
        test_failed.append("RUN")
# TEST THE EXPOSE
if (poll_obj["expose"] == None):
    test_failed.append("EXPOSE")
else:
    if check_expose():
        test_passed.append("EXPOSE")
    else:
        test_failed.append("EXPOSE")
# TEST THE LAUNCH
if (poll_obj["cmd"] == None):
    test_failed.append("LAUNCH")
else:
    if check_launch():
        test_passed.append("LAUNCH")
    else:
        test_failed.append("LAUNCH")

if (len(test_failed) == 0):
    print("GG")
else:
    for elem in test_failed:
        print(elem)
    if len(test_passed) == 0:
        print("BAD")