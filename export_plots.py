import os
from app import make_factor_stats_chart, make_correlation_heatmap, make_chart_at_step, make_waterfall, get_factors
from data import ROUND_KEYS

OUT = "plots"
os.makedirs(OUT, exist_ok=True)

# Tab 1: Factor Universe
means_fig, tstats_fig = make_factor_stats_chart()
means_fig.write_image(f"{OUT}/tab1_panel_a_factor_mean_returns.png", scale=2)
tstats_fig.write_image(f"{OUT}/tab1_panel_a_factor_tstatistics.png", scale=2)
print("Saved: factor mean returns + t-statistics")

heatmap = make_correlation_heatmap()
heatmap.update_layout(
    height=900,
    width=1600,              # wider canvas to give cells room
    margin=dict(l=220, r=320, t=30, b=180),
)
# Remove scaleanchor — let Plotly size cells freely within the plot area
heatmap.update_xaxes(scaleanchor=None)
heatmap.update_yaxes(scaleanchor=None)
heatmap.write_image(f"{OUT}/tab1_panel_b_correlation_heatmap.png", scale=2)
print("Saved: correlation heatmap")

# Tab 2: Factor Selection (all rounds × both weightings, fully revealed at step 3)
for rkey in ROUND_KEYS:
    for weighting in ("ew", "vw"):
        fig = make_chart_at_step(rkey, weighting, 3)
        
        items = sorted(get_factors(rkey, weighting), key=lambda x: x[1])
        values = [v for _, v in items]
        new_x_max = max(values + [0.01]) + 0.12
        
        # Fix label positions for very negative bars
        new_textpositions = ["inside" if v < -0.15 else "outside" for v in values]
        new_textcolors = ["white" if v < -0.15 else "#6c757d" for v in values]
        fig.update_traces(
            textposition=new_textpositions,
            textfont=dict(color=new_textcolors),
            cliponaxis=False,
        )
        
        fig.update_layout(
            width=1100,
            margin=dict(l=280, r=160, t=40, b=60),
            xaxis=dict(range=[min(values + [-0.21]) - 0.015, new_x_max]),
        )
        
        fname = f"{OUT}/tab2_{rkey}_{weighting}_factor_selection.png"
        fig.write_image(fname, scale=2)
        print(f"Saved: {fname}")

# Tab 3: Model Comparison
make_waterfall().write_image(f"{OUT}/tab3_panel_a_waterfall_pricing_error_reduction.png", scale=2)
print("Saved: waterfall chart")

print(f"\nAll plots saved to ./{OUT}/")
