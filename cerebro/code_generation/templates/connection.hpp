#pragma once

#include "population{{ connection.pre.id }}.hpp"
#include "population{{ connection.post.id }}.hpp"

extern Population{{ connection.pre.id }} population{{ connection.pre.id }} ;
extern Population{{ connection.post.id }} population{{ connection.post.id }} ;
{% for var in network_variables %}
extern {{ var.c_type }} {{ var.name }};
{% endfor %}

struct Connection{{ connection.id }} {
    std::vector<int> post_rank;
    std::vector< std::vector< int > > pre_rank;
    std::map< int, std::vector< std::pair<int, int> > > inv_pre_rank ;
    std::vector< int > inv_post_rank ;
    std::vector< std::vector<double> > w;

    {% for var in variables %}
    {% if var.scope == 'local' %}
    std::vector< std::vector< {{ var.c_type}} > > {{ var.name }};
    {% else %}
    {{ var.c_type }} {{ var.name }};
    {% endif %}
    {% endfor %}

    void init_connection() {
        for (int rank = 0;rank < population{{ connection.post.id }}.size; rank++)
            post_rank.push_back(rank);

        for (int post_rank_idx = 0;post_rank_idx < population{{ connection.post.id }}.size; post_rank_idx++) {
            pre_rank.push_back(std::vector<int>());

            for (int pre_rank_idx = 0;pre_rank_idx < population{{ connection.pre.id }}.size; pre_rank_idx++)
                pre_rank.back().push_back(pre_rank_idx);
        }

        inverse_connectivity_matrix();

        {% for var in variables %}
            {% if var.scope == 'local' %}
        {{ var.name }} = std::vector< std::vector<{{ var.c_type }}> >(post_rank.size(), std::vector<{{var.c_type}}>());
            {% else %}
        {{var.name}} = {{ var.init }};
            {% endif %}
        {% endfor %}

        {% for var in variables %}
            {% if var.scope == 'local' %}
        for(int post_idx = 0;post_idx < post_rank.size(); post_idx++)
            {{ var.name }}[post_idx] = std::vector<{{var.c_type}}>(pre_rank[post_idx].size(), {{ var.init }});
            {% endif %}
        {% endfor %}

        w = std::vector< std::vector<double> >(post_rank.size(), std::vector<double>());
        for(int post_idx = 0; post_idx < post_rank.size(); post_idx ++)
            w[post_idx] = std::vector<double>(pre_rank[post_idx].size(), 1.0);
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
            int rank_post = post_rank[i];

            for(int j = 0; j < pre_rank[i].size(); j++) {
                int rank_pre = pre_rank[i][j];

                {% for equation in update_equations %}
                double _{{ equation.variable.name }} = {{ equation.expression }};
                {% endfor %}

                {% for equation in update_equations %}
                {{ equation.variable.name }}[i][j] += _{{ equation.variable.name }};
                {% endfor %}
            }
        }
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

    {% for var in variables %}
    {% if var.scope == 'local' %}
    std::vector<std::vector< {{var.c_type}} > > get_{{ var.name }}() {
        return {{ var.name }};
    }

    std::vector<{{var.c_type}}> get_dendrite_{{ var.name }}(int rank) {
        return {{ var.name }}[rank];
    }

    double get_synapse_{{ var.name }}(int rank_post, int rank_pre) {
        return {{ var.name }}[rank_post][rank_pre];
    }

    void set_{{ var.name }}(std::vector<std::vector< {{var.c_type}} > >value) {
        {{ var.name }} = value;
    }

    void set_dendrite_{{ var.name }}(int rank, std::vector<{{var.c_type}}> value) {
        {{ var.name }}[rank] = value;
    }

    void set_synapse_{{ var.name }}(int rank_post, int rank_pre, {{var.c_type}} value) {
        {{ var.name }}[rank_post][rank_pre] = value;
    }
    {% else %}

     {{var.c_type}} get_{{ var.name }}() {
        return {{ var.name }};
     }

    void set_{{ var.name }}({{var.c_type}} value) {
        {{ var.name }} = value;
    }
    {% endif %}
    {% endfor %}
};
