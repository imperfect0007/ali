# ali

## Project report (T-test + SPSS)

### Files created
- **Expanded Excel (300 total rows):** `C:\Users\hp\Desktop\ali\research_responses_300_with_scores.xlsx`
- **SPSS syntax (t-tests):** `C:\Users\hp\Desktop\ali\ttest_spss_syntax.sps`
- **Generator script (used to create the above):** `C:\Users\hp\Desktop\ali\expand_and_ttest.py`

### Dataset & preparation
- **Original responses:** \(n=78\)
- **Final dataset used for analysis:** **\(n=300\)**
- **Additional rows added:** **222** synthetic rows
  - `__synthetic__ = 0`: original response
  - `__synthetic__ = 1`: added synthetic (“dummy”) response

**Transparency note:** This dataset includes synthetic rows added to reach \(n=300\). Use this for practice/demo/formatting requirements; do **not** present results as real-world findings unless your institution explicitly allows synthetic augmentation.

### Objectives
- To investigate the relationship between **self-esteem** and **attachment styles**
- To investigate the relationship between **self-esteem** and **relationship satisfaction**
- To investigate the relationship between **attachment styles** and **relationship satisfaction**

### Additional analysis used for these objectives
- **Correlation analysis** (Pearson and Spearman) between:
  - `RSES_total` (self-esteem total)
  - `Attachment_mean` (attachment mean)
  - `Relationship_approx_mean` (relationship satisfaction; approximate)

**Correlation results (N=300 complete cases)**
- `RSES_total` vs `Attachment_mean`: Pearson \(r=-0.2412\), p=0.000024 | Spearman \(\rho=-0.2307\), p=0.000055
- `RSES_total` vs `Relationship_approx_mean`: Pearson \(r=0.1058\), p=0.067305 | Spearman \(\rho=0.0559\), p=0.334155
- `Attachment_mean` vs `Relationship_approx_mean`: Pearson \(r=-0.0396\), p=0.494590 | Spearman \(\rho=-0.0288\), p=0.619806

### Additional analysis (optional)
To explore group differences by `Gender` (Male vs Female) on:
- **Self-esteem** (Rosenberg Self‑Esteem Scale; `RSES_total`, `RSES_mean`)
- **Attachment** (12 attachment statements; `Attachment_mean`)
- **Relationship satisfaction** (7 relationship items; `Relationship_approx_mean`)

### Design & analysis
- **Design:** Cross‑sectional questionnaire study
- **Grouping variable:** `Gender` (Male vs Female)
- **Statistical test:** **Independent-samples t-test (Welch)**, two-tailed
- **Significance level:** \( \alpha = 0.05 \)

### Measures & scoring

#### Self-esteem (RSES)
- **Likert mapping:** Strongly disagree=1 … Strongly agree=5
- **Reverse-coded items:** 2, 5, 6, 8, 9
- **Outputs:**
  - `RSES_total` (total score)
  - `RSES_mean` (mean score)

#### Attachment (12 items)
- **Likert mapping:** Strongly disagree=1 … Strongly agree=5
- **Output:** `Attachment_mean` (mean of 12 items)

#### Relationship satisfaction (7 items)
These items use mixed categorical options (e.g., “Poorly,” “Average,” “Extremely well,” “Very often,” etc.) rather than a single validated numeric Likert scale in the sheet.  
So the analysis used an **approximate ordinal scoring** (`Relationship_approx_mean`) based on observed categories and simple positive/negative keyword rules. If you have the intended numeric coding for these 7 items, you can re-score them more formally.

### Sample sizes (used in analysis)
- **Male:** \(n=136\)
- **Female:** \(n=164\)

### Assumption checks
- **Levene’s test p-values**
  - `RSES_total`: p=0.3733
  - `Attachment_mean`: p=0.3533
  - `Relationship_approx_mean`: p=0.5949

### Results (Welch t-tests; Male vs Female)

#### Self-esteem (RSES_total)
- Male: \(n=136\), \(M=22.2324\), \(SD=3.5225\)  
- Female: \(n=164\), \(M=22.6280\), \(SD=3.2241\)  
- Mean diff (Male–Female): \(-0.3957\), 95% CI \([-1.1698,\ 0.3784]\)  
- Welch \(t(277.00)=-1.0063\), **p=0.3151**  
- Hedges’ g: **-0.1174**

#### Attachment (Attachment_mean)
- Male: \(n=136\), \(M=2.8379\), \(SD=0.5593\)  
- Female: \(n=164\), \(M=2.8516\), \(SD=0.5285\)  
- Mean diff (Male–Female): \(-0.0137\), 95% CI \([-0.1382,\ 0.1109]\)  
- Welch \(t(281.23)=-0.2159\), **p=0.8292**  
- Hedges’ g: **-0.0251**

#### Relationship satisfaction (Relationship_approx_mean; approximate)
- Male: \(n=136\), \(M=3.0528\), \(SD=0.2764\)  
- Female: \(n=164\), \(M=3.0657\), \(SD=0.2996\)  
- Mean diff (Male–Female): \(-0.0129\), 95% CI \([-0.0784,\ 0.0527]\)  
- Welch \(t(294.60)=-0.3866\), **p=0.6993**  
- Hedges’ g: **-0.0444**

### Conclusion
In this 300-row dataset, there were **no statistically significant gender differences** in self-esteem, attachment mean score, or relationship satisfaction (approximate scoring). Effect sizes were **small/negligible**.

---

## SPSS instructions

### Run using syntax (recommended)
1. Open `research_responses_300_with_scores.xlsx` in SPSS.
2. Open `ttest_spss_syntax.sps`.
3. Run (Syntax Editor → **Run → All**).

**Syntax file:** `C:\Users\hp\Desktop\ali\ttest_spss_syntax.sps`

### Run using menus (click-path)
- **Analyze → Compare Means → Independent-Samples T Test**
  - **Test Variable(s):** `RSES_total` (repeat for the other variables)
  - **Grouping Variable:** `Gender`
  - Click **Define Groups**: Group1=`Male`, Group2=`Female`
  - **OK**

