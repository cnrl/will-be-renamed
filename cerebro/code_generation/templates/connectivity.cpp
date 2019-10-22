#pragma once

#include "connectivity.h"

std::vector< std::vector<int> > connect_all_to_all(int pre_size, int post_size){
    std::vector< std::vector<int> > connectivity;

    for (int post_rank_idx = 0;post_rank_idx < post_size; post_rank_idx++) {
        connectivity.push_back(std::vector<int>());
        for (int pre_rank_idx = 0;pre_rank_idx < pre_size; pre_rank_idx++)
            connectivity.back().push_back(pre_rank_idx);
        }
    return connectivity;
}