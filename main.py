# PUBLIC: https://github.com/nngogol/miniVideoEditor-crop-tool
# made it 2020-05-03 21:02:46

import PySimpleGUI as sg, os, pyperclip
from just_utils import *
cd = os.path.dirname(os.path.abspath(__file__))

# ==========
# PSG layout
# ==========
def Field(key='', title=''):
	return [sg.T(title), sg.I(key=key, size=(10,1))]
# get current destop size              and make it .85 smaller
screen_size = complex(*sg.Window.get_screen_size())*.85
canvas_size = int(screen_size.real), int(screen_size.imag)

# g as graph
g        = sg.Graph(canvas_size, (0, canvas_size[1]), (canvas_size[0], 0), enable_events=True, key='-GRAPH-', background_color='lightblue', drag_submits=True)
psg_playhead = sg.Slider(range=(0, 1000), default_value=0, orientation='h', size=(canvas_size[0]*.12, 20), key='playhead', enable_events=True)
Instructions = sg.T(
		'o - open new video        c - copy selection_area IN text buffer (ctrl+c)        '
		'e - export cropped image IN output.png', size=(100, 1)
	)
window = sg.Window('Test', [
	[g],
	[*Field(key='qwe', title='empty')
	,*Field(key='-start-', title='start x, y: ')
	,*Field(key='-end-', title='end x, y: ')
	,*Field(key='-size-', title='size w, h: ')
	,Instructions
	]
	,[psg_playhead]
], return_keyboard_events=True, finalize=True, location=(0,0))

# Selection, that we draw with mouse
selection = g.draw_rectangle((0, 0), (10, 10), line_width=1)

#                  _       _     _           
#                 (_)     | |   | |          
# __   ____ _ _ __ _  __ _| |__ | | ___  ___ 
# \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __|
#  \ V / (_| | |  | | (_| | |_) | |  __/\__ \
#   \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/

# >>> setup
econfig = {  # this is current (video)editor configuration state
	# lo is "last opened"
	'lo_video_path' : None,   # last opened video file path (absolute path)
	'lo_video_obj'  : None,   # moviepy.VideoFileClip object of current video
	'playhead_pos'  : None,   # current frame position a.k.a. playhead(slider) position a.k.a. frame number
	'fps'           : None,   # fps of video
	'durationf'     : None,   # (float) in frames
	'psg_frame'     : None,  # psg key in Graph element
}

# SETUP 1.mkv as default video
default_video = os.path.join(cd, 'RESOURCE_files/test.mkv')
load_new_video(default_video, psg_playhead, econfig=econfig, graph_Element=g)


#  _       _                        _ 
# (_)     | |                      | |
#  _ _ __ | |_ ___ _ __ _ __   __ _| |
# | | '_ \| __/ _ \ '__| '_ \ / _` | |
# | | | | | ||  __/ |  | | | | (_| | |
# |_|_| |_|\__\___|_|  |_| |_|\__,_|_|  stuff

# mouse vars
start_x = 0; start_y = 0; end_x = 0; end_y = 0
mouse_is_pressed, mouse_state = False, 'normal'

# general vars
_pevent = None
while True:
	event, values = window(timeout=250)
	if event in ('q', 'Exit', None): break

	# MOUSE MANAGEMANT
	if event == '-GRAPH-':
		if not mouse_is_pressed: 	mouse_state = f'press_moment'
		else: 						mouse_state = f'moving'
		mouse_is_pressed = True
	else:
		if _pevent == '-GRAPH-+UP':
			mouse_is_pressed = False
			mouse_state = f'release_moment'
		else:
			if not mouse_is_pressed: 	mouse_state = f'normal'
			else: 						mouse_state = f'holding'
	
	if event == 'playhead': # playhead moved
		update_frame(values['playhead'], econfig=econfig, graph_Element=g)

	##############################################
	#     _____ ____    _             _          #
	#    |_   _/ __ \  | |           (_)         #
	#      | || |  | | | | ___   __ _ _  ___     #
	#      | || |  | | | |/ _ \ / _` | |/ __|    #
	#     _| || |__| | | | (_) | (_| | | (__     #
	#    |_____\____/  |_|\___/ \__, |_|\___|    #
	#                            __/ |           #
	#                           |___/            #
	##############################################
	# 
	# keyboard logic
	# 
	if event == 'o': # open
		video_path = sg.PopupGetFile(message='pick a video', no_window=True ,file_types=(("ALL Files", "*.webm *.mkv *.mp4"),) )
		if os.path.exists(video_path):
			load_new_video(video_path, psg_playhead, econfig=econfig, graph_Element=g)
			
	elif event == 's': # print ot console selection
		res = (values['-start-'] +' '+ values['-end-']).split(' ')
	elif event == 'c': # copy to buffer
		pyperclip.copy(
			':'.join((values['-start-'] + values['-size-']).split(' '))
		)
	
	elif event == 'e': # export selected area
		x0, y0, x1, y1 = map(int, (values['-start-'] +' '+ values['-end-']).split(' '))
		export_cropped_img(outputname=os.path.join(cd, 'output.png')
				   ,crop_area=(x0, y0, x1, y1)
				   ,econfig=econfig)

	# 
	# Mouse logic
	# 
	if mouse_state == 'moving':
		# DRAW SELECTION RECTANGLE

		mouseX, mouseY = values['-GRAPH-']    # ] 
		end_x, end_y = mouseX, mouseY         # ] - a "mouse coordinates" design pattern. Just like:      event, values = window(...)

		# erase selection and make new
		g.DeleteFigure(selection)
		selection = g.draw_rectangle((start_x, start_y), (end_x, end_y), line_color='#ff0000', line_width=1)

		# Output to GUI
		window['-start-'](f'{start_x} {start_y}')
		window['-end-'](f'{end_x} {end_y}')
		window['-size-'](f'{end_x-start_x} {end_y-start_y}')

	elif mouse_state == 'press_moment':
		mouseX, mouseY = values['-GRAPH-']
		start_x, start_y = mouseX, mouseY
		end_x, end_y = start_x, start_y

	elif mouse_state == 'release_moment':
		pass


	_pevent = event
window.close()