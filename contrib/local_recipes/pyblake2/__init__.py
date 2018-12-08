from pythonforandroid.recipe import CythonRecipe


class Pyblake2bRecipe(CythonRecipe):

    url = 'https://github.com/dchest/pyblake2/archive/master.zip'
    depends = ['setuptools']

recipe = Pyblake2bRecipe()
