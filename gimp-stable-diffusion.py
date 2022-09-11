#!/usr/bin/python

# v1.0.0

import urllib2
import tempfile
import os

from gimpfu import *

INIT_FILE = "init.png"
GENERATED_FILE = "generated.png"
API_ENDPOINT = "api/img2img"

initFile = r"{}".format(os.path.join(tempfile.gettempdir(), INIT_FILE))
generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))

def getImageData(image, drawable):
   pdb.file_png_save_defaults(image, drawable, initFile, initFile)
   imageFile = open(initFile, "rb")
   return imageFile.read()

def displayGenerated(image):
   image = pdb.file_png_load(generatedFile, generatedFile)
   pdb.gimp_display_new(image)
   return

def img2img(image, drawable, initStrength, promptStrength, steps, prompt, url):
   headers = {
      "init_strength": float(initStrength),
      "prompt_strength": float(promptStrength),
      "steps": int(steps),
      "width": image.width,
      "height": image.height,
      "prompt": prompt
   }

   headers.update({"Content-Type": "application/octet-stream"})

   imageData = getImageData(image, drawable)

   pdb.gimp_progress_set_text("starting dreaming now...")
   url = url + API_ENDPOINT
   request = urllib2.Request(url=url, data=imageData, headers=headers)
   response = urllib2.urlopen(request)

   imageFile = open(generatedFile, "wb+")
   imageFile.write(response.read())
   imageFile.close()

   displayGenerated(image)

   if os.path.exists(initFile):
       os.remove(initFile)

   if os.path.exists(generatedFile):
       os.remove(generatedFile)

   return

register(
   "img2img",
   "img2img",
   "img2img",
   "BlueTurtleAI",
   "BlueTurtleAI",
   "2022",
   "<Image>/AI/Stable img2img",
   "*",
   [
      (PF_SLIDER, "initStrength", "Init Strength", 0.3, (0.1, 0.9, 0.1)),
      (PF_SLIDER, "promptStrength", "Prompt Strength", 7.5, (0, 20, 0.1)),
      (PF_SLIDER, "steps", "Steps", 50, (10, 500, 1)),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "url", "Backend root URL", "")
   ],
   [],
   img2img
)

main()