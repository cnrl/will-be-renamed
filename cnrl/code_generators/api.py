import os
from jinja2 import FileSystemLoader, Environment
from sympy import Symbol

from cnrl.exceptions import IllegalStateException
from cnrl.globals import SUBSCRIPTABLE_VAR_NAMES

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

def _is_variable_population_dependent(variable):
    return str(variable).startswith('_')

def _generate_population_dependent_variable_codes(variable):
    for population in ['pre', 'post']:
        population_indicator = '_{}_'.format(population)
        if population_indicator in variable:
            population_dependent_variable = variable.split(population)[-1]
            return "population{{ connection.{}.id }}.{}[rank_{}]".format(
                population,
                population_dependent_variable,
                population
            )

def _generate_variable_equation_codes(equations, variables):
    codes = []
    for equation in equations:
        lhs = equation['lhs_parsed']
        rhs = equation['rhs_parsed']
        for rhs_var in rhs.atoms():
            print(rhs, type(rhs))
            if _is_variable_population_dependent(rhs_var):
                sym = Symbol(_generate_population_dependent_variable_codes(str(rhs_var)))
                rhs = rhs.subs(rhs_var, sym)
            elif isinstance(rhs_var, Symbol) and \
                    (str(rhs_var) in SUBSCRIPTABLE_VAR_NAMES or
                             variables[str(rhs_var)]['scope'] == 'self'):
                sym = Symbol(str(rhs_var) + '[i]')
                print(str(rhs_var) , sym, rhs)
                rhs = rhs.subs(rhs_var , sym)

        codes.append((str(lhs), rhs))

    return codes

def _generate_populations(base_path, template_env, populations):
    template = template_env.get_template('population.hpp')

    for population in populations:
        codes = _generate_variable_equation_codes(
            population.neuron.equations.equations_list,
            population.neuron.parameters.vars
        )
        rendered = template.render(population=population, codes=codes)

        full_path = os.path.join(base_path, 'population{}.hpp'.format(population.id))
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()


def _generate_connections(base_path, template_env, connections):
    template = template_env.get_template('connection.hpp')

    for connection in connections:
        codes = _generate_variable_equation_codes(
            connection.synapse.equations.equations_list,
            connection.synapse.parameters.vars
        )
        rendered = template.render(connection=connection, codes=codes)
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
