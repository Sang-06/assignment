import pandas as pd
import plotly.express as px

data = {
    "Epoch": list(range(1, 11)),
    "Training Loss": [0.95, 0.80, 0.65, 0.55, 0.48, 0.44, 0.42, 0.41, 0.405, 0.40]
}

df = pd.DataFrame(data)

fig = px.line(
    df,
    x="Epoch",
    y="Training Loss",
    title="Training Loss Over Epochs",
    markers=True
)

fig.update_layout(
    xaxis_title="Epoch",
    yaxis_title="Training Loss"
)
fig.add_annotation(
    x=8,
    y=0.41,
    text="Loss stabilizes here",
    showarrow=True,
    arrowhead=2
)
fig.show()