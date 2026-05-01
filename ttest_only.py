import re

import numpy as np
import pandas as pd


# Input should already contain 300 rows (or any N) + scored columns.
INPUT_XLSX = r"C:\Users\hp\Desktop\ali\research_responses_300_with_scores.xlsx"

# Writes a small summary table (optional) and prints results to console.
OUTPUT_SUMMARY_XLSX = r"C:\Users\hp\Desktop\ali\ttest_summary.xlsx"


def _norm_text(x):
    if pd.isna(x):
        return None
    if isinstance(x, str):
        x = x.strip()
        return x if x != "" else None
    return x


def _colname_like(cols, needle_substrs):
    for c in cols:
        cl = str(c).lower()
        if any(n in cl for n in needle_substrs):
            return c
    return None


def _welch_ttest(x: np.ndarray, y: np.ndarray):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]

    nx, ny = len(x), len(y)
    mx, my = x.mean(), y.mean()
    vx, vy = x.var(ddof=1), y.var(ddof=1)
    t = (mx - my) / np.sqrt(vx / nx + vy / ny)
    dfw = (vx / nx + vy / ny) ** 2 / (
        (vx * vx) / (nx * nx * (nx - 1)) + (vy * vy) / (ny * ny * (ny - 1))
    )

    try:
        from scipy import stats

        p = 2 * stats.t.sf(abs(t), dfw)
    except Exception:
        p = float("nan")

    return dict(
        t=float(t),
        df=float(dfw),
        p=float(p),
        nx=int(nx),
        ny=int(ny),
        mx=float(mx),
        my=float(my),
        sx=float(np.sqrt(vx)),
        sy=float(np.sqrt(vy)),
    )


def _score_likert(series: pd.Series, mapping: dict[str, int], reverse: bool = False):
    def map_one(x):
        x = _norm_text(x)
        if x is None:
            return np.nan
        x_norm = re.sub(r"\s+", " ", str(x).strip().lower())
        if x_norm not in mapping:
            return np.nan
        v = mapping[x_norm]
        return (max(mapping.values()) + 1 - v) if reverse else v

    return series.map(map_one).astype(float)


def ensure_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure the key scored variables exist.
    If they already exist, they are left as-is.
    If missing, we attempt to compute them from the raw item columns.
    """
    cols = list(df.columns)

    likert_map = {
        "strongly disagree": 1,
        "slightly disagree": 2,
        "disagree": 2,
        "neutral": 3,
        "agree": 4,
        "strongly agree": 5,
    }

    # Self-esteem items (by keywords)
    if "RSES_total" not in df.columns or "RSES_mean" not in df.columns:
        se_items = [
            c
            for c in cols
            if re.match(r"^\s*\d+\.\s+", str(c))
            and any(
                k in str(c).lower()
                for k in [
                    "satisfied with myself",
                    "no good",
                    "good qualities",
                    "person of worth",
                    "failure",
                    "positive attitude",
                ]
            )
        ]
        seen = set()
        se_items = [x for x in se_items if not (x in seen or seen.add(x))]
        reverse_nums = {2, 5, 6, 8, 9}
        se_scores = []
        for c in se_items:
            m = re.match(r"^\s*(\d+)\.", str(c))
            num = int(m.group(1)) if m else None
            se_scores.append(_score_likert(df[c], likert_map, reverse=(num in reverse_nums)))
        if se_scores:
            if "RSES_total" not in df.columns:
                df["RSES_total"] = np.nanmean(np.vstack(se_scores), axis=0) * len(se_scores)
            if "RSES_mean" not in df.columns:
                df["RSES_mean"] = np.nanmean(np.vstack(se_scores), axis=0)

    # Attachment mean (by keywords)
    if "Attachment_mean" not in df.columns:
        attach_items = [
            c
            for c in cols
            if re.match(r"^\s*\d+\.\s+", str(c))
            and any(
                k in str(c).lower()
                for k in ["romantic partner", "abandon", "close", "reassurance", "available"]
            )
        ]
        seen = set()
        attach_items = [x for x in attach_items if not (x in seen or seen.add(x))]
        att_scores = [_score_likert(df[c], likert_map, reverse=False) for c in attach_items]
        if att_scores:
            df["Attachment_mean"] = np.nanmean(np.vstack(att_scores), axis=0)

    return df


def main():
    df = pd.read_excel(INPUT_XLSX, sheet_name="Form Responses 1")
    df = ensure_scores(df)

    cols = list(df.columns)
    gender_col = _colname_like(cols, ["gender"])
    if not gender_col:
        raise SystemExit("Could not find a Gender column.")

    g = df[gender_col].map(_norm_text)
    male_mask = g.astype(str).str.strip().str.lower().eq("male")
    female_mask = g.astype(str).str.strip().str.lower().eq("female")

    dvs = [c for c in ["RSES_total", "RSES_mean", "Attachment_mean", "Relationship_approx_mean"] if c in df.columns]
    if not dvs:
        raise SystemExit("No scored DV columns found (expected RSES_total / Attachment_mean / etc.).")

    out_rows = []
    print("Welch independent-samples t-tests (Male vs Female)")
    for dv in dvs:
        a = df.loc[male_mask, dv].astype(float)
        b = df.loc[female_mask, dv].astype(float)
        if a.notna().sum() < 2 or b.notna().sum() < 2:
            continue
        r = _welch_ttest(a.to_numpy(), b.to_numpy())
        print(
            f"- DV={dv}: Male(n={r['nx']}, mean={r['mx']:.4f}, sd={r['sx']:.4f}) "
            f"vs Female(n={r['ny']}, mean={r['my']:.4f}, sd={r['sy']:.4f}) | "
            f"Welch t({r['df']:.2f})={r['t']:.4f}, p={r['p']:.6f}"
        )
        out_rows.append(
            {
                "DV": dv,
                "Male_n": r["nx"],
                "Male_mean": r["mx"],
                "Male_sd": r["sx"],
                "Female_n": r["ny"],
                "Female_mean": r["my"],
                "Female_sd": r["sy"],
                "Welch_t": r["t"],
                "df": r["df"],
                "p": r["p"],
            }
        )

    if out_rows:
        pd.DataFrame(out_rows).to_excel(OUTPUT_SUMMARY_XLSX, index=False)
        print(f"\nWrote summary: {OUTPUT_SUMMARY_XLSX}")


if __name__ == "__main__":
    main()

