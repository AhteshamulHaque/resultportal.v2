from googleapiclient.http import MediaIoBaseUpload
import os

def SaveImage(images, gdrive, cursor):
   # folder to upload image to
   image_folder_id = '1r5e_KfOn9M1zXc7V9Hp1wnPZ5fbSuruD'
   
   # Call the Drive v3 API
   for image in images:
      
      student_id = image.split('.')[0] # image name eg: 2342.jpg
      
      # upload image to gdrive here
      try:
         image_metadata = { 'name': image.filename, 'parents': [image_folder_id] }
         
         media = MediaIoBaseUpload(image.stream, mimetype=image.mimetype,
         chunksize=1024*1024, resumable=False)
         
         uploaded_image = gdrive.files().create(body=image_metadata,
                                                media_body=media,
                                                fields='webViewLink, thumbnailLink').execute()
         
         # update mysql database
         stmt = "UPDATE nilekrator$admin.users SET thumbnail_link='{thumbnail_link}', image_link='{image_link}' WHERE student_id='{student_id}'".format(
            thumbnail_link=uploaded_image['thumbnailLink'],
            image_link=uploaded_image['webViewLink'],
            student_id=student_id
         )
         cursor.execute(stmt)
         
         
      except Exception as error:
         print(error)