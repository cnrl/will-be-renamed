#include "pop0.hpp"
#include "pop1.hpp"

extern PopStruct0 pop0;
extern PopStruct1 pop1;

struct ProjStruct0{
    int size;

    std::vector<int> post_rank;
    std::vector< std::vector< int > > pre_rank;
    std::vector< std::vector< double > > w;
    std::map< int, std::vector< std::pair<int, int> > > inv_pre_rank ;
    std::vector< int > inv_post_rank ;

    std::vector< std::vector<double > > tau;
    std::vector< std::vector<double > > alpha;

    void init_projection() {
        inverse_connectivity_matrix();

        tau = std::vector< std::vector<double> >(post_rank.size(), std::vector<double>());
        alpha = std::vector< std::vector<double> >(post_rank.size(), std::vector<double>());
    }

    void inverse_connectivity_matrix() {
        inv_pre_rank =  std::map<int, std::vector< std::pair<int, int> > > ();
        for(int i = 0; i < pre_rank.size(); i++) {
            for(int j = 0; j <pre_rank[i].size(); j++) {
                inv_pre_rank[pre_rank[i][j]].push_back(std::pair<int, int>(i, j));
            }
        }

        inv_post_rank = std::vector<int> (pop1.size, -1);
        for(int i = 0; i < post_rank.size(); i++) {
            inv_post_rank[post_rank[i]] = i;
        }
    }

    void compute_psp() {
        int nb_post;
        double sum;

        for(int _idx_j = 0; _idx_j < pop0.spiked.size(); _idx_j++) {

            int rk_j = pop0.spiked[_idx_j];

            auto inv_post_ptr = inv_pre_rank.find(rk_j);
            if (inv_post_ptr == inv_pre_rank.end())
                continue;

            std::vector< std::pair<int, int> >& inv_post = inv_post_ptr->second;

            int nb_post = inv_post.size();
            for(int _idx_i = 0; _idx_i < nb_post; _idx_i++){
                int i = inv_post[_idx_i].first;
                int j = inv_post[_idx_i].second;

                pop1.g_exc[post_rank[i]] += w[i][j];
            }
        }
    }

    void update_synapse() {
        for(int i = 0; i < post_rank.size(); i++) {
            int rk_post = post_rank[i];

            for(int j = 0; j < pre_rank[i].size(); j++) {
                int rk_pre = pre_rank[i][j];

                double _w = -pop1.r[rk_post] * (pop1.r[rk_post] * w[i][j] - pop0.r[rk_pre]) / 5000;

                w[i][j] += _w ;
            }
        }
    }

    int get_size() { return size; }
    void set_size(int _size) { size = _size; }

    std::vector<int> get_post_rank() { return post_rank; }
    void set_post_rank(std::vector<int> _post_rank) { post_rank = _post_rank; }
    std::vector< std::vector<int> > get_pre_rank() { return pre_rank; }
    void set_pre_rank(std::vector< std::vector<int> > _pre_rank) { pre_rank = _pre_rank; }
    int nb_synapses(int n) { return pre_rank[n].size(); }

    std::vector<std::vector< double > > get_w() {
        std::vector< std::vector< double > > w_new(w.size(), std::vector<double>());
        for(int i = 0; i < w.size(); i++) {
            w_new[i] = std::vector<double>(w[i].begin(), w[i].end());
        }
        return w_new;
    }
    std::vector< double > get_dendrite_w(int rank) { return std::vector<double>(w[rank].begin(), w[rank].end()); }
    double get_synapse_w(int rank_post, int rank_pre) { return w[rank_post][rank_pre]; }
    void set_w(std::vector<std::vector< double > > _w) {
        w = std::vector< std::vector<double> >(_w.size(), std::vector<double>());
        for(int i = 0; i < _w.size(); i++) {
            w[i] = std::vector<double>(_w[i].begin(), _w[i].end());
        }
    }
    void set_dendrite_w(int rank, std::vector< double > _w) { w[rank] = std::vector<double>(_w.begin(), _w.end()); }
    void set_synapse_w(int rank_post, int rank_pre, double _w) { w[rank_post][rank_pre] = _w; }


    // Local parameter tau
    std::vector<std::vector< double > > get_tau() { return tau; }
    std::vector<double> get_dendrite_tau(int rk) { return tau[rk]; }
    double get_synapse_tau(int rk_post, int rk_pre) { return tau[rk_post][rk_pre]; }
    void set_tau(std::vector<std::vector< double > >value) { tau = value; }
    void set_dendrite_tau(int rk, std::vector<double> value) { tau[rk] = value; }
    void set_synapse_tau(int rk_post, int rk_pre, double value) { tau[rk_post][rk_pre] = value; }

    // Local parameter alpha
    std::vector<std::vector< double > > get_alpha() { return alpha; }
    std::vector<double> get_dendrite_alpha(int rk) { return alpha[rk]; }
    double get_synapse_alpha(int rk_post, int rk_pre) { return alpha[rk_post][rk_pre]; }
    void set_alpha(std::vector<std::vector< double > >value) { alpha = value; }
    void set_dendrite_alpha(int rk, std::vector<double> value) { alpha[rk] = value; }
    void set_synapse_alpha(int rk_post, int rk_pre, double value) { alpha[rk_post][rk_pre] = value; }
};
