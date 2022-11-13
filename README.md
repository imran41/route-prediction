

# Deploying a Streamlit Dashboard with Heroku


```

1. Create a Git Repo

_Note: Heroku allows deployment using Git or Docker._

```sh
git init
```

2. Build your App

```py
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
    #data = data.head(250)
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

```

3. Test your App (Local Environment)

```sh
~$ streamlit run App.py
```

4. Create your requeriments.txt file

This file contains the libraries that your code needs to work. To do this, you can use ```pipreqs```.

```sh
pipreqs /path/to/your/app/
```
After this command, a requirements.txt will be created in the folder of your app

```
matplotlib==3.5.1
networkx==2.8.7
numpy==1.21.5
pandas==1.4.2
streamlit==1.14.0

```

5. Setup.sh and Procfile

Heroku needs these files for starting the app

    - setup.sh : create a streamlit folder with both credentials.toml and config.toml files.
    - Procfile : This file executes the setup.sh and then call streamlit run to run the app

```sh
# Setup.sh
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```
```sh
# Procfile
web: sh setup.sh && streamlit run App.py
```

6. Create a Heroku Account

Create a free account

7. Install Heroku CLI

[Follow these steps](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

8. Login into Heroku CLI

Move to your App folder and execute ```heroku login```

9. Deploy the App

Deploy your app by running ```heroku create``` in your app folder

10. Check it

Check your app by running ```heroku ps:scale web=1```

After that, push your code

```sh
git add .
git commit -m "message"
git push heroku master
```

11. Open it

Open your app using ```heroku open```

Thanks to [Gilbert Tanner](https://gilberttanner.com/blog/deploying-your-streamlit-dashboard-with-heroku) for his tutorial
