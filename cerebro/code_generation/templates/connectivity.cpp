#include "connectivity.h"

bool all_to_all_func(int pre_rank_idx, int post_rank_idx){
    return true;
}

bool probability_func(int pre_rank_idx, int post_rank_idx, float prob){
    std::uniform_real_distribution<> dis(0.0, 1.0);
    return dis(random_generator) < prob;
}

bool gaussian_func(int pre_rank_idx, int post_rank_idx, float sigma){
    float gauss = exp(-0.5 *(pow(pre_rank_idx - post_rank_idx, 2.0) / pow(sigma, 2.0)));
    std::uniform_real_distribution<> dis(0.0, 1.0);
    return dis(random_generator) < gauss;
}

bool dog_func(int pre_rank_idx, int post_rank_idx, float sigma1, float sigma2){
    float gauss1 = exp(-0.5 *(pow(pre_rank_idx - post_rank_idx, 2.0) / pow(sigma1, 2.0)));
    float gauss2 = exp(-0.5 *(pow(pre_rank_idx - post_rank_idx, 2.0) / pow(sigma2, 2.0)));
    std::uniform_real_distribution<> dis(0.0, 1.0);
    return dis(random_generator) < gauss1 - gauss2; // FIXME
}

std::vector< std::vector<int> > connect_all_to_all(int pre_size, int post_size){
    return connect_by_func(all_to_all_func, pre_size, post_size);
}

std::vector< std::vector<int> > connect_with_probability(int pre_size, int post_size, float prob){
    return connect_by_func(probability_func, pre_size, post_size, prob);
}

std::vector< std::vector<int> > connect_gaussian(int pre_size, int post_size, float sigma){
    return connect_by_func(gaussian_func, pre_size, post_size, sigma);
}

std::vector< std::vector<int> > connect_dog(int pre_size, int post_size, float sigma1, float sigma2){
    return connect_by_func(dog_func, pre_size, post_size, sigma1, sigma2);
}

template<class F, typename... Args>
std::vector< std::vector<int> > connect_by_func(F func, int pre_size, int post_size, Args... args){
    std::vector< std::vector<int> > connectivity;

    for (int post_rank_idx = 0;post_rank_idx < post_size; post_rank_idx++) {
        connectivity.push_back(std::vector<int>());
        for (int pre_rank_idx = 0;pre_rank_idx < pre_size; pre_rank_idx++)
            if (func(pre_rank_idx, post_rank_idx, args...))
                connectivity.back().push_back(pre_rank_idx);
        }
    return connectivity;
}