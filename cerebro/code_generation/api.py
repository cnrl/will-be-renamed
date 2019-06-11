import os
import importlib

from jinja2 import FileSystemLoader, Environment
from sympy import Symbol

from cerebro.exceptions import IllegalStateException


# generates cpp code, compiles it and returns dynamically loaded module
def generate(net_id, populations, connections):
    base_path = _create_dirs(net_id)

    _generate_files(base_path, populations, connections)

    _compile_files(base_path)

    return _load_module(net_id)


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


def _generate_population_dependent_variable_codes(connection, variable):
    var_access_code = None

    for population_indicator in ['pre', 'post']:
        split_factor = '_{}_'.format(population_indicator)
        if split_factor in variable:
            population_dependent_variable = variable.split(split_factor)[-1]
            target_population = getattr(connection, population_indicator)

            var_access_code = 'population{}.{}'.format(target_population.id, population_dependent_variable)
            if target_population.neuron.variables.vars[population_dependent_variable]['scope'] == 'self':
                var_access_code += '[rank_{}]'.format(population_indicator)

    return var_access_code


def _generate_population_update_equations(population):
    equations = population.neuron.equations.equations_list
    variables = population.neuron.variables.vars

    update_equations = []

    for equation in equations:
        lhs = equation['lhs_parsed']
        rhs = equation['rhs_parsed']
        for rhs_var in rhs.atoms():
            if isinstance(rhs_var, Symbol) and variables[str(rhs_var)]['scope'] == 'self':
                symbol = Symbol(str(rhs_var) + '[i]')
                rhs = rhs.subs(rhs_var, symbol)

        update_equations.append((str(lhs), rhs))

    return update_equations


def _generate_spike_conditions(population):
    condition = population.neuron.spike.equations_list[0]
    variables = population.neuron.variables.vars

    equation = condition["equation"]
    for var in equation.atoms():
        if isinstance(var, Symbol) and variables[str(var)]['scope'] == 'self':
            symbol = Symbol(str(var) + '[i]')
            equation = equation.subs(var, symbol)

    return str(equation)


def _generate_reset_equations(population):
    equations = population.neuron.reset.equations_list
    variables = population.neuron.variables.vars
    reset_equations = []

    for equation in equations:
        sides = [equation['lhs_parsed'], equation['rhs_parsed']]
        for i in range(len(sides)):
            for var in sides[i].atoms():
                if isinstance(var, Symbol) and variables[str(var)]['scope'] == 'self':
                    symbol = Symbol(str(var) + '[i]')
                    sides[i] = sides[i].subs(var, symbol)
        reset_equations.append(str(sides[0]) + ' = ' + str(sides[1]))

    return reset_equations


def _generate_connection_update_equations(connection):
    equations = connection.synapse.equations.equations_list
    variables = connection.synapse.variables.vars

    update_equations = []

    for equation in equations:
        lhs = equation['lhs_parsed']
        rhs = equation['rhs_parsed']
        for rhs_var in rhs.atoms():
            symbol = None
            if _is_variable_population_dependent(rhs_var):
                symbol = _generate_population_dependent_variable_codes(connection, str(rhs_var))
            elif isinstance(rhs_var, Symbol) and variables[str(rhs_var)]['scope'] == 'self':
                symbol = Symbol(str(rhs_var) + '[i][j]')
            rhs = rhs.subs(rhs_var, symbol)

        update_equations.append((str(lhs), rhs))

    return update_equations


def _generate_populations(base_path, template_env, populations):
    template = template_env.get_template('population.hpp')

    for population in populations:
        update_equations = _generate_population_update_equations(population)
        spike_condition = _generate_spike_conditions(population) if population.neuron.spike is not None else None
        reset_equations = _generate_reset_equations(population)

        rendered = template.render(
            population=population,
            update_equations=update_equations,
            spike_condition=spike_condition,
            reset_equations=reset_equations
        )

        full_path = os.path.join(base_path, 'population{}.hpp'.format(population.id))
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()


def _generate_connections(base_path, template_env, connections):
    template = template_env.get_template('connection.hpp')

    for connection in connections:
        update_equations = _generate_connection_update_equations(connection)
        rendered = template.render(connection=connection, update_equations=update_equations)
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


def _load_module(net_id):
    return importlib.import_module('build.net{}.wrapper'.format(net_id))
