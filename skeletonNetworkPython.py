import networkx as nx
import plotly.graph_objects as go
import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/juliaDataScience-22/skeletonNetwork/refs/heads/main/skeletonNetwork2.csv", delimiter=';')

G = nx.Graph()

for _, row in data.iterrows():
    bone = row["Bone"]
    connected_bones = row["Connections"].split(",") 
    G.add_node(bone)
    for connected_bone in connected_bones:
        if connected_bone.strip():
            G.add_edge(bone, connected_bone.strip())



manual_positions = {
    "Hyoid bone": (-0.5, 0.25), 
    "Malleus": (-1, 0.5),
    "Incus": (-0.9, 0.65),
    "Stapes": (-0.8, 0.9)
}

auto_positions = nx.spring_layout(G, seed=42, k=2 / len(G.nodes()) ** 0.5)

positions = {node: manual_positions.get(node, auto_positions[node]) for node in G.nodes()}

x_vals = [positions[node][0] for node in G.nodes()]
y_vals = [positions[node][1] for node in G.nodes()]

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = positions[edge[0]]
    x1, y1 = positions[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='gray'),
    hoverinfo='none',
    mode='lines')

node_trace = go.Scatter(
    x=x_vals, y=y_vals,
    mode='markers+text',
    text=[node for node in G.nodes()],
    textposition='bottom center',
    marker=dict(
        showscale=True,
        colorscale='Viridis',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        )
    )
)

fig = go.Figure(data=[edge_trace, node_trace])

fig.update_layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(l=0, r=0, b=0, t=0),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False),
    dragmode='pan',
    height=1000 
)

fig.write_html('network_graph.html')

fig.show()
