#!/usr/bin/env python3

# pip3 install Pillow
from PIL import Image
import os
from time import sleep

from case_fixer import CaseFixer


def process_file(f = "Images-HT/starwars/VirtualAlternateImage-Dark/hires/iamyourfather_ai.png", attempt=0):

  if not os.path.isfile(f):
    print("Could not find file {}. Was it renamed?".format(f))

    cf = CaseFixer()
    f = cf.generate_new_filename(f)

    print("Trying again, but with: {}".format(f))

  if not os.path.isfile(f):
    print("file is not a file?... Waiting a few seconds for the filesystem to settle.")
    sleep(2)

  try:
    with Image.open(f) as im:
      width, height = im.size
      print("    * size:",width,"x",height)
      gif_filename   = f.replace(".png", ".gif").replace("hires", "large")
      gif_t_filename = f.replace(".png", ".gif").replace("hires/", "t_").replace("large/", "t_")
      git_dir = gif_filename.replace(gif_filename.split("/")[-1], "")
      git_t_dir = gif_t_filename.replace(gif_t_filename.split("/")[-1], "")

      print("    * gif_t....: "+gif_t_filename)
      print("    * gif......: "+gif_filename)
      print("    * gif_t dir: "+git_t_dir)
      print("    * gif dir..: "+git_dir)

      if (not os.path.isdir(git_t_dir)):
        print("    * gif_t dir does not exist... making")
        os.mkdir(git_t_dir)

      if (not os.path.isdir(git_dir)):
        print("    * gif dir does not exist... making")
        os.mkdir(git_dir)

      if height > width:
        print("    * tall - generate portrait card (745x1039)")
        if ("large/" in f):
          print("    ! NOT WRITING large gif. Target same as source.")
        else:
          write_gif(im, size_tall, gif_filename)
          print(os.popen('git add '+gif_filename).read())
        if ("t_" in f):
          print("    ! NOT WRITING t_ gif. Source should never be a t_ file.")
        elif ("t_" not in gif_t_filename):
          print("    ! NOT WRITING t_ gif. Target file should have t_ in the name.")
        else:
          write_gif(im, size_tall_t, gif_t_filename)
          print(os.popen('git add '+gif_t_filename).read())

      else:
        print("    * wide - generate landscape card (1039x745)")
        if ("large/" in f):
          print("    ! NOT WRITING large gif. Target same as source.")
        else:
          write_gif(im, size_wide, gif_filename)
          print(os.popen('git add '+gif_filename).read())
        if ("t_" in f):
          print("    ! NOT WRITING t_ gif. Source should never be a t_ file.")
        else:
          write_gif(im, size_wide_t, gif_t_filename)
          print(os.popen('git add '+gif_t_filename).read())

  except Exception as e:
    print("Unable to Open File: {}".format(f))
    print(e)
    if attempt < 2:
      print(" Waiting a few seconds for the filesystem to settle and trying again...")
      sleep(2)
      process_file(f, attempt+1)
    else:
      print("bailing out...")
      exit(1)




def write_gif(im, size, filename):
  try:
    print("    * Writing image file ("+str(size)+"): "+filename)
    ##
    ## ANTIALIAS is deprecated and will be removed in Pillow 10 (2023-07-01).
    ## Use Resampling.LANCZOS instead
    ##
    #im.thumbnail(size, Image.ANTIALIAS)
    im.thumbnail(size, Image.Resampling.LANCZOS)
    im.save(filename, "PNG")
  except IOError:
    print("    ! Unable to generate image !")
    exit(1)





size_wide=1039,745
size_tall=745,1039

size_wide_t=87,67
size_tall_t=67,87

process_all_files = False


##
## process ALL files
##
if process_all_files:
  rootdir='Images-HT/starwars'
  for file in os.listdir(rootdir):
    d = os.path.join(rootdir, file)
    if os.path.isdir(d):
      print(d)
      hires_dir = d+"/hires"
      if os.path.isdir(hires_dir):
        for f in os.listdir(hires_dir):
          dd = os.path.join(hires_dir, f)
          print("  * "+dd)
          process_file(dd)

##
## process files changed in the last commit
##
if not process_all_files:
  print("\nFinding files changed in last git commit\n")
  pngs = os.popen("git log --name-only --pretty=oneline --full-index HEAD^^..HEAD | grep 'Images-HT/starwars'").read()
  pngs = pngs.split("\n")
  pngs.sort()
  for f in pngs:
    if f != "":
      if ("t_" in f):
        print("  IGNORING: "+f)
      else:
        print("  "+f)
        process_file(f)


exit(0)



