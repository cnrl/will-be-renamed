#include "core.h"

double dt;
long int t;

{% for population in populations %}
Population{{ population._id }} population{{ population._id }};
{% endfor %}

{% for connection in connections %}
Connection{{ connection._id }} connection{{ connection._id }};
{% endfor %}

void single_step();

void run(int steps) {
    for(int i = 0; i < steps; i++) {
        single_step();
    }
}

void initialize(double _dt) {
    dt = _dt;
    t = (long int)(0);

    {% for population in populations %}
    population{{ population._id }}.init_population();
    {% endfor %}

    {% for connection in connections %}
    connection{{ connection._id }}.init_connection();
    {% endfor %}
}

void single_step()
{
    {% for connection in connections %}
    connection{{ connection._id }}.compute_psp();
    {% endfor %}

    {% for population in populations %}
    population{{ population._id }}.update();
    {% endfor %}

    {% for connection in connections %}
    connection{{ connection._id }}.update_synapse();
    {% endfor %}

    t++;
}

long int get_time() { return t; }
void set_time(long int _t) { t = _t; }
double get_dt() { return dt; }
void set_dt(double _dt) { dt = _dt; }