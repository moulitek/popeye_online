import ruamel.yaml
import json
import os

in_file = 'docker-compose.yml'
out_file = 'output.json'
test_passed = []
test_failed = []

try:
    yaml = ruamel.yaml.YAML(typ='safe')
    with open(in_file) as fpi:
        cpy = yaml.load(fpi)
    with open(out_file, 'w') as fpo:
        json.dump(cpy, fpo, indent=2)

    with open('output.json') as json_file:
        data = json.load(json_file)
        os.remove("output.json")
except:
    print("docker-compose.yml missing or invalid")
    exit(84)
# TEST VERSION
if data == None or "version" not in data.keys() or data["version"] != '3':
    test_failed.append("Bad version")
else:
    test_passed.append("Good version")

    #================================#  POLL SERVICES #===============================#
if data == None or "poll" not in data["services"].keys() or data["services"]["poll"] == None:
    test_failed.append("no services poll")
else:
    poll = data["services"]["poll"]
    ##  BUILD  ##
    if "build" not in poll.keys() or poll["build"] == None:
        test_failed.append("poll build")
    elif poll["build"] == "./poll" or poll["build"] == "poll/":
        test_passed.append("poll build")
    else:
        test_failed.append("poll build")
        ##  RESTART  ##
    if "restart" not in poll.keys() or poll["restart"] == None:
        test_failed.append("poll restart")
    elif poll["restart"] == "always" or poll["restart"] == "on-failure":
        test_passed.append("poll restart")
    else:
        test_failed.append("poll restart")
        ##  ports  ##
    if "ports" not in poll.keys() or poll["ports"] == None:
        test_failed.append("poll ports")
    elif poll["ports"][0] == "5000:80":
        test_passed.append("poll ports")
    else:
        test_failed.append("poll ports")
        ##  network  ##
    if "networks" not in poll.keys() or poll["networks"] == None:
        test_failed.append("poll networks")
    elif poll["networks"][0] == "poll-tier" and len(poll["networks"]) == 1:
        test_passed.append("poll networks")
    else:
        test_failed.append("poll networks")
        ##  environment  ##
    if "environment" not in poll.keys() or poll["environment"] == None:
        test_failed.append("poll environment")
    else:
        test_passed.append("poll environment")
    if "depends_on" not in poll.keys() or poll["depends_on"] == None:
        test_failed.append("poll depends_on")
    elif poll["depends_on"][0] == "redis" and len(poll["depends_on"]) == 1:
        test_passed.append("poll depends_on")
    else:
        test_failed.append("poll depends_on")


#================================#  REDIS SERVICES #===============================#
if data == None or "redis" not in data["services"].keys():
    test_failed.append("no services redis")
else:
    redis = data["services"]["redis"]
    #  image  ##
    if "image" not in redis.keys() or redis["image"] == None:
        test_failed.append("redis image")
    elif redis["image"].startswith("redis"):
        test_passed.append("redis image")
    else:
        test_failed.append("redis image")
        ##  RESTART  ##
    if "restart" not in redis.keys() or redis["restart"] == None:
        test_failed.append("redis restart")
    elif redis["restart"] == "always" or redis["restart"] == "on-failure":
        test_passed.append("redis restart")
    else:
        test_failed.append("redis restart")
        ##  expose or ports ##
    if "ports" in redis.keys() and redis["ports"] != None:
        if redis["ports"][0].startswith("6379"):
            test_passed.append("redis expose")
        else:
            test_failed.append("redis expose")
    elif "expose" in redis.keys() and redis["expose"] != None:
        if redis["expose"][0].startswith("6379"):
            test_passed.append("redis expose")
        else:
            test_failed.append("redis expose")
    else:
        test_failed.append("redis expose")
        ##  network  ##
    if "networks" not in redis.keys() or redis["networks"] == None:
        test_failed.append("redis networks")
    elif "poll-tier" in redis["networks"] and "back-tier" in redis["networks"] and len(redis["networks"]) == 2:
        test_passed.append("redis networks")
    else:
        test_failed.append("redis networks")
        ##  depends_on  ##
    if "depends_on" not in redis.keys() or redis["depends_on"] == None:
        test_failed.append("redis depends_on")
    elif redis["depends_on"][0] == "db":
        test_passed.append("redis depends_on")
    else:
        test_failed.append("redis depends_on")
#================================#  worker SERVICES #===============================#
if data == None or "worker" not in data["services"].keys():
    test_failed.append("no services worker")
else:
    worker = data["services"]["worker"]
    #  build  ##
    if "build" not in worker.keys() or worker["build"] == None:
        test_failed.append("worker build")
    elif worker["build"] == "./worker" or worker["build"] == "worker/":
        test_passed.append("worker build")
    else:
        test_failed.append("worker build")
        ##  RESTART  ##
    if "restart" not in worker.keys() or worker["restart"] == None:
        test_failed.append("worker restart")
    elif worker["restart"] == "always" or worker["restart"] == "on-failure":
        test_passed.append("worker restart")
    else:
        test_failed.append("worker restart")
        ##  network  ##
    if "networks" not in worker.keys() or worker["networks"] == None:
        test_failed.append("worker networks")
    elif worker["networks"][0] == "back-tier" and len(worker["networks"]) == 1:
        test_passed.append("worker networks")
    else:
        test_failed.append("worker networks")
        ##  depends_on  ##
    if "depends_on" not in worker.keys() or worker["depends_on"] == None:
        test_failed.append("worker depends_on")
    elif "db" in worker["depends_on"] and "redis" in worker["depends_on"] and len(worker["depends_on"]) == 2:
        test_passed.append("worker depends_on")
    else:
        test_failed.append("worker depends_on")
        ##  environment  ##
    if "environment" not in worker.keys() or worker["environment"] == None:
        test_failed.append("worker environment")
    else:
        test_passed.append("worker environment")
#================================#  result SERVICES #===============================#
if data == None or "result" not in data["services"].keys() or data["services"]["result"] == None:
    test_failed.append("no services result")
else:
    result = data["services"]["result"]
    ##  BUILD  ##
    if "build" not in result.keys() or result["build"] == None:
        test_failed.append("result build")
    elif result["build"] == "./result" or result["build"] == "result/":
        test_passed.append("result build")
    else:
        test_failed.append("result build")
        ##  RESTART  ##
    if "restart" not in result.keys() or result["restart"] == None:
        test_failed.append("result restart")
    elif result["restart"] == "always" or result["restart"] == "on-failure":
        test_passed.append("result restart")
    else:
        test_failed.append("result restart")
        ##  ports  ##
    if "ports" not in result.keys() or result["ports"] == None:
        test_failed.append("result ports")
    elif result["ports"][0] == "5001:80":
        test_passed.append("result ports")
    else:
        test_failed.append("result ports")
        ##  network  ##
    if "networks" not in result.keys() or result["networks"] == None:
        test_failed.append("result networks")
    elif result["networks"][0] == "result-tier" and len(result["networks"]) == 1:
        test_passed.append("result networks")
    else:
        test_failed.append("result networks")
        ##  environment  ##
    if "environment" not in result.keys() or result["environment"] == None:
        test_failed.append("result environment")
    else:
        test_passed.append("result environment")
        ## depends_on ##
    if "depends_on" not in result.keys() or result["depends_on"] == None:
        test_failed.append("result depends_on")
    elif result["depends_on"][0] == "db" and len(result["depends_on"]) == 1:
        test_passed.append("result depends_on")
    else:
        test_failed.append("result depends_on")
#================================#  db SERVICES #===============================#
if data == None or "db" not in data["services"].keys() or data["services"]["db"] == None:
    test_failed.append("no services db")
else:
    db = data["services"]["db"]
    ##  image  ##
    if "image" not in db.keys() or db["image"] == None:
        test_failed.append("db image")
    elif db["image"].startswith("postgres"):
        test_passed.append("db image")
    else:
        test_failed.append("db image")
        ##  RESTART  ##
    if "restart" not in db.keys() or db["restart"] == None:
        test_failed.append("db restart")
    elif db["restart"] == "always" or db["restart"] == "on-failure":
        test_passed.append("db restart")
    else:
        test_failed.append("db restart")
        ##  network  ##
    if "networks" not in db.keys() or db["networks"] == None:
        test_failed.append("db networks")
    elif "result-tier" in db["networks"] and "back-tier" in db["networks"] and len(db["networks"]) == 2:
        test_passed.append("db networks")
    else:
        test_failed.append("db networks")
        ##  environment  ##
    if "environment" not in db.keys() or db["environment"] == None:
        test_failed.append("db environment")
    else:
        test_passed.append("db environment")
        ## depends_on ##
    if "volumes" not in db.keys() or db["volumes"] == None:
        test_failed.append("db volumes")
    elif "db-data:/var/lib/postgresql/data" in db["volumes"] and any([line.startswith("./schema.sql:/docker-entrypoint-initdb.d") for line in db["volumes"]]) and len(db["volumes"]) == 2:
        test_passed.append("db volumes")
    else:
        test_failed.append("db volumes")
#================================#  Volumes #===============================#
if data == None or "volumes" not in data.keys() or data["volumes"] == None:
    test_failed.append("no volumes")
else:
    volumes = data["volumes"]
    if "db-data" not in volumes.keys():
        test_failed.append("wrong volumes")
    else:
        test_passed.append("good volumes")

#================================#  networks #===============================#
if data == None or "networks" not in data.keys() or data["networks"] == None:
    test_failed.append("no networks")
else:
    networks = data["networks"]
    if "poll-tier" in networks.keys() and "result-tier" in networks.keys() and "back-tier" in networks.keys() and len(networks) == 3:
        test_passed.append("good networks")
    else:
        test_failed.append("wrong networks")

if (len(test_failed) == 0):
    print("GG")
else:
    for elem in test_failed:
        print(elem)
    if len(test_passed) == 0:
        print("BAD")
