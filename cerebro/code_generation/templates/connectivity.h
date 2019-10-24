#include <vector>
#include <random>
#include "core.h"

extern std::default_random_engine random_generator;
std::vector< std::vector<int> > connect_all_to_all(int, int);
bool all_to_all_func(int , int );
bool connect_with_probability(int , int, float);
std::vector< std::vector<int> > connect_by_func(bool (*)(int, int), int , int );