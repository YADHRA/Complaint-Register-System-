import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yadhra@2006')
    SQLALCHEMY_DATABASE_URI = 'postgresql://srs_cfbj_user:c6virotY64HWY1wTrCGZ1M2n16r40rKp@dpg-d3e04dnfte5s73f2mmi0-a.singapore-postgres.render.com/srs_cfbj'
    SQLALCHEMY_TRACK_MODIFICATIONS = False