FACTOR_LABELS = {
    "mkt":  "Market (MKT)",
    "smb":  "Size (SMB)",
    "hml":  "Book-To-Market (HML)",
    "mom":  "Momentum (MOM)",
    "skew": "Coskewness (SKEW)",
    "psl":  "PSL",
    "roe":  "ROE",
    "ia":   "Investment (IA)",
    "qmj":  "Quality-Minus-Junk (QMJ)",
    "bab":  "Betting-Against-Beta (BAB)",
    "gp":   "Gross Profitability (GP)",
    "cma":  "Conservative Minus Aggressive (CMA)",
    "rmw":  "Robust Minus Weak (RMW)",
    "civ":  "Common Idiosyncratic Volatility (CIV)",
}

FACTOR_STATS = {
    "mkt":  {"mean": 0.052, "tstat": 2.17},
    "smb":  {"mean": 0.022, "tstat": 1.32},
    "hml":  {"mean": 0.048, "tstat": 3.08},
    "mom":  {"mean": 0.081, "tstat": 3.54},
    "skew": {"mean": 0.024, "tstat": 1.84},
    "psl":  {"mean": 0.055, "tstat": 2.99},
    "roe":  {"mean": 0.068, "tstat": 5.09},
    "ia":   {"mean": 0.057, "tstat": 5.76},
    "qmj":  {"mean": 0.048, "tstat": 3.74},
    "bab":  {"mean": 0.105, "tstat": 5.98},
    "gp":   {"mean": 0.039, "tstat": 3.24},
    "cma":  {"mean": 0.047, "tstat": 4.44},
    "rmw":  {"mean": 0.033, "tstat": 2.92},
    "civ":  {"mean": 0.060, "tstat": 3.48},
}

CORRELATION_MATRIX = {
    "mkt":  {"mkt":  1.00, "smb":  0.30, "hml": -0.32, "mom": -0.14, "skew": -0.02, "psl": -0.05, "roe": -0.19, "ia": -0.39, "qmj": -0.54, "bab": -0.09, "gp":  0.08, "cma": -0.41, "rmw": -0.21, "civ":  0.17},
    "smb":  {"mkt":  0.30, "smb":  1.00, "hml": -0.24, "mom": -0.03, "skew": -0.05, "psl": -0.04, "roe": -0.39, "ia": -0.26, "qmj": -0.54, "bab": -0.07, "gp":  0.06, "cma": -0.16, "rmw": -0.42, "civ":  0.27},
    "hml":  {"mkt": -0.32, "smb": -0.24, "hml":  1.00, "mom": -0.15, "skew":  0.23, "psl":  0.03, "roe": -0.11, "ia":  0.69, "qmj":  0.02, "bab":  0.40, "gp": -0.34, "cma":  0.71, "rmw":  0.11, "civ":  0.13},
    "mom":  {"mkt": -0.14, "smb": -0.03, "hml": -0.15, "mom":  1.00, "skew":  0.03, "psl": -0.03, "roe":  0.51, "ia":  0.04, "qmj":  0.26, "bab":  0.18, "gp":  0.01, "cma":  0.01, "rmw":  0.10, "civ": -0.18},
    "skew": {"mkt": -0.02, "smb": -0.05, "hml":  0.23, "mom":  0.03, "skew":  1.00, "psl":  0.10, "roe":  0.19, "ia":  0.15, "qmj":  0.13, "bab":  0.24, "gp": -0.01, "cma":  0.05, "rmw":  0.27, "civ":  0.04},
    "psl":  {"mkt": -0.05, "smb": -0.04, "hml":  0.03, "mom": -0.03, "skew":  0.10, "psl":  1.00, "roe": -0.06, "ia":  0.02, "qmj":  0.03, "bab":  0.06, "gp": -0.03, "cma":  0.03, "rmw":  0.03, "civ":  0.05},
    "roe":  {"mkt": -0.19, "smb": -0.39, "hml": -0.11, "mom":  0.51, "skew":  0.19, "psl": -0.06, "roe":  1.00, "ia":  0.04, "qmj":  0.68, "bab":  0.25, "gp":  0.34, "cma": -0.10, "rmw":  0.68, "civ": -0.26},
    "ia":   {"mkt": -0.39, "smb": -0.26, "hml":  0.69, "mom":  0.04, "skew":  0.15, "psl":  0.02, "roe":  0.04, "ia":  1.00, "qmj":  0.15, "bab":  0.35, "gp": -0.26, "cma":  0.90, "rmw":  0.05, "civ": -0.00},
    "qmj":  {"mkt": -0.54, "smb": -0.54, "hml":  0.02, "mom":  0.26, "skew":  0.13, "psl":  0.03, "roe":  0.68, "ia":  0.15, "qmj":  1.00, "bab":  0.19, "gp":  0.45, "cma":  0.07, "rmw":  0.76, "civ": -0.28},
    "bab":  {"mkt": -0.09, "smb": -0.07, "hml":  0.40, "mom":  0.18, "skew":  0.24, "psl":  0.06, "roe":  0.25, "ia":  0.35, "qmj":  0.19, "bab":  1.00, "gp": -0.11, "cma":  0.32, "rmw":  0.26, "civ":  0.11},
    "gp":   {"mkt":  0.08, "smb":  0.06, "hml": -0.34, "mom":  0.01, "skew": -0.01, "psl": -0.03, "roe":  0.34, "ia": -0.26, "qmj":  0.45, "bab": -0.11, "gp":  1.00, "cma": -0.34, "rmw":  0.49, "civ": -0.00},
    "cma":  {"mkt": -0.41, "smb": -0.16, "hml":  0.71, "mom":  0.01, "skew":  0.05, "psl":  0.03, "roe": -0.10, "ia":  0.90, "qmj":  0.07, "bab":  0.32, "gp": -0.34, "cma":  1.00, "rmw": -0.08, "civ":  0.04},
    "rmw":  {"mkt": -0.21, "smb": -0.42, "hml":  0.11, "mom":  0.10, "skew":  0.27, "psl":  0.03, "roe":  0.68, "ia":  0.05, "qmj":  0.76, "bab":  0.26, "gp":  0.49, "cma": -0.08, "rmw":  1.00, "civ": -0.10},
    "civ":  {"mkt":  0.17, "smb":  0.27, "hml":  0.13, "mom": -0.18, "skew":  0.04, "psl":  0.05, "roe": -0.26, "ia": -0.00, "qmj": -0.28, "bab":  0.11, "gp": -0.00, "cma":  0.04, "rmw": -0.10, "civ":  1.00},
}
ROUNDS = {
    "round1": {
        "label": "Round 1",
        "baseline_ew": "None (intercept only)",
        "baseline_vw": "None (intercept only)",
        "narrative_ew": (
            "Starting from scratch (intercept-only baseline), we test every candidate "
            "factor. The market factor (MKT) obliterates the multiple-testing threshold "
            "with p = 0.000, making it the clear winner. It enters the EW model."
        ),
        "narrative_vw": (
            "Same starting point for value-weighted portfolios. The market again wins "
            "decisively (p = 0.000). It enters the VW model."
        ),
        "winner_ew": "mkt",
        "winner_vw": "mkt",
        "factors": {
            "mkt":  {"si_ew": -0.206, "si_vw": -0.444},
            "smb":  {"si_ew": -0.109, "si_vw": -0.059},
            "hml":  {"si_ew":  0.108, "si_vw":  0.144},
            "mom":  {"si_ew":  0.110, "si_vw":  0.153},
            "skew": {"si_ew": -0.002, "si_vw": -0.027},
            "psl":  {"si_ew":  0.002, "si_vw":  0.035},
            "roe":  {"si_ew":  0.187, "si_vw":  0.105},
            "ia":   {"si_ew":  0.291, "si_vw":  0.382},
            "qmj":  {"si_ew":  0.358, "si_vw":  0.363},
            "bab":  {"si_ew": -0.049, "si_vw": -0.048},
            "gp":   {"si_ew":  0.030, "si_vw": -0.082},
            "cma":  {"si_ew":  0.199, "si_vw":  0.314},
            "rmw":  {"si_ew":  0.137, "si_vw":  0.045},
            "civ":  {"si_ew": -0.130, "si_vw": -0.115},
        },
        "thresh_ew": -0.095, "p_ew": 0.001,
        "thresh_vw": -0.258, "p_vw": 0.000,
        "multi_thresh_ew": -0.147, "multi_p_ew": 0.002,
        "multi_thresh_vw": -0.258, "multi_p_vw": 0.000,
    },
    "round2": {
        "label": "Round 2",
        "baseline_ew": "MKT",
        "baseline_vw": "MKT",
        "narrative_ew": (
            "With MKT in the model, we re-run the factor selection. SMB edges past the "
            "threshold (p = 0.032) and joins the EW baseline."
        ),
        "narrative_vw": (
            "For value-weighted portfolios, QMJ wins round 2 (p = 0.002), not SMB. "
            "Quality minus junk enters the VW model alongside the market."
        ),
        "winner_ew": "smb",
        "winner_vw": "qmj",
        "factors": {
            "smb":  {"si_ew": -0.062, "si_vw":  0.018},
            "hml":  {"si_ew": -0.047, "si_vw": -0.038},
            "mom":  {"si_ew":  0.089, "si_vw":  0.130},
            "skew": {"si_ew": -0.003, "si_vw": -0.044},
            "psl":  {"si_ew": -0.003, "si_vw":  0.016},
            "roe":  {"si_ew":  0.180, "si_vw": -0.079},
            "ia":   {"si_ew":  0.015, "si_vw": -0.042},
            "qmj":  {"si_ew":  0.193, "si_vw": -0.149},
            "bab":  {"si_ew": -0.014, "si_vw": -0.088},
            "gp":   {"si_ew":  0.017, "si_vw": -0.037},
            "cma":  {"si_ew": -0.031, "si_vw": -0.052},
            "rmw":  {"si_ew":  0.048, "si_vw": -0.146},
            "civ":  {"si_ew": -0.049, "si_vw":  0.035},
        },
        "thresh_ew": -0.052, "p_ew": 0.032,
        "thresh_vw": -0.079, "p_vw": 0.002,
        "multi_thresh_ew": -0.057, "multi_p_ew": 0.039,
        "multi_thresh_vw": -0.083, "multi_p_vw": 0.004,
    },
    "round3": {
        "label": "Round 3",
        "baseline_ew": "MKT + SMB",
        "baseline_vw": "MKT + QMJ",
        "narrative_ew": (
            "Baseline is now MKT + SMB. HML clears the bar (p = 0.011) and completes "
            "the classic Fama-French 3-factor model for EW portfolios."
        ),
        "narrative_vw": (
            "With MKT + QMJ as the VW baseline, no factor clears the multiple-testing "
            "threshold (best p = 0.113). The VW model stops here at two factors."
        ),
        "winner_ew": "hml",
        "winner_vw": None,
       "factors_ew": {
            "hml":  {"si_ew": -0.040},
            "mom":  {"si_ew":  0.076},
            "skew": {"si_ew": -0.015},
            "psl":  {"si_ew":  0.016},
            "roe":  {"si_ew":  0.074},
            "ia":   {"si_ew":  0.008},
            "qmj":  {"si_ew":  0.061},
            "bab":  {"si_ew": -0.014},
            "gp":   {"si_ew":  0.020},
            "cma":  {"si_ew": -0.009},
            "rmw":  {"si_ew": -0.016},
            "civ":  {"si_ew":  0.003},
        },
        "factors_vw": {
            "smb":  {"si_vw":  0.076},
            "hml":  {"si_vw": -0.016},
            "mom":  {"si_vw":  0.125},
            "skew": {"si_vw": -0.020},
            "psl":  {"si_vw":  0.034},
            "roe":  {"si_vw":  0.038},
            "ia":   {"si_vw":  0.078},
            "bab":  {"si_vw": -0.026},
            "gp":   {"si_vw": -0.022},
            "cma":  {"si_vw":  0.019},
            "rmw":  {"si_vw":  0.053},
            "civ":  {"si_vw": -0.017},
        },
        "thresh_ew": -0.025, "p_ew": 0.011,
        "thresh_vw": -0.024, "p_vw": 0.113,
        "multi_thresh_ew": -0.027, "multi_p_ew": 0.018,
        "multi_thresh_vw": -0.069, "multi_p_vw": 0.637,
    },
    "round4": {
        "label": "Round 4",
        "baseline_ew": "MKT + SMB + HML",
        "baseline_vw": None,
        "narrative_ew": (
            "EW baseline is now the full Fama-French 3-factor model. Every remaining "
            "candidate fails the threshold. The EW model is complete."
        ),
        "narrative_vw": None,
        "winner_ew": None,
        "winner_vw": None,
        "factors_ew": {
            "mom":  {"si_ew":  0.046},
            "skew": {"si_ew": -0.001},
            "psl":  {"si_ew":  0.007},
            "roe":  {"si_ew":  0.080},
            "ia":   {"si_ew":  0.051},
            "qmj":  {"si_ew":  0.137},
            "bab":  {"si_ew":  0.040},
            "gp":   {"si_ew":  0.055},
            "cma":  {"si_ew":  0.023},
            "rmw":  {"si_ew":  0.043},
            "civ":  {"si_ew":  0.016},
        },
        "thresh_ew": -0.017, "p_ew": 0.932,
        "multi_thresh_ew": -0.017, "multi_p_ew": 0.932,
    },
}

ROUND_KEYS = ["round1", "round2", "round3", "round4"]

FINAL_MODELS = {
    "ew": "MKT + SMB + HML",
    "vw": "MKT + QMJ",
    "ew_label": "Fama-French 3-Factor",
    "vw_label": "Market + Quality",
}
