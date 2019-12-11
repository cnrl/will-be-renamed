"""This module is responsible for code generation procedure.

*Class*:

* **CodeGeneration**:
    Contains procedure to generate the C++ code.
"""


import os
import importlib
import shutil

from jinja2 import FileSystemLoader, Environment

from cerebro.exceptions import IllegalStateException


class CodeGeneration:
    """
    This class holds procedures for generating C++ code.
    """
    def __init__(self, network, populations, connections, network_variable_specs, population_variable_specs,
                 connection_variable_specs, population_equations, population_reset_equations,
                 population_spike_condition, connection_equations, connection_pre_spike, connection_post_spike):
        """
        :param network: The network object
        :param populations: List of populations in the network
        :param connections: List of connections in the network
        :param network_variable_specs: Specifications of variables in the network
        :param population_variable_specs: Specifications of variables in the populations
        :param connection_variable_specs: Specifications of variables in the connections
        :param population_equations: Equations defined in populations
        :param population_reset_equations: Equations defined in populations as neuron reset equations
        :param population_spike_condition: Logical expression in populations, defined as spike condition
        :param connection_equations: Equations defined in connections
        :param connection_pre_spike: Equations to be applied after pre-synaptic neuron's spike
        :param connection_post_spike: Equations to be applied after post-synaptic neuron's spike

        :type network: cerebro.models.network.Network
        :type populations: list
        :type connections: list
        :type network_variable_specs: list
        :type population_variable_specs: collections.defaultdict
        :type connection_variable_specs: collections.defaultdict
        :type population_equations: collections.defaultdict
        :type population_reset_equations: collections.defaultdict
        :type population_spike_condition: collections.defaultdict
        :type connection_equations: collections.defaultdict
        :type connection_pre_spike: collections.defaultdict
        :type connection_post_spike: collections.defaultdict
        """
        print(type(population_equations))
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
        self.connection_pre_spike = connection_pre_spike
        self.connection_post_spike = connection_post_spike
        self.base_path = self.create_dirs()

        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.base_templates_path = os.path.join(current_dir_path, 'templates')

        file_loader = FileSystemLoader(self.base_templates_path)
        self.template_env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    def generate(self):
        """
        Generates the files, compiles them and imports the network module.
        """
        self.generate_files()
        self.compile_files()
        return self.load_module()

    def compile_files(self):
        """
        Compiles the files.

        :raises: RuntimeError: If it fails to make the files.
        """
        os.chdir(self.base_path)
        return_code = os.system('make')
        if return_code:
            raise RuntimeError('make process failed')

    def generate_files(self):
        """
        Generates files, namely, the C++ code files, python modules and the MakeFile.
        """
        self.generate_cpp_codes()
        self.copy_python_modules()
        self.generate_make_file()

    def generate_cpp_codes(self):
        """
        Generates C++ codes.
        """
        self.generate_core()
        self.generate_connectivity()
        self.generate_random_functions()
        self.generate_delayed_potential()
        self.generate_populations()
        self.generate_connections()
        self.generate_wrapper()

    def copy_python_modules(self):
        """
        Copies python modules needed.
        """
        self.copy_monitoring_modules()

    def copy_monitoring_modules(self):
        """
        Copies monitoring modules.
        """
        module_to_copy_path = os.path.join(self.base_templates_path, 'monitoring.py')
        destination_path = os.path.join(self.base_path, 'monitoring.py')

        shutil.copyfile(module_to_copy_path, destination_path)

    def generate_core(self):
        """
        Generates the `core.h` and `core.cpp` files.
        """
        for template_name in ['core.h', 'core.cpp']:
            template = self.template_env.get_template(template_name)
            rendered = template.render(populations=self.populations, connections=self.connections,
                                       network_variables=self.network_variable_specs)

            full_path = os.path.join(self.base_path, template_name)
            file = open(full_path, "w+")

            file.write(rendered)

            file.close()

    def generate_bare_files(self, file_names):
        """
        Generates files defined by `file_names`.

        :param file_names: Name of files to be generated

        :type file_names: list
        """
        for template_name in file_names:
            template = self.template_env.get_template(template_name)
            rendered = template.render({})

            full_path = os.path.join(self.base_path, template_name)
            file = open(full_path, "w+")
            file.write(rendered)
            file.close()

    def generate_connectivity(self):
        """
        Generates the `connectivity.h` and `connectivity.cpp` files, responsible for types of connections.
        """
        self.generate_bare_files(['connectivity.cpp', 'connectivity.h'])

    def generate_delayed_potential(self):
        """
        Generates the `delayed_potential.h` and `delayed_potential.cpp` files, responsible for generics for delay.
        """
        self.generate_bare_files(['delayed_potential.cpp', 'delayed_potential.h'])

    def generate_random_functions(self):
        """
        Generates the `random_functions.h` and `random_functions.cpp` files, responsible for random functions.
        """
        self.generate_bare_files(['random_functions.cpp', 'random_functions.h'])

    def generate_populations(self):
        """
        Generates a file for each population in the network.
        """
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
        """
        Generates a file for each connection in the network.
        """
        template = self.template_env.get_template('connection.hpp')

        for connection in self.connections:
            update_equations = self.connection_equations[connection]
            update_pre_spike_equations = self.connection_pre_spike[connection]
            update_post_spike_equations = self.connection_post_spike[connection]
            variables = self.connection_variable_specs[connection]
            rendered = template.render(
                connection=connection,
                network_variables=self.network_variable_specs,
                variables=variables,
                update_equations=update_equations,
                update_pre_spike_equations=update_pre_spike_equations,
                update_post_spike_equations=update_post_spike_equations,
                connect_function=connection.connection_type.get_c_definition(connection)
            )
            full_path = os.path.join(self.base_path, 'connection{}.hpp'.format(connection.id))

            file = open(full_path, "w+")

            file.write(rendered)

            file.close()

    def generate_wrapper(self):
        """
        Generates the wrapper file.
        """
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
        """
        Generates the MakeFile.
        """
        import numpy

        template = self.template_env.get_template('Makefile')

        numpy_includes = "-I" + numpy.get_include()

        rendered = template.render(numpy_includes=numpy_includes)

        full_path = os.path.join(self.base_path, 'Makefile')
        file = open(full_path, "w+")

        file.write(rendered)

        file.close()

    def load_module(self):
        """
        Loads the module.
        """
        return importlib.import_module('build.net{}.wrapper'.format(self.network.id))

    def create_dirs(self):
        """
        Creates the directories for files.

        :returns: Base path of the directory

        :rtype: str

        :raises: IllegalStateException: If the directory `build` already exists.
        """
        cwd = os.getcwd()

        dir_path = os.path.join(cwd, 'build')

        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        base_path = os.path.join(dir_path, 'net' + str(self.network.id))
        if os.path.exists(base_path):
            raise IllegalStateException("directory {} already exists".format(base_path))
        os.mkdir(base_path)
        return base_path
