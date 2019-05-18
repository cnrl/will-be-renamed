import os
from jinja2 import FileSystemLoader, Environment
from cnrl.code_generators.models import Population, Projection
from cnrl.exceptions import IllegalStateException, IllegalArgumentException


# generates cpp code, compiles it and returns dynamically loaded module
def generate(name, pops, projs):
    _check_args(name, pops, projs)

    base_path = _create_dirs(name)

    _generate_files(base_path, pops, projs)


def _check_args(name, pops, projs):
    if type(name) != str:
        raise IllegalArgumentException("name must be a string")

    if type(pops) != list:
        raise IllegalArgumentException("pops must be a list")
    for pop in pops:
        if not isinstance(pop, Population):
            raise IllegalArgumentException("pops must be a list of Populations")

    if type(projs) != list:
        raise IllegalArgumentException("projs must be a list")
    for proj in projs:
        if not isinstance(proj, Projection):
            raise IllegalArgumentException("projs must be a list of Projections")


def _create_dirs(name):
    cwd = os.getcwd()

    dir_path = os.path.join(cwd, 'build')

    if os.path.exists(dir_path):
        raise IllegalStateException('cannot create build folder, a file or directory with this name exists')

    os.mkdir(dir_path)

    base_path = os.path.join(dir_path, name)
    os.mkdir(base_path)

    return base_path


def _generate_files(base_path, pops, projs):
    current__dir_path = os.path.dirname(os.path.abspath(__file__))

    file_loader = FileSystemLoader(os.path.join(current__dir_path, 'templates'))
    template_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    _generate_cpp_codes(base_path, template_env, pops, projs)


def _generate_cpp_codes(base_path, template_env, pops, projs):
    _generate_core(base_path, template_env, pops, projs)
    _generate_populations(base_path, template_env, pops)


def _generate_core(base_path, template_env, pops, projs):
    for template_name in ['core.h', 'core.cpp']:
        template = template_env.get_template(template_name)
        rendered = template.render(pops=pops, projs=projs)

        full_path = os.path.join(base_path, template_name)
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()


def _generate_populations(base_path, template_env, pops):
    template = template_env.get_template('pop.hpp')

    for pop in pops:
        rendered = template.render(pop=pop)

        full_path = os.path.join(base_path, '{}.hpp'.format(pop.name))
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()
