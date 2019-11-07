#include "random_functions.h"

double random_uniform(double a, double b) {
    std::uniform_real_distribution<> dis(a, b);

    return dis(random_generator);
}
double random_normal(double m, double s) {
    std::normal_distribution<> dis{m, s};

    return dis(random_generator);
}