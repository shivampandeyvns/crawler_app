import networkx as nx
import plotly.graph_objects as go


def create_network_graph(graph, df):

    pos = nx.spring_layout(
        graph,
        seed=42,
        k=0.5
    )

    edge_x = []
    edge_y = []

    for edge in graph.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=1,
            color="gray"
        ),
        hoverinfo="none"
    )

    node_x = []
    node_y = []

    node_size = []
    node_color = []

    hover_text = []

    for node in graph.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)

        score = float(df.iloc[node]["pagerank"])

        node_size.append(score * 5000 + 15)

        node_color.append(score)

        hover_text.append(
            f"<b>{df.iloc[node]['title']}</b>"
            f"<br>Source: {df.iloc[node]['source']}"
            f"<br>PageRank: {score:.4f}"
        )

    node_trace = go.Scatter(

        x=node_x,
        y=node_y,

        mode="markers",

        hoverinfo="text",

        hovertext=hover_text,

        marker=dict(

            size=node_size,

            color=node_color,

            colorscale="Viridis",

            showscale=True,

            colorbar=dict(
                title="PageRank"
            ),

            line=dict(width=1)

        )

    )

    fig = go.Figure(
        data=[
            edge_trace,
            node_trace
        ]
    )

    fig.update_layout(

        title="Article Similarity Network",

        showlegend=False,

        hovermode="closest",

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        )

    )

    return fig