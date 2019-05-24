#include "core.h"

double dt;
long int t;

{% for population in populations %}
Population{{ population.id }} population{{ population.id }};
{% endfor %}

{% for connection in connections %}
Connection{{ connection.id }} connection{{ connection.id }};
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
    population{{ population.id }}.init_population();
    {% endfor %}

    {% for connection in connections %}
    connection{{ connection.id }}.init_connection();
    {% endfor %}
}

void single_step()
{
    {% for connection in connections %}
    connection{{ connection.id }}.compute_psp();
    {% endfor %}

    {% for population in populations %}
    population{{ population.id }}.update();
    {% endfor %}

    {% for connection in connections %}
    connection{{ connection.id }}.update_synapse();
    {% endfor %}

    t++;
}

long int get_time() { return t; }
void set_time(long int _t) { t = _t; }
double get_dt() { return dt; }
void set_dt(double _dt) { dt = _dt; }