import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config( page_title="Lab 3", layout="wide" )
sns.set_style( "darkgrid" )

#9
col_filters, col_output = st.columns( [1, 3] )

df = pd.read_csv( "C:/unic/2nd/ad/Data-Science/lab2/VHI/df.csv" )

DEFAULT_METRIC = "VCI"
DEFAULT_REGION = df[ "Region" ].unique( )[ 0 ]
DEFAULT_WEEK_RANGE = ( df[ "Week" ].min(), df[ "Week" ].max() ) 
DEFAULT_YEAR_RANGE = ( df[ "Year" ].min(), df[ "Year" ].max() )

with col_filters :
    st.header( "Фільтри" )

    #1
    if "selected_metric" not in st.session_state :
        st.session_state.selected_metric = DEFAULT_METRIC

    st.session_state.selected_metric = st.selectbox(
        "1. Оберіть часовий ряд (VCI, TCI, VHI):",
        options=["VCI", "TCI", "VHI"],
        index=["VCI", "TCI", "VHI"].index(st.session_state["selected_metric"])
    )

    #2
    if "selected_region" not in st.session_state :
        st.session_state.selected_region = DEFAULT_REGION

    st.session_state.selected_region = st.selectbox(
        "2. Оберіть область:",
        options=df["Region"].unique(),
        index=list(df["Region"].unique()).index(st.session_state["selected_region"])
    )

    #3
    if "week_range" not in st.session_state :
        st.session_state.week_range = DEFAULT_WEEK_RANGE

    st.session_state.week_range = st.slider(
        "3. Виберіть інтервал тижнів", 
        min_value=DEFAULT_WEEK_RANGE[0], 
        max_value=DEFAULT_WEEK_RANGE[1], 
        value=st.session_state.week_range
    )

    #4
    if "year_range" not in st.session_state :
        st.session_state.year_range = DEFAULT_YEAR_RANGE

    st.session_state.year_range = st.slider(
        "3. Виберіть інтервал років", 
        min_value=DEFAULT_YEAR_RANGE[0], 
        max_value=DEFAULT_YEAR_RANGE[1], 
        value=st.session_state.year_range
    )

    #8
    if "ascending_order" not in st.session_state :
        st.session_state.ascending_order = False

    if "downward_order" not in st.session_state :
        st.session_state.downward_order = False
    
    def ascending( ) :

        st.session_state.ascending_order = not st.session_state.ascending_order
        if st.session_state.downward_order :
            st.session_state.downward_order = False

    def downward( ) :

        st.session_state.downward_order = not st.session_state.downward_order
        if st.session_state.ascending_order :
            st.session_state.ascending_order = False

    ascending_order = st.checkbox(
        "⬆ Сортувати за зростанням",
        value=st.session_state.ascending_order,
        on_change=ascending
    )

    downward_order = st.checkbox(
        "⬇ Сортувати за спаданням",
        value=st.session_state.downward_order,
        on_change=downward
    )

    year_min, year_max = st.session_state.year_range
    week_min, week_max = st.session_state.week_range

    filtered_df = df[
        (df["Year"].between(year_min, year_max)) &
        (df["Week"].between(week_min, week_max))
    ]

    if st.session_state.ascending_order and not st.session_state.downward_order :
        filtered_df = filtered_df.sort_values( by=st.session_state.selected_metric, ascending=True )
    elif st.session_state.downward_order and not st.session_state.ascending_order :
        filtered_df = filtered_df.sort_values( by=st.session_state.selected_metric, ascending=False )

    region_data = filtered_df[ filtered_df["Region"] == st.session_state.selected_region ]

    #5
    if st.button( "Скинути всі фільтри" ) :
        st.session_state.selected_metric = DEFAULT_METRIC
        st.session_state.selected_region = DEFAULT_REGION
        st.session_state.week_range = DEFAULT_WEEK_RANGE
        st.session_state.year_range = DEFAULT_YEAR_RANGE
        st.session_state.ascending_order = False
        st.session_state.downward_order = False

with col_output :
    #6
    tab1, tab2, tab3 = st.tabs( ["Таблиця з відфільтрованими даними", "Графік порівнянь даних по роках", 
                                 "Графік порівнянь даних по областях"] )

    with tab1 :

        st.subheader( "Відфільтровані дані вибраного регіону" )
        st.dataframe( region_data )

    #7
    with tab2 :

        st.subheader( f"Часові ряди для регіону: {st.session_state.selected_region}" )

        plt.figure( figsize=(10, 5) )
        sns.lineplot( data=region_data, x="Week", y=st.session_state.selected_metric, hue="Year", marker="o" )
        plt.title( f"{st.session_state.selected_metric} протягом тижнів" )
        st.pyplot( plt )

    #7
    with tab3 :

        st.subheader( f"Порівняння даних області {st.session_state.selected_region} з іншими областями" )

        plt.figure( figsize=(10, 5) )
        sns.lineplot( data=filtered_df, x="Week", y=st.session_state.selected_metric, hue="Region", marker="o" )
        plt.title( f"Порівняння {st.session_state.selected_metric} обраної області з іншими областями" )

        st.pyplot( plt )
