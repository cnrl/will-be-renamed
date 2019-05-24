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

        {% for var_name, var in population.neuron.parameters.vars.items() %}
        {% if var.scope == 'population' %}
        double  get_{{ var_name }}()
        void set_{{ var_name }}(double)
        {% elif var.scope == 'self' %}
        vector[double] get_{{ var_name }}()
        double get_single_{{ var_name }}(int)
        void set_{{ var_name }}(vector[double])
        void set_single_{{ var_name }}(int, double)
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

        {% for var_name, var in connection.synapse.parameters.vars.items() %}
        {% if var_name != 'w' %}
        vector[vector[double]] get_{{ var_name }}()
        vector[double] get_dendrite_{{ var_name }}(int)
        double get_synapse_{{ var_name }}(int, int)
        void set_{{ var_name }}(vector[vector[double]])
        void set_dendrite_{{ var_name }}(int, vector[double])
        void set_synapse_{{ var_name }}(int, int, double)
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

    {% for var_name, var in population.neuron.parameters.vars.items() %}
    {% if var.scope == 'population' %}
    cpdef double get_{{ var_name }}(self):
        return population{{ population.id }}.get_{{ var_name }}()

    cpdef set_{{ var_name }}(self, double value):
        population{{ population.id }}.set_{{ var_name }}(value)
    {% elif var.scope == 'self' %}
    cpdef np.ndarray get_{{ var_name }}(self):
        return np.array(population{{ population.id }}.get_{{ var_name }}())

    cpdef set_{{ var_name }}(self, np.ndarray value):
        population{{ population.id }}.set_{{ var_name }}( value )

    cpdef double get_single_{{ var_name }}(self, int rank):
        return population{{ population.id }}.get_single_{{ var_name }}(rank)

    cpdef set_single_{{ var_name }}(self, int rank, value):
        population{{ population.id }}.set_single_{{ var_name }}(rank, value)
    {% endif %}

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

    {% for var_name, var in connection.synapse.parameters.vars.items() %}
    {% if var_name != 'w' %}
    def get_{{ var_name }}(self):
        return connection{{ connection.id }}.get_{{ var_name }}()

    def set_{{ var_name }}(self, value):
        connection{{ connection.id }}.set_{{ var_name }}(value)

    def get_dendrite_{{ var_name }}(self, int rank):
        return connection{{ connection.id }}.get_dendrite_{{ var_name }}(rank)

    def set_dendrite_{{ var_name }}(self, int rank, vector[double] value):
        connection{{ connection.id }}.set_dendrite_{{ var_name }}(rank, value)

    def get_synapse_{{ var_name }}(self, int rank_post, int rank_pre):
        return connection{{ connection.id }}.get_synapse_{{ var_name }}(rank_post, rank_pre)

    def set_synapse_{{ var_name }}(self, int rank_post, int rank_pre, double value):
        connection{{ connection.id }}.set_synapse_{{ var_name }}(rank_post, rank_pre, value)

    {% endif %}
    {% endfor %}

{% endfor %}