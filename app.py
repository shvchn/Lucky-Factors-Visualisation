import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from data import ROUNDS, ROUND_KEYS, FACTOR_LABELS, FINAL_MODELS, FACTOR_STATS, CORRELATION_MATRIX

# ── Palette ───────────────────────────────────────────────────────────────────

C = {
    "bg":        "#f8f9fa",
    "card":      "#ffffff",
    "border":    "#dee2e6",
    "text":      "#212529",
    "muted":     "#6c757d",
    "winner":    "#0FA872",  # mygreen
    "neutral":   "#ced4da",
    "active":    "#0E62B5",  # myblue
    "threshold": "#e03131",
    "purple":    "#280E9C",  # mypurple
    "plot_bg":   "#ffffff",
    "grid":      "#f1f3f5",
    "past":      "#0F8FA8",  # mylightblue
    "current":   "#0E62B5",  # myblue
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_factors(rkey, weighting):
    rd = ROUNDS[rkey]
    ew = weighting == "ew"
    if rkey in ("round1", "round2"):
        key = "si_ew" if ew else "si_vw"
        return [(k, v[key]) for k, v in rd["factors"].items()]
    if rkey == "round3":
        src = rd["factors_ew"] if ew else rd["factors_vw"]
        key = "si_ew" if ew else "si_vw"
        return [(k, v[key]) for k, v in src.items()]
    return [(k, v["si_ew"]) for k, v in rd["factors_ew"].items()]


WINNERS_EW = ["mkt", "smb", "hml", None]
WINNERS_VW = ["mkt", "qmj", None, None]


def accumulated_factors(round_idx, weighting):
    winners = WINNERS_EW if weighting == "ew" else WINNERS_VW
    return [w for w in winners[:round_idx + 1] if w]

# ── Chart (step-based, no frames) ─────────────────────────────────────────────
# step 0 → bars at 0, gray
# step 1 → bars at values, gray
# step 2 → bars at values, gray + threshold line
# step 3 → bars at values, coloured + threshold line

def make_chart_at_step(rkey, weighting, step):
    rd  = ROUNDS[rkey]
    ew  = weighting == "ew"
    step = step or 0

    if rkey == "round4" and not ew:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor=C["plot_bg"], plot_bgcolor=C["plot_bg"],
            annotations=[dict(text="VW selection complete after Round 3",
                              showarrow=False, font=dict(color=C["muted"], size=15),
                              xref="paper", yref="paper", x=0.5, y=0.5)],
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            height=400, margin=dict(l=0, r=0, t=20, b=0),
        )
        return fig

    items  = sorted(get_factors(rkey, weighting), key=lambda x: x[1])
    labels = [FACTOR_LABELS.get(k, k) for k, _ in items]
    values = [v for _, v in items]
    keys   = [k for k, _ in items]
    n      = len(labels)

    thresh = rd["multi_thresh_ew"] if ew else rd.get("multi_thresh_vw")
    winner = rd["winner_ew"] if ew else rd.get("winner_vw")

    gray  = [C["neutral"]] * n
    final = [
        C["winner"] if k == winner
        else (C["active"] if thresh is not None and v <= thresh else C["neutral"])
        for k, v in zip(keys, values)
    ]

    show_values    = step >= 1
    show_threshold = step >= 2
    show_colors    = step >= 3

    bar_vals   = values if show_values else [0] * n
    bar_colors = final  if show_colors else gray

    x_min = min(values + [-0.21]) - 0.015
    x_max = max(values + [0.01])  + 0.04

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bar_vals, y=labels,
        orientation="h",
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{v:+.3f}" for v in bar_vals] if show_values else [""] * n,
        textposition="outside",
        textfont=dict(color=C["muted"], size=14),
        hovertemplate="%{y}: SI = %{x:.4f}<extra></extra>",
    ))

    if show_threshold and thresh is not None:
        fig.add_vline(
            x=thresh, line_width=2.5, line_dash="dash", line_color=C["threshold"],
            annotation_text=f"Threshold ({thresh:.3f})",
            annotation_position="top left",
            annotation_font=dict(color=C["threshold"], size=14),
        )

    fig.add_vline(x=0, line_width=1, line_color=C["border"])

    fig.update_layout(
        paper_bgcolor=C["plot_bg"],
        plot_bgcolor=C["plot_bg"],
        font=dict(color=C["text"], family="Inter, sans-serif"),
        margin=dict(l=10, r=60, t=20, b=30),
        xaxis=dict(
            title="Scaled Intercept Reduction (SI)",
            title_font=dict(color=C["muted"], size=14),
            gridcolor=C["grid"], zeroline=False,
            tickfont=dict(size=14, color=C["muted"]),
            range=[x_min, x_max],
        ),
        yaxis=dict(
            gridcolor=C["grid"],
            tickfont=dict(size=14, color=C["text"]),
            type="category",
        ),
        showlegend=False,
        height=600,
        bargap=0.45,
        dragmode="pan",
        transition=dict(duration=650, easing="cubic-in-out"),
    )
    return fig

# ── Sub-components ────────────────────────────────────────────────────────────

def make_step_indicator(round_idx):
    items = []
    for i, rk in enumerate(ROUND_KEYS):
        rd = ROUNDS[rk]
        if i < round_idx:
            bg, fg, border = C["past"],    "#fff", C["past"]
        elif i == round_idx:
            bg, fg, border = C["current"], "#fff", C["current"]
        else:
            bg, fg, border = "transparent", C["muted"], C["border"]

        items.append(html.Span(
            rd["label"],
            style={
                "display": "inline-block",
                "padding": "8px 22px",
                "borderRadius": "20px",
                "background": bg,
                "border": f"2px solid {border}",
                "color": fg,
                "fontSize": "17px",
                "fontWeight": 600,
                "margin": "0 6px",
            }
        ))
        if i < len(ROUND_KEYS) - 1:
            items.append(html.Span("→", style={"color": C["border"],
                                               "fontSize": "20px", "margin": "0 4px"}))
    return html.Div(items, style={"textAlign": "center", "marginBottom": "16px"})


def make_model_progress(round_idx, weighting):
    factors = accumulated_factors(round_idx, weighting)
    if not factors:
        return html.Div()

    chips = []
    for i, f in enumerate(factors):
        chips.append(html.Span(
            FACTOR_LABELS.get(f, f.upper()),
            style={
                "display": "inline-block",
                "padding": "4px 12px",
                "borderRadius": "6px",
                "background": "#e6f7f1",
                "border": f"1px solid {C['winner']}",
                "color": C["winner"],
                "fontSize": "16px",
                "fontWeight": 600,
                "margin": "2px 4px",
            }
        ))
        if i < len(factors) - 1:
            chips.append(html.Span("+", style={"color": C["muted"], "fontWeight": 700,
                                               "fontSize": "18px", "margin": "0 2px"}))

    return dbc.Card(dbc.CardBody([
        html.P("Model so far", className="small fw-bold mb-2",
               style={"color": C["muted"], "textTransform": "uppercase",
                      "letterSpacing": "0.05em"}),
        html.Div(chips),
    ]), className="mt-3",
       style={"background": "#f0fbf7", "border": f"1px solid {C['winner']}33",
              "borderRadius": "8px"})


def make_scoreboard(rkey, weighting, round_idx):
    rd  = ROUNDS[rkey]
    ew  = weighting == "ew"

    def model_so_far():
        factors = accumulated_factors(round_idx, weighting)
        if not factors:
            return html.Div()
        chips = []
        for i, f in enumerate(factors):
            chips.append(html.Span(
                FACTOR_LABELS.get(f, f.upper()),
                style={"display": "inline-block", "padding": "4px 10px",
                       "borderRadius": "6px", "background": "#e6f7f1",
                       "border": f"1px solid {C['winner']}", "color": C["winner"],
                       "fontSize": "14px", "fontWeight": 600, "margin": "2px 3px"},
            ))
            if i < len(factors) - 1:
                chips.append(html.Span("+", style={"color": C["muted"],
                                                   "fontWeight": 700, "fontSize": "16px",
                                                   "margin": "0 2px"}))
        return html.Div([
            html.Hr(style={"borderColor": C["border"], "margin": "10px 0"}),
            html.P("Model so far", className="mb-1",
                   style={"color": C["muted"], "fontSize": "13px",
                          "textTransform": "uppercase", "letterSpacing": "0.05em",
                          "fontWeight": 600}),
            html.Div(chips),
        ])

    if rkey == "round4" and not ew:
        return dbc.Card(dbc.CardBody([
            html.P("Final VW Model", className="small fw-bold mb-1",
                   style={"color": C["muted"]}),
            html.H5("MKT + QMJ", style={"color": C["winner"]}),
            html.P("Selection completed in Round 3", className="small",
                   style={"color": C["muted"]}),
            model_so_far(),
        ]), style={"background": C["card"], "border": f"1px solid {C['border']}"},
           className="h-100")

    baseline = rd["baseline_ew"]      if ew else rd.get("baseline_vw", "—")
    winner   = rd["winner_ew"]        if ew else rd.get("winner_vw")
    thresh   = rd["thresh_ew"]        if ew else rd.get("thresh_vw", "—")
    p_val    = rd["p_ew"]             if ew else rd.get("p_vw", "—")
    multi_p  = rd.get("multi_p_ew")   if ew else rd.get("multi_p_vw")
    multi_th = rd.get("multi_thresh_ew") if ew else rd.get("multi_thresh_vw")

    winner_text  = FACTOR_LABELS.get(winner, winner) if winner else "None — selection stops"
    winner_color = C["winner"] if winner else C["threshold"]

    def row(label, val, color=C["text"]):
        return html.Div([
            html.P(label, className="mb-0", style={"color": C["muted"], "fontSize": "13px"}),
            html.P(val, className="mb-2", style={"color": color, "fontWeight": 600, "fontSize": "18px"}),
        ])

    rows = [
        html.H6("Results", className="fw-bold mb-3", style={"color": C["text"]}),
        row("Baseline", baseline or "—"),
        html.Hr(style={"borderColor": C["border"], "margin": "8px 0"}),
        row("Selected this round", winner_text, winner_color),
    ]
    if winner and isinstance(multi_th, float):
        winner_si = dict(get_factors(rkey, weighting)).get(winner)
        sig = C["winner"] if (isinstance(multi_p, float) and multi_p < 0.05) else C["threshold"]
        rows += [
            html.Hr(style={"borderColor": C["border"], "margin": "8px 0"}),
            row("Winner SI", f"{winner_si:.3f}" if winner_si is not None else "—"),
            row("Multi-test threshold", f"{multi_th:.3f}"),
            row("Multi-test p", f"{multi_p:.3f}", sig),
        ]

    rows.append(model_so_far())

    return dbc.Card(
        dbc.CardBody(rows),
        style={"background": C["card"], "border": f"1px solid {C['border']}"},
        className="h-100",
    )

# ── Tab 1 charts ─────────────────────────────────────────────────────────────

def make_factor_stats_chart():
    factors = list(FACTOR_LABELS.keys())
    labels  = [FACTOR_LABELS[f] for f in factors]
    means   = [FACTOR_STATS[f]["mean"] for f in factors]
    tstats  = [FACTOR_STATS[f]["tstat"] for f in factors]

    both     = {"mkt"}
    one_only = {"smb", "hml", "qmj"}

    def get_color(f):
        if f in both:     return C["winner"]
        if f in one_only: return C["active"]
        return C["neutral"]

    colors = [get_color(f) for f in factors]

    def make_bars(values, title, ytitle):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=labels, y=values,
            marker_color=colors,
            marker_line_width=0,
            text=[f"{v:.3f}" if title == "Mean Annual Returns" else f"{v:.2f}" for v in values],
            textposition="outside",
            textfont=dict(size=11, color=C["muted"]),
            hovertemplate="%{x}<br>" + ytitle + ": %{y}<extra></extra>",
        ))

        bab_idx = factors.index("bab")
        bab_val = values[bab_idx]
        fig.add_annotation(
            x=labels[bab_idx],
            y=bab_val,
            text="Highest return<br>yet never selected" if title == "Mean Annual Returns"
                 else "Highest t-stat<br>yet never selected",
            showarrow=True,
            arrowhead=2,
            arrowcolor=C["threshold"],
            font=dict(color=C["threshold"], size=12),
            ax=60, ay=-40,
        )


        fig.update_layout(
            paper_bgcolor=C["plot_bg"],
            plot_bgcolor=C["plot_bg"],
            font=dict(color=C["text"], family="Inter, sans-serif"),
            margin=dict(l=10, r=10, t=40, b=120),
            xaxis=dict(
                tickfont=dict(size=11, color=C["text"]),
                tickangle=-35,
                gridcolor=C["grid"],
            ),
            yaxis=dict(
                title=ytitle,
                title_font=dict(color=C["muted"], size=13),
                gridcolor=C["grid"],
                zeroline=True, zerolinecolor=C["border"],
                tickfont=dict(size=12, color=C["muted"]),
            ),
            showlegend=False,
            height=420,
            bargap=0.35,
            title=dict(text=title, font=dict(size=15, color=C["text"]), x=0.5),
        )
        return fig

    return make_bars(means, "Mean Annual Returns", "Mean Annual Return"), \
           make_bars(tstats, "t-Statistics", "t-statistic")


def make_correlation_heatmap():
    factors = ["mkt", "smb", "mom", "skew", "psl", "bab", "gp", "civ",
               "hml", "ia", "cma",
               "roe", "qmj", "rmw"]
    labels  = [FACTOR_LABELS[f] for f in factors]

    z = [[CORRELATION_MATRIX[r][c] for c in factors] for r in factors]

    fig = go.Figure(go.Heatmap(
        z=z,
        x=labels, y=labels,
        colorscale=[
            [0.0,  "#280E9C"],
            [0.25, "#0E62B5"],
            [0.5,  "#ffffff"],
            [0.75, "#0F8FA8"],
            [1.0,  "#0FA872"],
        ],
        zmid=0,
        zmin=-1, zmax=1,
        text=[[f"{CORRELATION_MATRIX[r][c]:.2f}" for c in factors] for r in factors],
        texttemplate="%{text}",
        textfont=dict(size=9),
        hovertemplate="%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>",
        colorbar=dict(
            title=dict(text="Correlation", font=dict(size=12)),
            tickfont=dict(size=11),
            thickness=15,
        ),
    ))

    value_indices  = [8, 9, 10]
    profit_indices = [11, 12, 13]

    for indices, color, label in [
        (value_indices,  "#e67e22", "Value cluster — HML, IA, CMA<br>(correlations 0.69–0.90)"),
        (profit_indices, "#8e44ad", "Profitability cluster — ROE, QMJ, RMW<br>(correlations 0.68–0.76)"),
    ]:
        mn = min(indices) - 0.5
        mx = max(indices) + 0.5

        fig.add_shape(
            type="rect",
            x0=mn, x1=mx,
            y0=mn, y1=mx,
            line=dict(color=color, width=3),
            fillcolor="rgba(0,0,0,0)",
        )

        fig.add_annotation(
            x=mx + 0.2,
            y=(mn + mx) / 2,
            text=label,
            showarrow=True,
            arrowhead=2,
            arrowcolor=color,
            arrowwidth=1.5,
            ax=80,
            ay=0,
            font=dict(color=color, size=11, family="Inter, sans-serif"),
            bgcolor="white",
            bordercolor=color,
            borderwidth=1.5,
            borderpad=4,
            xanchor="left",
        )

    fig.update_layout(
        paper_bgcolor=C["plot_bg"],
        plot_bgcolor=C["plot_bg"],
        font=dict(color=C["text"], family="Inter, sans-serif"),
        margin=dict(l=10, r=220, t=20, b=10),
        height=620,
        xaxis=dict(
            tickfont=dict(size=10),
            tickangle=-35,
            side="bottom",
        ),
        yaxis=dict(
            tickfont=dict(size=10),
            autorange="reversed",
        ),
    )
    return fig


# ── Tab 3 charts ─────────────────────────────────────────────────────────────

def make_waterfall():
    fig = go.Figure()

    fig.add_trace(go.Waterfall(
        name="Equal-Weighted",
        orientation="v",
        measure=["relative", "relative", "relative", "total"],
        x=["MKT", "SMB", "HML", "Total"],
        y=[20.6, 4.9, 3.0, 28.5],
        text=["+20.6%", "+4.9%", "+3.0%", "28.5%"],
        textposition="outside",
        textfont=dict(size=13, color=C["text"]),
        increasing=dict(marker=dict(color=C["winner"])),
        totals=dict(marker=dict(color=C["active"])),
        decreasing=dict(marker=dict(color=C["threshold"])),
        connector=dict(line=dict(color=C["muted"], width=1.5, dash="dot")),
        xaxis="x1",
        yaxis="y1",
    ))

    fig.add_trace(go.Waterfall(
        name="Value-Weighted",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["MKT", "QMJ", "Total"],
        y=[44.4, 8.3, 52.7],
        text=["+44.4%", "+8.3%", "52.7%"],
        textposition="outside",
        textfont=dict(size=13, color=C["text"]),
        increasing=dict(marker=dict(color=C["winner"])),
        totals=dict(marker=dict(color=C["active"])),
        decreasing=dict(marker=dict(color=C["threshold"])),
        connector=dict(line=dict(color=C["muted"], width=1.5, dash="dot")),
        xaxis="x2",
        yaxis="y2",
    ))

    fig.update_layout(
        paper_bgcolor=C["plot_bg"],
        plot_bgcolor=C["plot_bg"],
        font=dict(color=C["text"], family="Inter, sans-serif"),
        margin=dict(l=10, r=10, t=40, b=40),
        height=460,
        showlegend=False,
        grid=dict(rows=1, columns=2, pattern="independent"),
        xaxis=dict(
            title="Equal-Weighted Model",
            title_font=dict(color=C["muted"], size=13),
            tickfont=dict(size=13, color=C["text"]),
            gridcolor=C["grid"],
            domain=[0.0, 0.42],
        ),
        yaxis=dict(
            title="% Reduction in Pricing Errors",
            title_font=dict(color=C["muted"], size=13),
            tickfont=dict(size=12, color=C["muted"]),
            gridcolor=C["grid"],
            ticksuffix="%",
            range=[0, 70],
        ),
        xaxis2=dict(
            title="Value-Weighted Model",
            title_font=dict(color=C["muted"], size=13),
            tickfont=dict(size=13, color=C["text"]),
            gridcolor=C["grid"],
            domain=[0.58, 1.0],
        ),
        yaxis2=dict(
            title="% Reduction in Pricing Errors",
            title_font=dict(color=C["muted"], size=13),
            tickfont=dict(size=12, color=C["muted"]),
            gridcolor=C["grid"],
            ticksuffix="%",
            range=[0, 70],
            anchor="x2",
        ),
        annotations=[
            dict(
                text="EW total: 28.5%",
                x=0.21, y=1.05, xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=13, color=C["active"]),
            ),
            dict(
                text="VW total: 52.7%",
                x=0.79, y=1.05, xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=13, color=C["active"]),
            ),
        ],
    )
    return fig


def make_divergence_table():
    factors = ["smb", "hml", "mom", "skew", "psl", "roe", "ia",
               "qmj", "bab", "gp", "cma", "rmw", "civ"]
    rows = []
    rd = ROUNDS["round2"]
    for f in factors:
        fdata = rd["factors"].get(f, {})
        rows.append({
            "Factor": FACTOR_LABELS.get(f, f.upper()),
            "SI (EW)": fdata.get("si_ew", "—"),
            "SI (VW)": fdata.get("si_vw", "—"),
            "Winner EW": "Selected" if f == rd["winner_ew"] else "",
            "Winner VW": "Selected" if f == rd["winner_vw"] else "",
        })

    header_style = {
        "background": C["active"],
        "color": "white",
        "fontWeight": 700,
        "fontSize": "13px",
        "padding": "10px 14px",
        "textAlign": "center",
    }
    cell_style_base = {
        "fontSize": "13px",
        "padding": "8px 14px",
        "textAlign": "center",
        "borderBottom": f"1px solid {C['border']}",
    }

    header = html.Tr([
        html.Th("Factor",    style={**header_style, "textAlign": "left"}),
        html.Th("SI (EW)",   style=header_style),
        html.Th("SI (VW)",   style=header_style),
        html.Th("EW Winner", style=header_style),
        html.Th("VW Winner", style=header_style),
    ])

    table_rows = []
    for r in rows:
        si_ew = r["SI (EW)"]
        si_vw = r["SI (VW)"]
        is_ew_winner = r["Winner EW"] == "Selected"
        is_vw_winner = r["Winner VW"] == "Selected"

        def cell_color(val, is_winner):
            if is_winner: return C["winner"]
            if isinstance(val, float) and val < 0: return C["active"]
            return C["text"]

        table_rows.append(html.Tr([
            html.Td(r["Factor"],
                    style={**cell_style_base, "textAlign": "left",
                           "fontWeight": 600, "color": C["text"]}),
            html.Td(f"{si_ew:.3f}" if isinstance(si_ew, float) else si_ew,
                    style={**cell_style_base,
                           "color": cell_color(si_ew, is_ew_winner),
                           "fontWeight": 700 if is_ew_winner else 400}),
            html.Td(f"{si_vw:.3f}" if isinstance(si_vw, float) else si_vw,
                    style={**cell_style_base,
                           "color": cell_color(si_vw, is_vw_winner),
                           "fontWeight": 700 if is_vw_winner else 400}),
            html.Td(r["Winner EW"],
                    style={**cell_style_base, "color": C["winner"],
                           "fontWeight": 700, "fontSize": "16px"}),
            html.Td(r["Winner VW"],
                    style={**cell_style_base, "color": C["winner"],
                           "fontWeight": 700, "fontSize": "16px"}),
        ], style={"background": "#f8fffe" if is_ew_winner or is_vw_winner else C["card"]}))

    return html.Table(
        [html.Thead(header), html.Tbody(table_rows)],
        style={"width": "100%", "borderCollapse": "collapse",
               "borderRadius": "8px", "overflow": "hidden"},
    )


# ── App layout ────────────────────────────────────────────────────────────────

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Lucky Factors",
)

app.layout = dbc.Container([

    dcc.Store(id="weighting", data="ew"),
    dcc.Store(id="round-idx", data=0),

    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Lucky Factors",
                    style={"color": C["text"], "fontWeight": 700, "marginBottom": "4px"}),
            html.P("Bootstrap-based sequential factor selection via panel regression",
                   style={"color": C["muted"], "fontSize": "18px", "marginBottom": "2px"}),
            html.P("Harvey & Liu · Journal of Financial Economics · 2021",
                   style={"color": C["muted"], "fontSize": "13px", "fontWeight": 400,
                          "letterSpacing": "0.03em"}),
        ], width=12),
    ], className="mb-4 pt-4"),

    dbc.Tabs([

        # ── Tab 1: Factor Universe ─────────────────────────────────────────
        dbc.Tab(label="Factor Universe", tab_id="tab-universe",
                label_style={"color": C["purple"], "fontWeight": 600},
                children=[

            html.Div(style={"height": "24px"}),

            dbc.Row([
                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.P("PANEL A", className="mb-1",
                               style={"color": C["muted"], "fontSize": "11px",
                                      "fontWeight": 700, "letterSpacing": "0.06em"}),
                        html.P("Factor Returns & t-statistics",
                               style={"color": C["text"], "fontSize": "17px",
                                      "fontWeight": 600, "marginBottom": "4px"}),
                        html.Div([
                            html.Span("■", style={"color": C["winner"], "fontSize": "16px", "marginRight": "4px"}),
                            html.Span("Selected in both EW & VW", style={"color": C["muted"], "fontSize": "13px", "marginRight": "16px"}),
                            html.Span("■", style={"color": C["active"], "fontSize": "16px", "marginRight": "4px"}),
                            html.Span("Selected in one model only", style={"color": C["muted"], "fontSize": "13px", "marginRight": "16px"}),
                            html.Span("■", style={"color": C["neutral"], "fontSize": "16px", "marginRight": "4px"}),
                            html.Span("Never selected", style={"color": C["muted"], "fontSize": "13px"}),
                        ], style={"marginBottom": "16px"}),
                        dbc.ButtonGroup([
                            dbc.Button("Mean Returns", id="btn-means", size="sm",
                                       color="primary", outline=False),
                            dbc.Button("t-Statistics", id="btn-tstats", size="sm",
                                       color="primary", outline=True),
                        ], className="mb-3"),
                        dcc.Graph(id="factor-stats-chart", config={"displayModeBar": False}),
                    ]), style={"background": C["card"],
                               "border": f"1px solid {C['border']}",
                               "borderRadius": "10px",
                               "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
                ], width=12, className="mb-4"),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.P("PANEL B", className="mb-1",
                               style={"color": C["muted"], "fontSize": "11px",
                                      "fontWeight": 700, "letterSpacing": "0.06em"}),
                        html.P("Factor Correlation Matrix",
                               style={"color": C["text"], "fontSize": "17px",
                                      "fontWeight": 600, "marginBottom": "12px"}),
                        html.P(
                            "High correlations within the value group (HML, IA, CMA) and "
                            "profitability group (QMJ, RMW, ROE) motivate the multiple-testing "
                            "correction — correlated candidates inflate false discovery rates.",
                            style={"color": C["muted"], "fontSize": "14px", "marginBottom": "12px"},
                        ),
                        dcc.Graph(
                            figure=make_correlation_heatmap(),
                            config={"displayModeBar": False},
                        ),
                    ]), style={"background": C["card"],
                               "border": f"1px solid {C['border']}",
                               "borderRadius": "10px",
                               "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
                ], width=12, className="mb-4"),
            ]),

            html.Div(style={"height": "40px"}),
        ]),

        # ── Tab 2: Factor Selection ────────────────────────────────────────
        dbc.Tab(label="Factor Selection", tab_id="tab-selection",
                label_style={"color": C["purple"], "fontWeight": 600},
                children=[

            html.Div(style={"height": "24px"}),

            # Insight callout
            dbc.Alert([
                html.Strong("How to read: "),
                "The red dashed line shows how well the best factor could do by chance. "
                "Any bar left of it is genuinely significant. Use Prev/Next to step through rounds.",
            ], color="light", className="mb-4",
               style={"border": f"1px solid {C['border']}",
                      "borderLeft": f"4px solid {C['active']}",
                      "borderRadius": "6px", "color": C["text"]}),

            # EW/VW toggle
            dbc.Row([
                dbc.Col([
                    dbc.ButtonGroup([
                        dbc.Button("Equal-Weighted", id="btn-ew", size="sm",
                                   color="primary", outline=False),
                        dbc.Button("Value-Weighted", id="btn-vw", size="sm",
                                   color="primary", outline=True),
                    ]),
                ], width="auto"),
            ], className="mb-3"),

            # Step indicator
            html.Div(id="step-indicator", className="mb-3"),

            # Main card
            dbc.Card(dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div(id="round-label",
                                 style={"color": C["active"], "fontWeight": 700,
                                        "fontSize": "11px", "textTransform": "uppercase",
                                        "letterSpacing": "0.06em", "marginBottom": "4px"}),
                        html.Div(id="narrative",
                                 style={"color": C["text"], "fontSize": "18px",
                                        "lineHeight": "1.75"}),
                    ], width=12),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="main-chart",
                                  config={"scrollZoom": True, "displayModeBar": False}),
                    ], width=9),
                    dbc.Col([
                        html.Div(id="scoreboard", className="h-100"),
                    ], width=3),
                ], className="g-3 align-items-stretch"),
            ]), className="mb-3",
               style={"background": C["card"], "border": f"1px solid {C['border']}",
                      "borderRadius": "10px", "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),

            # Navigation
            dbc.Row([
                dbc.Col([
                    dbc.Button("← Previous", id="btn-prev", size="lg",
                               color="secondary", outline=True, disabled=True),
                ], width="auto"),
                dbc.Col([
                    html.Div(id="round-counter",
                             style={"color": C["muted"], "fontSize": "17px",
                                    "textAlign": "center", "paddingTop": "10px"}),
                ]),
                dbc.Col([
                    dbc.Button("Next →", id="btn-next", size="lg",
                               color="primary", outline=False),
                ], width="auto", className="ms-auto"),
            ], className="mb-2", align="center"),

            html.Div(style={"height": "40px"}),

        ]),

        # ── Tab 3: Model Comparison ────────────────────────────────────────
        dbc.Tab(label="Model Comparison", tab_id="tab-comparison",
                label_style={"color": C["purple"], "fontWeight": 600},
                children=[

            html.Div(style={"height": "24px"}),

            dbc.Row([
                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.P("PANEL A", className="mb-1",
                               style={"color": C["muted"], "fontSize": "11px",
                                      "fontWeight": 700, "letterSpacing": "0.06em"}),
                        html.P("Cumulative Pricing Error Reduction",
                               style={"color": C["text"], "fontSize": "17px",
                                      "fontWeight": 600, "marginBottom": "4px"}),
                        html.P(
                            "Each bar shows the incremental reduction in pricing errors "
                            "from adding that factor to the model. VW explains nearly double "
                            "what EW does — driven by the market factor's outsized explanatory "
                            "power for large stocks.",
                            style={"color": C["muted"], "fontSize": "14px",
                                   "marginBottom": "12px"},
                        ),
                        dcc.Graph(
                            figure=make_waterfall(),
                            config={"displayModeBar": False},
                        ),
                    ]), style={"background": C["card"],
                               "border": f"1px solid {C['border']}",
                               "borderRadius": "10px",
                               "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
                ], width=12, className="mb-4"),
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card(dbc.CardBody([
                        html.P("PANEL B", className="mb-1",
                               style={"color": C["muted"], "fontSize": "11px",
                                      "fontWeight": 700, "letterSpacing": "0.06em"}),
                        html.P("EW vs VW Divergence — Round 2 (Baseline = MKT)",
                               style={"color": C["text"], "fontSize": "17px",
                                      "fontWeight": 600, "marginBottom": "4px"}),
                        html.P(
                            "After MKT enters the model, EW and VW paths diverge. "
                            "Under EW, SMB wins — equal weighting amplifies small-stock effects. "
                            "Under VW, QMJ wins — profitability better explains large firm returns. "
                            "SMB has a positive SI under VW, meaning it actually worsens pricing errors "
                            "for value-weighted portfolios.",
                            style={"color": C["muted"], "fontSize": "14px",
                                   "marginBottom": "16px"},
                        ),
                        make_divergence_table(),
                    ]), style={"background": C["card"],
                               "border": f"1px solid {C['border']}",
                               "borderRadius": "10px",
                               "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"}),
                ], width=12, className="mb-4"),
            ]),

            html.Div(style={"height": "40px"}),

        ]),

    ], id="tabs", active_tab="tab-universe",
       style={"borderBottom": f"2px solid {C['border']}", "marginBottom": "8px"}),

], fluid=True, style={"background": C["bg"], "minHeight": "100vh",
                      "fontFamily": "Inter, sans-serif"})

# ── Callbacks ─────────────────────────────────────────────────────────────────

MAX_ROUND = len(ROUND_KEYS) - 1


@callback(
    Output("weighting",  "data"),
    Output("round-idx",  "data"),
    Output("btn-ew",     "outline"),
    Output("btn-vw",     "outline"),
    Input("btn-ew",      "n_clicks"),
    Input("btn-vw",      "n_clicks"),
    Input("btn-prev",    "n_clicks"),
    Input("btn-next",    "n_clicks"),
    State("weighting",   "data"),
    State("round-idx",   "data"),
)
def handle_controls(_, __, ___, ____, weighting, round_idx):
    btn = dash.callback_context.triggered[0]["prop_id"].split(".")[0] if dash.callback_context.triggered else ""
    if btn == "btn-ew":
        return "ew", 0, False, True
    if btn == "btn-vw":
        return "vw", 0, True, False
    if btn == "btn-next":
        return weighting, min(round_idx + 1, MAX_ROUND), weighting != "ew", weighting == "ew"
    if btn == "btn-prev":
        return weighting, max(round_idx - 1, 0), weighting != "ew", weighting == "ew"
    return weighting, round_idx, weighting != "ew", weighting == "ew"


@callback(
    Output("main-chart",     "figure"),
    Output("narrative",      "children"),
    Output("round-label",    "children"),
    Output("scoreboard",     "children"),
    Output("step-indicator", "children"),
    Output("round-counter",  "children"),
    Output("btn-prev",       "disabled"),
    Output("btn-next",       "disabled"),
    Input("round-idx",       "data"),
    Input("weighting",       "data"),
)
def update_display(round_idx, weighting):
    rkey = ROUND_KEYS[round_idx]
    rd   = ROUNDS[rkey]
    ew   = weighting == "ew"

    if rkey == "round4" and not ew:
        narrative = "VW model selection completed in Round 3 — no further rounds needed."
    else:
        narrative = rd["narrative_ew"] if ew else (rd.get("narrative_vw") or rd["narrative_ew"])

    return (
        make_chart_at_step(rkey, weighting, 3),
        narrative,
        rd["label"],
        make_scoreboard(rkey, weighting, round_idx),
        make_step_indicator(round_idx),
        f"Round {round_idx + 1} of {len(ROUND_KEYS)}",
        round_idx == 0,
        round_idx == MAX_ROUND,
    )


@callback(
    Output("factor-stats-chart", "figure"),
    Output("btn-means",          "outline"),
    Output("btn-tstats",         "outline"),
    Input("btn-means",           "n_clicks"),
    Input("btn-tstats",          "n_clicks"),
)
def update_factor_chart(_, __):
    btn = dash.callback_context.triggered[0]["prop_id"].split(".")[0] \
          if dash.callback_context.triggered else ""
    means_fig, tstats_fig = make_factor_stats_chart()
    if btn == "btn-tstats":
        return tstats_fig, True, False
    return means_fig, False, True


if __name__ == "__main__":
    app.run(debug=True)
