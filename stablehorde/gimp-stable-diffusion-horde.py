#!/usr/bin/python

# v1.0.2

import urllib2
import tempfile
import os
import base64
import json
import ssl
import sched, time
import gimp
from gimpfu import *

VERSION = 102
GENERATED_FILE = "generated.png"
API_ROOT = "https://stablehorde.net/api/v2/"

# check every 5 seconds
CHECK_WAIT = 5
checkMax = None

ssl._create_default_https_context = ssl._create_unverified_context

generatedFile = r"{}".format(os.path.join(tempfile.gettempdir(), GENERATED_FILE))
s = sched.scheduler(time.time, time.sleep)

checkCounter = 0
id = None

def checkUpdate():
  try:
     gimp.get_data("update_checked")
     updateChecked = True
  except Exception as ex:
     updateChecked = False

  if updateChecked is False:
     try:
        url = "https://raw.githubusercontent.com/blueturtleai/gimp-stable-diffusion/main/stablehorde/version.json"
        response = urllib2.urlopen(url)
        data = response.read()
        data = json.loads(data)
        gimp.set_data("update_checked", "1")

        if VERSION < int(data["version"]):
           pdb.gimp_message(data["message"])
     except Exception as ex:
        ex = ex

def displayGenerated(images):
   color = pdb.gimp_context_get_foreground()
   pdb.gimp_context_set_foreground((0, 0, 0))

   for image in images:
      imageFile = open(generatedFile, "wb+")
      imageFile.write(base64.b64decode(image["img"]))
      imageFile.close()

      imageLoaded = pdb.file_webp_load(generatedFile, generatedFile)
      pdb.gimp_display_new(imageLoaded)
      # image, drawable, x, y, text, border, antialias, size, size_type, fontname
      pdb.gimp_text_fontname(imageLoaded, None, 2, 2, str(image["seed"]), -1, TRUE, 12, 1, "Sans")
      pdb.gimp_image_set_active_layer(imageLoaded, imageLoaded.layers[1])

   pdb.gimp_context_set_foreground(color)
   return

def getImages():
   url = API_ROOT + "generate/status/" + id
   response = urllib2.urlopen(url)
   data = response.read()
   data = json.loads(data)

   return data["generations"]

def checkStatus():
   url = API_ROOT + "generate/check/" + id
   response = urllib2.urlopen(url)
   data = response.read()
   data = json.loads(data)

   global checkCounter
   checkCounter = checkCounter + 1

   if data["processing"] == 0:
      text = "Queue position: " + str(data["queue_position"]) + ", Wait time: " + str(data["wait_time"]) + "s"
   elif data["processing"] > 0:
      text = "Generating..."

   pdb.gimp_progress_set_text(text)

   if checkCounter < checkMax and data["done"] == False:
      s.enter(CHECK_WAIT, 1, checkStatus, ())
      s.run()
   elif checkCounter == checkMax:
      minutes = (checkMax * CHECK_WAIT)/60
      raise Exception("Image generation timed out after " + str(minutes) + " minutes. Please try it again later.")
   elif data["done"] == True:
      return

def text2img(image, drawable, promptStrength, steps, seed, nsfw, prompt, apikey, maxWaitMin):
   pdb.gimp_progress_init("", None)

   global checkMax
   checkMax = (maxWaitMin * 60)/CHECK_WAIT

   data = {
      "prompt": prompt,
      "params": {
         "cfg_scale": float(promptStrength),
         "height": 512,
         "width": 512,
         "steps": int(steps),
         "seed": seed
      },
      "nsfw": nsfw,
      "censor_nsfw": False
   }

   data = json.dumps(data)

   apikey = "0000000000" if not apikey else apikey

   headers = {"Content-Type": "application/json", "Accept": "application/json", "apikey": apikey}
   url = API_ROOT + "generate/async"

   request = urllib2.Request(url=url, data=data, headers=headers)

   try:
      response = urllib2.urlopen(request)
      data = response.read()

      try:
         data = json.loads(data)
         global id
         id = data["id"]
      except Exception as ex:
         raise Exception(data)

      checkStatus()
      images = getImages()
      displayGenerated(images)
   except Exception as ex:
      raise ex
   finally:
      pdb.gimp_progress_end()
      checkUpdate()

   return

register(
   "text2img",
   "text2img",
   "text2img",
   "BlueTurtleAI",
   "BlueTurtleAI",
   "2022",
   "<Image>/AI/Stablehorde text2img",
   "*",
   [
      (PF_SLIDER, "promptStrength", "Prompt Strength", 7.5, (0, 20, 0.5)),
      (PF_SLIDER, "steps", "Steps", 50, (10, 150, 1)),
      (PF_STRING, "seed", "Seed (optional)", ""),
      (PF_TOGGLE, "nsfw", "NSFW", False),
      (PF_STRING, "prompt", "Prompt", ""),
      (PF_STRING, "apiKey", "API key (optional)", ""),
      (PF_SLIDER, "maxWaitMin", "Max Wait (minutes)", 5, (1, 10, 1))
   ],
   [],
   text2img
)

main()
