import docker

docker = docker.from_env()

def dispay_image():
    list = docker.images.list(all=True)
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

    for cont in containers:
        print(containers)
        cont.remove(force=True)


if __name__ == '__main__':
    print(dispay_image())
    print(remove_containers_inactive())
    print(remove_networks())
    print(remove_volumes())
    print(remove_containers_active())
    print(remove_image())