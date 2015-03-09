## Syncrhroize the Docker repoistories from Docker Hub to local Registry


### Editing image lists
Edit the images.txt of the repos for syncing


### Usage

Help
 
```sh
python sync_images -h|--help
```

Synchroize images
```sh
python sync_images [-f|--file <config_file>] [-d|--docker_host <tcp://server:port>|'unix://var/run/docker.sock'] [-r|--registry <host:port>] [-i|--insecure_registry]
```


  