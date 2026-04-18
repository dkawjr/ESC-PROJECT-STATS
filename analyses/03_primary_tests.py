"""Step 3: primary paired tests."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

import pandas as pd

from nows_esc.scales import attitude_items_rev, comfort_items, knowledge_items
from nows_esc.stats.effect_sizes import rank_biserial_from_diff
from nows_esc.stats.hodges_lehmann import hodges_lehmann, walsh_ci
from nows_esc.stats.mcnemar import mcnemar_exact, mcnemar_or_and_ci
from nows_esc.stats.wilcoxon import wilcoxon_signed_rank
from nows_esc.tables import export_table


def _discordant(pre: pd.Series, post: pd.Series) -> tuple[int, int]:
    b = int(((pre == 1) & (post == 0)).sum())
    c = int(((pre == 0) & (post == 1)).sum())
    return b, c


def main() -> None:
    root = ROOT
    df = pd.read_csv(root / "data" / "interim" / "cleaned_wide.csv")
    rows: list[dict[str, float | str | int]] = []

    k_pre, k_post = knowledge_items()
    for pre_col, post_col in zip(k_pre, k_post):
        pre = pd.to_numeric(df[pre_col], errors="coerce")
        post = pd.to_numeric(df[post_col], errors="coerce")
        b, c = _discordant(pre, post)
        p = mcnemar_exact(b, c)
        or_ci = mcnemar_or_and_ci(b, c)
        rows.append(
            {
                "family": "knowledge_items",
                "outcome": pre_col.replace("Pre Simulation ", ""),
                "test": "Exact McNemar",
                "statistic": min(b, c),
                "p_exact": p["exact_p"],
                "p_mid": p["mid_p"],
                "effect_size": or_ci["or"],
                "effect_ci_low": or_ci["or_ci_low"],
                "effect_ci_high": or_ci["or_ci_high"],
                "n": int((pre.notna() & post.notna()).sum()),
            }
        )

    for fam, pairs, zero_method in [
        ("comfort_items", zip(*comfort_items()), "pratt"),
        ("attitude_items", zip(*attitude_items_rev()), "wilcox"),
    ]:
        for pre_col, post_col in pairs:
            pre = pd.to_numeric(df[pre_col], errors="coerce")
            post = pd.to_numeric(df[post_col], errors="coerce")
            w = wilcoxon_signed_rank(pre.values, post.values, zero_method=zero_method, method="auto")
            diff = post.values - pre.values
            hl = hodges_lehmann(diff)
            lo, hi = walsh_ci(diff)
            rows.append(
                {
                    "family": fam,
                    "outcome": pre_col.replace("__rev", ""),
                    "test": f"Wilcoxon ({zero_method})",
                    "statistic": w["statistic"],
                    "p_exact": w["p_value"],
                    "p_mid": w["p_value"],
                    "effect_size": rank_biserial_from_diff(diff),
                    "effect_ci_low": lo,
                    "effect_ci_high": hi,
                    "hl_delta": hl,
                    "n": w["n"],
                }
            )

    for pre_col, post_col, label in [
        ("knowledge_pre_total", "knowledge_post_total", "knowledge_total"),
        ("comfort_pre_total", "comfort_post_total", "comfort_domain"),
        ("attitude_pre_total", "attitude_post_total", "attitude_domain"),
    ]:
        pre = pd.to_numeric(df[pre_col], errors="coerce")
        post = pd.to_numeric(df[post_col], errors="coerce")
        w = wilcoxon_signed_rank(pre.values, post.values, zero_method="wilcox", method="auto")
        diff = post.values - pre.values
        hl = hodges_lehmann(diff)
        lo, hi = walsh_ci(diff)
        rows.append(
            {
                "family": "domain_primary",
                "outcome": label,
                "test": "Wilcoxon exact/auto",
                "statistic": w["statistic"],
                "p_exact": w["p_value"],
                "p_mid": w["p_value"],
                "effect_size": rank_biserial_from_diff(diff),
                "effect_ci_low": lo,
                "effect_ci_high": hi,
                "hl_delta": hl,
                "n": w["n"],
            }
        )

    out = pd.DataFrame(rows)
    export_table(out, root / "results" / "tables" / "table2_primary_outcomes")
    out.to_csv(root / "results" / "tables" / "primary_outcomes_raw.csv", index=False)
    print("primary tests complete")


if __name__ == "__main__":
    main()
