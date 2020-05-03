# miniVideoEditor-crop-tool

function:

- View Video
- Make a selection
- Export selected image
- View Video

# Install requirements:

```bash
pip install Pillow PySimpleGUI moviepy

# # # 
# # # For Unix-like OS:
# # # 
$ apt install libmagick++-dev
$ echo -e 'export FFMPEG_BINARY="/usr/bin/ffmpeg"\nexport IMAGEMAGICK_BINARY="/usr/bin/convert"' >> ~/.bashrc
$ sudo sed -i -e '/<policy\ domain=\"path\"\ rights=\"none\"\ pattern=\"\@\*\"\/>/ c\  <!-- <policy domain="path" rights="none" pattern="@*"/> -->' /etc/ImageMagick-6/policy.xml

```

# Run itself:

```bash
python3 main.py
```


# How it looks (GUI):

![Gui](https://github.com/nngogol/miniVideoEditor-crop-tool/blob/master/gui.png)


# Why?

Maybe you:
- NEED to cut image from video
- WANT input dataset for some ML project
- SEARCH to small icons in video
