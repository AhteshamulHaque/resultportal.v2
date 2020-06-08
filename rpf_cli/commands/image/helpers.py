# for testing purpose
import urllib.parse
import requests, re, os, json, traceback
from yaspin import yaspin
from colorama import init, Fore, Back, Style
from string import Template

class ImageDownloaderUploader:
   
   def __init__(self):
       self.image_dir  = 'images'
   
   def download_upload_with_progress(self, image_list, url, op_type):
      
      '''
         image_list -> list of images to upload ( list of ids ) or download( list of filepath or filename)
         url -> url to upload image to or download from
         op_type -> ['upload', 'download']
      '''
      
      init(autoreset=True)

      # variable text
      placeholder_text = Template(Fore.YELLOW+Style.BRIGHT+Back.BLACK+"$text |Progress: $progress%|")
      
      # download text
      download_text = Template("Downloading image with student_id=$img_id")
      
      # upload text
      upload_text = Template("Uploading image with student_id=$img_id")
      
      # file contained id of failed downloads
      fp = open('images.failed.log', 'a')

      with yaspin(color="cyan") as sp:
         
         for index, img_info in enumerate(image_list):
            
            if op_type == 'upload':
               text = upload_text.substitute(img_id=img_info)
            elif op_type == 'download':
               text=download_text.substitute(img_id=img_info)
            
            progress = "{:.1f}".format( (index/ len(image_list)) * 100)
            
            sp.text = placeholder_text.substitute(text=text, progress=progress)
               
            try:
               
               if op_type == 'upload':
                  self.upload_image(img_info, url) # img_info is here filename or filepath
                  
               elif op_type == 'download':   
                  # download image
                  self.download_image( str(img_info), url) # imag_info is here an id
               
               # log the download success
               sp.write(Fore.GREEN+Style.BRIGHT+"✔ "+Style.RESET_ALL+"student_id={img_info}".format(img_info=img_info))
               
            except Exception:
               # log the error on stdout
               sp.write(Fore.RED+Style.BRIGHT+"✕ student_id={img_info} ".format(img_info=img_info)+Fore.RED+"FAILED!")
               # log the error in a file in json format
               
               if op_type == 'upload':
                  fp.write(json.dumps({'img_info': img_info, 'type': 'upload', 'error': traceback.format_exc()})+'\n')
                  
               elif op_type == 'download':
                  fp.write(json.dumps({'img_info': img_info, 'type': 'download', 'error': traceback.format_exc()})+'\n')
                  
      # The below line updates the progress to 100% which is not done
      # in the last step of the previous for loop
      sp.text = placeholder_text.substitute(text="Completed", progress=100)
      
      # finalize
      sp.ok("✔")
      
      # close file
      fp.close()
      
   
   def download_image(self, img_id, url):
      # resp = requests.get(url.format(str(img_id)+'.jpg'))
      
      # for testing purpose   
      with requests.get( urllib.parse.urljoin(url, img_id+'.jpg'), stream=True ) as resp:
         resp.raise_for_status()
         
         # image extension from content-type using regex for jpeg, png, jpg files
         # EXPECTING ONLY `JPEG` AND `PNG` FILE
         img_ext = re.match(r'image/([a-z]+)', resp.headers.get('content-type', 'image/jpeg')).group(1)
         
         #TODO: add progress bar download support
         if not os.path.exists( self.image_dir ):
            os.makedirs( self.image_dir )
            
         with open( os.path.join( self.image_dir, img_id+'.'+img_ext) , 'wb') as fp:
            for chunk in resp.iter_content(chunk_size=1024):
                  fp.write(chunk)
                  
      
   def upload_image(self, img_path, url):
      
      with open(img_path, 'rb') as fp:
         resp = requests.post(url, {'images': fp})
         resp.raise_for_status()