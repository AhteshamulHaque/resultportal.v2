import re, json
import commands.scraper.roll_option as roll_option
import commands.scraper.range_option as range_option

'''
{ File content
      "roll_query": {
         "roll1": [...semesters...],
         "roll2": [...semesters...],
         ...................,
      },

   "range_query": [
         { "start": "...", "end": "...", "semesters": [...] } ,
         { "start": "...", "end": "...", "semesters": [...] } ,
         ........,
      ]
   }
   
   start -> 2017UGCS002
   end -> 2017UGCS034
'''
   
def execute(file_obj):
   '''
      This function downloads every result for every semester from the rolls array
   '''
   query = json.load(file_obj)
   
   if query.get('roll_query'):
      
      for roll, semesters in query.items():
         roll_option.execute(roll, semesters, False)
         
   
   if query.get('range_query'):
      
      for _range in query['range_query']:
         range_option.execute( _range['start']+'-'+_range['end'], _range['semesters'], False)    