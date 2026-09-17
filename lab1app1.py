import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pyvis.network import Network

nodeColors = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "purple",
    4: "gold",
    5: "red"
}


@st.cache_data
def data_load():
    data = pd.read_csv("data/game-of-thrones-battles.csv")
    battles_df = data.loc[:, ['name', 'attacker_king', 'defender_king', 'attacker_size', 'defender_size']]
    return battles_df.dropna()


def buildGraph(battles_df_cleaned):
    net5kings = Network(
                bgcolor="#242020",
                font_color="white",
                height="1000px",
                width="100%",
                directed=True,
                cdn_resources="remote")

    nodes = list(set([*battles_df_cleaned['attacker_king'],
                      *battles_df_cleaned['defender_king']
                     ]))
    net5kings.add_nodes(nodes, title=[str(node) for node in nodes])

    edges = battles_df_cleaned.loc[:, ["attacker_king", "defender_king"]].values.tolist()
    unique_edges = set(tuple(edge) for edge in edges)

    edges_w = battles_df_cleaned.groupby(by=["attacker_king", "defender_king"])["name"].count()
    edges_titles = battles_df_cleaned.groupby(by=["attacker_king", "defender_king"])["name"].agg(lambda name: ", ".join(name))

    for edge in unique_edges:
        net5kings.add_edge(edge[0], edge[1], weight=int(edges_w[edge]), value=int(edges_w[edge]), title=edges_titles[edge])

    enemies_map = net5kings.get_adj_list()
    for node in net5kings.nodes:
        node["value"] = 1 + len(enemies_map[node["id"]])
        node["color"] = nodeColors[node["value"]]

    return net5kings


def main():
    st.set_page_config(page_title="Lab1. Part 1", layout="wide")
    st.title('Lab1. Part 1: Network of battles of the War of 5 Kings')

    battles_df_cleaned = data_load()

    tab1, tab2 = st.tabs(["Battles network", "Battles data"])

    with tab1:
        net5kings = buildGraph(battles_df_cleaned)
        components.html(net5kings.generate_html(), height=1050)

    with tab2:
        st.dataframe(battles_df_cleaned, hide_index=True)


if __name__ == '__main__':
    main()
