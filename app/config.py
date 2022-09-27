#######################Database conf############################

import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysql://mdx8:I.lovesarrah758400@localhost/low-life')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

##################################################################

