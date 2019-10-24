#pragma once

#include "connectivity.h"

bool all_to_all_func(int pre_rank_idx, int post_rank_idx){
    return true;
}

std::vector< std::vector<int> > connect_all_to_all(int pre_size, int post_size){
    return connect_by_func(all_to_all_func, pre_size, post_size);
}

bool connect_with_probability(int pre_rank_idx, int post_rank_idx, float prob){
    std::uniform_real_distribution<> dis(0.0, 1.0);
    return dis(random_generator) < prob;
}

std::vector< std::vector<int> > connect_by_func(bool (*func)(int, int), int pre_size, int post_size){
    std::vector< std::vector<int> > connectivity;

    for (int post_rank_idx = 0;post_rank_idx < post_size; post_rank_idx++) {
        connectivity.push_back(std::vector<int>());
        for (int pre_rank_idx = 0;pre_rank_idx < pre_size; pre_rank_idx++)
            if (func(pre_rank_idx, post_rank_idx))
                connectivity.back().push_back(pre_rank_idx);
        }
    return connectivity;
}