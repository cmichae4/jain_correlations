
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


@st.cache_data
def plot_fast(top_k, bottom_k):
    """Fast simple plot"""
    # Create labels and values
    all_data = pd.concat([top_k, bottom_k])
    labels = [f"{pair[0]}-{pair[1]}" for pair in all_data.index]
    values = all_data.values
    colors = ['red'] * len(top_k) + ['blue'] * len(bottom_k)

    # Simple plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(range(len(values)), values, color=colors, alpha=0.7)
    ax.set_yticks(range(len(values)))
    ax.set_yticklabels(labels)
    ax.axvline(0, color='black', alpha=0.3)

    st.pyplot(fig)


@st.cache_data
def plot_heatmap_smart(corr_df, top_k, bottom_k):
    """Smart heatmap - only unique stocks from top/bottom pairs"""
    # Get unique stocks (should be small number)
    all_stocks = set()
    for pair in list(top_k.index) + list(bottom_k.index):
        all_stocks.update(pair)

    all_stocks = list(all_stocks)

    # Only plot if reasonable size
    if len(all_stocks) > 50:
        st.write(f"Too many stocks ({len(all_stocks)}) for heatmap, showing bar plot instead")
        plot_fast(top_k, bottom_k)
        return

    # Create subset heatmap
    import seaborn as sns
    subset = corr_df.loc[all_stocks, all_stocks]

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(subset, cmap='RdBu_r', center=0, ax=ax, square=True)
    ax.set_title(f'Correlation Heatmap ({len(all_stocks)} stocks)')

    st.pyplot(fig)