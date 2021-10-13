import docker 
import PySimpleGUI as sg

client = docker.from_env()

def get_docker_images():
  docker_images = []
  images =client.images.list()
  for image in images:
    docker_images.append(image)
  return docker_images

def get_docker_containers():
  docker_containers = []
  docker_dictionary = {}
  containers = client.containers.list(all)
  for container in containers:
    if container not in docker_dictionary:
      docker_dictionary[container.short_id] = []
    docker_dictionary[container.short_id].extend([container.image, container.name, container.status])
    #docker_containers.append(container.id)
  docker_containers = docker_dictionary.items()  
  return docker_containers

def get_docker_network():
  docker_networks = []
  networks = client.networks.list()
  for network in networks:
    docker_networks.append(network)
  return docker_networks

def get_docker_volumes():
  docker_volumes = []
  volumes = client.volumes.list()
  for volume in volumes:
    docker_volumes.append(volume)
  return docker_volumes


images_layout = [[sg.Text('Search:', size=(8,1)),sg.Input('',key='image_search')],
           [sg.Listbox(size=(60,20), enable_events=True, values=[], key='images')],
           [sg.Button('Refresh',key='refresh_image_list'), sg.Button('Delete',key='delete_image')]]

containers_layout = [[sg.Text('Search:', size=(8,1)),sg.Input('',key='container_search')],
           [sg.Listbox(size=(60,20), enable_events=True, values=[get_docker_containers()], key='containers')],
           [sg.Button('Refresh',key='refresh_container_list'), sg.Button('Delete',key='delete_container')]]

network_layout = [[sg.Text('Search:', size=(8,1)),sg.Input('',key='network_search')],
           [sg.Listbox(size=(60,20), enable_events=True, values=[], key='networks')],
           [sg.Button('Refresh',key='refresh_networks_list'), sg.Button('Delete',key='delete_network')]]

volumes_layout = [[sg.Text('Search:', size=(8,1)),sg.Input('',key='volumes_search')],
           [sg.Listbox(size=(60,20), enable_events=True, values=[], key='volumes')],
           [sg.Button('Refresh',key='refresh_volumes_list'), sg.Button('Delete',key='delete_volume')]]


tabgrp = [[sg.TabGroup([[
                        sg.Tab('Images', images_layout, title_color='Gray'),
                        sg.Tab('Containers', containers_layout, title_color='Blue'),
                        sg.Tab('Network', network_layout,title_color='Black'),
                        sg.Tab('Volumes', volumes_layout,title_color='Green')]]),
                        sg.Button('Close')]]  


window = sg.Window("ContainerDashboard", tabgrp)

while True:    
    event, values = window.read()    
    if event == 'refresh_image_list':
      images = get_docker_images()
      window['images'].update(images)
    if event == 'refresh_container_list':
      window['containers'].update(get_docker_containers())
      print(get_docker_containers())
    if event == 'Close' or event == sg.WIN_CLOSED:          
      break



window.Close()
