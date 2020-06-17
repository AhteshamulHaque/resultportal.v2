# for testing purpose
import urllib.parse
import requests, re, os, json, traceback, time
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
      placeholder_text = Template(Style.BRIGHT+"$text |Progress: $progress%|")
      
      # download text
      download_text = "Downloading Images"
      
      # upload text
      upload_text = "Uploading Images"
      
      # file contained id of failed downloads
      fp = open('logs/images.failed.log', 'a')

      with yaspin(color="cyan") as sp:
         
         for index, img_info in enumerate(image_list):
            
            if op_type == 'upload':
               text = upload_text
            elif op_type == 'download':
               text = download_text
            
            progress = "{:.1f}".format( (index/ len(image_list)) * 100)
            
            sp.text = placeholder_text.substitute(text=text, progress=progress)
               
            try:
               
               if op_type == 'upload':
                  self.upload_image(img_info, url) # img_info is either filename or filepath
                  
               elif op_type == 'download':   
                  # download image
                  self.download_image( str(img_info), url) # image_info is an id
               
               # log the download success
               sp.write(Fore.GREEN+"[ SUCCESS ] "+Style.RESET_ALL+"--- {img_info}".format(img_info=img_info))
               
            except Exception as error:
               # log the error on stdout
               sp.write(Fore.RED+f"[ FAILED - {error.__class__.__name__} ] "+Style.RESET_ALL+"--- {img_info}".format(img_info=img_info))
               
               # log the error in a file in json format
               if op_type == 'upload':
                  fp.write( json.dumps({"img_info": img_info, "type": "upload", "error": traceback.format_exc()}) )
                  fp.write('\n')
                  
               elif op_type == 'download':
                  fp.write(json.dumps({"img_info": img_info, "type": "download", "error": traceback.format_exc()}) )
                  fp.write('\n')
                  
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
      time.sleep(1)
        
      with requests.get( urllib.parse.urljoin(url, img_id+'.jpg'), stream=True ) as resp:
         resp.raise_for_status()
         
         # image extension from content-type using regex for jpeg, png, jpg files
         # EXPECTING ONLY `JPEG` AND `PNG` FILE
         img_ext = re.match(r'image/([a-z]+)', resp.headers.get('content-type', 'image/jpeg')).group(1)
         
         if not os.path.exists( self.image_dir ):
            os.makedirs( self.image_dir )
            
         with open( os.path.join( self.image_dir, img_id+'.'+img_ext) , 'wb') as fp:
            for chunk in resp.iter_content(chunk_size=1024):
                  fp.write(chunk)
                  
      
   def upload_image(self, img_path, url):
      
      resp = None
      with open(img_path, 'rb') as fp:
         resp = requests.post(url, files={'image': fp})
         resp.raise_for_status()
      