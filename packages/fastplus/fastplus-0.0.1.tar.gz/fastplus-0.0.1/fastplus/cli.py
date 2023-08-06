from pathlib import Path

import click


class FastPlusCommands(click.MultiCommand):
    COMMANDS_DIR = Path(__file__).parent.absolute() / 'commands'

    def list_commands(self, ctx):
        print(self.COMMANDS_DIR)
        commands_list = []
        for filename in map(lambda p: p.parts[-1], self.COMMANDS_DIR.rglob('*.py')):
            if not filename.startswith('_'):
                commands_list.append(filename[:-3])
        return commands_list

    def get_command(self, ctx, name):
        namespace = {}
        command_path = self.COMMANDS_DIR / (name + '.py')
        with open(command_path) as f:
            code = compile(f.read(), command_path, 'exec')
            eval(code, namespace, namespace)
        return namespace[name]


@click.command(
    cls=FastPlusCommands
)
def fastplus():
    pass


if __name__ == '__main__':
    fastplus()
