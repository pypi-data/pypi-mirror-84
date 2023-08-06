import setuptools
import setup
from distutils.core import setup
from distutils.command.clean import clean
from distutils.command.install import install


class MyInstall(install):

    # Calls the default run command, then deletes the build area
    # (equivalent to "setup clean --all").
    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()


if __name__ == "__main__":

    print(f'found packages: {setuptools.find_packages()}')
    setup(
        # cmdclass={'install': MyInstall},
        name='utp',         # How you named your package folder (MyLib)
        packages=setuptools.find_packages(),   # Chose the same as "name"
        version='0.2',      # Start with a small number and increase it with every change you make
        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
        license='MIT',
        # Give a short description about your library
        description='helper functions for typical python problems',
        author='Patryk Seweryn',                   # Type in your name
        author_email='patryk.seweryn@gmail.com',      # Type in your E-Mail
        # Provide either the link to your github or to your website
        url='https://github.com/user/reponame',
        # I explain this later on
        download_url='https://github.com/p-severin/utp/archive/v_0.1.tar.gz',
        # Keywords that define your package best
        keywords=['images', 'preprocessing', 'python'],
        install_requires=[            # I get to this in a second
            'opencv-python',
        ],
        classifiers=[
            # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Development Status :: 3 - Alpha',
            # Define that your audience are developers
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',   # Again, pick a license
            # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
        ],
    )
