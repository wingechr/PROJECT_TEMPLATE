import os
import logging

logging.basicConfig(
    format="[%(asctime)s %(levelname)7s] %(message)s",
    level=logging.INFO
)

env = Environment(
    ENV=os.environ,
    TMP="temp",
    BLD="build",
    SRC="src",
    DEBUG=True
)

if not Virtualenv():
    logging.warning('VIRTUAL_ENV not activated')

env.Decider('MD5-timestamp')
env.Clean('all', ['$TMP', '$BLD'])

Export('env')
SConscript(env.GetBuildPath('#/$SRC/js/SConscript'))
SConscript(env.GetBuildPath('#/$SRC/css/SConscript'))
SConscript(env.GetBuildPath('#/$SRC/html/SConscript'))
SConscript(env.GetBuildPath('#/$SRC/static/SConscript'))
