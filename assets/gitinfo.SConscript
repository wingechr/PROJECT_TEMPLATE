from SCons.Script import Environment, Import  # type:ignore

env = Environment()
Import("env")  # this will overwrite env

# always save git buildinfo
env.AlwaysBuild(env.Command("#$BLD/.buildinfo", [], "git rev-parse HEAD > $TARGET"))
