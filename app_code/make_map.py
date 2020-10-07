import json
import numpy as np
import pandas as pd
import folium
from folium.features import Choropleth


def generate_map(path, school_weight=0.5):
    df = pd.read_csv(path)
    df['zip_code'] = df['zip_code'].astype(str)
    df = df[df['one_family_dwelling'] != 0.].copy()
    
    df['school_score_unit'] = (df['school_score'] / df['school_score'].max() * 4) + 1
    df['crime_score_unit'] = ((df['crime_score'].max() - df['crime_score']) / df['crime_score'].max() * 4) + 1
    df['one_family_dwelling_unit'] = (df['one_family_dwelling'] / df['one_family_dwelling'].max() * 4) + 1

    df['overall_score'] = (school_weight * df['school_score_unit'] + (1 - school_weight) * df['crime_score_unit']) / df['one_family_dwelling_unit']
    df['overall_score_norm'] = (df['overall_score'] - df['overall_score'].mean()) / df['overall_score'].std()

    # modified code from https://towardsdatascience.com/visualizing-data-at-the-zip-code-level-with-folium-d07ac983db20
    with open('nyc.geojson', 'r') as jsonFile:
        data = json.load(jsonFile)
    tmp = data

    geozips = []
    for i in range(len(tmp['features'])):
        cur_zip = tmp['features'][i]['properties']['postalcode']
        if cur_zip in df['zip_code'].values:
            geozips.append(tmp['features'][i])

    new_json = dict.fromkeys(['type', 'features'])
    new_json['type'] = 'FeatureCollection'
    new_json['features'] = geozips

    open("needed_zips.json", "w").write(
        json.dumps(new_json, 
                   sort_keys=True, 
                   indent=4,
                   separators=(',', ': '))
    )
    
    la_geo = r'needed_zips.json'
    m = folium.Map(location=[40.767180, -73.977622], zoom_start=11)

    Choropleth(
        geo_data=la_geo,
        name='choropleth',
        data=df,
        columns=['zip_code', 'overall_score_norm'],
        key_on='feature.properties.postalcode',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Great School Score in NYC'
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m
