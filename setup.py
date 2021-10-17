import re
import dockerengine as de
import PySimpleGUI as sg

images_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[de.get_docker_images()], key='images')]]

containers_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[de.get_docker_containers()], key='containers')]]

network_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[de.get_docker_network()], key='networks')]]

volumes_layout = [
           [sg.Listbox(size=(60,20), select_mode=sg.SELECT_MODE_EXTENDED, enable_events=True, values=[de.get_docker_volumes()], key='volumes')]]

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

    if event == 'refresh':
      if group == 'Images':
        images = de.get_docker_images()
        window['images'].update(images)
      if group == 'Containers':
        window['containers'].update(de.get_docker_containers())
      if group == 'Volumes':
        window['volumes'].update(de.get_docker_volumes())
      if group == 'Network':
        window['networks'].update(de.get_docker_network())
    if event == 'delete':
      if group == 'Network':
        network = window['networks'].get()
        if not network:
          sg.popup_error('Must select an item')
        else:
          tuple = network[0]
          fn = tuple[0]
          de.del_docker_network(fn)
      if group == 'Containers':
        container = window['containers'].get()
        if not container:
          sg.popup_error('Must select an item')
        else:
          tuple = container[0]
          fc = tuple[0]
          de.del_docker_container(fc)
      if group == 'Volumes':
        volume = window['volumes'].get()
        if not volume:
          sg.popup_error('Must select an item')
        else:
          de.del_docker_volume(volume[0])
      if group == 'Images':
        image = window['images'].get()
        if not image:
          sg.popup_error('Must select an item')
        else:
          tuple = image[0]    
          fi = tuple[0]
          fi = re.sub('sha256:','',fi)
          de.del_docker_images(fi)
    if event == 'new':
      if group == 'Images':
        image = sg.popup_get_text('Image', 'Please input image name, only latest will be downloaded')
        try:
          new_image=de.new_docker_image(image)
          sg.popup(new_image.id)
        except: 
          sg.popup_error('Image not found: Please login or do a docker pull: ', image)
      if group == 'Containers':
        image = sg.popup_get_text('Container Image', 'Please input image name to use in container, only latest will be downloaded')
        try:
          new_container=de.new_docker_container(image)
          sg.popup(new_container.id)
        except: 
          sg.popup_error('Image not found: Please login or do a docker create: ', image)
      if group == 'Network':
        network = sg.popup_get_text('Network', 'Please input Network name: ')
        try:
          new_network=de.new_docker_network(network)
          sg.popup(new_network.name)
        except: 
          sg.popup_error('Network cannot be created')
      if group == "Volumes":
        volume = sg.popup_get_text('Volume', 'Please input Volume name: ')
        try:
          new_volume=de.new_docker_volume(volume)
          sg.popup(new_volume.name)
        except: 
          sg.popup_error('Volume cannot be created')

window.Close()
