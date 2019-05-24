#pragma once

#include "core.h"

extern double dt;
extern long int t;

struct Population{{ population.id }} {

    int size;

    int get_size() { return size; }
    void set_size(int _size) { size  = _size; }

    std::vector<long int> last_spike;
    std::vector<int> spiked;

    {% for var_name, var in population.neuron.parameters.vars.items() %}
    {% if var.scope == 'population'%}
    double {{ var_name }};
    {% elif var.scope == 'self'%}
    std::vector< double > {{ var_name }};
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

    {% for var_name, var in population.neuron.parameters.vars.items() %}
    {% if var.scope == 'population'%}
    double get_{{ var_name }}() { return {{ var_name }}; }
    void set_{{ var_name }}(double _{{ var_name }}) { {{ var_name }} = _{{ var_name }}; }

    {% elif var.scope == 'self'%}
    std::vector< double > get_{{ var_name }}() { return {{ var_name }}; }
    double get_single_{{ var_name }}(int rank) { return {{ var_name }}[rank]; }
    void set_{{ var_name }}(std::vector< double > _{{ var_name }}) { {{ var_name }} = _{{ var_name }}; }
    void set_single_{{ var_name }}(int rank, double _{{ var_name }}) { {{ var_name }}[rank] = _{{ var_name }}; }

    {% endif %}
    {% endfor %}

    void init_population() {

        {% for var_name, var in population.neuron.parameters.vars.items() %}
        {% if var.scope == 'population'%}
        {{ var_name }} = 0.0;
        {% elif var.scope == 'self'%}
        {{ var_name }} = std::vector<double>(size, 0.0);
        {% endif %}
        {% endfor %}

        v = std::vector<double>(size, 0.0);
        r = std::vector<double>(size, 0.0);
        g_exc = std::vector<double>(size, 0.0);

        spiked = std::vector<int>(0, 0);
        last_spike = std::vector<long int>(size, -10000L);

        _spike_history = std::vector< std::queue<long int> >(size, std::queue<long int>());
        _mean_fr_window = 0;
        _mean_fr_rate = 1.0;
    }

    void update() {
        spiked.clear();

        for(int i = 0; i < size; i++) {
            {% for var, equation in update_equations %}
            double _{{ var }} = {{ equation }};
            {% endfor %}

            {% for var, _ in update_equations %}
            {{ var }}[i] += dt * _{{ var }};
            {% endfor %}


            g_exc[i] = 0.0;

            if(v[i] > -10) {
                v[i] = 0;

                spiked.push_back(i);
                last_spike[i] = t;

                if(_mean_fr_window > 0)
                    _spike_history[i].push(t);
            }

            if(_mean_fr_window > 0) {
                while((_spike_history[i].size() != 0) && (_spike_history[i].front() <= t - _mean_fr_window)) {
                    _spike_history[i].pop();
                }

                r[i] = _mean_fr_rate * float(_spike_history[i].size());
            }
        }
    }
};