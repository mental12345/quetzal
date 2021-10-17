import docker

client = docker.from_env()

def get_docker_images():
  docker_images = []
  docker_img_dict = {}
  images =client.images.list()
  for image in images:
    if image  not in docker_img_dict:
      docker_img_dict[image.short_id] = []
    docker_img_dict[image.short_id].extend([image.tags])
  docker_images = docker_img_dict.items()
  return docker_images

def del_docker_images(image):
  client.images.remove(image, force=True)

def new_docker_image(name):
  image = client.images.pull(name)
  return image

def get_docker_containers():
  docker_containers = []
  docker_dictionary = {}
  containers = client.containers.list(all)
  for container in containers:
    if container not in docker_dictionary:
      docker_dictionary[container.short_id] = []
    docker_dictionary[container.short_id].extend([container.image.tags, container.name, container.status])
  docker_containers = docker_dictionary.items()  
  return docker_containers

def del_docker_container(container):
  client.containers.get(container).remove(force=True)
  
def new_docker_container(container):
  new_container = client.containers.create(container)
  return new_container

def get_docker_network():
  docker_networks = []
  network_dictionary = {}
  networks = client.networks.list()
  for network in networks:
    if network not in network_dictionary:
      network_dictionary[network.short_id] = []
    network_dictionary[network.short_id].extend([network.name, network.containers])
  docker_networks = network_dictionary.items()
  return docker_networks

def del_docker_network(network):
  client.networks.get(network).remove()

def new_docker_network(name):
  new_network = client.networks.create(name, driver="bridge")
  return new_network


def get_docker_volumes():
  docker_volumes = []
  volumes_dictionary = {}
  volumes = client.volumes.list()
  for volume in volumes:
    docker_volumes.append(volume.short_id)
  return docker_volumes

def del_docker_volume(volume):
  client.volumes.get(volume).remove()

def new_docker_volume(name):
  new_volume = client.volumes.create(name, driver='local')
  return new_volume