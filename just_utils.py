r'''

Installing moviepy (on gnu/linux)
	1 $ pip install moviepy
	2 $ apt install libmagick++-dev
	3   edit /etc/ImageMagick-6/policy.xml
		change tihs:
			<policy domain="path" rights="none" pattern="@*"/>
		to tihs:
			<!-- <policy domain="path" rights="none" pattern="@*"/> -->
	3 edit ~/.bashrc , add this lines:
			export FFMPEG_BINARY="/usr/bin/ffmpeg"
			export IMAGEMAGICK_BINARY="/usr/bin/convert"


		 _                 
		| |                
	  __| | ___   ___ ___  
	 / _` |/ _ \ / __/ __| 
	| (_| | (_) | (__\__ \ 
	 \__,_|\___/ \___|___/  for mouse state

	'holding'         - holding btn
	'normal'          - not holding btn
	'moving'          - moving moment (that's holding AND draging mouse)
	'press_moment'    - special press-MOMENT
	'release_moment'  - special release-MOMENT
'''


from base64 import b64encode
from PIL import Image
from moviepy.editor import VideoFileClip
import os

def readbin(filename):
	# read binary file
	with open(filename, 'rb') as ff:
		data = ff.read()
	return data

cd = CD = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH_TO_EXPORT_IMAGE = os.path.join(cd, 'RESOURCE_files', '_.png')

def jpg2pngBinary(jpg_file, _img=DEFAULT_PATH_TO_EXPORT_IMAGE):
	# convert jpeg image to png
	# return binary of png file
	Image.open(jpg_file).save(_img)
	data = readbin(_img) #; os.remove(_img)
	return data


def numpy2pngBinary(np_array, _img=DEFAULT_PATH_TO_EXPORT_IMAGE):
	# convert numpy array to png
	# return binary of png file
	Image.fromarray(np_array).save(_img)
	data = readbin(_img) #; os.remove(_img)
	return data

def load_video(videofile_path:str):
	return VideoFileClip(videofile_path)
def update_frame(new_position, use_percent=False, econfig=None, graph_Element=None):
	
	if not econfig: raise 'Error with econfig'
	
	econfig['playhead_pos'] = new_position
	
	# clear prev frame, it is was rendered in GraphElement
	if econfig['psg_frame'] != None:
		graph_Element.DeleteFigure(econfig['psg_frame'])

	# draw in GraphElement
	pos = econfig['playhead_pos']/econfig['fps']
	np_img = econfig['lo_video_obj'].get_frame(pos)
	binary_png_img = numpy2pngBinary(np_img)

	b64_frame = b64encode(binary_png_img)
	econfig['psg_frame'] = graph_Element.draw_image(data=b64_frame, location=(0, 0))
	graph_Element.draw_image(data=b64_frame, location=(0, 0))
def load_new_video(videofile_path:str, playhead, econfig=None, **kw):
	if not econfig: raise 'Error with econfig'

	# update state of editor
	econfig['lo_video_path'] = videofile_path
	econfig['lo_video_obj'] = load_video(videofile_path)
	econfig['durationf'] = int(econfig['lo_video_obj'].duration * econfig['lo_video_obj'].fps) - 1
	econfig['fps'] = int(econfig['lo_video_obj'].fps)
	playhead.update(range=(0, econfig['durationf']))

	# draw first frame in GraphElement
	update_frame(0, econfig=econfig, **kw)

def export_cropped_img(outputname, crop_area, econfig=None):
	if not econfig: raise 'Error with econfig'
	np_img = econfig['lo_video_obj'].get_frame(econfig['playhead_pos']/econfig['fps'])
	(Image.fromarray(np_img)
		.crop(crop_area)
		.save(outputname))

