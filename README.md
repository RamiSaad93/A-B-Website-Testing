# Vanguard Website A/B Test Analysis

This project analyzes Vanguard's A/B test comparing the traditional online process (**Control**) with a redesigned interface (**Test**).

The analysis focuses on three main KPIs:

- Completion rate
- Time spent during the process
- Error rate from backwards navigation

## Datasets

The project uses:

- **Client profiles** – age, tenure, accounts, balances, calls, and logons
- **Digital footprints** – timestamped user interactions with each process step
- **Experiment roster** – Test and Control group assignments

Raw data is stored in `data/raw/`, and the analysis is available in:

`notebooks/vanguard_ab_test_analysis.ipynb`

## Key Findings

| Metric | Control | Test |
|---|---:|---:|
| Total visits | 32,182 | 37,121 |
| Completed visits | 16,040 | 21,724 |
| Completion rate | 49.84% | 58.52% |
| Error rate | 7.67% | 10.37% |

The Test version increased completion by **8.68 percentage points**, which represents a **17.42% relative uplift**.

The statistical tests show that:

- The Test version has a significantly higher completion rate than the Control version (`p < 0.001`).
- The relative uplift is significantly greater than Vanguard's required **5% threshold** (`RR = 1.174`, `p < 0.001`).
- The completed-visit time comparison also shows significantly lower recorded total time for the Test group (`p < 0.001`).

Overall, the redesigned interface improves completion and exceeds the required 5% relative uplift, although the Test group shows a higher backwards-navigation error rate.

## Run the Project

```bash
python -m pip install -r requirements.txt
cd notebooks
jupyter notebook vanguard_ab_test_analysis.ipynb
```

## Presentation

[Original Canva Presentation](https://www.canva.com/design/DAGELpGVvfY/f5u4ym93ZeYuBqXU086aAA/edit?utm_content=DAGELpGVvfY&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

