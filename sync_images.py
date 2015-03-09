import docker
import sys
import os
import getopt

# print help and exit
def help():
    print "python sync_images -h|--help"
    print "python sync_images [-f|--file <config_file>] [-d|--docker_host <tcp://server:port>|'unix://var/run/docker.sock'>'] [-r|--registry <host:port>] [-i|--insecure_registry]"
    sys.exit(1)
   

options = []
DEFAULT_CONFIG_FILE = "./images.txt"
DEFAULT_REGISTRY = 'jadetest.cn.ibm.com:5000'
INSECURE_REGISTRY = False

docker_host = None
registry = DEFAULT_REGISTRY
insecure_registry = INSECURE_REGISTRY
filename = DEFAULT_CONFIG_FILE

# parse command line arguments
try:
    (options, args) = getopt.getopt(sys.argv[1:], 'f:d:r:ih', ['file=', 'docker_host=', 'registry=', 'insecure_registry', 'help'])
except getopt.GetoptError:
    help()

for option in options:
    if option[0] == '-f' or option[0] == '--file':
        filename = option[1]
    elif option[0] == '-r' or option[0] == '--registry':
        registry = option[1]
    elif option[0] == '-d' or option[0] == '--docker_host':
        docker_host = option[1]
    elif option[0] == '-i' or option[0] == '--insecure_registry':
        insecure_registry = True
    elif option[0] == '-h' or option[0] == '--help':
        help()

if (not os.path.exists(filename)):
    print >>sys.stderr, "Cannot file configuration for image sync: %s" % file
    sys.exit(1)

lines = [line.strip() for line in open(filename)]

client = docker.Client(docker_host)
for repo in lines:
    #Ignore comment
    if repo.startswith('#'):
        continue
    if repo == '':
        continue
    print "Pulling repository %s ..." % repo
    client.pull(repo, insecure_registry=insecure_registry)

    images = client.images(name=repo)

    # Get the repo name without registry
    repo_name = repo
    repo_names = repo_name.split('/')
    if len(repo_names) == 3:
        repo_name = repo_names[1] + '/' + repo_names[2]

    new_repo_name = registry + "/" + repo_name

    print "Original repository is %s ." % repo_name
    print "New repository is %s ." % new_repo_name

    for image in images:
        name = image[u'RepoTags'][0].encode('utf-8')
        image_name = name.split(':')
        tag = name.split(':')[len(image_name) - 1]
        print "Tagging %s:%s %s:%s" % (repo, tag, new_repo_name, tag)
        client.tag(repo, new_repo_name, tag, True)

    print "Pushing repository %s ..." % repo
    client.push(new_repo_name, insecure_registry=insecure_registry)
    print "Complete the sync of repository %s." % repo
