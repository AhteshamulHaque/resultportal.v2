from googleapiclient.http import MediaIoBaseUpload
import os, mimetypes

def SaveImage(image, gdrive, cursor):
   
   # folder to upload image to
   image_folder_id = '1Sz_0-nAde9_4FSPjnduorbOCqx8Yri6I'
      
   student_id = image.filename.split('.')[0] # image name eg: 2342.jpg
   
   # upload image to gdrive here
   image_metadata = { 'name': image.filename, 'parents': [image_folder_id] }
   
   # FIXME: image.mimetype is None, reason not known, hence used mimetype module
   media = MediaIoBaseUpload(image.stream, mimetype= mimetypes.guess_type(image.filename)[0],
   chunksize=1024*1024, resumable=False)

   uploaded_image = gdrive.files().create(body=image_metadata,
                                          media_body=media,
                                          fields='id, webViewLink, thumbnailLink').execute()
   
   # update mysql database
   stmt = "UPDATE nilekrator$admin.users SET thumbnail_link='{thumbnail_link}', webview_link='{webview_link}' WHERE student_id='{student_id}'".format(
      thumbnail_link=uploaded_image['thumbnailLink'],
      webview_link=uploaded_image['webViewLink'],
      student_id=student_id
   )
   cursor.execute(stmt)
   
   return {
      'student_id': student_id,
      'thumbnail_link': uploaded_image['thumbnailLink'],
      'webview_link': uploaded_image['webViewLink']
   }