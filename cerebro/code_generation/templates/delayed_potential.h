#include<vector>

class DelayedPotentiation {
    private:
    int post_rank;
    float potentiation;

    public:
    float time_to_apply;

    DelayedPotentiation(int, float, float);
    bool operator< (const DelayedPotentiation&) const ;
	void apply(std::vector<float>&) const;
};
