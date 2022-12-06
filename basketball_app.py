import streamlit as st
import pandas as pd #for dataframes and webscraping
import base64 # for converting bytecode to downloadable csv
import matplotlib.pyplot as plt # these 3 libs are for the heatmap
import seaborn as sb
import numpy as np

st.title('NBA Player Stats')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header("User Input Features")
year =  st.sidebar.selectbox('Year', list(reversed(range(1950,2022))))

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == "Age"].index)
    raw = raw.fillna(0)
    stats = raw.drop(['Rk'], axis = 1)
    return stats
stat = load_data(year)

sorted_team = sorted(stat.Tm.unique())
team = st.sidebar.multiselect('team', sorted_team, sorted_team)

unique_pos = ['C','PF','SF','PG','SG']
position = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = stat[(stat.Tm.isin(team)) & (stat.Pos.isin(position))] #filter

st.header('Dataframe of selected teams(s) and position(s)')
st.write('Dimensions: ' + str(df_selected_team.shape[0]) + ' rows, '+ str(df_selected_team.shape[1]) + ' columns')
test = df_selected_team.astype(str)
st.dataframe(test)

def fileDownload(df):
    csv = df.to_csv(index = False)
    base = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{base}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(fileDownload(df_selected_team), unsafe_allow_html=True)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False) # we passed the output csv to a variable then repassed it to read_csv to work
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sb.axes_style("dark"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sb.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(ax.figure)

