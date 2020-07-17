#!/usr/bin/env python

import os
import PySimpleGUI as sg
import ytdl_script as dl

sg.change_look_and_feel("LightGreen")

url = 'url-input'
folder = 'folder-input'
btn_audio = 'audio-input'

layout = [
            [sg.Text('Link to video or playlist'), ],
            [sg.Input(focus=True, key=url), ],
            [sg.Text('Output Folder'), ],
            [sg.Input(key=folder), ],
            [
                sg.FolderBrowse(target=folder),
                sg.Radio('Audio Only', btn_audio, key='audio', default=True), sg.Radio('Video', btn_audio, key='video'),
                sg.Checkbox('Suppress Errors', key='no-error', default=False),
            ],
            [sg.Button('Download'), sg.CloseButton('Exit')]
         ]

window = sg.Window('Youtube Downloader GUI', layout,
                   return_keyboard_events=True, use_default_focus=False)

while True:
    event, values = window.read(timeout=200)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event in ('Enter', 'Download', 'Return::35'):
        print("Hit OK")
        og_dir = os.getcwd()
        try:
            os.chdir(values[folder])
            args = [f'{values[url].strip()}']
            downloaded = '\n'.join(dl.download(args, audio=values['audio'], ignore_errors=values['no-error']))
            sg.popup('Media downloaded successfully as:\n'
                     f'{downloaded}.\n', f'Output Location: {os.getcwd()}',
                     title='Success', custom_text='OK')
        except Exception as e:
            print(e)
            if not values['no-error']:
                sg.popup('Something went wrong while\ndownloading the provided media.',
                         title='Error', custom_text='Cancel')

        os.chdir(og_dir)


window.close()
