#include "core.h"

double dt;
long int t;

{% for pop in pops %}
{{ pop._class_name }} {{ pop.name }};
{% endfor %}

{% for proj in projs %}
{{ proj._class_name }} {{ proj.name }};
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

    {% for pop in pops %}
    {{ pop.name }}.init_population();
    {% endfor %}

    {% for proj in projs %}
    {{ proj.name }}.init_projection();
    {% endfor %}
}

void single_step()
{
    {% for proj in projs %}
    {{ proj.name }}.compute_psp();
    {% endfor %}

    {% for pop in pops %}
    {{ pop.name }}.update();
    {% endfor %}

    {% for proj in projs %}
    {{ proj.name }}.update_synapse();
    {% endfor %}

    t++;
}

long int get_time() { return t; }
void set_time(long int _t) { t = _t; }
double get_dt() { return dt; }
void set_dt(double _dt) { dt = _dt; }