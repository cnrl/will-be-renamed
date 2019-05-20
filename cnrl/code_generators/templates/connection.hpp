#include "Population{{ connection.pre.id }}.hpp"
#include "Population{{ connection.post.id }}.hpp"

extern Population{{ connection.pre.id }} population{{ connection.pre.id }} ;
extern Population{{ connection.post.id }} population{{ connection.post.id }} ;

struct Connection{{ connection.id }} {
    std::vector<int> post_rank;
    std::vector< std::vector< int > > pre_rank;
    std::vector< std::vector< double > > w;
    std::map< int, std::vector< std::pair<int, int> > > inv_pre_rank ;
    std::vector< int > inv_post_rank ;

    {% for var in connection.synapse.parameters.vars %}
    std::vector< std::vector<double > > {{ var.name }};
    {% endfor %}

    void init_projection() {
        inverse_connectivity_matrix();

        {% for var in connection.synapse.parameters.vars %}
        {{ var.name }} = std::vector< std::vector<double> >(post_rank.size(), std::vector<double>());
        {% endfor %}
    }

    void inverse_connectivity_matrix() {
        inv_pre_rank =  std::map<int, std::vector< std::pair<int, int> > > ();
        for(int i = 0; i < pre_rank.size(); i++) {
            for(int j = 0; j <pre_rank[i].size(); j++) {
                inv_pre_rank[pre_rank[i][j]].push_back(std::pair<int, int>(i, j));
            }
        }

        inv_post_rank = std::vector<int> (population{{ connection.post.id }}.size, -1);
        for(int i = 0; i < post_rank.size(); i++) {
            inv_post_rank[post_rank[i]] = i;
        }
    }

    void compute_psp() {
        for(int pre_idx = 0; pre_idx < population{{ connection.pre.id }}.spiked.size(); pre_idx++) {

            int spiked_idx = population{{ connection.pre.id }}.spiked[pre_idx];

            auto inv_post_ptr = inv_pre_rank.find(spiked_idx);
            if (inv_post_ptr == inv_pre_rank.end())
                continue;

            std::vector< std::pair<int, int> > &inv_post = inv_post_ptr->second;

            for(int post_idx = 0; post_idx < inv_post.size(); post_idx++) {
                int i = inv_post[post_idx].first;
                int j = inv_post[post_idx].second;

                population{{ connection.post.id }}.g_exc[post_rank[i]] += w[i][j];
            }
        }
    }

    void update_synapse() {
        for(int i = 0; i < post_rank.size(); i++) {
            int rk_post = post_rank[i];

            for(int j = 0; j < pre_rank[i].size(); j++) {
                int rk_pre = pre_rank[i][j];

                double _w = -population{{ connection.post.id }}.r[rk_post] * (population{{ connection.post.id }}.r[rk_post] * w[i][j] - population{{ connection.pre.id }}.r[rk_pre]) / 5000;

                w[i][j] += _w ;
            }
        }
    }

    int get_size() {
        return size;
    }
    void set_size(int _size) {
        size = _size;
    }

    std::vector<int> get_post_rank() {
        return post_rank;
    }

    void set_post_rank(std::vector<int> _post_rank) {
        post_rank = _post_rank;
    }

    std::vector< std::vector<int> > get_pre_rank() {
        return pre_rank;
    }

    void set_pre_rank(std::vector< std::vector<int> > _pre_rank) {
        pre_rank = _pre_rank;
    }

    int nb_synapses(int n) {
        return pre_rank[n].size();
    }

    std::vector<std::vector< double > > get_w() {
        std::vector< std::vector< double > > w_new(w.size(), std::vector<double>());

        for(int i = 0; i < w.size(); i++)
            w_new[i] = std::vector<double>(w[i].begin(), w[i].end());

        return w_new;
    }

    std::vector< double > get_dendrite_w(int rank) {
        return std::vector<double>(w[rank].begin(), w[rank].end());
    }

    double get_synapse_w(int rank_post, int rank_pre) {
        return w[rank_post][rank_pre];
    }

    void set_w(std::vector<std::vector< double > > _w) {
        w = std::vector< std::vector<double> >(_w.size(), std::vector<double>());

        for(int i = 0; i < _w.size(); i++)
            w[i] = std::vector<double>(_w[i].begin(), _w[i].end());
    }

    void set_dendrite_w(int rank, std::vector< double > _w) {
        w[rank] = std::vector<double>(_w.begin(), _w.end());
    }

    void set_synapse_w(int rank_post, int rank_pre, double _w) {
        w[rank_post][rank_pre] = _w;
    }

    {% for var in connection.synapse.parameters.vars %}
    std::vector<std::vector< double > > get_{{ var.name }}() {
        return {{ var.name }};
    }

    std::vector<double> get_dendrite_{{ var.name }}(int rank) {
        return {{ var.name }}[rank];
    }

    double get_synapse_{{ var.name }}(int rank_post, int rank_pre) {
        return {{ var.name }}[rank_post][rank_pre];
    }

    void set_{{ var.name }}(std::vector<std::vector< double > >value) {
        {{ var.name }} = value;
    }

    void set_dendrite_{{ var.name }}(int rank, std::vector<double> value) {
        {{ var.name }}[rank] = value;
    }

    void set_synapse_{{ var.name }}(int rank_post, int rank_pre, double value) {
        {{ var.name }}[rank_post][rank_pre] = value;
    }

    {% endfor %}
}
