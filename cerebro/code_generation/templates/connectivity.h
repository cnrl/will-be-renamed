#include "core.h"

extern std::default_random_engine random_generator;
std::vector< std::vector<int> > connect_all_to_all(int, int, float);
bool all_to_all_func(int , int , float);
bool probability_func(int, int, float);
std::vector< std::vector<int> > connect_with_probability(int , int, float);
bool gaussian_func(int, int, float);
std::vector< std::vector<int> > connect_gaussian(int, int, float);
std::vector< std::vector<int> > connect_by_func(bool (*)(int, int, float), int , int , float);