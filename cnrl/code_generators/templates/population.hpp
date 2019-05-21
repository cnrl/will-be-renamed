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

    {% for var in population.neuron.parameters.vars %}
    {% if var.scope == 'population'%}
    double {{ var.name }};
    {% elif var.scope == 'self'%}
    std::vector< double > {{ var.name }};
    {% endif %}
    {% endfor %}

    std::vector< double > v;
    std::vector< double > r;
    std::vector< double > g_exc;

    std::vector< std::queue<long int> > _spike_history;
    long int _mean_fr_window;
    double _mean_fr_rate;
    void compute_firing_rate(double window){
        if(window>0.0){
            _mean_fr_window = int(window/dt);
            _mean_fr_rate = 1000./window;
        }
    };

    {% for var in population.neuron.parameters.vars %}
    {% if var.scope == 'population'%}
    double get_{{ var.name }}() { return {{ var.name }}; }
    void set_{{ var.name }}(double _{{ var.name }}) { {{ var.name }} = _{{ var.name }}; }

    {% elif var.scope == 'self'%}
    std::vector< double > get_{{ var.name }}() { return {{ var.name }}; }
    double get_single_{{ var.name }}(int rank) { return {{ var.name }}[rank]; }
    void set_{{ var.name }}(std::vector< double > _{{ var.name }}) { {{ var.name }} = _{{ var.name }}; }
    void set_single_{{ var.name }}(int rank, double _{{ var.name }}) { {{ var.name }}[rank] = _{{ var.name }}; }

    {% endif %}
    {% endfor %}

    std::vector< double > get_v() { return v; }
    double get_single_v(int rank) { return v[rank]; }
    void set_v(std::vector< double > _v) { v = _v; }
    void set_single_v(int rank, double _v) { v[rank] = _v; }

    std::vector< double > get_r() { return r; }
    double get_single_r(int rank) { return r[rank]; }
    void set_r(std::vector< double > _r) { r = _r; }
    void set_single_r(int rank, double _r) { r[rank] = _r; }

    std::vector< double > get_g_exc() { return g_exc; }
    double get_single_g_exc(int rank) { return g_exc[rank]; }
    void set_g_exc(std::vector< double > _g_exec) { g_exc = _g_exec; }
    void set_single_g_exc(int rank, double _g_exec) { g_exc[rank] = _g_exec; }

    void init_population() {

        {% for var in population.neuron.parameters.vars %}
        {% if var.scope == 'population'%}
        {{ var.name }} = 0.0;
        {% elif var.scope == 'self'%}
        {{ var.name }} = std::vector<double>(size, 0.0);
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
            double _v = ((g_exc[i] * v[i]) - v[i]) / 10;

            v[i] += dt * _v ;

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