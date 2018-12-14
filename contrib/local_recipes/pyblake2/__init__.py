from pythonforandroid.recipe import CythonRecipe
from pythonforandroid.toolchain import current_directory
import shutil
import glob

class Pyblake2bRecipe(CythonRecipe):

    version = '1.1.2'
    url = 'https://github.com/dchest/pyblake2/archive/v{version}.tar.gz'
    depends = ['setuptools']

#    def build_arch(self, arch):
#        super(Pyblake2bRecipe, self).build_arch(arch)

#        env = self.get_recipe_env(arch)
#        with current_directory(self.get_build_dir(arch.arch)):
#            so_file = glob.glob('./build/lib*/*so')
#            shutil.copyfile(so_file[0], self.ctx.get_libs_dir(arch.arch) + "/pyblake2.so")

recipe = Pyblake2bRecipe()
