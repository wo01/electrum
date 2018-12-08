from pythonforandroid.recipe import CythonRecipe


class Pyblake2bRecipe(CythonRecipe):

    version = '1.1.2'
    url = 'https://github.com/dchest/pyblake2/archive/v{version}.tar.gz'
    depends = ['setuptools']

recipe = Pyblake2bRecipe()
