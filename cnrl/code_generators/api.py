import os
from jinja2 import FileSystemLoader, Environment

from cnrl.exceptions import IllegalStateException


# generates cpp code, compiles it and returns dynamically loaded module
def generate(net_id, populations, connections):
    base_path = _create_dirs(net_id)

    _generate_files(base_path, populations, connections)


def _create_dirs(net_id):
    cwd = os.getcwd()

    dir_path = os.path.join(cwd, 'build')

    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    base_path = os.path.join(dir_path, 'net' + str(net_id))
    if os.path.exists(base_path):
        raise IllegalStateException("directory {} already exists".format(base_path))
    os.mkdir(base_path)

    return base_path


def _generate_files(base_path, populations, connections):
    current_dir_path = os.path.dirname(os.path.abspath(__file__))

    file_loader = FileSystemLoader(os.path.join(current_dir_path, 'templates'))
    template_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    _generate_cpp_codes(base_path, template_env, populations, connections)


def _generate_cpp_codes(base_path, template_env, populations, connections):
    _generate_core(base_path, template_env, populations, connections)
    _generate_populations(base_path, template_env, populations)
    _generate_connections(base_path, template_env, connections)

def _generate_core(base_path, template_env, populations, connections):
    for template_name in ['core.h', 'core.cpp']:
        template = template_env.get_template(template_name)
        rendered = template.render(populations=populations, connections=connections)

        full_path = os.path.join(base_path, template_name)
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()


def _generate_populations(base_path, template_env, populations):
    template = template_env.get_template('population.hpp')

    for population in populations:
        rendered = template.render(population=population)

        full_path = os.path.join(base_path, 'population{}.hpp'.format(population.id))
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()

def _generate_connections(base_path, template_env, connections):
    template = template_env.get_template('connection.hpp')

    for connection in connections:
        print(connection)
        rendered = template.render(connection=connection)
        full_path = os.path.join(base_path, 'connection{}.hpp'.format(connection.id))

        file = open(full_path, "w+")

        file.write(rendered)

        file.close()

