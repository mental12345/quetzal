import docker 
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

def delete_image():
  print("Hello world")

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

def get_docker_volumes():
  docker_volumes = []
  volumes_dictionary = {}
  volumes = client.volumes.list()
  for volume in volumes:
    docker_volumes.append(volume.short_id)
  return docker_volumes


images_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_images()], key='images')],
           [sg.Button('Refresh',key='refresh_image_list')]]

containers_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_containers()], key='containers')],
           [sg.Button('Refresh',key='refresh_container_list')]]

network_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_network()], key='networks')],
           [sg.Button('Refresh',key='refresh_networks_list')]]

volumes_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[get_docker_volumes()], key='volumes')],
           [sg.Button('Refresh',key='refresh_volumes_list')]]


tabgrp = [[sg.TabGroup([[
                        sg.Tab('Images', images_layout, title_color='Gray'),
                        sg.Tab('Containers', containers_layout, title_color='Blue'),
                        sg.Tab('Network', network_layout,title_color='Black'),
                        sg.Tab('Volumes', volumes_layout,title_color='Green')]], key='_TAB_GROUP_'),
                        [sg.Button('Close'),
                        sg.Button('New',key='new'),
                        sg.Button('Delete',key='delete')]]]


window = sg.Window("Quetzal: ContainerDashboard", tabgrp)

while True:   
    event, values = window.read()
    if event == 'Close' or event == sg.WIN_CLOSED or event is None:          
      break    
    group = values['_TAB_GROUP_']
    
    if event == 'refresh_image_list':
      images = get_docker_images()
      window['images'].update(images)
    if event == 'refresh_container_list':
      window['containers'].update(get_docker_containers())
    if event == 'refresh_networks_list':
      window['networks'].update(get_docker_network())
    if event == 'refresh_volumes_list':
      window['volumes'].update(get_docker_volumes())
    #General Actions
    if event == 'delete':
      if group == 'Network':
        print("Network")
      if group == 'Containers':
        print("COntainers") 
      if group == 'Volumes':
        print("Volumes") 
      if group == 'Images':
        print("Images") 
    



window.Close()
