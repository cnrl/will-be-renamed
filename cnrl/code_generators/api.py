import os
from jinja2 import FileSystemLoader, Environment

from cnrl.exceptions import IllegalStateException


# generates cpp code, compiles it and returns dynamically loaded module
def generate(net_id, populations, connections):
    base_path = _create_dirs(net_id)

    _generate_files(base_path, populations, connections)

    _compile_files(base_path)


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
    _generate_make_file(base_path, template_env)


def _generate_cpp_codes(base_path, template_env, populations, connections):
    _generate_core(base_path, template_env, populations, connections)
    _generate_populations(base_path, template_env, populations)
    _generate_connections(base_path, template_env, connections)
    _generate_wrapper(base_path, template_env, populations, connections)


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
        rendered = template.render(connection=connection)
        full_path = os.path.join(base_path, 'connection{}.hpp'.format(connection.id))

        file = open(full_path, "w+")

        file.write(rendered)

        file.close()


def _generate_wrapper(base_path, template_env, populations, connections):
    template = template_env.get_template('wrapper.pyx')

    rendered = template.render(populations=populations, connections=connections)

    full_path = os.path.join(base_path, 'wrapper.pyx')
    file = open(full_path, "w+")

    file.write(rendered)

    file.close()


def _generate_make_file(base_path, template_env):
    import numpy

    template = template_env.get_template('Makefile')

    numpy_includes = "-I" + numpy.get_include()

    rendered = template.render(numpy_includes=numpy_includes)

    full_path = os.path.join(base_path, 'Makefile')
    file = open(full_path, "w+")

    file.write(rendered)

    file.close()


def _compile_files(base_path):
    os.chdir(base_path)
    return_code = os.system('make')
    if return_code:
        raise RuntimeError('make process failed')
