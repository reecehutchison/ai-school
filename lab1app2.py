import json
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from pyvis.network import Network

from src.GameOfThronesGraphClass import GameOfThronesGraph


@st.cache_data
def data_load():
    with open("data/game-of-thrones-characters-groups.json") as f:
        json_data = json.load(f)
    return json_data['groups']


def buildStrengthChart(GameOfThronesHouses):
    visualisationData = {}
    for house in GameOfThronesHouses:
        visualisationData[house.name] = house.getStrength()

    x = list(visualisationData.keys())
    y = list(visualisationData.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=x, y=y, hue=x, palette="husl", legend=False, ax=ax)
    ax.set(xlabel='Houses',
           ylabel='Strength (N family members)',
           title='Strength of GameOfThronesHouses')
    ax.tick_params(axis='x', rotation=45)
    return fig


def buildGraph(GameOfThronesHouses):
    colorKeys = [house.name for house in GameOfThronesHouses if house.name != "Include"]
    nodeColors = dict(zip(colorKeys, [tuple(int(c*255) for c in cs) for cs in sns.color_palette("husl", len(colorKeys))]))

    g = nx.Graph()
    myEdges = []
    for house in GameOfThronesHouses:
        if house.name != "Include":
            g.add_node(house.name, size=house.getStrength())
            g.add_nodes_from(house)
            for person in house:
                myEdges.append((house.name, person))
    g.add_edges_from(myEdges)

    GameOfThronesNet = Network(
                bgcolor="#242020",
                font_color="white",
                height="1000px",
                width="100%",
                cdn_resources="remote")
    GameOfThronesNet.from_nx(g)

    for node in GameOfThronesNet.nodes:
        if node["id"] in GameOfThronesHouses:
            node["color"] = '#%02x%02x%02x' % nodeColors[node["id"]]
        else:
            for house in GameOfThronesHouses:
                if house.name != "Include":
                    if node["id"] in house:
                        node["color"] = '#%02x%02x%02x' % nodeColors[house.name]

    return GameOfThronesNet


def main():
    st.set_page_config(page_title="Lab1. Part 2", layout="wide")
    st.title('Lab1. Part 2: Relationships between characters in the Game of Thrones')

    corpusData = data_load()
    GameOfThronesHouses = GameOfThronesGraph(corpusData)

    tab1, tab2, tab3 = st.tabs(["Houses network", "Strength of Houses", "Houses data"])

    with tab1:
        GameOfThronesNet = buildGraph(GameOfThronesHouses)
        components.html(GameOfThronesNet.generate_html(), height=1050)

    with tab2:
        st.pyplot(buildStrengthChart(GameOfThronesHouses))

    with tab3:
        for house in GameOfThronesHouses:
            with st.expander(f"{house.name} ({house.getStrength()} members)"):
                st.write(", ".join(house))


if __name__ == '__main__':
    main()
