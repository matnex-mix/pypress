'''
    template rendering algorithm
'''
from models import define
import os,re

class Render:
    def __init__(self, template, data):
        self.path = template
        self.data = data
        self.workspace = ''
        if( os.path.isfile(define.PYPRESS_HOME+'\\'+template+'.html') ):
            self.workspace = define.PYPRESS_HOME+'\\'
            self.path = self.workspace+template+'.html'
        elif( os.path.isfile(define.PYPRESS_HOME+'\\controllers\\default\\templates\\'+template+'.html') ):
            self.workspace = define.PYPRESS_HOME+'\\controllers\\default\\templates\\'
            self.path = self.workspace+template+'.html'
        else:
            self.template_string = 'Template File not found'
            return False
        with open(self.path) as template_string:
            self.template_string = template_string.read()

    def show(self):
        self.include_files()
        self.inject_data()
        self.run_logics()

        return self.template_string

    # file could be included thus:
    # {{i=filename}}
    def include_files(self):
        includes = re.findall("\{\{i=[^\{\}]+\}\}", self.template_string)
        for inc in includes:
            file = inc.split('=')[1].replace('}}', '')
            if( os.path.isfile(self.workspace+file+'.html') ):
                with open(self.workspace+file+'.html') as file:
                    file = file.read()
                self.template_string = self.template_string.replace(inc, file)

    # data injection in this format:
    # {{data}}
    def inject_data(self):
        # Case 1: simple data replacement: {{data_key}}
        includes = re.findall("\{\{[\w]+\}\}", self.template_string)
        for inc in includes:
            data_key = inc.split('{{')[1].replace('}}', '')
            if( self.data.get(data_key) != None ):
                self.template_string = self.template_string.replace(inc, str(self.data[data_key]))

        # Case 2: complex data replacement
        

    def run_logics(self):
        self.template_string