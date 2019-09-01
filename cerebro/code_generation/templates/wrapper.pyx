# cython: embedsignature=True
from libcpp.vector cimport vector
import numpy as np
cimport numpy as np

cdef extern from "core.h":

    cpdef long int get_time() ;
    cpdef void set_time(long int) ;

    cpdef double get_dt() ;
    cpdef void set_dt(double);

    cpdef void initialize(double) ;

    cpdef void run(int);


    {% for population in populations %}
    cdef struct Population{{ population.id }}:
        int get_size()
        void set_size(int)

        {% for var in population_variable_specs[population] %}
        {% if var.scope == 'shared' %}
        {{ var.c_type }}  get_{{ var.name }}()
        void set_{{ var.name }}({{ var.c_type }})
        {% elif var.scope == 'local' %}
        vector[{{ var.c_type }}] get_{{ var.name }}()
        {{ var.c_type }} get_single_{{ var.name }}(int)
        void set_{{ var.name }}(vector[{{ var.c_type }}])
        void set_single_{{ var.name }}(int, {{ var.c_type }})
        {% endif %}

        {% endfor %}

        {% for var in population_variable_specs[population] %}
        {% if var.scope == 'shared' %}
        vector[{{ var.c_type }}] get_{{ var.name }}_history()
        {% elif var.scope == 'local' %}
        vector[vector[{{ var.c_type }}]] get_{{ var.name }}_history()
        {% endif %}

        {% endfor %}
        void compute_firing_rate(double window)

    {% endfor %}

    {% for population in populations %}
    Population{{ population.id }} population{{ population.id }}
    {% endfor %}

    {% for connection in connections %}
    cdef struct Connection{{ connection.id }}:
        int get_size()
        int nb_synapses(int)
        void set_size(int)

        vector[int] get_post_rank()
        vector[vector[int]] get_pre_rank()
        void set_post_rank(vector[int])
        void set_pre_rank(vector[vector[int]])

        void inverse_connectivity_matrix()

        vector[vector[double]] get_w()
        vector[double] get_dendrite_w(int)
        double get_synapse_w(int, int)
        void set_w(vector[vector[double]])
        void set_dendrite_w(int, vector[double])
        void set_synapse_w(int, int, double)

        {% for var in connection_variable_specs[connection] %}
        {% if var.name != 'w' %}
        {% if var.scope == 'local' %}
        vector[vector[{{ var.c_type }}]] get_{{ var.name }}()
        vector[{{ var.c_type }}] get_dendrite_{{ var.name }}(int)
        {{ var.c_type }} get_synapse_{{ var.name }}(int, int)
        void set_{{ var.name }}(vector[vector[{{ var.c_type }}]])
        void set_dendrite_{{ var.name }}(int, vector[{{ var.c_type }}])
        void set_synapse_{{ var.name }}(int, int, {{ var.c_type }})
        {% else %}
        {{ var.c_type }} get_{{ var.name }}()
        void set_{{ var.name }}({{ var.c_type }})
        {% endif %}
        {% endif %}
        {% endfor %}
    {% endfor %}

    {% for connection in connections %}
    Connection{{ connection.id }} connection{{ connection.id }}
    {% endfor %}

{% for population in populations %}
cdef class Population{{ population.id }}Wrapper:
    def __cinit__(self, size):
        population{{ population.id }}.set_size(size)

    property size:
        def __get__(self):
            return population{{ population.id }}.get_size()

    {% for var in population_variable_specs[population] %}
    {% if var.scope == 'shared' %}
    cpdef {{ var.c_type }} get_{{ var.name }}(self):
        return population{{ population.id }}.get_{{ var.name }}()

    cpdef set_{{ var.name }}(self, {{ var.c_type }} value):
        population{{ population.id }}.set_{{ var.name }}(value)
    {% elif var.scope == 'local' %}
    cpdef np.ndarray get_{{ var.name }}(self):
        return np.array(population{{ population.id }}.get_{{ var.name }}())

    cpdef set_{{ var.name }}(self, np.ndarray value):
        population{{ population.id }}.set_{{ var.name }}( value )

    cpdef {{ var.c_type }} get_single_{{ var.name }}(self, int rank):
        return population{{ population.id }}.get_single_{{ var.name }}(rank)

    cpdef set_single_{{ var.name }}(self, int rank, value):
        population{{ population.id }}.set_single_{{ var.name }}(rank, value)
    {% endif %}

    {% endfor %}

    {% for var in population_variable_specs[population] %}
    cpdef np.ndarray get_{{ var.name }}_history(self):
        return np.array(population{{ population.id }}.get_{{ var.name }}_history())

    {% endfor %}

    cpdef compute_firing_rate(self, double window):
        population{{ population.id }}.compute_firing_rate(window)

{% endfor %}

{% for connection in connections %}
cdef class Connection{{ connection.id }}Wrapper:

    def nb_synapses(self, rank):
        return connection{{ connection.id }}.nb_synapses(rank)

    def get_w(self):
        return connection{{ connection.id }}.get_w()

    def set_w(self, value):
        connection{{ connection.id }}.set_w(value)

    def get_dendrite_w(self, int rank):
        return connection{{ connection.id }}.get_dendrite_w(rank)

    def set_dendrite_w(self, int rank, vector[double] value):
        connection{{ connection.id }}.set_dendrite_w(rank, value)

    def get_synapse_w(self, int rank_post, int rank_pre):
        return connection{{ connection.id }}.get_synapse_w(rank_post, rank_pre)

    def set_synapse_w(self, int rank_post, int rank_pre, double value):
        connection{{ connection.id }}.set_synapse_w(rank_post, rank_pre, value)

    {% for var in connection_variable_specs[connection] %}
    {% if var.name != 'w' %}
    def get_{{ var.name }}(self):
        return connection{{ connection.id }}.get_{{ var.name }}()

    def set_{{ var.name }}(self, value):
        connection{{ connection.id }}.set_{{ var.name }}(value)

    {% if var.scope == 'local' %}
    def get_dendrite_{{ var.name }}(self, int rank):
        return connection{{ connection.id }}.get_dendrite_{{ var.name }}(rank)

    def set_dendrite_{{ var.name }}(self, int rank, vector[{{ var.c_type }}] value):
        connection{{ connection.id }}.set_dendrite_{{ var.name }}(rank, value)

    def get_synapse_{{ var.name }}(self, int rank_post, int rank_pre):
        return connection{{ connection.id }}.get_synapse_{{ var.name }}(rank_post, rank_pre)

    def set_synapse_{{ var.name }}(self, int rank_post, int rank_pre, {{ var.c_type }} value):
        connection{{ connection.id }}.set_synapse_{{ var.name }}(rank_post, rank_pre, value)
    {% endif %}

    {% endif %}
    {% endfor %}

{% endfor %}
