#include "core.h"

extern std::default_random_engine random_generator;
bool all_to_all_func(int , int);
bool probability_func(int, int, float);
bool gaussian_func(int, int, float);
bool dog_func(int, int, float, float);
std::vector< std::vector<int> > connect_all_to_all(int, int);
std::vector< std::vector<int> > connect_with_probability(int , int, float);
std::vector< std::vector<int> > connect_gaussian(int, int, float);
std::vector< std::vector<int> > connect_dog(int, int, float, float);

template<class F, typename... Args>
std::vector< std::vector<int> > connect_by_func(F, int , int , Args...);