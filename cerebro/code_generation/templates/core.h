#pragma once

#include <vector>
#include <queue>
#include <map>
#include <random>
#include <math.h>
#include <set>


{% for population in populations %}
#include "population{{ population.id }}.hpp"
{% endfor %}

{% for connection in connections %}
#include "connection{{ connection.id }}.hpp"
{% endfor %}

extern std::default_random_engine random_generator;

extern double dt;
extern long int t;

{% for var in network_variables %}
extern {{ var.c_type }} {{ var.name }};
{% endfor %}

long int get_time() ;
void set_time(long int _t) ;

double get_dt() ;
void set_dt(double _dt);

{% for population in populations %}
extern Population{{ population.id }} population{{ population.id }};
{% endfor %}

{% for connection in connections %}
extern Connection{{ connection.id }} connection{{ connection.id }};
{% endfor %}

void initialize(double _dt) ;

void run(int steps);
