import streamlit as st

import src.cached_data_loader

st.header("Welcome to Correlation Calculator")
st.markdown("""
    This is an application for extracting historical price data for a universe of stocks, 
    and calculating trailing-window return correlations. 
    
    You will find two pages you can navigate to using the sidebar. They each serve different
    perspectives into exploring the calculated correlations.
    
    - ### Aggregate Window Correlations:\n
        This page's main index is the **target date** - representing the end of the lookback window.
        Once you select a date, we surface\n
        a) the top 10 positive and top 10 negative correlations amongst the universe\n
        b) a heatmap of all stocks included in the most (inversely or not) correlated stocks.\n
        Additionally, by selecting a **ticker** from the dropdown, you are able to see information for the same
        window on a more granular level - mainly:\n
        a) The top 10 positive and top 10 negative correlations **to that specific ticker** over the window.
    
    - ### Two Stock Correlations:\n
        This page serves a different purpose in allowing you to explore two tickers' correlation throughout
        the full history of available price data.
        
""")
st.markdown("Please pick a page from the side bar to navigate to calculations")


# _ = src.cached_data_loader.get_pivot_table()

if 'preload_triggered' not in st.session_state:
    _ = src.cached_data_loader.get_pivot_table()
    st.session_state['preload_triggered'] = True