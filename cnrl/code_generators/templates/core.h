#include <vector>
#include <queue>

{% for population in populations %}
#include "Population{{ population.id }}.hpp"
{% endfor %}

{% for connection in connections %}
#include "Connection{{ connection.id }}.hpp"
{% endfor %}

extern double dt;
extern long int t;

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
