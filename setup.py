import docker 
import re
import PySimpleGUI as sg

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

images_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_images()], key='images')]]

containers_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_containers()], key='containers')]]

network_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_network()], key='networks')]]

volumes_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_volumes()], key='volumes')]]


tabgrp = [[sg.TabGroup([[
                        sg.Tab('Images', images_layout, title_color='Gray'),
                        sg.Tab('Containers', containers_layout, title_color='Blue'),
                        sg.Tab('Network', network_layout,title_color='Black'),
                        sg.Tab('Volumes', volumes_layout,title_color='Green')]], key='_TAB_GROUP_'),
                        [sg.Button('New',key='new'),
                        sg.Button('Refresh', key='refresh'),
                        sg.Button('Delete',key='delete'),
                        sg.Button('Close')]]]


window = sg.Window("Quetzal: ContainerDashboard", tabgrp)

while True:   
    event, values = window.read()
    if event == 'Close' or event == sg.WIN_CLOSED or event is None:          
      break    
    group = values['_TAB_GROUP_']

    #General Actions
    if event == 'refresh':
      if group == 'Images':
        images = get_docker_images()
        window['images'].update(images)
      if group == 'Containers':
        window['containers'].update(get_docker_containers())
      if group == 'Volumes':
        window['volumes'].update(get_docker_volumes())
      if group == 'Network':
        window['networks'].update(get_docker_network())
    if event == 'delete':
      if group == 'Network':
        network = window['networks'].get()
        if not network:
          sg.popup_error('Must select an item')
        else:
          tuple = network[0]
          fn = tuple[0]
          del_docker_network(fn)
      if group == 'Containers':
        container = window['containers'].get()
        if not container:
          sg.popup_error('Must select an item')
        else:
          tuple = container[0]
          fc = tuple[0]
          del_docker_container(fc)
      if group == 'Volumes':
        volume = window['volumes'].get()
        if not volume:
          sg.popup_error('Must select an item')
        else:
          del_docker_volume(volume[0])
      if group == 'Images':
        image = window['images'].get()
        if not image:
          sg.popup_error('Must select an item')
        else:
          tuple = image[0]    
          fi = tuple[0]
          fi = re.sub('sha256:','',fi)
          del_docker_images(fi)
    if event == 'new':
      if group == 'Images':
        image = sg.popup_get_text('Image', 'Please input image name, only latest will be downloaded')
        try:
          new_image=new_docker_image(image)
          sg.popup(new_image.id)
        except: 
          sg.popup_error('Image not found: Please login or do a docker pull: ', image)
      if group == 'Containers':
        image = sg.popup_get_text('Container Image', 'Please input image name to use in container, only latest will be downloaded')
        try:
          new_container=new_docker_container(image)
          sg.popup(new_container.id)
        except: 
          sg.popup_error('Image not found: Please login or do a docker create: ', image)
      if group == 'Network':
        network = sg.popup_get_text('Network', 'Please input Network name: ')
        try:
          new_network=new_docker_network(network)
          sg.popup(new_network.name)
        except: 
          sg.popup_error('Network cannot be created')
      if group == "Volumes":
        volume = sg.popup_get_text('Volume', 'Please input Volume name: ')
        try:
          new_volume=new_docker_volume(volume)
          sg.popup(new_volume.name)
        except: 
          sg.popup_error('Volume cannot be created')

window.Close()
