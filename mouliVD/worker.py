test_passed = []
test_failed = []

poll_maven = {
    "img_version": None,
    "cpy": None,
    "run": [],
    "locate": None,
    "workdir": None
}

try:
    file = open("worker/Dockerfile", "r")
    data = file.read().split('FROM')
    file.close()
except:
    print("FILE")
    exit(84)

if (len(data) > 1):
    maven = [e for e in data[1].split('\n') if len(e) > 0]
else:
    maven = None
if (len(data) > 2):
    open = [e for e in data[2].split('\n') if len(e) > 0]
else:
    open = None

def init_dict_maven():
    if maven == None:
        return 0
    poll_maven["img_version"] = maven[0].strip()
    for i in maven:
        if "COPY" in i:
            poll_maven["cpy"] = i
        if "RUN" in i:
            poll_maven["run"].append(i)
        if "CMD" in i:
            poll_maven["cmd"] = i
        if "WORKDIR" in i:
            poll_maven["workdir"] = i
    if (poll_maven["cpy"] != None):
        poll_maven["locate"] = poll_maven["cpy"][7:]
    else:
        poll_maven["locate"] = "."


def init_dict_open():
    if open == None:
        return 0
    poll_open["img_version"] = open[0].strip()
    for i in open:
        if "COPY" in i:
            poll_open["cpy"] = i
        if "RUN" in i:
            poll_open["run"]
        if "CMD" in i:
            poll_open["cmd"] = i
        if "WORKDIR" in i:
            poll_open["workdir"] = i
    if (poll_open["cpy"] != None):
        poll_open["locate"] = poll_open["cpy"].split(' ')
        poll_open = poll_open[len(poll_open)]
    else:
        poll_open["locate"] = "."


def check_run_maven_one():
    founded = 0
    txt = poll_maven["run"][0]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "mvn":
            founded += 1
        if elem == "dependency:resolve":
            founded += 1
    return founded == 2


def check_run_maven_two():
    founded = 0
    txt = poll_maven["run"][1]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "mvn":
            founded += 1
        if elem == "package":
            founded += 1
    return founded == 2


def check_maven_img():
    founded = 0
    txt = poll_maven["run"]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "maven:3.8.4-jdk-11-slim":
            founded += 1
        if elem == "as" or elem == "AS":
            founded += 1
        if elem == "builder":
            founded += 1
    return founded == 3


init_dict_maven()
# =============   TEST MAVEN ==============


# TEST PYTHON VERSION
if (poll_maven["img_version"] == None):
    test_failed.append("MAVEN VERSION")
else:
    if check_maven_img:
        test_passed.append("MAVEN VERSION")
    else:
        test_failed.append("MAVEN VERSION")

# TEST DE COPY
if (poll_maven["cpy"] == None):
    test_failed.append("MAVEN COPY")
else:
    if poll_maven["cpy"].startswith("COPY . ") and len(poll_maven["cpy"]) > 7:
        test_passed.append("MAVEN COPY")
    else:
        test_failed.append("MAVEN COPY")

# TEST WORKDIR TP IF NOT IN THE ROOT
if (poll_maven["locate"] != "." and poll_maven["workdir"] == None):
    test_failed.append("MAVEN WORKDIR")

if (poll_maven["workdir"] != None):
    if not poll_maven["workdir"].endswith(str(poll_maven["locate"])):
        test_failed.append("MAVEN WORKDIR")

# TEST THE RUN CMD
if (poll_maven["run"] == None or len(poll_maven["run"]) == 0):
    test_failed.append("MAVEN RUN DEPEDENCY")
else:
    if check_run_maven_one():
        test_passed.append("MAVEN RUN")
    else:
        test_failed.append("MAVEN RUN DEPEDENCY")
if (len(poll_maven["run"]) < 2):
    test_failed.append("MAVEN RUN PACKAGE")
else:
    if check_run_maven_two():
        test_passed.append("RUN TEST maven")
    else:
        test_failed.append("MAVEN RUN PACKAGE")

######################     OPEN     #####################

poll_open = {
    "img_version": None,
    "cpy": None,
    "expose": None,
    "cmd": None,
    "locate": None,
    "workdir": None
}


def check_launch_open():
    founded = 0
    txt = poll_open["cmd"]
    txt = txt.replace(',', ' ')
    txt = txt.replace(']', ' ')
    txt = txt.replace('[', ' ')
    txt = txt.replace('"', ' ')
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    for elem in tmp:
        if elem == "java":
            founded += 1
        if elem == "-jar":
            founded += 1
        if elem == "worker-jar-with-dependencies.jar":
            founded += 1
    return founded == 3

def check_expose():
    txt = poll_open["expose"]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    if len(tmp) != 2:
        return 0
    if tmp[0] == "EXPOSE" and tmp[1] == "80":
        return 1
    return 0

def check_open_cpy():
    founded = 0
    txt = poll_open["cpy"]
    tmp = [e for e in txt.split(' ') if len(e) > 0]
    if (tmp[1] == "--from=builder"):
        founded += 1
    for elem in tmp:
        if elem.startswith("/target/"):
            founded += 1
        if elem == poll_open["locate"]:
            founded += 1
    return founded == 3

if open != None:
    poll_open["img_version"] = open[0].strip()
    for i in open:
        if "COPY" in i:
            poll_open["cpy"] = i
        if "EXPOSE" in i:
            poll_open["expose"] = i
        if "RUN" in i:
            poll_open["run"]
        if "CMD" in i:
            poll_open["cmd"] = i
        if "WORKDIR" in i:
            poll_open["workdir"] = i
    if (poll_open["cpy"] != None):
        poll_open["locate"] = poll_open["cpy"].split(' ')[-1]
    else:
        poll_open["locate"] = "."


if (poll_open["img_version"] == None):
    test_failed.append("OPEN VERSION")
else:
    if check_maven_img:
        test_passed.append("OPEN VERSION")
    else:
        test_failed.append("OPEN VERSION")
# TEST EXPOSE
if (poll_open["expose"] == None):
    test_failed.append("OPEN EXPOSE")
else:
    if check_expose():
        test_passed.append("OPEN EXPOSE")
    else:
        test_failed.append("OPEN EXPOSE")
# TEST DE COPY
if (poll_open["cpy"] == None):
    test_failed.append("OPEN COPY")
else:
    if check_open_cpy():
        test_passed.append("OPEN COPY")
    else:
        test_failed.append("OPEN COPY")

# TEST WORKDIR TP IF NOT IN THE ROOT
if (poll_open["locate"] != "." and poll_open["workdir"] == None):
    test_failed.append("OPEN WORKDIR")

if (poll_open["workdir"] != None):
    if not poll_open["workdir"].endswith(str(poll_open["locate"])):
        test_failed.append("OPEN WORKDIR")

# TEST THE LAUNCH CMD
if (poll_open["cmd"] == None):
    test_failed.append("OPEN LAUNCH")
else:
    if check_launch_open():
        test_passed.append("OPEN LAUNCH")
    else:
        test_failed.append("OPEN LAUNCH")

if (len(test_failed) == 0):
    print("GG")
else:
    for elem in test_failed:
        print(elem)
    if len(test_passed) == 0:
        print("BAD")