from logging.handlers import RotatingFileHandler
import logging, os
from zipfile import ZipFile, ZIP_DEFLATED

class CompressingRotatingFileHandler(RotatingFileHandler):
   
   def __init__(self, *args, **kws):
      super().__init__(*args, **kws)
            
   def rotate(self, source, dest):
      '''
         Custom rotate method to compress from (say .*.log -> .*.log.zip)
         and remove the source file
      '''
      with ZipFile(dest, 'w', compression=ZIP_DEFLATED) as zp, open(source) as src:
         zp.writestr( os.path.split(source)[1], src.read())
   
      os.remove(source)
      
   def doRollover(self):
      """
      Do a rollover, as described in __init__().
      """
      if self.stream:
         self.stream.close()
         self.stream = None
         
      if self.backupCount > 0:
         for i in range(self.backupCount - 1, 0, -1):
               sfn = self.rotation_filename("%s.%d.zip" % (self.baseFilename, i))
               dfn = self.rotation_filename("%s.%d.zip" % (self.baseFilename,
                                                      i + 1))
               if os.path.exists(sfn):
                  if os.path.exists(dfn):
                     os.remove(dfn)
                  os.rename(sfn, dfn)  # older files are renamed here
                  
         dfn = self.rotation_filename(self.baseFilename + ".1.zip")
         if os.path.exists(dfn):
               os.remove(dfn)
         
         self.rotate(self.baseFilename, dfn) # new file is archived here
         
      if not self.delay:
         self.stream = self._open()