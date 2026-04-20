# Lucky Factors Dashboard

Interactive visualisation of the sequential factor selection methodology in Harvey & Liu (2021), *Journal of Financial Economics* 141, 413–435.
https://doi.org/10.1016/j.jfineco.2021.04.014

The dashboard steps through a bootstrap-based factor selection procedure testing 14 candidate asset pricing factors. At each round, factors compete on how much they reduce cross-sectional pricing errors, with a multiple-testing correction ensuring only genuinely useful factors enter the model. Equal-weighting recovers the Fama-French 3-factor model. Value-weighting selects MKT and QMJ instead, challenging the conventional role of SMB and HML.

---

## Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/shvchn/Lucky-Factors-Visualisation
cd Lucky-Factors-Visualisation
pip install dash dash-bootstrap-components plotly
```

Run the app:

```bash
python app.py
```

Open your browser at `http://127.0.0.1:8050`.

---

## Tabs

**Factor Universe**
Reproduces Table 1 of the paper. Panel A shows mean annual returns and t-statistics for all 14 candidate factors (toggle between the two views using the buttons above the chart). Green bars are selected in both final models, blue in one model only, grey never selected. Note BAB has the highest return and t-statistic yet never enters any model. Panel B shows the full 14x14 factor correlation matrix with annotated cluster boxes highlighting the value group (HML, IA, CMA) and profitability group (QMJ, RMW, ROE), this motivate the multiple-testing correction.

**Factor Selection**
Reproduces Tables 2 and 3. Steps through the sequential selection rounds interactively using the Prev/Next buttons. Toggle between equal-weighted (EW) and value-weighted (VW) specifications. At each round the bar chart shows the SI statistic for every candidate factor, where bars to the left of the red dashed threshold line are genuinely significant. The scoreboard on the right shows the winner, its SI value, the bootstrap 5th percentile threshold, and the multiple-test p-value.

**Model Comparison**
Panel A shows a cumulative waterfall chart of pricing error reduction for each selected factor under EW and VW side by side. VW explains nearly double what EW does (52.7% vs 28.5%), driven by the market factor's outsized power for large stocks. Panel B shows the full Round 2 candidate table under both weightings, the point at which EW and VW paths diverge. SMB wins under EW but worsens pricing errors under VW, while QMJ does the opposite.

---

## Data

All data is hardcoded directly from Tables 1, 2, and 3 of Harvey & Liu (2021). No external data sources or API calls are required. Sample period is January 1968 to December 2012.

---

## Reference

Harvey, C.R. & Liu, Y. (2021). Lucky Factors. *Journal of Financial Economics*, 141(2), 413–435.
https://doi.org/10.1016/j.jfineco.2021.04.014
