# Vanguard Website A/B Test Analysis

Vanguard compared its traditional online process (**Control**) with a redesigned interface (**Test**) during the project period March 15–June 20, 2017. This analysis assesses visit-level completion, backwards navigation, and recorded elapsed time, and tests the assignment's minimum **5% relative completion uplift**.

Read the [executed analysis notebook](notebooks/vanguard_ab_test_analysis.ipynb) for data preparation, summary tables, statistical results, and interpretation. Useful outputs are saved for review directly on GitHub.

## Findings

| Metric | Control | Test |
|---|---:|---:|
| Visits in completion analysis | 32,182 | 37,121 |
| Completed visits | 16,040 | 21,724 |
| Visit-level completion rate | 49.8415% | 58.5221% |
| Backwards-step error rows / retained event rows | 7.6700% | 10.3727% |
| Mean recorded span for completing visit IDs (seconds) | 383.52 | 320.42 |

Completion improves by **8.6806 percentage points**, equivalent to **17.4164% relative uplift** (risk ratio **1.174164**). Under the specified unadjusted visit-level tests:

- The one-sided completion z-test gives z = 22.886499, p = 3.16633 × 10⁻¹¹⁶.
- The one-sided log-risk-ratio test against RR = 1.05 gives z = 15.748925, p = 3.49292 × 10⁻⁵⁶.

The redesign meets the assignment's completion-uplift criterion under these test assumptions, but backwards navigation is more frequent. The timing result describes recorded spans among completing visit IDs; it does not establish time to first confirmation or a causal speed improvement. Shared session IDs and repeated visits limit inference, as explained below. Actual costs and profitability are not measured.

## Data and structure

The four comma-separated raw text files represent three datasets:

| File under `data/raw/` | Description |
|---|---|
| `df_final_demo.txt` | Client demographics, accounts, balances, and recent calls/logons |
| `df_final_experiment_clients.txt` | Test/Control assignments, including unassigned clients |
| `df_final_web_data_pt_1.txt` | Timestamped process events, first part |
| `df_final_web_data_pt_2.txt` | Timestamped process events, second part |

There are 70,609 raw client profiles and 755,405 web-event rows across both parts. Before profile cleaning, the roster contains 26,968 Test and 23,532 Control clients. Raw files are preserved byte-for-byte. All cleaned and merged datasets remain in memory.

```text
A-B-Website-Testing/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── raw/
│       ├── df_final_demo.txt
│       ├── df_final_experiment_clients.txt
│       ├── df_final_web_data_pt_1.txt
│       └── df_final_web_data_pt_2.txt
└── notebooks/
    └── vanguard_ab_test_analysis.ipynb
```

## Methodology and KPI definitions

1. **Client cleaning:** preserve the original minimum-seven-present-fields rule, removing 14 incomplete profiles. Impute the one remaining missing age with the mean, retain integer truncation, map gender `X` to `U`, and use descriptive column names. Performance analysis includes retained clients with a Test/Control assignment.
2. **Event preparation:** concatenate both files, parse timestamps, sort by visit ID/time, and keep the first row in each run of consecutive identical steps. No additional global deduplication or outlier filtering is introduced.
3. **Completion:** one binary outcome per `(variation, visit_id)`. A visit succeeds if it contains at least one `confirm`. Divide completed visits by total visits, using the same table for the KPI and both completion tests.
4. **Errors:** preserve the sequence mapping and per-visit loop. A backwards move through `start → step_1 → step_2 → step_3 → confirm` flags the arriving row. Divide error rows by all retained event rows, including first rows. This is neither a per-transition nor a per-visit error rate.
5. **Timing:** preserve `current timestamp − previous timestamp` by visit ID, assigning zero to the first row. Per-step tables describe incoming elapsed intervals, not page dwell times. The secondary duration metric sums intervals for visit IDs containing confirmation; it can include post-confirmation activity.
6. **Population analysis:** distinguish all retained profiles from retained experiment clients, with demographic, account, and activity summaries.

## Statistical approach

Use α = 0.05 for two separate completion questions:

| Question | Null hypothesis | Alternative | Method |
|---|---|---|---|
| Is Test completion higher? | p_test ≤ p_control | p_test > p_control | One-sided two-proportion z-test |
| Does uplift exceed the business threshold? | RR ≤ 1.05 | RR > 1.05 | One-sided Wald test of log(RR) |

RR = p_test / p_control. The log-risk-ratio standard error is
`sqrt(1/test_successes - 1/test_total + 1/control_successes - 1/control_total)`.
The threshold is relative uplift, not five percentage points. See statsmodels' [proportion z-test](https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportions_ztest.html) and [independent-proportion comparison](https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.test_proportions_2indep.html) documentation.

The original secondary one-sided Welch test compares mean recorded spans for completing visit IDs (Control > Test). It is exploratory, conditional on completion, and not adjusted for multiple comparisons. Obsolete completion t-tests have been removed.

## Run the project

Use Python 3 with a virtual environment. The saved notebook was executed with Python 3.10, pandas 2.3.3, NumPy 2.2.6, SciPy 1.15.3, and statsmodels 0.15.0. Requirements are intentionally unpinned; these versions document the validation environment.

```bash
git clone https://github.com/RamiSaad93/A-B-Website-Testing.git
cd A-B-Website-Testing
git switch Cleanup-Brach
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies and launch Jupyter from the notebook directory:

```bash
python -m pip install -r requirements.txt
cd notebooks
jupyter notebook vanguard_ab_test_analysis.ipynb
```

Select the environment's Python kernel, choose **Restart Kernel and Run All Cells**, then save. Paths resolve from `notebooks/` to `../data/raw/`. After installation and cloning, execution requires no internet connection. Export examples at the end are commented out; no processed-data directory or CSV is generated.

## Validation and numerical reconciliation

The cleaned notebook executed in a fresh kernel with **28 sequential code cells**, no cell errors, and no warning outputs. All four raw-file Git blob hashes are unchanged after relocation.

- **Preserved results:** replaying the original pipeline reproduces backwards-step counts, every visit's total elapsed time, group/step timing means, completed-visit duration means, and the original completion z-test statistic and p-value. The cleaned notebook matches them.
- **Completion:** the old KPI counted 21,804 Test and 16,091 Control confirmation rows (58.7376% and 50.0000%). Removing 80 and 51 repeated confirmation rows gives 21,724 and 16,040 completed visits. These match the original proportion-test counts; total visits are unchanged.
- **Errors:** the hard-coded overall rate used 48,842 / 284,503 = 17.1675%, contradicting its own loop output. The preserved loop yields 26,082 error rows and 258,421 non-error rows: **9.1676% overall**. The row denominator and group-specific error rates are preserved.
- **Timing:** no later alignment correction is present in the source notebook. Incoming intervals and recorded spans are preserved and accurately labelled; no unseen presentation correction is assumed.
- **Business threshold:** replace the absolute-difference test with the requested relative-risk test. Its result was independently verified against statsmodels' log-risk-ratio implementation.

## Limitations

- **235 retained visit IDs span multiple clients**, including **118 in both groups**. Original grouping is preserved for comparability; shared IDs can mix journeys. Completion uses `(variation, visit_id)`; legacy timing/error grouping uses `visit_id` across groups.
- Consequently, the legacy duration sample has 16,051 Control and 21,729 Test group/visit pairs: confirmation eligibility is inherited across shared IDs. These differ from completion-test success counts. The timing sample is never used for completion inference.
- Repeated visits per client and shared IDs violate the independent-visit assumption to an unknown extent. Tests are not client-cluster-adjusted; their p-values and threshold conclusions are conditional on the stated assumptions.
- **369 visit/timestamp pairs contain different steps**, making their actual order ambiguous. Consecutive-step compression, incomplete-profile exclusions, and unobserved final-page dwell time also affect interpretation.
- A client-aware session-definition sensitivity analysis and investigation of backwards navigation are needed before relying on the findings for deployment. No actual costs or revenue are measured.

## Presentation

[Original Canva presentation](https://www.canva.com/design/DAGELpGVvfY/f5u4ym93ZeYuBqXU086aAA/edit?utm_content=DAGELpGVvfY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton). It has not been edited or revalidated; use the executed notebook for the verified results reported here.

