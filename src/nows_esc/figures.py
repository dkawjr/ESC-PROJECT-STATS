"""Figure generators for primary outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from .scales import attitude_items_rev, comfort_items, knowledge_items


def _save_all(fig: plt.Figure, stem: Path) -> None:
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def fig1_knowledge(df: pd.DataFrame, out_dir: Path) -> None:
    """Grouped bar of pre/post percent correct by knowledge item."""
    sns.set_theme(style="whitegrid", palette=sns.color_palette("colorblind"))
    pre_cols, post_cols = knowledge_items()
    rows: list[dict[str, float | str]] = []
    for p, q in zip(pre_cols, post_cols):
        rows.append({"item": p.split(": ")[-1], "time": "Pre", "pct_correct": 100 * pd.to_numeric(df[p], errors="coerce").mean()})
        rows.append({"item": p.split(": ")[-1], "time": "Post", "pct_correct": 100 * pd.to_numeric(df[q], errors="coerce").mean()})
    plot_df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=plot_df, x="item", y="pct_correct", hue="time", ax=ax)
    ax.set_ylabel("Percent correct")
    ax.set_xlabel("Knowledge item")
    ax.set_ylim(0, 100)
    _save_all(fig, out_dir / "fig1_knowledge_items")


def fig2_comfort(df: pd.DataFrame, out_dir: Path) -> None:
    """Paired dotplot for comfort items."""
    pre_cols, post_cols = comfort_items()
    rows: list[dict[str, float | str]] = []
    for p, q in zip(pre_cols, post_cols):
        rows.extend(
            [
                {"item": p.split(": ")[-1], "time": "Pre", "score": float(v)}
                for v in pd.to_numeric(df[p], errors="coerce").dropna().tolist()
            ]
        )
        rows.extend(
            [
                {"item": p.split(": ")[-1], "time": "Post", "score": float(v)}
                for v in pd.to_numeric(df[q], errors="coerce").dropna().tolist()
            ]
        )
    plot_df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.stripplot(data=plot_df, x="item", y="score", hue="time", dodge=True, alpha=0.7, ax=ax)
    ax.set_ylim(0.8, 5.2)
    ax.set_ylabel("Likert score")
    _save_all(fig, out_dir / "fig2_comfort_items")


def fig3_attitude(df: pd.DataFrame, out_dir: Path) -> None:
    """Paired dotplot for reverse-scored attitude items."""
    pre_cols, post_cols = attitude_items_rev()
    rows: list[dict[str, float | str]] = []
    for p, q in zip(pre_cols, post_cols):
        rows.extend(
            [{"item": p.split(": ")[-1].replace("__rev", ""), "time": "Pre", "score": float(v)} for v in pd.to_numeric(df[p], errors="coerce").dropna().tolist()]
        )
        rows.extend(
            [{"item": p.split(": ")[-1].replace("__rev", ""), "time": "Post", "score": float(v)} for v in pd.to_numeric(df[q], errors="coerce").dropna().tolist()]
        )
    plot_df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.violinplot(data=plot_df, x="item", y="score", hue="time", split=True, inner="quart", ax=ax)
    ax.set_ylim(0.8, 5.2)
    ax.set_ylabel("Reverse-scored attitude Likert")
    _save_all(fig, out_dir / "fig3_attitude_items")


def fig4_domains(df: pd.DataFrame, out_dir: Path) -> None:
    """Domain-level paired score panel."""
    domains = [
        ("knowledge_pre_total", "knowledge_post_total", "Knowledge"),
        ("comfort_pre_total", "comfort_post_total", "Comfort"),
        ("attitude_pre_total", "attitude_post_total", "Attitude"),
    ]
    rows: list[dict[str, float | str | int]] = []
    for pre, post, label in domains:
        for idx, val in enumerate(pd.to_numeric(df[pre], errors="coerce").tolist()):
            rows.append({"participant": idx, "domain": label, "time": "Pre", "score": float(val)})
        for idx, val in enumerate(pd.to_numeric(df[post], errors="coerce").tolist()):
            rows.append({"participant": idx, "domain": label, "time": "Post", "score": float(val)})
    plot_df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.pointplot(data=plot_df, x="domain", y="score", hue="time", dodge=0.3, errorbar=None, ax=ax)
    sns.stripplot(data=plot_df, x="domain", y="score", hue="time", dodge=0.3, alpha=0.4, legend=False, ax=ax)
    ax.set_ylabel("Domain score")
    _save_all(fig, out_dir / "fig4_domain_scores")


def supp_fig_s1_symmetry(df: pd.DataFrame, out_dir: Path) -> None:
    """Histogram of paired differences as Wilcoxon symmetry diagnostic."""
    domains = [
        ("knowledge_post_total", "knowledge_pre_total", "Knowledge"),
        ("comfort_post_total", "comfort_pre_total", "Comfort"),
        ("attitude_post_total", "attitude_pre_total", "Attitude"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5), sharey=False)
    for ax, (post, pre, label) in zip(axes, domains):
        diff = pd.to_numeric(df[post], errors="coerce") - pd.to_numeric(df[pre], errors="coerce")
        ax.hist(diff.dropna(), bins=8, alpha=0.8)
        ax.axvline(0, color="black", linestyle="--", linewidth=1)
        ax.set_title(label)
        ax.set_xlabel("Post - Pre")
    axes[0].set_ylabel("Count")
    _save_all(fig, out_dir / "supp_fig_s1_difference_symmetry")
