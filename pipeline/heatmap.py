import json
import pandas as pd
import matplotlib.pyplot as plt

with open("outputs/positions.json", "r") as f:
    positions = json.load(f)

df = pd.DataFrame(positions)

plt.figure(figsize=(10, 6))

plt.hist2d(
    df["x"],
    df["y"],
    bins=50
)

plt.colorbar()

plt.gca().invert_yaxis()

plt.title("Customer Movement Heatmap")

plt.savefig("outputs/heatmap.png")

plt.show()