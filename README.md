## Synchronize images from Docker Hub to local Registry


### Editing image lists
Edit the images.txt of the repos for syncing


### Usage

Help
 
```sh
python sync_images -h|--help
```


Synchronize images from specific repository 

```sh
python sync_images -n|--name <repo_name> 
```


Synchronize images from the configuraiton files, by default "images.txt"

```sh
python sync_images [-f|--file <config_file>]
```

Other optional arguments


```sh
-d|--docker_host <tcp://server:port>|<'unix:///var/run/docker.sock'>

-r|--registry <host:port>

-i|--insecure_registry
```