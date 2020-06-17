from googleapiclient.http import MediaIoBaseUpload
from util import parse_roll
import mimetypes

def SavePDF(pdf, gdrive, cursor):
   # folder to upload pdf to
   pdf_folder_id = '15mfvhEPuILJafvBy617wa9ilkW-ukbfk'
   
   regno, semester = pdf.filename.split('.')[0].split('_') # pdf name eg: 2017UGCS036_5.pdf
   year, course, branch = parse_roll(regno)
   
   # upload pdf to gdrive here
   pdf_metadata = { 'name': pdf.filename, 'parents': [pdf_folder_id] }
   
   media = MediaIoBaseUpload(pdf.stream, mimetype= mimetypes.guess_type(pdf.mimetype)[0],
   chunksize=1024*1024, resumable=False)
   
   uploaded_pdf = gdrive.files().create(body=pdf_metadata,
                                          media_body=media,
                                          fields='id, webViewLink').execute()
   
   # update mysql database
   stmt = "UPDATE nilekrator${year}.{course}_{branch}_{semester} SET pdf_link='{pdf_link}' WHERE regno='{regno}'".format(
      year=year,
      course=course,
      branch=branch,
      semester=semester,
      pdf_link=uploaded_pdf['webViewLink'],
      regno=regno
   )
   cursor.execute(stmt)
   
   return {
      'regno': regno,
      'webview_link': uploaded_pdf['webViewLink']
   }