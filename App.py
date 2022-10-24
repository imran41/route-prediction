#from tkinter import font
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx.algorithms.community as nx_comm
#from community import community_louvain

st.title('Optimal traffic routes prediction for shuttle service')
st.markdown('Karate Club Graph')

uploaded_file = st.file_uploader(" ", type=['csv']) #Only accepts csv file format

if uploaded_file is not None:     
    data = pd.read_csv(uploaded_file)
    data
    g = nx.karate_club_graph()
    g = nx.from_pandas_edgelist(data, source = "road", target = "Destination") #Use the Graph API to create an empty network graph object

    partition = nx_comm.louvain_communities(g)

    if st.button("Click to show partition: "):
        st.write(partition, len(partition))

    color_map = []
    # color the nodes according to their partition
    for node in g:
        if node in partition[0]:
            color_map.append('red')
        elif node in partition[1]:
            color_map.append('green')
        elif node in partition[2]:
            color_map.append('blue')
        else:
            color_map.append('yellow')

    
    fig, ax = plt.subplots(figsize = (30,15))
    pos = nx.spring_layout(g)


    nx.draw_networkx(g, pos, partition, 
                    with_labels=True, 
                    node_size = 250, 
                    node_shape = "s", 
                    edge_color = "k", 
                    style = "--", 
                    node_color = color_map,
                    font_size = 15)

    st.pyplot(fig)
   
    #########################################
    st.info("Partition Graph")

    com_4 = nx_comm.louvain_communities(g)

    st.subheader("For louvain_communities")
    st.write("Modularity: ", nx_comm.modularity(g, com_4))
    st.write("Partition Quality: ", nx_comm.partition_quality(g, com_4))
    st.write("Coverage: ", nx_comm.coverage(g, com_4)) 
    st.write("Performance: ", nx_comm.performance(g, com_4))

    if st.button("Click to show edge betweeness centrality of graph"):
        edge_BC = nx.edge_betweenness_centrality(g)
        st.info(sorted(edge_BC.items(), key=lambda edge_BC : (edge_BC[1], edge_BC[0]), reverse = True))
    
    st.subheader("Thanks for visit.")

    st.balloons()
