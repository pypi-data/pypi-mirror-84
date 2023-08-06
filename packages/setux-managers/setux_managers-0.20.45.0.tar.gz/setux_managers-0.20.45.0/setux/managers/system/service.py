from setux.core.service import Service


class Debian(Service):
    manager = 'SystemD'

    def data(self, svc):
        ret, out, err = self.run(
            f'systemctl -q --no-pager show {svc}',
            report='quiet',
        )
        rows = (i.split('=', 1) for i in out)
        data = dict(i for i in rows if len(i)==2)
        return data

    def do_enabled(self, svc):
        data = self.data(svc)
        state = data.get('UnitFileState')
        return state=='enabled'

    def do_status(self, svc):
        data = self.data(svc)
        active = data['ActiveState']=='active'
        running = data['SubState']=='running'
        return active and running

    def do_start(self, svc):
        self.run(f'systemctl start {svc}')

    def do_stop(self, svc):
        self.run(f'systemctl stop {svc}')

    def do_restart(self, svc):
        self.run(f'systemctl restart {svc}')

    def do_enable(self, svc):
        self.run(f'systemctl enable {svc}')

    def do_disable(self, svc):
        self.run(f'systemctl disable {svc}')


class FreeBSD(Service):
    manager = 'Service'

    def update_conf(self, org, dst):
        cfg = '/etc/rc.conf'
        cont = target.read(cfg)
        if dst in cont: return
        done, updated = False, []
        for line in cont.split('\n'):
            if line == org:
                updated.append(dst)
                done = True
            else:
                updated.append(line)
        if not done:
            updated.append(dst)
        target.write(cfg, '\n'.join(updated))

    def do_status(self, svc):
        ret, out, err = self.run(f'service {svc} status')
        return out[0].startswith(f'{svc} is running')

    def do_start(self, svc):
        self.run(f'service {svc} onestart')

    def do_stop(self, svc):
        self.run(f'service {svc} onestop')

    def do_restart(self, svc):
        self.run(f'service {svc} onerestart')

    def do_enabled(self, svc):
        ret, out, err = self.run(f'service {svc} rcvar')
        return 'YES' in out[0]

    def _do_enable(self, svc):
        self.update_conf(
            org = f'{svc}_enable="NO"',
            dst = f'{svc}_enable="YES"',
        )

    def _do_disable(self, svc):
        self.update_conf(
            org = f'{svc}_enable="YES"',
            dst = f'{svc}_enable="NO"',
        )

    def _do_enable(self, svc):
        self.run(f'sysrc {svc}_enable=YES')

    def do_disable(self, svc):
        self.run(f'sysrc {svc}_enable=NO')

