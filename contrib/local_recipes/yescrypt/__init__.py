from pythonforandroid.recipe import CythonRecipe


class YescryptRecipe(CythonRecipe):

    url = 'https://github.com/wo01/yescrypt_python/archive/master.zip'

    patches = ['./setup.patch']

recipe = YescryptRecipe()
