import docker

docker = docker.from_env()

def dispay_image():
    list = docker.images.list(all=True)

    if list == []:
        return "{'Image list is empty': None}"
    else:
        return list 

def remove_image():
    img = docker.images.prune(filters={'dangling': False})
    return img

def remove_containers_inactive():
    cont = docker.containers.prune()
    return cont 

def remove_networks():
    net = docker.networks.prune()
    return net

def remove_volumes():
    vol = docker.volumes.prune()
    return vol 

def remove_containers_active():
    containers = docker.containers.list(all=True)
    
    if containers == []:
        return "{'Active Container list is empty': None}"
    else:
        for cont in containers:
            cont.remove(force=True)
        return containers

if __name__ == '__main__':
    print(dispay_image())
    print(remove_networks())
    print(remove_containers_inactive())
    print(remove_volumes())
    print(remove_containers_active())
    print(remove_image())