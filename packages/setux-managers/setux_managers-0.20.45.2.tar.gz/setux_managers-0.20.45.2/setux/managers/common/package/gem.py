from setux.core.package import CommonPackager


# pylint: disable=no-member


class Distro(CommonPackager):
    manager = 'gem'

    def do_init(self):
        self.target.distro.Package.install('ruby-dev')
        self.target.distro.Package.install('rubygems')

    def ls(self):
        ret, out, err = self.run('gem list')
        for line in self.out:
            line = line.replace('(', '')
            line = line.replace(')', '')
            n, *_, v = line.split()
            yield n, v

    def do_installed(self):
        for n, v in self.ls():
            yield n , v

    def do_available(self):
        for n, v in self.ls():
            yield n , v

    def do_remove(self, pkg):
        self.run(f'gem uninstall {pkg}')

    def do_cleanup(self):
        pass

    def do_update(self):
        pass

    def do_install(self, pkg, ver=None):
        self.run(f'gem install {pkg}')
