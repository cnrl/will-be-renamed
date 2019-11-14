import os
import importlib
import shutil

from jinja2 import FileSystemLoader, Environment

from cerebro.exceptions import IllegalStateException


class CodeGeneration:
    def __init__(self, network, populations, connections, network_variable_specs, population_variable_specs,
                 connection_variable_specs, population_equations, population_reset_equations,
                 population_spike_condition, connection_equations):
        self.network = network
        self.populations = populations
        self.connections = connections
        self.network_variable_specs = network_variable_specs
        self.population_variable_specs = population_variable_specs
        self.connection_variable_specs = connection_variable_specs
        self.population_equations = population_equations
        self.population_reset_equations = population_reset_equations
        self.population_spike_condition = population_spike_condition
        self.connection_equations = connection_equations
        self.base_path = self.create_dirs()

        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.base_templates_path = os.path.join(current_dir_path, 'templates')

        file_loader = FileSystemLoader(self.base_templates_path)
        self.template_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    def generate(self):
        self.generate_files()
        self.compile_files()
        return self.load_module()

    def compile_files(self):
        os.chdir(self.base_path)
        return_code = os.system('make')
        if return_code:
            raise RuntimeError('make process failed')

    def generate_files(self):
        self.generate_cpp_codes()
        self.copy_python_modules()
        self.generate_make_file()

    def generate_cpp_codes(self):
        self.generate_core()
        self.generate_connectivity()
        self.generate_random_functions()
        self.generate_delayed_potential()
        self.generate_populations()
        self.generate_connections()
        self.generate_wrapper()

    def copy_python_modules(self):
        self.copy_monitoring_modules()

    def copy_monitoring_modules(self):
        module_to_copy_path = os.path.join(self.base_templates_path, 'monitoring.py')
        destination_path = os.path.join(self.base_path, 'monitoring.py')

        shutil.copyfile(module_to_copy_path, destination_path)

    def generate_core(self):
        for template_name in ['core.h', 'core.cpp']:
            template = self.template_env.get_template(template_name)
            rendered = template.render(populations=self.populations, connections=self.connections,
                                       network_variables=self.network_variable_specs)

            full_path = os.path.join(self.base_path, template_name)
            file = open(full_path, "w+")

            file.write(rendered)

            file.close()

    def generate_bare_files(self, file_names):
        for template_name in file_names:
            template = self.template_env.get_template(template_name)
            rendered = template.render({})

            full_path = os.path.join(self.base_path, template_name)
            file = open(full_path, "w+")
            file.write(rendered)
            file.close()

    def generate_connectivity(self):
        self.generate_bare_files(['connectivity.cpp', 'connectivity.h'])

    def generate_delayed_potential(self):
        self.generate_bare_files(['delayed_potential.cpp', 'delayed_potential.h'])

    def generate_random_functions(self):
        self.generate_bare_files(['random_functions.cpp', 'random_functions.h'])

    def generate_populations(self):
        template = self.template_env.get_template('population.hpp')

        for population in self.populations:
            update_equations = self.population_equations[population]
            spike_condition = self.population_spike_condition[population]
            reset_equations = self.population_reset_equations[population]

            rendered = template.render(
                population_id=population.id,
                network_variables=self.network_variable_specs,
                variables=self.population_variable_specs[population],
                update_equations=update_equations,
                spike_condition=spike_condition,
                reset_equations=reset_equations
            )

            full_path = os.path.join(self.base_path, 'population{}.hpp'.format(population.id))
            file = open(full_path, "w+")

            file.write(rendered)

            file.close()

    def generate_connections(self):
        template = self.template_env.get_template('connection.hpp')

        for connection in self.connections:
            update_equations = self.connection_equations[connection]
            variables = self.connection_variable_specs[connection]
            rendered = template.render(
                connection=connection,
                network_variables=self.network_variable_specs,
                variables=variables,
                update_equations=update_equations,
                connect_function=connection.connection_type.get_c_definition(connection)
            )
            full_path = os.path.join(self.base_path, 'connection{}.hpp'.format(connection.id))

            file = open(full_path, "w+")

            file.write(rendered)

            file.close()

    def generate_wrapper(self):
        template = self.template_env.get_template('wrapper.pyx')

        rendered = template.render(populations=self.populations,
                                   population_variable_specs=self.population_variable_specs,
                                   connections=self.connections,
                                   connection_variable_specs=self.connection_variable_specs,
                                   network_variable_specs=self.network_variable_specs)

        full_path = os.path.join(self.base_path, 'wrapper.pyx')
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()

    def generate_make_file(self):
        import numpy

        template = self.template_env.get_template('Makefile')

        numpy_includes = "-I" + numpy.get_include()

        rendered = template.render(numpy_includes=numpy_includes)

        full_path = os.path.join(self.base_path, 'Makefile')
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()

    def load_module(self):
        return importlib.import_module('build.net{}.wrapper'.format(self.network.id))

    def create_dirs(self):
        cwd = os.getcwd()

        dir_path = os.path.join(cwd, 'build')

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        base_path = os.path.join(dir_path, 'net' + str(self.network.id))
        if os.path.exists(base_path):
            raise IllegalStateException("directory {} already exists".format(base_path))
        os.mkdir(base_path)
        return base_path
