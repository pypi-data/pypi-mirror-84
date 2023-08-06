from setux.core.package import CommonPackager


# pylint: disable=no-member


class Distro(CommonPackager):
    manager = 'npm'

    def do_init(self):
        self.target.distro.Package.install('npm')

    def ls(self):
        ret, out, err = self.run('npm list -g --depth=0')
        for line in self.out[1:]:
            if len(line)<5: continue
            n, v = line[4:].split('@')
            yield n, v

    def do_installed(self):
        for n, v in self.ls():
            yield n , v

    def do_available(self):
        for n, v in self.ls():
            yield n , v

    def do_remove(self, pkg):
        self.run(f'npm uninstall {pkg}')

    def do_cleanup(self):
        pass

    def do_update(self):
        pass

    def do_install(self, pkg, ver=None):
        self.run(f'npm install -g {pkg}')
