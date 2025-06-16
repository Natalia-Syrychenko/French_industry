import streamlit as st

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# import geopandas as gpd
import matplotlib.patches as mpatches # Still needed for other potential legend elements, but not for this specific change
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import seaborn as sns
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import spearmanr
from scipy.stats import pearsonr
#import gdown

st.set_page_config(layout="wide")

@st.cache_data
def load_all_static_data():
    eu_lo_gap = pd.read_csv('datasets/eurogap.csv')
    eu_lo_gap2014 = pd.read_csv('datasets/eurogap14.csv')
    co = pd.read_csv('datasets/base_etablissement_par_tranche_effectif.csv')
    sa = pd.read_csv('datasets/sa_cleaned.csv')
    seco = pd.read_csv('datasets/companies_by_sector.csv')
    co_sa_lo_po_no_city = pd.read_csv('datasets/merge_one_to_four.csv')
    agekpi = pd.read_csv('datasets/AGEKPI.csv')
    busikpi = pd.read_csv('datasets/BUSIPKPI.csv')
    sakpi = pd.read_csv('datasets/SALARIESKPI.csv')
    new_po_lo_co_sa_unique = pd.read_csv('datasets/new_po_lo_co_sa_unique.csv')
    seco_gap = pd.read_csv('datasets/seco_gap.csv')
    G = pd.read_csv('datasets/G.csv')
    return eu_lo_gap, eu_lo_gap2014, co, sa, seco, co_sa_lo_po_no_city, agekpi, busikpi, sakpi, new_po_lo_co_sa_unique, G, seco_gap 
eu_lo_gap, eu_lo_gap2014, co, sa, seco, co_sa_lo_po_no_city, agekpi, busikpi, sakpi, new_po_lo_co_sa_unique, G, seco_gap  = load_all_static_data()
#@st.cache_data
#def load_data():
    # First file (population data)
    #file1_id = '..........'
    #url1 = f'https://drive.google.com/uc?id={file1_id}'
    #output1 = 'population.csv'
    #if not os.path.exists(output1):
        #gdown.download(url1, output1, quiet=False)
    #po = pd.read_csv(output1)

        # Second file (geographic information)
    #file2_id = '.....'
    #url2 = f'https://drive.google.com/uc?id={file2_id}'
    #output2 = 'name_geographic_information.csv'

    #if not os.path.exists(output2):
        #gdown.download(url2, output2, quiet=False)
    #lo = pd.read_csv(output2)


#---Data Cleaning---
    # --- Population File Data Cleaning and Renaming ---
    #po = po.drop('NIVGEO', axis=1) # Drop the 'NIVGEO' column

    # Rename columns for 'lo' DataFrame
    #lo = lo.rename(columns={
        #"code_insee": "city_id",
        #"nom_commune": "city_name",
        #"code_région": "region_no",
        #"nom_région": "region_name",
        #"numéro_département": "dep_no",
        #"nom_département": "dep_name",
        #"préfecture": "prefecture",
        #"EU_circo": "eu_election_circle_fr",
        #"chef.lieu_région": "region_capital",
        #"numéro_circonscription": "electoral_district_no",
        #"codes_postaux": "postal_code",
        #"latitude": "latitude",
        #"longitude": "longitude",
        #"éloignement": "distance_index"
    #})

    # Convert columns to appropriate types for 'lo'
    #lo['dep_no'] = pd.to_numeric(lo['dep_no'], errors='coerce').astype('Int64')
    #lo['postal_code'] = pd.to_numeric(lo['postal_code'], errors='coerce').astype('Int64')
    #lo['longitude'] = pd.to_numeric(lo['longitude'], errors='coerce')
    #lo['latitude'] = pd.to_numeric(lo['latitude'], errors='coerce')

    # Rename columns for 'po' DataFrame
    #po = po.rename(columns={
        #"CODGEO": "city_id",
        #"LIBGEO": "city_name",
        #"REG": "region_no",
        #"DEP": "dep_no",
        #"MOCO": "cohab_mode",
        #"AGEQ80_17": "age_group",
        #"SEXE": "sex",
        #"NB": "people_no"
    #})

    # Replace numeric codes in 'cohab_mode'
    #cohab_explanation = {
        #11: "child_2_parents",
        #12: "child_1_parent",
        #21: "adult_couple_no_kids",
        #22: "adult_couple_kids",
        #23: "adult_alone_kids",
        #31: "nonfamily_household",
        #32: "living_alone"
    #}
    #po["cohab_mode"] = po["cohab_mode"].replace(cohab_explanation)

    # Change 'age_group' column type and replace numbers with ranges
    #po["age_group"] = po["age_group"].astype(object)
    #po["age_group"] = po["age_group"].replace({
        #0: "0-4", 5: "5-9", 10: "10-14", 15: "15-19", 20: "20-24",
        #25: "25-29", 30: "30-34", 35: "35-39", 40: "40-44", 45: "45-49",
        #50: "50-54", 55: "55-59", 60: "60-64", 65: "65-69", 70: "70-74",
        #75: "75-79", 80: "80-84"
    #})
    # Replace 1 for men and 2 for women in 'sex'
    #po["sex"] = po["sex"].replace({1: "men", 2: "women"})

    #return po, lo

# Load data only once
#po, lo = load_data()
#st.session_state['po'] = po
#st.session_state['lo'] = lo'''


#Cleaning co
#reducing company size categories

co['micro'] = co['E14TS1'] + co['E14TS6']
co['small'] = co['E14TS10'] + co['E14TS20']
co['mid'] = co['E14TS50'] + co['E14TS100']
co['large'] = co['E14TS200'] + co['E14TS500']

#deleting redundant columns
co = co.drop(['E14TS1', 'E14TS6', 'E14TS10', 'E14TS20', 'E14TS50', 'E14TS100', 'E14TS200', 'E14TS500'], axis = 1)

#renaming the rest of the cells
co = co.rename(columns={
    "CODGEO": "city_id",
    "LIBGEO": "city_name",
    "REG": "region_no",
    "DEP": "dep_no",

    # Company size info
    "E14TST": "total_co",
    "E14TS0ND": "na_size_co",
    })

size_labels = ["Micro: 1-9", "Small: 10-49", "Mid: 50-199", "Large: 200+"]

    # --- Salary File Data Cleaning and Renaming ---

# --- Custom CSS for larger font ---
st.markdown("""
<style>
.big-font {
    font-size:20px !important;
}
</style>
""", unsafe_allow_html=True)




# --- Streamlit UI ---
st.title("French Industry - A Structural and Socioeconomic Study")
st.sidebar.title("Table of Contents")
pages = ["Introduction & Objectives", "Datasets & Cleaning", "Demographics", "Regional Economic Impact", "Gender Pay Gap", 
         "Further Investigation Areas", "Conclusion" ]
page = st.sidebar.radio("Go to", pages)
st.sidebar.write("### 🇫🇷 Project Members")
st.sidebar.write("""- Angelika Tabak\n- Mir Geiassudin Seifie\n- Natalia Syrychenko\n- Daneyssa Aguilera Medina\n\n Mentor: Christophe Feith
                """)

if page == "Introduction & Objectives":
    st.title("« Bonjour! »")
    st.image("pictures/french_bar_charts.gif")
    st.markdown("""
    Contemporary labor markets are being shaped by ongoing demographic changes, shortages of skilled workers, and the resulting 
    long-term challenges for pension systems. In this context, it is increasingly important to analyze both structural and socio-economic 
    inequalities at the national level - particularly in countries like France, which stands as the second-largest contributor to the European 
    Union’s Gross Domestic Product [(GDP)](https://european-union.europa.eu/principles-countries-history/facts-and-figures-european-union_en). 
    In 2022, the **Île-de-France region** was the [single largest regional contributor to GDP in the EU](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Economy_at_regional_level) :chart:, 
    significantly outpacing other regions across the Union.
    
    Economic growth and social prosperity can only be sustained if we ensure **equal pay** :scales: and equal opportunities for women in the workplace, especially given that women begin to outnumber men in France 
    already in their twenties. This is not only a matter of fairness, but also one of economic urgency: societies and their pension systems will increasingly depend on fully integrating women’s potential into 
    the labor market.     

    The technology sector 👩🏿‍💻:male-technologist: deserves special focus in this context, as 
    [75% of new jobs between now and 2050 are expected to emerge in science and tech fields](https://lafrenchtech.gouv.fr/en/the-ecosystems-commitments/parity-pact/).                    
    
                
    :dart: Whether you're a data professional, a student in economics or STEM (Science, Technology, Engineering, and Mathematics), or simply curious about structural and socioeconomic trends — this study offers data-driven insights into pressing questions of equality and opportunity.
    And especially if you're an executive, manager, or HR professional in a position to shape organizational culture, we hope this work sparks ideas, reflection, and action.

                
    To introduce the chapters of our study, we’ve drawn inspiration from an adapted version of France’s national motto: 
    « Liberté, Égalité, Sororité, Fraternité » - Liberty, Equality, Sisterhood, Brotherhood.            
                
    """)
    st.image("pictures/FrenchMotto.png")
    st.markdown("""
    After a quick overview of our data setup, and cleaning steps, we dive into the visual and statistical chapters—the ones illustrated in the graphic above.

    If you're short on time, feel free to jump directly to the sections using the sidebar on the left :arrow_left:.

    """)
    st.header("About Our Team :busts_in_silhouette::busts_in_silhouette:")
    st.markdown("""
    Three of our four team members hold degrees in Business Administration, allowing us to frame our findings within broader economic theories such as economies of scale, contract theory, and market competition—especially in the Regional Economic Impact chapter.
    The Gender Pay Gap section is further enriched by the firsthand expertise of an independent HR and recruitment consultant with over a decade of experience across Europe, bringing practical insights into structural inequality and workplace dynamics.
    Real-life examples - from unconscious bias to evolving hiring practices - helped us translate abstract statistics into concrete human realities, while also highlighting positive trends in inclusion and equity, particularly in tech and STEM.

    """)
   
elif page == "Datasets & Cleaning":
    st.header(":open_file_folder: Datasets")

    

    st.markdown("""
    Our core analysis uses datasets from 2014, primarily provided by DataScientest, supplemented with sector and EU-level data for comparison. Despite efforts to obtain newer sources, especially from INSEE (the French National Institute of Statistics and Economic Studies), most comparable datasets were only available for 2014. This constrained our ability to analyze long-term trends but provided a strong foundation for cross-sectional insights.
    """)

    st.subheader(""":hourglass: Quick Information on our Datasets""")
    st.markdown("""
    ### Dataset Overview
    | Dataset                         | Year        | Description                                                             | Source         |
    |----------------------------------|-------------|-------------------------------------------------------------------------|----------------|
    | `population.csv`                | 2014        | 8,536,584 rows; Demographic city/commun population data , incl. age, gender, household types            | DataScientest  |
    | Salary file 'sa' `net_salary_per_town_categories.csv` | 2014    |5136 rows (1 per city/commune); Avg. net hourly salary by gender, job level and age group                          | DataScientest  |
    | Location file 'lo' `name_geographic_information.csv` | 2014      | Administrative and geographical data, several lines per city (also postal codes and cities electoral district numbers included)                                    | DataScientest  |
    | company file 'co' `base_etablissement_par_tranche_effectif.csv` | 2014 | 36,681 rows per city/commune; Companies by size in each city         | DataScientest, [INSEE](https://www.insee.fr/fr/statistiques/1893274#:~:text=Ces%20fichiers%20donnent%20la%20structure,selon%20la%20tranche%20d'effectifs%20salari%C3%A9s)  |
    | `companies_by_sector.csv` = 'seco'      | 2014        | 36,681 rows per city/commune; Number of companies by sector per city                                  | [INSEE](https://www.insee.fr/fr/statistiques/1893274#:~:text=Ces%20fichiers%20donnent%20la%20structure,selon%20la%20tranche%20d'effectifs%20salari%C3%A9s)          |
    | EU pay gap file 'eu_lo_gap' `Paygap_2014_2023Eurostat.csv`  | 2014–2023   | Gender pay gap trends by EU country |[Eurostat](https://ec.europa.eu/eurostat/databrowser/view/earn_gr_gpgr2/default/table?lang=en)  |

    """)

    st.markdown("""⚧️**A note on gender inclusivity:** This analysis uses gender data categorized as "female" and "male" based on the available dataset. We acknowledge that this binary classification does not capture the full spectrum of gender identities.""")

    st.subheader(""":broom: Cleaning""")
                
    st.markdown("""
    **Key adjustments** included:
    - We renamed French variable names and INSEE-coded variables to clear, descriptive, and easy-to-understand names. The most important variables for our merges were:
    - `CODGEO`, `code_insee` → `city_id`
    - `LIBGEO`, `nom_commune` → `city_name`

    - Merged sector categories into broader labels: technology, consumer, finance_re, etc.
    - Cleaning missing values and standardizing formats (e.g., adding leading zeros to city codes)
    - Deleting duplicates
    - Changing of dtypes
    - Dropping of unnecessary columns as well as rows 
    """)

    st.subheader(""":construction: Limitations""")

    st.markdown("""
    - The primary dataset is from 2014, making it 11 years old. Despite extensive searching, no newer equivalent dataset was found. To show trends, we included additional statistics illustrating how the gender pay gap changed from 2014 to 2023.
    - Two company-related datasets were used:
      One shows the number of companies by size within each city.
      The other shows the number of companies by sector.
      Neither dataset includes information on the number of employees per company.
    - The salary dataset provides average net hourly wages per city or commune, but does not report how many individual salaries were used to calculate the averages.
    - The population dataset includes total population, age structure, and household arrangements per locality. It does not include information on employment status (e.g. employed, unemployed, self-employed, retired).
    - To improve representativeness, we combined the population dataset with others to allow group-level analysis by city size. However, its large size increases loading times and computing requirements.
    - In some cases, assumptions were needed. For example, the higher executive pay gaps in male-dominated sectors may reflect the underrepresentation of women in high-paying leadership positions.
    - The “company” (co) and “company by sector” (seco) datasets include variables with unclear background:
      The variable ‘na_size_co’ refers to businesses of unknown or zero size, containing self-employed individuals or bankrupt companies.
      The variable ‘other’ includes unspecified industries.
      These were excluded from percentage-based analyses due to lack of detail.
    - The “salary” (sa), “company” (co), and “company by sector” (seco) datasets each include a different number of city entries. During merging, some cities were dropped, which affected visualizations and analyses. As the general proportions remained consistent, we continued the analysis with the available data.
    """)


elif page == "Demographics":
    st.title("""Demographic Landscape of France: An Overview""")
   
    st.markdown("""
    <p class="big-font">
    Welcome to our analysis of France's population. This section provides a concise 
    overview of key demographic trends, including how population is distributed across cities, 
    the age and sex breakdown, and the prevalent cohabitation styles that define French households. 
    These insights are crucial for understanding social structures, economic drivers, and future 
    planning within the country.
    </p>
    <br>
    """, unsafe_allow_html=True)


    # Retrieve data from session state
    #po = st.session_state['po']
    #lo = st.session_state['lo']

 # --- 1. Population Distribution Map (with smaller icon) ---
    st.markdown('<h3><span class="small-emoji">🌍</span> Population Distribution Across French Cities</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p class="big-font">This map illustrates the distribution of population across French cities and highlights the seven most populous urban centers.
    The size and color intensity of the points correspond to population size, showing that population is concentrated in certain areas.
    Our findings show that Paris has a significantly larger population than any other city, confirming its central role, while other major cities like Marseille,
    Lyon, and Toulouse also have substantial populations. Despite the concentration in Paris, France benefits from a robust transportation network centered around the capital.</p>
    """, unsafe_allow_html=True)

    #Deactivating code with large file and using image instead
    st.image('pictures/population.png', width=900)

   # Data preparation for the map
    #lo_cleaned = lo[
        #(lo['latitude'].notna()) & (lo['longitude'].notna()) &
        #(lo['latitude'] != 0) & (lo['longitude'] != 0)
    #].copy()
    #lo_cleaned['city_id'] = lo_cleaned['city_id'].astype(str)

    #po_cleaned = po.copy()
    #po_cleaned['city_id'] = po_cleaned['city_id'].astype(str)

    #merged_df = pd.merge(po_cleaned[['city_id', 'city_name', 'people_no']], lo_cleaned[['city_id', 'latitude', 'longitude']], on='city_id', how='inner')

    #city_population = merged_df.groupby(['city_name', 'latitude', 'longitude']).agg({'people_no': 'sum'}).reset_index()
    #city_population = city_population.rename(columns={'people_no': 'total_population'})

    #top_7_cities = city_population.sort_values(by='total_population', ascending=False).head(7)

    #geometry_all = gpd.points_from_xy(city_population['longitude'], city_population['latitude'])
    #all_cities_gdf = gpd.GeoDataFrame(city_population, geometry=geometry_all, crs="EPSG:4326")

    #geometry_top_7 = gpd.points_from_xy(top_7_cities['longitude'], top_7_cities['latitude'])
    #top_7_cities_gdf = gpd.GeoDataFrame(top_7_cities, geometry=geometry_top_7, crs="EPSG:4326")


    #france_map = gpd.read_file("https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip")
    #france_map = france_map[france_map['NAME'] == 'France']

    #min_lon, max_lon = -6, 10
    #min_lat, max_lat = 41, 52

    # Plotting
    # *** CHANGE HERE: Reduced figsize for the map ***
    #fig, ax = plt.subplots(1, 1, figsize=(7, 7)) # Was (10, 10)

    #france_map.plot(ax=ax, color='lightgrey', edgecolor='black')
    #ax.set_xlim(min_lon, max_lon)
    #ax.set_ylim(min_lat, max_lat)

    #norm = plt.Normalize(all_cities_gdf['total_population'].min(), all_cities_gdf['total_population'].max())
    #sm = plt.cm.ScalarMappable(cmap='viridis', norm=norm)
    #sm.set_array([])

    #scatter = ax.scatter(all_cities_gdf.geometry.x, all_cities_gdf.geometry.y,
                       #s=all_cities_gdf['total_population'] / 3000,
                       #c=all_cities_gdf['total_population'], cmap='viridis', alpha=0.6)

    #for x, y, city in zip(top_7_cities_gdf.geometry.x, top_7_cities_gdf.geometry.y, top_7_cities_gdf['city_name']):
        #ax.text(x, y, city, fontsize=9, ha='left', va='bottom', color='lime')

    #cbar = fig.colorbar(sm, ax=ax, orientation='vertical', label='Population Size')
    #cbar.set_label('Population Size', fontsize=10)
    #cbar.ax.tick_params(labelsize=8)

    #ax.set_title("Where is Population Distributed Across French Cities?", fontsize=12)
    #ax.set_xlabel("Longitude", fontsize=10)
    #ax.set_ylabel("Latitude", fontsize=10)
    #ax.tick_params(axis='x', labelsize=8)
    #ax.tick_params(axis='y', labelsize=8)

    #plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

    #st.pyplot(fig)

    st.markdown("---")

    # --- 2. Demographic Distribution by Age and Sex (with smaller icon) ---
    st.markdown('<h3><span class="small-emoji">📊</span> Demographic Distribution by Age and Sex</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p class="big-font">The chart illustrates the population distribution across different age groups and by sex (women and men) in France, 2014.
    From this chart we see that the 80-84 women’s age group was larger than the 70-74 age group due to higher birth rates in the early 1930s,
    improved healthcare and longevity, and lower birth rates during World War II (1940-1944). Migration had less impact on these older age groups.
    Men have lower longevity than women. WWII had a greater negative impact on the male population. Lifestyle and health factors contribute to higher male mortality.
    There are fewer men than women in the 80-84 age group. For the age group from 0-24, there is a balanced gender ratio in younger ages.
    The population is declining compared to older generations, which indicates a potential future workforce shrinkage. Gender dynamics are stable in younger ages.</p>
    """, unsafe_allow_html=True)

    #Deactivating code with large file and using image instead
    st.image('pictures/age_sex.png')

    # Define the desired order of age groups
    #age_order = [
        #'0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39',
        #'40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', # Fixed age_order: removed 70: '70-74', 75: '75-79', 80: '80-84' which were incorrect syntax
        #'75-79', '80-84'
    #]


    # Group and aggregate data
    #po_agg = po.groupby(['age_group', 'sex'], as_index=False)['people_no'].sum()

    # Ensure age_group is a categorical variable with the correct order
    #po_agg['age_group'] = pd.Categorical(po_agg['age_group'], categories=age_order, ordered=True)

    # Plotting
    # *** CHANGE HERE: Reduced figsize for the bar chart ***
    #fig, ax = plt.subplots(figsize=(9, 5)) # Was (12, 6)
    #sns.barplot(x='age_group', y='people_no', data=po_agg, hue="sex", palette={"men": "#2ca02c", "women": "#d62728"}, ax=ax)

    #ax.set_xlabel("Age Group", fontsize=12)
    #ax.set_ylabel("Total Population", fontsize=12)
    #ax.set_title("What is the Population Distribution by Age Group and Sex?", fontsize=14)
    #plt.xticks(rotation=45, fontsize=10)
    #plt.yticks(fontsize=10)
    #ax.legend(fontsize=10)
    #plt.tight_layout()

    #st.pyplot(fig)

    st.markdown("---")

    # --- 3. Spectrum of Cohabitation Styles (%) (with smaller icon) ---
    st.markdown('<h3><span class="small-emoji">🏠</span> Spectrum of Cohabitation Styles (%)</h3>', unsafe_allow_html=True)
    st.markdown("""
    <p class="big-font">The chart illustrates a significant portion of the population lives in family structures with children. Adult couples with kids make up 23.9% of households,
    children living with two parents make up 22.1%, children living with one parent make up 6.7%, and adults living alone with kids make up 4.3%. The prevalence of families
    with children has several implications. Economically, it drives demand for childcare and schools, shapes housing needs such as the demand for larger homes, influences workforce participation,
    especially for parents, and affects consumer spending, such as on children's goods. Socially, it influences family support policies, parental leave, and child welfare, affects educational outcomes
    and child development, and shapes social cohesion and community structures. Demographically, it influences fertility rates and population growth, determines the future workforce size and composition,
    and impacts the dependency ratio, which is the ratio of non-workers to workers. Politically, it shapes political debates on family-oriented policies and influences government
    spending on education, healthcare, and social services for families.</p>
    """, unsafe_allow_html=True)

    #Deactivating code with large file and using image instead
    st.image('pictures/pie_coliving.png')

    # Group by cohabitation type and sum people
    #cohab_counts = po.groupby("cohab_mode")["people_no"].sum()

    # Convert to percentages
    #cohab_percent = (cohab_counts / cohab_counts.sum()) * 100

    # Round and sort descending
    #cohab_percent = cohab_percent.round(2).sort_values(ascending=False)

    # Plotting
    # *** CHANGE HERE: Reduced figsize for the pie chart ***
    #fig, ax = plt.subplots(figsize=(6, 6)) # Was (8, 8)
    #ax.pie(cohab_percent, labels=cohab_percent.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 10})
    #ax.set_title("What is the Distribution of Cohabitation Types (%)?", fontsize=14)
    #ax.axis('equal')
    #plt.tight_layout()

    #st.pyplot(fig)'''

    st.markdown('<h3><span class="small-emoji">📊</span> Salary in Different Age Groups</h3>', unsafe_allow_html=True)


    st.markdown("""
    <p class="big-font">
    This boxplot shows hourly net salary distributions in France by age and gender.
    </p>
    """, unsafe_allow_html=True)

# Filter only age-related columns
    age_cols = [col for col in sa.columns if 'age' in col]

# Melt the data into long format
    age_data = sa[age_cols].melt(var_name='Category', value_name='Salary')

# Extract Gender
    age_data['Gender'] = age_data['Category'].apply(lambda x: 'Female' if 'fem' in x else 'Male')

# Map to readable Age Groups
    age_group_map = {
        'fem_age_18_25': '18 to 25 years',
        'fem_age_26_50': '26 to 50 years',
        'fem_age_50p': '50+ years',
        'male_age_18_25': '18 to 25 years',
        'male_age_26_50': '26 to 50 years',
        'male_age_50p': '50+ years'
    }
    age_data['Age_Group'] = age_data['Category'].map(age_group_map)

# Define neutral custom colors
    custom_palette = {'Female': '#FF885B', 'Male': '#15B392'}  

# Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Age_Group', y='Salary', hue='Gender', data=age_data, palette=custom_palette, ax=ax)
    ax.set_title("How Do Hourly Net Salaries Vary Across Age Groups and Genders?")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Salary (€)")
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown("""
    <p class="big-font">
    Median salaries rise with age, but while men continue to see salary growth, women’s median earnings plateau after age 26. This suggests limited advancement opportunities for women, likely influenced by family responsibilities, part-time work, and concentration in lower-paying sectors.
    Men consistently earn more than women in every age group, with the gap widening significantly after age 50. High outliers among older men suggest access to top-paying roles, a trend less evident for women.
    Reflecting findings from <a href="https://www.eurofound.europa.eu/en/resources/article/2014/france-effect-motherhood-employment-public-and-private-sectors?utm_source" target="_blank">national studies</a>, these patterns demonstrate how caregiving and societal expectations can hinder women’s career progression and financial outcomes over time.
    </p>
    """, unsafe_allow_html=True)

# Only render this block if the main page is selected
if page == "Regional Economic Impact":
    st.sidebar.markdown("### Subsections")
    section = st.sidebar.radio(
        "Jump to:", 
        ["Effect on Salary", "Regression Analysis", "Income vs. Longrun Costs"],
        key="regional_nav"
    )

    st.header("Regional Economic Impact")

    if section == "Effect on Salary":
        st.title("Effect on Salary Analysis")

        st.markdown("### Company Size Distribution by Region")

        busikpi = pd.read_csv("datasets/BUSIPKPI.csv").rename(columns={"na_size_co": "other_small_co"})
        company_sizes = [
            "other_small_co", "micro_5_co", "micro_9_co", "small_19_co", "small_49_co",
            "mid_99_co", "mid_199_co", "large_499_co", "large_500p_co"
        ]
        default_selection = "small_19_co"

        line_col, btn_col = st.columns([4, 1])

        with btn_col:
            st.markdown("#### Select Size")
            label_map = {size: size.replace("_", " ").title() for size in company_sizes}
            selected = st.radio(
                label="",
                options=company_sizes,
                index=company_sizes.index(default_selection),
                format_func=lambda x: label_map[x],
                horizontal=False
            )

        if selected in busikpi.columns:
            grouped = busikpi.groupby("eu_election_circle_fr")[selected].sum().reset_index()
            grouped["percentage"] = (grouped[selected] / grouped[selected].sum()) * 100
            median_val = grouped[selected].median()

            fig_line = make_subplots(
                rows=2, cols=1,
                subplot_titles=("Absolute Values", "Percentage Values"),
                shared_xaxes=True,
                vertical_spacing=0.15
            )

            fig_line.add_trace(
                go.Scatter(
                    x=grouped["eu_election_circle_fr"],
                    y=grouped[selected],
                    mode="lines+markers",
                    name="Absolute",
                    line=dict(color="#D2691E")
                ),
                row=1, col=1
            )
            fig_line.add_trace(
                go.Scatter(
                    x=grouped["eu_election_circle_fr"],
                    y=[median_val] * len(grouped),
                    mode="lines",
                    name="Median (Absolute)",
                    line=dict(color="red", dash="dot")
                ),
                row=1, col=1
            )
            fig_line.add_trace(
                go.Scatter(
                    x=grouped["eu_election_circle_fr"],
                    y=grouped["percentage"],
                    mode="lines+markers",
                    name="Percentage",
                    line=dict(color="#B8860B")
                ),
                row=2, col=1
            )

            fig_line.update_layout(
                height=400,
                margin=dict(t=40, b=20, l=40, r=10),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=0.99, xanchor="center", x=0.1)
            )
            fig_line.update_xaxes(tickangle=-45, title_text="Geographical Region", row=2, col=1)
            fig_line.update_yaxes(title_text="Count", row=1, col=1)
            fig_line.update_yaxes(title_text="Share (%)", row=2, col=1)

            with line_col:
                st.plotly_chart(fig_line, use_container_width=True)

        # === Salary Analysis ===
        salaries_df = pd.read_csv("datasets/SALARIESKPI.csv")
        age_df = new_po_lo_co_sa_unique.copy()
        scatter_df_source = new_po_lo_co_sa_unique.copy()

        positions = ["executive", "manager", "employee", "worker"]
        regions = salaries_df["eu_election_circle_fr"].dropna().unique().tolist()

        if "selected_region" not in st.session_state:
            st.session_state.selected_region = regions[0]
        if "selected_position" not in st.session_state:
            st.session_state.selected_position = positions[0]

        selected_region = st.session_state.selected_region
        selected_position = st.session_state.selected_position

        st.markdown("#### Select Region")
        selected_region = st.radio(
            label="",
            options=regions,
            index=regions.index(selected_region),
            horizontal=True
        )
        st.session_state.selected_region = selected_region

        fem_col = f"fem_{selected_position}_sa"
        male_col = f"male_{selected_position}_sa"

        df_filtered = salaries_df.dropna(subset=[fem_col, male_col])
        region_data = df_filtered[df_filtered["eu_election_circle_fr"] == selected_region]

        global_median_fem = df_filtered[fem_col].median()
        global_median_male = df_filtered[male_col].median()

        region_median_fem = region_data[fem_col].median()
        region_median_male = region_data[male_col].median()

        q1_fem = region_data[fem_col].quantile(0.25)
        q3_fem = region_data[fem_col].quantile(0.75)
        iqr_fem = q3_fem - q1_fem
        upper_fence_fem = q3_fem + 1.5 * iqr_fem

        q1_male = region_data[male_col].quantile(0.25)
        q3_male = region_data[male_col].quantile(0.75)
        iqr_male = q3_male - q1_male
        upper_fence_male = q3_male + 1.5 * iqr_male

        iqr = (iqr_fem + iqr_male) / 2
        diff_median_fem = region_median_fem - global_median_fem
        diff_median_male = region_median_male - global_median_male
        upper_fence_diff = upper_fence_fem - upper_fence_male

        def kpi_box(title, value, color="#ffe6cc"):
            return f"""
            <div style='background-color:{color};padding:8px 10px;border:2px solid black;
                        text-align:center; width:140px; height:80px; margin:6px;
                        border-radius:6px; font-family:sans-serif'>
                <div style='font-size:12px;font-weight:600'>{title}</div>
                <div style='font-size:18px;font-weight:900'>{value:.2f}  </div>
            </div>
            """

        left_col, right_col = st.columns([3, 1])

        with left_col:
            fig = make_subplots(
                rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.15,
                subplot_titles=(f"{selected_position.title()} Salary in {selected_region}", "Regional Salary Distribution")
            )

            for label, color, colname, offset in [("Female", "gold", fem_col, 0), ("Male", "red", male_col, 1)]:
                vals = region_data[colname]
                vals = vals[vals <= 37]
                fig.add_trace(go.Box(
                    y=vals, name=label, marker_color=color, boxpoints="outliers",
                    jitter=0.3, pointpos=-1.8, offsetgroup=offset, width=0.45, line=dict(width=2)),
                    row=1, col=1
                )

            fig.add_hline(y=global_median_fem, line_dash="dash", line_color="gold",
                        annotation_text="Global Median Female", annotation_position="top right", row=1, col=1)
            fig.add_hline(y=global_median_male, line_dash="dash", line_color="red",
                        annotation_text="Global Median Male", annotation_position="bottom right", row=1, col=1)

            for gender_label, color, colname in [("Female", "gold", fem_col), ("Male", "red", male_col)]:
                for i, region in enumerate(regions):
                    vals = salaries_df[salaries_df["eu_election_circle_fr"] == region][colname]
                    vals = vals[vals <= 37]
                    fig.add_trace(go.Box(
                        y=vals, x=[region]*len(vals), name=gender_label, marker_color=color,
                        boxpoints="outliers", offsetgroup=gender_label, width=0.5, line=dict(width=1.5),
                        legendgroup=gender_label, showlegend=(i == 0)),
                        row=2, col=1
                    )

            fig.update_layout(
                height=900,
                boxmode="group",
                margin=dict(t=50, b=50),
                legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=0.35)
            )

            st.plotly_chart(fig, use_container_width=True)

        with right_col:
            st.markdown("### K P I")

            kpis = [
                ("IQR Male (Boxplot)", iqr_male),
                ("Region - Global Median (F)", diff_median_fem),
                ("Region - Global Median (M)", diff_median_male),
                ("Upper Fence F - M", upper_fence_diff)
            ]

            kpi_cols = st.columns(2, gap="small")

            with kpi_cols[0]:
                for title, val in kpis:
                    st.markdown(kpi_box(title, val), unsafe_allow_html=True)

            with kpi_cols[1]:
                st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
                for pos in positions:
                    is_selected = (pos == selected_position)
                    btn_style = f"""
                    <style>
                        .btn-{pos} {{
                            background-color: {'#007acc' if is_selected else '#e6f0fa'};
                            color: {'white' if is_selected else 'black'};
                            border: 2px solid #007acc;
                            border-radius: 4px;
                            width: 120px;
                            height: 64px;
                            font-weight: 600;
                            font-family: sans-serif;
                            cursor: pointer;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            user-select: none;
                            margin: 8px 0;
                        }}
                        .btn-{pos}:hover {{
                            background-color: #005f99;
                            color: white;
                        }}
                    </style>
                    """
                    st.markdown(btn_style, unsafe_allow_html=True)
                    if st.button(pos.title(), key=f"btn_pos_{pos}"):
                        st.session_state.selected_position = pos
                        selected_position = pos

            age_cols = ["age_26_50", "age_50p"]
            age_data = age_df[age_df["eu_election_circle_fr"] == selected_region]
            combined_ages = age_df[age_cols].dropna().values.flatten()
            y_min, y_max = np.percentile(combined_ages, [1, 99])
            y_max = min(y_max, 40)

            fig_age = go.Figure()
            for col_name, color in zip(age_cols, ["#B8860B", "#FFA500"]):
                vals = age_data[col_name]
                vals = vals[vals <= 40]
                fig_age.add_trace(go.Box(
                    y=vals,
                    name=col_name.replace("_", " ").title(),
                    marker_color=color,
                    boxpoints="outliers",
                    width=0.3,
                    line=dict(width=1.3)
                ))
            fig_age.update_layout(
                height=250,
                margin=dict(l=10, r=10, t=10, b=10),
                yaxis=dict(range=[y_min, y_max]),
                showlegend=False
            )
            st.plotly_chart(fig_age, use_container_width=True)

            scatter_df = scatter_df_source.copy()
            scatter_df = scatter_df[scatter_df["eu_election_circle_fr"] == selected_region]

            x_col = f"male_{selected_position}_sa"
            y_col = f"fem_{selected_position}_sa"
            scatter_df = scatter_df[[x_col, y_col]].dropna()

            min_val, max_val = 0, 40
            if len(scatter_df) > 0:
                min_val = min(scatter_df[x_col].min(), scatter_df[y_col].min())
                max_val = max(scatter_df[x_col].max(), scatter_df[y_col].max())

            fig_scatter = go.Figure()
            fig_scatter.add_trace(go.Scatter(
                x=scatter_df[x_col],
                y=scatter_df[y_col],
                mode='markers',
                marker=dict(size=6, color="red", opacity=0.7)
            ))
            fig_scatter.add_shape(
                type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val,
                line=dict(color="gray", dash="dash")
            )
            fig_scatter.update_layout(
                height=250,
                margin=dict(t=10, b=10, l=10, r=10),
                xaxis=dict(title="M Salary ( )", range=[min_val, max_val]),
                yaxis=dict(title="F Salary ( )", range=[min_val, max_val]),
                showlegend=False
            )
            st.plotly_chart(fig_scatter, use_container_width=True)




    elif section == "Regression Analysis":
        st.title("Regression Analysis")
        df = new_po_lo_co_sa_unique.copy()

        salary_cols = [
            'fem_executive_sa', 'fem_manager_sa', 'fem_employee_sa', 'fem_worker_sa',
            'male_executive_sa', 'male_manager_sa', 'male_employee_sa', 'male_worker_sa'
        ]

        df_salary = df.melt(
            id_vars=['city_name'],
            value_vars=salary_cols,
            var_name='var',
            value_name='salary'
        )
        df_salary['gender'] = df_salary['var'].str.extract(r'^(fem|male)')
        df_salary['position'] = df_salary['var'].str.extract(r'_(executive|manager|employee|worker)')

        age_cols = [
            'fem_age_18_25', 'fem_age_26_50', 'fem_age_50p',
            'male_age_18_25', 'male_age_26_50', 'male_age_50p'
        ]

        df_age = df.melt(
            id_vars=['city_name'],
            value_vars=age_cols,
            var_name='age_var',
            value_name='age_dummy'
        )
        df_age['gender'] = df_age['age_var'].str.extract(r'^(fem|male)')
        df_age['age_class'] = df_age['age_var'].str.extract(r'(\d{2}_\d{2}|50p)')

        company_cols = [
            'micro_5_co', 'micro_9_co', 'small_19_co',
            'small_49_co', 'mid_99_co', 'mid_199_co', 'large_499_co', 'large_500p_co'
        ]

        df_company = df.melt(
            id_vars=['city_name'],
            value_vars=company_cols,
            var_name='company_size',
            value_name='company_dummy'
        )
        df_company['company_size'] = df_company['company_size'].str.replace('_co$', '', regex=True)

        df_merge = df_salary.merge(df_age, on=['city_name', 'gender'])
        df_merge = df_merge.merge(df_company, on='city_name')

        df_final = df_merge[
            (df_merge['age_dummy'] > 0) &
            (df_merge['company_dummy'] > 0)
        ].copy()

        model = smf.ols("salary ~ C(gender) + C(position) + C(age_class) + C(company_size)", data=df_final).fit()

        st.header("Regressions-Results")

        coefs = model.summary2().tables[1].reset_index()
        coefs.rename(columns={
            'index': 'Variable',
            'Coef.': 'Coeffizient',
            'Std.Err.': 'Standarderror',
            'P>|t|': 'p-value',
            '[0.025': 'CI 2.5%',
            '0.975]': 'CI 97.5%'
        }, inplace=True)

        st.dataframe(coefs.style.format({
            'Koeffizient': '{:.2f}',
            'Standarderror': '{:.2f}',
            'p-Wert': '{:.3f}',
            'CI 2.5%': '{:.2f}',
            'CI 97.5%': '{:.2f}'
        }))



    elif section == "Income vs. Longrun Costs":
        st.title("Income vs. Longrun Costs")
        required_base_cols = ["avg_city_sa", "avg_city_sa_mean_of_all", "eu_election_circle_fr"]
        for col in required_base_cols:
            if col not in G.columns:
                st.error(f"? Column '{col}' is missing.")
                st.stop()

        
        possible_columns = [
            "adult_alone_kids",
            "adult_couple_kids",
            "adult_couple_no_kids",
            "child_1_parent",
            "child_2_parents",
            "living_alone"
        ]

        for col in possible_columns:
            if col not in G.columns:
                st.error(f"? Column '{col}' is missing.")
                st.stop()

        # Globale Y-Achse berechnen
        y_min, y_max = float("inf"), float("-inf")
        for col in possible_columns:
            y1 = G[col] * G["avg_city_sa"]
            y2 = G[col] * G["avg_city_sa_mean_of_all"]
            diff = y1 - y2
            y_min = min(y_min, y1.min(), y2.min(), diff.min())
            y_max = max(y_max, y1.max(), y2.max(), diff.max())

        # Zwei-Spalten-Layout
        col1, col2 = st.columns([4, 1])

        selected_var = st.session_state.get("selected_var", possible_columns[0])

        # Berechnungen
        G["x_avg"] = G[selected_var] * G["avg_city_sa"]
        G["x_mean"] = G[selected_var] * G["avg_city_sa_mean_of_all"]
        G["diff"] = G["x_avg"] - G["x_mean"]
        G = G.sort_values(by="eu_election_circle_fr")

        with col1:
            # Plot erstellen
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=G["eu_election_circle_fr"],
                y=G["x_avg"],
                mode="lines+markers",
                name="Regional income / h",
                line=dict(color="blue")
            ))
            fig.add_trace(go.Scatter(
                x=G["eu_election_circle_fr"],
                y=G["x_mean"],
                mode="lines+markers",
                name="France average income (approx. future cost / h)",
                line=dict(color="red")
            ))
            fig.add_trace(go.Bar(
                x=G["eu_election_circle_fr"],
                y=G["diff"],
                name="Difference",
                marker_color="red",
                opacity=0.6
            ))

            fig.update_layout(
                xaxis_title="Geographical Region",
                xaxis_tickangle=-45,
                height=600,
                margin=dict(t=50, b=50),
                legend=dict(orientation="h", y=1.2, x=0.5, xanchor="center"),
                yaxis=dict(
                    title="Weighted Value ( )",
                    range=[y_min, y_max]
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # Radio Buttons horizontal
            selected_var = st.radio(
                label="",
                options=possible_columns,
                index=possible_columns.index(selected_var),
                horizontal=True,
                key="selected_var"
            )

        # KPI-Boxen rechts
        with col2:
            st.markdown("### Difference")
            st.markdown("""
                <style>
                    .kpi-box {
                        background-color: rgba(255, 200, 200, 0.2);
                        padding: 10px 14px;
                        border-radius: 0px;
                        border: 1px solid #ddd;
                        margin-bottom: 6px;
                        font-size: 13px;
                        font-family: Arial, sans-serif;
                    }
                    .kpi-label {
                        color: #555;
                    }
                    .kpi-value.positive {
                        color: #1f77b4;
                    }
                    .kpi-value.negative {
                        color: #d62728;
                    }
                </style>
            """, unsafe_allow_html=True)

            for region, value in zip(G["eu_election_circle_fr"], G["diff"]):
                euro_value = f"{value:,.2f}  ".replace(",", "X").replace(".", ",").replace("X", ".")
                value_class = "positive" if value >= 0 else "negative"
                st.markdown(f"""
                    <div class="kpi-box">
                        <div class="kpi-label">{region}</div>
                        <div class="kpi-value {value_class}">{euro_value}</div>
                    </div>
                """, unsafe_allow_html=True)



elif page == "Gender Pay Gap":

    st.header("Gender Pay Gap Studies and Influence of Business Sectors")
        
    tab1, tab2, tab3, tab4 = st.tabs(["🧮 About", "🇪🇺 vs. 🇫🇷", "🏔️ Leadership", "🏭 Sectors"])
    # --- Text block ---

    with tab1:
        st.subheader("""🧮 What is the Gender Pay Gap?""")

        st.markdown("""In this chapter, we examine the unadjusted gender pay gap (GPG), which is defined as the difference between the average gross hourly earnings of men and women, expressed as a 
                    percentage of men’s earnings. The term "unadjusted" means that this gap is calculated without taking into account factors such as job type, education, experience or working hours. 
                    At the European Union level, using Dataset 6, we calculate the GPG based on gross salaries. For the analysis specific to France (using Datasets 1 to 5), we use net hourly earnings 
                    instead. The formula applied is""") 
        
        st.latex(r"""
        \text{Pay Gap (\%)} = \left( \frac{\text{Male Salary} - \text{Female Salary}}{\text{Male Salary}} \right) \times 100
        """)
        
        st.markdown("""where positive values show a pay gap favoring men, and negative values indicate that women earn more. We call these negative values “negative pay gaps” rather than “reverse gaps” to avoid political sensitivity. 
                    More information on the Gender Pay Gap can be found on the [Eurostat page](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Gender_pay_gap_(GPG)).""")
        
        st.markdown("""The chapter ends by exploring how different business sectors and job roles influence the gender pay gap within France.""")
        
        #---New tab - Trend chart---

    with tab2:
        st.subheader("""How does the Gender Pay Gap in France 🇫🇷 compare to the other States of EU 🇪🇺(2014–2023)""")
        
        # Step 1: Add Region column
        eu_lo_gap['Region'] = eu_lo_gap['Country'].apply(lambda x: 'France' if x == 'France' else 'Rest of EU')

        # Step 2: Group by Year and Region
        eu_grouped = eu_lo_gap.groupby(['Year', 'Region'], as_index=False)['PayGap'].mean()

        # Step 3: Split into France and Rest of EU
        eu_france = eu_grouped[eu_grouped['Region'] == 'France']
        eu_rest = eu_grouped[eu_grouped['Region'] == 'Rest of EU']

        # Step 4: Create Plotly figure
        fig = go.Figure()

        # Trace for France
        fig.add_trace(go.Scatter(
        x=eu_france['Year'],
        y=eu_france['PayGap'],
        mode='lines+markers',
        name='France (🇫🇷)',
        line=dict(color='#E55050')
        ))

        # Trace for Rest of EU
        fig.add_trace(go.Scatter(
        x=eu_rest['Year'],
        y=eu_rest['PayGap'],
        mode='lines+markers',
        name='Rest of EU 🇪🇺',
        line=dict(color='#3A59D1')
        ))

        # Step 5: Layout
        fig.update_layout(
        yaxis_title='Pay Gap (%) between ♂ and ♀',
        xaxis_title='Year',
        showlegend=True
        )

        # Step 6: Display in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        
        st.markdown("""In 2014, France’s gender pay gap was about 2 percentage points higher than the 
                    average gap across the rest of the European Union. After 2018, this difference 
                    steadily decreased, narrowing to just 1 percentage point by 2023, showing that the 
                    gap between France and the EU average is closing. 
                    """)
        
        st.markdown("""To analyze this, the dataset was modified by adding a new column called "Region." 
                    This was done using a lambda function applied to the "Country" column, which labeled 
                    each row as "France" if the country was France, and "Rest of EU" otherwise. 
                    The data was then grouped by "Year" and "Region" to calculate the average pay gap 
                    for each group annually. Finally, a comparative line chart was created to visualize 
                    how the gender pay gap in France compares to the rest of the EU over time.""")
        

        # --- Bar Chart ---
        # Year selection
        st.subheader("""Which EU Countries Had the Highest 🔺 and Lowest 🔻 Gender Pay Gaps?""")
        selected_year = st.radio("Select Year", list(range(2014, 2024)), horizontal=True)

        # Filter dataset
        eu_lo_gap_year = eu_lo_gap[eu_lo_gap['Year'] == selected_year]

        if eu_lo_gap_year.empty:
            st.warning(f"No data available for year {selected_year}")
        else:
            # Identify max, min, and France rows
            max_row = eu_lo_gap_year[eu_lo_gap_year['PayGap'] == eu_lo_gap_year['PayGap'].max()].copy()
            min_row = eu_lo_gap_year[eu_lo_gap_year['PayGap'] == eu_lo_gap_year['PayGap'].min()].copy()
            france_row = eu_lo_gap_year[eu_lo_gap_year['Country'] == 'France'].copy()

            # Combine and drop duplicates
            display_df = pd.concat([max_row, min_row, france_row]).drop_duplicates()

            # Custom color map: red for France, blue for others
            display_df['CustomColor'] = display_df['Country'].apply(
                lambda x: '#E55050' if x == 'France' else '#3A59D1'
            )

            # Create signed text labels for positive and negative values
            display_df["PayGapLabel"] = display_df["PayGap"].map(lambda x: f"{x:+.1f}%")

            # Create Plotly bar chart
            fig = px.bar(
                display_df,
                x="PayGap",
                y="Country",
                orientation='h',
                color="Country",
                text="PayGapLabel",
                color_discrete_map={row['Country']: row['CustomColor'] for _, row in display_df.iterrows()}
            )

            # Show labels and grid
            fig.update_traces(
                texttemplate='%{text}',
                textposition='outside'
            )

            fig.update_layout(
                xaxis_title="Pay Gap (%)",
                yaxis_title="Country",
                xaxis=dict(showgrid=True),
                legend_title_text='Country',
                height=450,
                margin=dict(t=60, l=30, r=20, b=40)
            )

            # Display chart and description
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""These charts reveal a clear difference between the highest and lowest gender pay gaps 
                    within the European Union. While countries like Luxembourg consistently report low gaps and 
                    might seem like natural examples to follow, it's important to interpret these figures in 
                    context. Luxembourg is one of the EU’s smallest member states, with a highly international 
                    labor force and a [significant number of cross-border workers]("https://eures.europa.eu/living-and-working/labour-market-information-europe/labour-market-information-luxembourg_en"). 
                    A high percentage of employees work in large companies, where standardized pay structures may reduce gender-based wage 
                    differences. These structural characteristics mean that Luxembourg’s figures are certainly worth exploring — but not directly comparable without deeper analysis.""")
        
        st.markdown("""We used the max() and min() functions on the "PayGap" column to identify the countries with the highest
                    and lowest gaps. France’s data was added separately by filtering the "Country" column. The three rows were combined using 
                    pd.concat() and cleaned with drop_duplicates() to avoid duplicates in case of overlap.""")

        # --- Boxplot ---
        st.subheader("""📊How does France Pay Gap compare to EU Pay Gap Distribution?""")



        # Year selection
        selected_year = st.radio("Select Year", sorted(eu_lo_gap['Year'].unique()), horizontal=True,
                                key="year_radio_eu_boxplot")

        # Filter the data for the selected year
        eu_lo_gap_year = eu_lo_gap[eu_lo_gap['Year'] == selected_year]

        if eu_lo_gap_year.empty:
            st.warning(f"No data available for {selected_year}")
        else:
            # Create the box plot
            fig = px.box(
                eu_lo_gap_year,
                y='PayGap',
                color='Region',
                title=f"Distribution of Gender Pay Gaps in the EU ({selected_year})",
                color_discrete_map={
                    'France': '#E55050',
                    'Rest of EU': '#3A59D1'
                },
                points='all'  # Optional: show individual data points
            )

            # Update layout for styling
            fig.update_layout(
                yaxis_title='Pay Gap (%)',
                xaxis_title=None,
                showlegend=True,
                height=500
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("""Over time, the distribution of gender pay gaps across the EU has become more right-skewed. 
                    While a small number of countries continue to have high pay disparities, most now show lower 
                    gaps clustered together. This change, along with a falling median pay gap, suggests that many 
                    EU member states are making progress toward fairer pay. Despite this positive trend, some 
                    outliers and deeper structural issues still need to be addressed.""") 
        
        st.markdown("""In France, the median gender pay gap has notably decreased over the years. By 2023, France’s 
                    median gap matched that of the rest of the EU, reflecting an improvement in its relative 
                    position compared to earlier years.""")
        
        st.markdown("""We now turn back to the year 2014, the reference period for our Datasets 1 to 5. Although France 
                    has shown progress in reducing the gender pay gap in recent years, examining data from 2014 
                    allows us to identify patterns and challenges that may still persist today and require 
                    further attention.""")
        
        st.markdown("""Before moving forward, we conduct some preliminary work for the following chapters. 
                    Using the European gender pay gap data as a reference, we create categories to classify 
                    pay gaps as negative, low, medium, or high. This classification will be applied to French 
                    cities, providing a structured framework to analyze and interpret local variations in the 
                    gender pay gap more effectively.""")
        
        # --- Thresholds ---
        st.subheader("EU Pay Gap Categories (2014)")
        q1, q2, q3 = eu_lo_gap2014['PayGap'].quantile([0.25, 0.5, 0.75])
        max_val = eu_lo_gap2014['PayGap'].max()
        q1, q3, max_val = round(q1, 2), round(q3, 2), round(max_val, 2)

        st.markdown(f"""
        - 🔻 Negative pay gap: < 0
        - 🟢 Low: 0 to < {q1}
        - 🟡 Medium: {q1} to < {q3}
        - 🔴 High: {q3} to {max_val}
        """)

    with tab3:
        st.subheader("How Are Salaries Distributed Across Roles and Pay Gaps?")

        st.markdown("""In this section, we compare salary distributions across pay gap categories—negative, 
        low, medium, and high. Although negative pay gaps (where women earn more) are uncommon, 
        they deserve closer examination. Our goal is to identify salary levels linked to each category and 
        understand whether pay gaps result from lower female or higher male earnings. 
        The number of cities per category is shown on the x-axis to highlight their impact. We use boxplots 
        to visualize these patterns, analyzing all job roles together by gender.""")

        # 1) Define the mapping from Role → (label_col, female_col, male_col)
        options1 = {
            "Executive": {
                "label_col": "executive_pay_gap_label",
                "female_col": "fem_executive_sa",
                "male_col": "male_executive_sa",
            },
            "Manager": {
                "label_col": "manager_pay_gap_label",
                "female_col": "fem_manager_sa",
                "male_col": "male_manager_sa",
            },
            "Employee": {
                "label_col": "employee_pay_gap_label",
                "female_col": "fem_employee_sa",
                "male_col": "male_employee_sa",
            },
            "Worker": {
                "label_col": "worker_pay_gap_label",
                "female_col": "fem_worker_sa",
                "male_col": "male_worker_sa",
            },
        }

        # 2) Let the user pick a role
        role = st.radio("Select Role", list(options1.keys()), horizontal=True)

        # 3) Grab the sub‐dict for that role (safely)
        selected_role_config = options1.get(role)
        if selected_role_config is None:
            st.error("⚠️ Selected role is invalid. Please choose a valid option.")
            st.stop()

        # 4) Unpack the three column‐names for this role
        label_col = selected_role_config["label_col"]
        female_col = selected_role_config["female_col"]
        male_col = selected_role_config["male_col"]

        # 4a) Sanity‐check: co_sa_lo_po_no_city must be a DataFrame
        if not hasattr(co_sa_lo_po_no_city, "columns"):
            st.error("❌ Error: `co_sa_lo_po_no_city` is not a DataFrame. Got type: "
                    f"{type(co_sa_lo_po_no_city)}")
            st.stop()

        # 4b) Sanity‐check: the three columns must exist in the DataFrame
        missing = [c for c in (label_col, female_col, male_col) if c not in co_sa_lo_po_no_city.columns]
        if missing:
            st.error(f"❌ The following columns were not found in your DataFrame: {missing}")
            st.stop()

        # 5) Define the pay‐gap labels we want to iterate over
        gap_labels = [
            ("negative pay gap", "🟣 ♀ > ♂ Negative Pay Gap"),
            ("low pay gap",      "🟢 ♂ > ♀ Low Pay Gap"),
            ("medium pay gap",   "🟡 ♂ > ♀ Medium Pay Gap"),
            ("high pay gap",     "🔴 ♂ > ♀ High Pay Gap"),
        ]

        # 6) Build a single Plotly figure to hold all the Box plots
        fig = make_subplots(rows=1, cols=1)
        first_trace = True

        # 7) For each gap label, filter the DataFrame and add two Box traces
        for label_key, label_name in gap_labels:
            # 7a) Filter using .loc so that we get a DataFrame (not a string)
            try:
                mask = co_sa_lo_po_no_city[label_col] == label_key
                df_filtered = co_sa_lo_po_no_city.loc[mask]
            except Exception as e:
                st.error(f"❌ Error while filtering data for '{label_key}': {e}")
                st.stop()

            count = df_filtered.shape[0]
            label_with_count = f"{label_name}, cities = {count}"

            if count > 0:
                # 7b) Add the “female” Box plot for this label
                fig.add_trace(
                    go.Box(
                        y=df_filtered[female_col],
                        x=[label_with_count] * count,
                        name="Female",
                        marker_color="#FF885B",
                        showlegend=first_trace,
                    )
                )
                # 7c) Add the “male” Box plot for this label
                fig.add_trace(
                    go.Box(
                        y=df_filtered[male_col],
                        x=[label_with_count] * count,
                        name="Male",
                        marker_color="#15B392",
                        showlegend=first_trace,
                    )
                )
                first_trace = False

        # 8) Finalize layout
        fig.update_layout(
            title=f"How Are {role} Salaries Distributed in Cities With Different Pay Gaps?",
            yaxis_title="Average hourly salary (€)",
            boxmode="group",
            width=900,
            height=600,
            font=dict(size=12),
            legend=dict(
                title="Gender",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
            xaxis=dict(
                tickangle=45
            ),
        )

        # 9) Show the chart
        st.plotly_chart(fig)

        st.markdown("""This section compares salary distributions across four gender pay gap categories: negative, low, medium, and high. Negative pay gaps, 
                    where women earn more, are rare but notable, and we will explore their causes later. We analyze 
                    whether pay gaps result from lower female or higher male salaries, showing the number of cities 
                    in each category. Boxplots visualize salary patterns by gender across all roles.""")

        st.markdown("""Findings indicate that medium and high pay gaps are associated with higher male salaries and greater salary variation, especially in executive and managerial roles where women earn less and men’s salaries increase sharply. Many cities have high pay gaps in these roles, which are well-suited for further study due to their clear sector links and structured data. In France, positions covered by collective bargaining agreements often show lower gender pay gaps, while executive and managerial roles—less frequently covered—tend to have higher gaps.
                    For employees, the gender pay gap is also high but reflects the diversity of jobs included in this category. Women are more often in part-time or lower-qualified roles, while men are overrepresented in higher-paying STEM fields, contributing to wider pay disparities. Rising male salaries seem to mainly drive the gap, while female earnings tend to stagnate or grow at a slower rate; we will explore this hypothesis further.""")

        with st.expander("Data Preparation"):
            st.markdown("""
        **Data preparation:**  
        Merging city-level population, salary, company, and location data. Pay gaps were calculated per role using the formula (male salary−female salary)/male salary×100(male salary−female salary)/male salary×100 and categorized into four groups based on EU thresholds. Boxplots created with Plotly illustrate salary distributions by pay gap category.
        """)
       
        st.subheader("Which Cities stand out in Terms of Negative, Low, Medium Pay Gap in Leadership Positions?")

        st.markdown("""
        Our analysis focuses on gender pay gaps in executive and managerial roles since the salary dataset provides only average net hourly salaries - lacking details on the number of professionals per role or city - making weighted or representative analyses across occupational groups challenging. Therefore, concentrating on leadership positions, which are fewer in number but strategically significant, offers a methodologically sound basis for comparison.
        """)
        st.markdown("""🟣 ♀ > ♂ Negative Pay Gap | 🟢 ♂ > ♀ Low Pay Gap | 🟡 ♂ > ♀ Medium Pay Gap | 🔴 ♂ > ♀ High Pay Gap""")

        # Create two columns for side-by-side maps
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Executive Pay Gap Map")

            color_map_exec = {
                'negative pay gap': '#B771E5',
                'low pay gap': '#49B47E',
                'medium pay gap': '#FFD63A',
                'high pay gap': '#D91656'
            }

            fig_exec = go.Figure()
            for label, color in color_map_exec.items():
                subset = co_sa_lo_po_no_city[co_sa_lo_po_no_city['executive_pay_gap_label'] == label]
                fig_exec.add_trace(go.Scattergeo(
                    lon=subset['longitude'],
                    lat=subset['latitude'],
                    text=(
                        subset['city_name'] + '<br>' +
                        'Average Executive Salary: ' + subset['executive_sa'].astype(str) + ' €<br>' +
                        'Female Executive Salary: ' + subset['fem_executive_sa'].astype(str) + ' €<br>' +
                        'Male Executive Salary: ' + subset['male_executive_sa'].astype(str) + ' €<br>' +
                        'Executive Pay Gap: ' + subset['executive_pay_gap'].round(2).astype(str) + ' %<br>' +
                        'Population: ' + subset['people_no'].astype(int).astype(str)
                    ),
                    marker=dict(
                        size=subset['people_no'] / 800,
                        color=color,
                        line_color='black',
                        line_width=0.7,
                        sizemode='area',
                        opacity=0.6
                    ),
                    showlegend=False
                ))
            label_subset_exec = co_sa_lo_po_no_city[co_sa_lo_po_no_city['people_no'] >= 100000]
            fig_exec.add_trace(go.Scattergeo(
                lon=label_subset_exec['longitude'],
                lat=label_subset_exec['latitude'],
                text=label_subset_exec['city_name'],
                mode='text',
                textfont=dict(size=9, color='black'),
                showlegend=False
            ))
            fig_exec.update_layout(
                geo=dict(
                    scope='europe',
                    landcolor='rgb(230, 230, 230)',
                    showland=True,
                    showcountries=True,
                    projection_type='natural earth',
                    lonaxis_range=[-5, 10],
                    lataxis_range=[41, 52]
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=600
            )
            st.plotly_chart(fig_exec, use_container_width=True)

        with col2:
            st.subheader("Manager Pay Gap Map")

            color_map_mgr = {
                'negative pay gap': '#B771E5',
                'low pay gap': '#49B47E',
                'medium pay gap': '#FFD63A',
                'high pay gap': '#D91656'
            }

            fig_mgr = go.Figure()
            for label, color in color_map_mgr.items():
                subset = co_sa_lo_po_no_city[co_sa_lo_po_no_city['manager_pay_gap_label'] == label]
                fig_mgr.add_trace(go.Scattergeo(
                    lon=subset['longitude'],
                    lat=subset['latitude'],
                    text=(
                        subset['city_name'] + '<br>' +
                        'Average Manager Salary: ' + subset['manager_sa'].astype(str) + ' €<br>' +
                        'Female Manager Salary: ' + subset['fem_manager_sa'].astype(str) + ' €<br>' +
                        'Male Manager Salary: ' + subset['male_manager_sa'].astype(str) + ' €<br>' +
                        'Manager Pay Gap: ' + subset['manager_pay_gap'].round(2).astype(str) + ' %<br>' +
                        'Population: ' + subset['people_no'].astype(int).astype(str)
                    ),
                    marker=dict(
                        size=subset['people_no'] / 800,
                        color=color,
                        line_color='black',
                        line_width=0.7,
                        sizemode='area',
                        opacity=0.6
                    ),
                    showlegend=False
                ))
            label_subset_mgr = co_sa_lo_po_no_city[co_sa_lo_po_no_city['people_no'] >= 100000]
            fig_mgr.add_trace(go.Scattergeo(
                lon=label_subset_mgr['longitude'],
                lat=label_subset_mgr['latitude'],
                text=label_subset_mgr['city_name'],
                mode='text',
                textfont=dict(size=9, color='black'),
                showlegend=False
            ))
            fig_mgr.update_layout(
                geo=dict(
                    scope='europe',
                    landcolor='rgb(230, 230, 230)',
                    showland=True,
                    showcountries=True,
                    projection_type='natural earth',
                    lonaxis_range=[-5, 10],
                    lataxis_range=[41, 52]
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=600
            )
            st.plotly_chart(fig_mgr, use_container_width=True)

        st.markdown("""
        The pay gap among **managers** is notably less pronounced than among **executives**, which may be partly explained by broader collective agreement coverage, especially in countries like France, where around [98% of employees were covered in 2012](https://www.ifo.de/DocDL/dice-report-2018-4-poutvaara-nikolka-january.pdf). These agreements likely help standardize wages and reduce disparities. While some smaller cities with negative gaps aren't shown on maps due to scale, they remain important for our later analysis.
        """)


    with tab4:

        st.markdown("""
        In our cleaned dataset *'company by sector'*, we consolidated the sectors into six broader categories:
        - Technology  
        - Consumer  
        - Finance & Real Estate  
        - Construction  
        - Public / Education / Health / Social  
        - Manufacturing
        """)
        st.subheader("""How Are EXECUTIVE Pay Gaps distributed across Industries?""")

        st.markdown("""As a first step in our analysis of the relationship between pay gaps and industries, we aimed to understand the distribution of negative, low, medium, and high pay gaps across different sectors. 
                    To support this, we generated pairplots. You can view the full pairplot by expanding the section below. For a more focused analysis, we’ve included targeted snippets from the pairplot.
        """)


        st.image("pictures/""dist_exe_tech.png""")

        st.markdown("""
        At first glance, cities where the technology sector makes up less than 20% of the economic landscape tend to show the largest positive **executive pay gaps**. Interestingly, nearly all instances where female executives out-earn their male counterparts — the so-called **negative executive pay gaps** — also occur in these low-tech cities. This suggests a possible relationship: a lower presence of the technology sector may be linked to higher female executive salaries, and vice versa.

        Similar patterns can be observed in cities with low shares of construction and manufacturing. In contrast, sectors like consumer goods, public/education/social/health, and finance do not exhibit a consistent “under-20%” effect.

        However, these are preliminary observations. It remains unclear whether these patterns persist across small versus large cities or whether other structural factors are at play.
        """)

        with st.expander("Click to view the full executive pairplot"):
            #We create a pairplot to see the distribution of the pay gaps across the industries

            st.image('pictures/pairplot_executives.png')

        st.image("pictures/""dist_man_tech.png""")


        st.markdown("""
        Visually, the chart reveals a stronger concentration of medium **manager pay gaps** than before. While most cities still have technology sector shares below 20%, a few with higher tech representation (over 20%) now show outliers with unusually large manager pay gaps - a surprising contrast to the executive pay gap pattern.

        These results suggest we should further explore how representation in the technology sector affects disparities in both manager and executive pay, and overall salary structures.

        As a next step, we examine whether the share of a sector influences the average pay gap, helping us determine if there is a broader relationship between sector size and pay inequality.""")
        with st.expander("Click to view the full manager pairplot and data preparation"):
            #We create a pairplot to see the distribution of the pay gaps across the industries
            st.image('pictures/pairplot_managers.png')

            st.markdown("""**Data preparation:**  
            We created a DataFrame with only the relevant pay gap columns, merged it with the sector composition data, and calculated the sector share for “technology,” “consumer,” “finance_re,” “construction_industry,” and “public_edu_health_social.” We then visualized the relationships using Seaborn’s `pairplot`, first for executive pay gaps, then for **manager pay gaps**.
            """)

        st.subheader("""How do Average Pay Gaps correlate with Sectors in Cities with more than 100 000 Inhabitants?""")

        st.markdown("""
        To explore patterns in gender pay disparity, we focused on cities with over 100,000 inhabitants and compared outcomes with and without Paris, given its outsized economic influence.

        We looked at whether the share of specific sectors in a city correlates with the average gender pay gap.
        """)

       
        # Radio buttons to choose the dataset
        option = st.radio(
            "Select View:",
            ("Exclude Paris", "Include Paris"),
            horizontal=True
        )

        # Filter the appropriate dataset
        if option == "Exclude Paris":
            filtered_df = seco_gap[(seco_gap['people_no'] > 100000) & (seco_gap['city_name'] != 'Paris')]
            title = "Is the Average Pay Gap in Cities >100,000 (excluding Paris) Correlated to Sectors?"
        else:
            filtered_df = seco_gap[seco_gap['people_no'] > 100000]
            title = "Is the Average Pay Gap in Cities >100,000 (including Paris) Correlated to Sectors?"

        # Melt the DataFrame
        df_melt = filtered_df.melt(
            id_vars=['city_id', 'city_name', 'avg_pay_gap', 'people_no'],
            value_vars=[c for c in filtered_df.columns[23:29]],
            var_name='sector',
            value_name='sector_no'
        )

        # Create scatter plot
        fig = px.scatter(
            df_melt,
            y='sector_no',
            x='avg_pay_gap',
            size='people_no',
            size_max=40,
            facet_col='sector',
            facet_col_wrap=4,
            trendline='ols',
            opacity=0.6,
            height=1200,
            width=1000,
            labels={
                'sector_no': 'Company Proportion (%)',
                'avg_pay_gap': 'Average Pay Gap (%)'
            },
            title=title
        )

        # Optional: rotate x-labels for readability
        fig.update_xaxes(tickangle=-45)

        # Display chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        Most sectors show little correlation except for technology. Including Paris slightly strengthens the relationship. As the economically strongest city with a high proportion of tech companies and a higher-than-average pay gap, Paris brings us closer to confirming our hypothesis. Recently, Paris was named the new [European tech champion](https://www.reuters.com/technology/paris-named-europes-leading-tech-ecosystem-beating-london-2025-05-21/), surpassing London.
        """)


        

        st.subheader("Statistical Analysis of Sector Effects on Gender Pay Gaps")

        st.markdown("""
        In the following chapters, we conduct statistical tests to check whether earlier assumptions hold under closer scrutiny. To interpret the results accurately, a brief explanation of statistical basics is helpful—especially the concept of the p-value.

        The **p-value** indicates whether an observed relationship between two variables is likely due to chance. A low p-value (typically < 0.05) suggests that the result is statistically significant. However, significance does not imply proof—only that we can’t easily dismiss the observed correlation.

        At the core is the **null hypothesis (H0)**: it assumes there’s no relationship between two variables. If the p-value is high, we accept H0 and reject the alternative (H1). If the p-value is low, we reject H0, suggesting a statistically significant relationship exists.
        """)

        st.subheader("Tech Companies Share vs. High Executive and Manager Pay Gaps")

        st.markdown("""
        We first examine whether there’s a statistically significant link between **executive** pay gaps and the city-level presence of tech companies, using **Pearson** and **Spearman** correlation tests.
        """)

        st.image("pictures/high_tech_high_ex.png")

        st.markdown("""
        **Results (Executive Pay Gap vs. Tech Share):**  
        - P-Value Pearson: 1.61e-16  
        - Pearson correlation coefficient: 0.265  
        - P-Value Spearman: 1.33e-09  

        Both tests confirm statistical significance, with p-values far below 0.05. The Pearson coefficient of 0.265 suggests a moderate positive linear relationship: cities with more tech firms tend to have higher executive pay gaps.

        The Spearman test supports this trend in a monotonic sense, meaning that even if the increase isn’t linear, it consistently moves in one direction.

        The bubble chart shows cities like Paris with rising executive pay gaps as tech-sector shares increase. Notably, Paris—even with high tech presence—maintains a lower gap than smaller cities with similar tech profiles.

        This aligns with our earlier pairplot: smaller cities with tech-sector shares around 20% often show elevated executive pay gaps.
        """)

        st.markdown("""
        Next, we analyze **manager** pay gaps in relation to tech-sector concentration.
        """)

        st.image("pictures/high_tech_high_man.png")

        st.markdown("""
        **Results (Manager Pay Gap vs. Tech Share):**  
        - P-Value Pearson: 1.69e-09  
        - Pearson correlation coefficient: 0.361  
        - P-Value Spearman: 0.0311  

        Again, both tests confirm statistical significance. The Pearson value suggests a moderately positive linear correlation. Spearman also detects a significant monotonic trend.

        The bubble chart reveals a clustering of large cities with both high tech-sector shares and high manager pay gaps. Still, a few outliers remain—some large cities show lower gaps despite tech prominence.
        """)
        with st.expander("Data Preparation"):
            st.markdown("""
        **Data preparation:**  
        We used quantile thresholds (⅓ and ⅔) to create new columns for each sector with values “low proportion,” “medium proportion,” and “high proportion.” This categorization allowed us to filter the data and examine cities with both high tech-sector presence and high pay gaps—separately for executives and managers.
        """)
            

        st.subheader("When Women Earn More: City and Sector Patterns")

        st.markdown("""
        Some cities in the dataset show a less common trend: women earning more than men on average. On the earlier maps of negative, low, medium, and high executive pay gaps, these cases appeared as small purple areas—visually minor, but analytically interesting.

        Although relatively infrequent and statistically small in number, these cities raise questions about possible sectoral or demographic factors behind reversed pay gaps.

        To explore this, we focus on two groups of small cities:
        - Cities with a negative executive pay gap (62 cities, all under 3,000 residents)
        - Cities with a high executive pay gap (85 cities, all under 2,000 residents)

        By keeping the population range comparable, we aim for meaningful sectoral comparisons across the two groups.
        """)

        st.image("pictures/negative_heatmap.png")

        st.image("pictures/high_heatmap.png")

        st.markdown("""
        In both groups, the consumer sector shows a strong correlation with the total number of companies, suggesting that small cities may lean toward local retail-based economies.

        In cities with a negative executive pay gap, we see a strong correlation with companies in the health, education, public, and social sectors—areas typically associated with a higher share of female employment. This supports the idea that dominant sectors may help explain elevated female executive earnings.

        While we cannot confirm the relationship definitively, earlier research points in the same direction. For example, studies such as the [ISERT report](https://www.eurofound.europa.eu/en/resources/article/2014/france-effect-motherhood-employment-public-and-private-sectors) link lower pay gaps to improved work-life balance in the public sector—an important factor during child-raising years.

        In contrast, technology companies appear less frequently in cities with negative pay gaps, but are more common in small cities with high gaps. This contrast is also reflected in correlation coefficients: 0.68 for the negative-gap cities and 0.84 for the high-gap cities.

        These observations also reinforce the pattern seen in the earlier pairplot, where cities with lower tech-sector presence tended to show reversed or smaller pay gaps.

        To examine whether the observed patterns are statistically meaningful and potentially generalizable, we next apply an ANOVA test.
        """)

        st.subheader("ANOVA Test: Pay Gap Levels vs. Sector Shares")

        st.markdown("""
        The ANOVA test helps identify whether average pay gaps differ significantly across cities with varying sector concentrations.

        **Test Variables**  
        We used the share of companies per sector (e.g., technology_pct, consumer_pct) and compared these with pay gap classifications (negative, low, medium, high) across hierarchy levels like executive and employee.

        **Limitations of ANOVA Test**  
        ANOVA tells us if there are statistically significant differences between groups, but not in which direction or why. A significant result signals association—not causation—and may reflect complex or non-linear sector effects.

        **ANOVA Test: Public Sector vs. Executive Pay Gap**  
        **Test result:** p-value = 0.117 → H0 not rejected  
        There is no statistically significant relationship between public sector share and executive pay gap categories. This aligns with previous visualizations: public sector employment appears fairly stable across pay gap levels.

        **ANOVA Test: Consumer Sector vs. Employee Pay Gap**  
        **Test result:** p-value = 4.63e-28 → H0 rejected  
        A strong statistical relationship exists between the consumer sector and employee pay gap categories. While wages here tend to be lower, this sector’s presence appears to shape local pay gap patterns.

        **ANOVA Test: Technology Sector vs. Employee Pay Gap**  
        **Test result:** p-value = 7.25e-13 → H0 rejected  
        Technology sector share is also significantly associated with employee pay gap levels. The test does not tell us if gaps are higher or lower—only that meaningful differences exist.

        **ANOVA Test: Finance/Real Estate vs. Employee Pay Gap**  
        **Test result:** p-value = 0.000081 → H0 rejected  
        Although the finance and real estate sectors have fewer firms overall, they show a notable association with different categories of employee pay gaps. When we look at manager and executive pay gaps versus the share of finance and real estate companies in our pairplot above, we observe that cities where women earn more than men in these roles tend to have a higher proportion of firms in the finance and real estate sector. This suggests a possible link between sector composition and pay equity at senior levels and potentially at employee level.

        Interestingly, this pattern echoes what we see in Luxembourg, the EU country with one of the lowest — and in recent years, even negative — gender pay gaps. Luxembourg has a strong concentration of large financial companies, which may contribute to more equitable pay structures.

        
        This raises the question: could the finance and real estate sector be a driver of pay equity also for employees? Exploring this potential link could be a valuable direction for future research.
        """)

if page == "Further Investigation Areas":
    
    st.header("What We Couldn’t Explore (But Would Have Liked To)")

    st.markdown("""
    In the following section, we outline which areas could have been explored further if more time had been available. Most importantly, we would focus on studies based on recent years, particularly the period following the COVID-19 pandemic.

    **How do Company Size and Business Sector Proportion influence the Gender Pay Gap across Cities?**  
    While our report focuses on the gender pay gap and its relationship to sector distribution, company representation, and city size, there are several promising analytical directions we were unable to pursue due to time constraints. This chapter highlights these areas as potential next steps for further research.""")

    st.markdown("""Company Size Distribution in France’s Largest Cities: 
    We began an exploratory comparison of the five most populous French cities Paris, Marseille, Lyon, Toulouse, and Nice to understand the broader economic context in which companies operate.""")

    #In this pie chart we can observe the percentages of company sizes in these French cities: Nice, Toulouse, Marseille, Lyon, Paris side by side.

    cities = ["Nice", "Marseille", "Toulouse", "Lyon", "Paris"]
    fig, axs = plt.subplots(2, 3, figsize=(18, 12))
    axs = axs.flatten()

    # Normalize city_name in your DataFrame
    co['city_name'] = co['city_name'].str.strip().str.lower()

    for i, city in enumerate(cities):
        city_lower = city.lower()
        city_rows = co[co['city_name'] == city_lower]
        
        if not city_rows.empty:
            city_data = city_rows.iloc[0]
            sizes = [city_data['micro'], city_data['small'], city_data['mid'], city_data['large']]
            labels = ['Micro', 'Small', 'Mid', 'Large']
            axs[i].pie(sizes, labels=labels, autopct='%1.1f%%', pctdistance=0.7, startangle=190,
                    colors=['teal', 'pink', 'orange', 'yellow'])
            axs[i].set_title(city)
        else:
            axs[i].text(0.5, 0.5, f"No data for {city}", ha='center', va='center')
            axs[i].axis('off')

    # Hide unused axes
    if len(cities) < len(axs):
        axs[len(cities)].axis('off')

    plt.suptitle("How are Company Sizes distributed among France's Top Five Cities?", fontsize=20)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

   
    st.pyplot(fig)


 
    st.markdown("""A preliminary chart showed that Paris, as expected, dominates in terms of the absolute number of companies, significantly skewing national-level statistics.""")

    # Normalize city names
    co['city_name'] = co['city_name'].str.strip().str.lower()
    cities = ["Toulouse", "Lyon", "Marseille", "Paris", "Nice"]
    data = []

    for city in cities:
        city_lower = city.lower()
        if city_lower in co['city_name'].values:
            row = co[co['city_name'] == city_lower].iloc[0]
            counts = [row['micro'], row['small'], row['mid'], row['large']]
            data.append(counts)
        else:
            st.warning(f"No data found for {city}")

    if data:  # Only proceed if data is non-empty
        data = np.array(data)
        x = np.arange(len(size_labels))
        bar_width = 0.17

        fig, ax = plt.subplots(figsize=(14, 5))

        for i, city_data in enumerate(data):
            bars = ax.bar(x + i * bar_width, city_data, width=bar_width, label=cities[i])
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)

        ax.set_xlabel("Company Size")
        ax.set_ylabel("Number of Companies")
        ax.set_title("Company Size Distribution by City (Total Numbers)")
        ax.set_xticks(x + bar_width * (len(cities) - 1) / 2)
        ax.set_xticklabels(size_labels, rotation=45, ha='right')
        ax.legend()
        fig.tight_layout()

        st.pyplot(fig)
    else:
        st.error("No valid data available to plot.")


    st.markdown("""
    Because of this outsized influence, we chose to compare some city datasets with and without Paris to avoid distorted interpretations – something already familiar from our earlier regional analysis and comparing the average pay gap with business sectors.

    What we didn’t have time to fully analyze, however, was how company size is distributed across these cities, and whether certain industries contribute to these patterns. For instance, Toulouse appeared to have a relatively high share of small and midsize enterprises (SMEs). It would be interesting to investigate whether this distribution is linked to local industry structures, such as a higher concentration of startups or niche manufacturing firms, and how the relationship between industry type and company size influences the gender pay gap.

    As a starting hypothesis, we could explore whether tech-heavy cities tend to have more small firms and wider gender pay gaps, while finance hubs, often dominated by large corporations, like Luxembourg, exhibit narrower pay gaps. As this remains unconfirmed, it would require deeper research.
    """)

    # Additional topics in expanders
    with st.expander("💰📈🛒Company Size, Salary Levels, and Cost of Living"):
        st.markdown("""
        Our regression analysis in Regional Economic Impact showed a clear link between company size, salary levels and a link to cost of living. Larger firms tend to offer higher wages, particularly in regions like Île-de-France. A further step, if more time had been available, would have been to compare these salary patterns with the actual local cost of living. High salaries in cities like Paris may be offset by higher living expenses, affecting overall financial well-being as already indicated in our regional studies.
        """)

    with st.expander("💼Job Roles and Pay Gaps"):
        st.markdown("""
        We also noticed a potential divide between low- and high-paid employee roles. While we confirmed wage differences across sectors, we couldn’t fully explore how role, sector, and gender intersect.
        """)

    with st.expander("👩🏿‍💻STEM Gender Balance in Europe"):
        st.markdown("""
        [Eurostat data](https://ec.europa.eu/eurostat/web/products-eurostat-news/w/edn-20250211-1) shows regional differences in the share of female scientists and engineers across the EU. It would be valuable to examine whether regions with more women in STEM have narrower pay gaps or higher wages overall. We could not explore this further, but it remains a relevant angle, especially in light of the upcoming [EU Pay Transparency Action](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/gender-equality/equal-pay/eu-action-equal-pay_en) (June 2026).
        """)
        st.image('pictures/female_engineers.png')

    with st.expander("🏦 Financial Sector Effects"):
        st.markdown("""
        Our ANOVA test showed that the finance and real estate sector has a significant impact on employee pay gaps. Although fewer in number, companies in this sector tend to be large and high-paying. Further analysis could clarify how this concentration contributes to gender-based salary differences.
        """)

    with st.expander("🚀 Executive Pay in Tech Start-ups"):
        st.markdown("""
        In tech-driven cities, we observed higher leadership pay gaps. This could indicate a disconnect between top-level compensation and general workforce salaries, especially in startup-heavy regions. More detailed data would be needed to separate these effects by company size and role.
        """)

if page == "Conclusion":
    st.title("📌Conclusion")

    st.markdown("""
    Our findings suggest that regional and sectoral patterns in corporate concentration shape both salary levels and inequality. While small businesses dominate numerically, large firms—especially in Île-de-France—have a stronger impact on wages and tend to show wider gender pay disparities, particularly at the executive level.

    Though cost-of-living data was not available in our datasets, our regression analysis indicates that regions with more large companies often have both higher salaries and greater inequality. This underscores uneven access to financial stability and opportunity across regions.

    At the sector level, the technology industry stands out as closely linked to gender pay gaps—likely due to its male-dominated leadership structures. Yet, change is on the horizon. Programs like DataScientest’s bootcamps are making tech careers more accessible and already draw strong female participation.

    Still, structural challenges persist. Many women adjust their careers due to caregiving responsibilities, which affects long-term earnings and financial security. Public investment in childcare and better support for care-sector professions remain critical.

    Looking ahead, policies like the [EU Pay Transparency Directive](https://commission.europa.eu/strategy-and-policy/policies/justice-and-fundamental-rights/gender-equality/equal-pay/eu-action-equal-pay_en) and increased access to training in high-growth sectors can help shift the balance. Long-term progress depends not only on gender, but also on addressing regional, sector-based, and life-stage inequalities in how opportunity is distributed.
    """)


