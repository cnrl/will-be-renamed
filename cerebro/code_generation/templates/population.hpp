#pragma once

#include "core.h"
#include "random_functions.h"

extern std::default_random_engine random_generator;

extern double dt;
extern long int t;
{% for var in network_variables %}
extern {{ var.c_type }} {{ var.name }};
{% endfor %}

struct Population{{ population_id }} {

    int size;

    int get_size() { return size; }
    void set_size(int _size) { size  = _size; }

    std::vector<long int> last_spike;
    std::vector<int> spiked;
    std::vector<double> r;

    {% for variable in variables %}
    {% if variable.scope == 'shared' %}
    {{ variable.c_type }} {{ variable.name }};
    {% elif variable.scope == 'local' %}
    std::vector< {{ variable.c_type }} > {{ variable.name }};
    {% endif %}
    {% endfor %}

    {% for variable in variables %}
    {% if variable.scope == 'shared' %}
    std::vector<{{ variable.c_type }}> {{ variable.name }}_history;
    {% elif variable.scope == 'local' %}
    std::vector<std::vector< {{ variable.c_type }} > >{{ variable.name }}_history;
    {% endif %}

    {% endfor %}

    std::vector< std::queue<long int> > _spike_history;
    long int _mean_fr_window;
    double _mean_fr_rate;
    void compute_firing_rate(double window){
        if(window>0.0){
            _mean_fr_window = int(window/dt);
            _mean_fr_rate = 1000./window;
        }
    };

    {% for variable in variables %}
    {% if variable.scope == 'shared'%}
    {{ variable.c_type }} get_{{ variable.name }}() { return {{ variable.name }}; }
    void set_{{ variable.name }}({{ variable.c_type }} _{{ variable.name }}) { {{ variable.name }} = _{{ variable.name }}; }

    {% elif variable.scope == 'local'%}
    std::vector< {{ variable.c_type }} > get_{{ variable.name }}() { return {{ variable.name }}; }
    double get_single_{{ variable.name }}(int rank) { return {{ variable.name }}[rank]; }
    void set_{{ variable.name }}(std::vector< {{ variable.c_type }} > _{{ variable.name }}) { {{ variable.name }} = _{{ variable.name }}; }
    void set_single_{{ variable.name }}(int rank, {{ variable.c_type }} _{{ variable.name }}) { {{ variable.name }}[rank] = _{{ variable.name }}; }

    {% endif %}
    {% endfor %}

  {% for variable in variables %}
    {% if variable.scope == 'shared' %}
    std::vector<{{ variable.c_type }} > get_{{ variable.name }}_history() { return {{ variable.name }}_history; }

    {% elif variable.scope == 'local' %}
    std::vector< std::vector<{{ variable.c_type }}> > get_{{ variable.name }}_history() { return {{ variable.name }}_history; }

    {% endif %}
  {% endfor %}


    void init_population() {

        {% for variable in variables %}
        {% if variable.scope == 'shared' %}
        {{ variable.name }} = {{ variable.init }};
        {% elif variable.scope == 'local'%}
        {{ variable.name }} = std::vector<{{ variable.c_type }} >(size, {{ variable.init }});
        {% endif %}
        {% endfor %}

        spiked = std::vector<int>(0, 0);
        r = std::vector<double> (size, 0);

        last_spike = std::vector<long int>(size, -10000L);

        _spike_history = std::vector< std::queue<long int> >(size, std::queue<long int>());
        _mean_fr_window = 0;
        _mean_fr_rate = 1.0;
    }

    void update() {

        spiked.clear();
        for(int i = 0; i < size; i++) {

            // TODO: ODE
            // TODO: add network variable update capability
            {% for equation in update_equations %}
                {% if equation.equation_type == 'simple' %}
                    {% if equation.variable.scope == 'local' %}
            {{ equation.variable.name }}[i] = {{ equation.expression }};
                    {% else %}
            {{ equation.variable.name }} = {{ equation.expression }};
                {% endif %}
                {% endif %}
            {% endfor %}


            g_exc[i] = 0.0;

            {% if spike_condition %}
            if({{ spike_condition }}) {
                {% for equation in reset_equations %}
                    {% if equation.variable.scope == 'local' %}
                {{ equation.variable.name }}[i] = {{ equation.expression }};
                    {% else %}
                {{ equation.variable.name }} = {{ equation.expression }};
                    {% endif %}
                {% endfor %}

                spiked.push_back(i);
                last_spike[i] = t;

                if(_mean_fr_window > 0)
                    _spike_history[i].push(t);
            }
            {% endif %}

            if(_mean_fr_window > 0) {
                while((_spike_history[i].size() != 0) && (_spike_history[i].front() <= t - _mean_fr_window)) {
                    _spike_history[i].pop();
                }

                r[i] = _mean_fr_rate * float(_spike_history[i].size());
            }

        }
        
        {% for variable in variables %}
        {{ variable.name }}_history.push_back({{ variable.name }});  // TODO: to be considered

        {% endfor %}
    }
};
