#######################Database conf############################

import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://mdx8:I.lovecpu758400@localhost/low-life'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

##################################################################