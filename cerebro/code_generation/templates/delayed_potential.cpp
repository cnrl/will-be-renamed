#include "delayed_potential.h"

DelayedPotentiation::DelayedPotentiation(int post_rank_, float time_to_apply_, float potentiation_)
    :post_rank(post_rank_), time_to_apply(time_to_apply_), potentiation(potentiation_) {}

bool DelayedPotentiation::operator< (const DelayedPotentiation& dp) const {
	return (this->time_to_apply < dp.time_to_apply);
}

void DelayedPotentiation::apply(std::vector<float>& g_exc) const {
    g_exc[post_rank] += potentiation;
}
