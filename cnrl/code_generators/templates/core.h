#include <vector>
#include <queue>

{% for pop in pops %}
#include "{{ pop.name }}.hpp"
{% endfor %}

{% for proj in projs %}
#include "{{ proj.name }}.hpp"
{% endfor %}

extern double dt;
extern long int t;

long int get_time() ;
void set_time(long int _t) ;

double get_dt() ;
void set_dt(double _dt);

{% for pop in pops %}
extern {{ pop._class_name }} {{ pop.name }};
{% endfor %}

{% for proj in projs %}
extern {{ proj._class_name }} {{ proj.name }};
{% endfor %}

void initialize(double _dt) ;

void run(int steps);
