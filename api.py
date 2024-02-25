from pymongo import MongoClient
import folium
from folium.plugins import HeatMap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class worshipDB():
    # create a client
    client = MongoClient()

    # establish your db connection
    db = client['worship']

    # define collection
    worship = db.places

    def get_unique_religion(self):
        """ Get all unique religions from the places of worship """
        pipeline = [
            {
                "$match": {
                    "institution_info.subtype": {"$ne": "NOT AVAILABLE", "$exists": True},
                }
            },
            {
                "$group": {
                    "_id": "$institution_info.subtype"
                }
            }
        ]

        results = self.worship.aggregate(pipeline)

        return [result["_id"] for result in results]

    def find_k_nearest(self, latlon, religion=None, k=5):
        """Find k nearest chosen place of worship to the inputted location"""
        # make index
        self.worship.create_index([('location_info.coordinates', '2dsphere')])

        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": list(latlon)
                    },
                    "distanceField": "distance",
                    "spherical": True
                }
            },
            {
                "$project": {
                    "institution_info.name": 1,
                    "location_info.coordinates": 1,
                    "institution_info.subtype": 1,
                    "_id": 0
                }
            }
        ]

        if religion:
            pipeline.insert(1, {"$match": {"institution_info.subtype": religion}})

        pipeline.append({"$limit": k})

        results = list(self.worship.aggregate(pipeline))

        return results

    def find_state_largest(self, state='MA', religion=None, n=10):
        """Find top n number of worship places by state of given religion."""

        pipeline = [
            {
                "$match": {
                    "location_info.address.state": state,
                    "institution_info.denomination.members": {"$ne": "NOT AVAILABLE"}
                }
            },
            {
                "$project": {
                    "name": "$institution_info.name",
                    "size": "$institution_info.denomination.members",
                    "_id": 0
                }
            },
            {
                "$sort": {"size": -1}  # Sort by decreasing size
            },
            {
                "$limit": n
            }
        ]

        if religion:
            pipeline.insert(1, {"$match": {"institution_info.subtype": religion}})

        results = list(self.worship.aggregate(pipeline))

        return results

    def plot_religion(self, religion=None, html=True):
        """ Plot religion on heatmap to understand where it is most concentrated """
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "location_info.coordinates": 1,
                    "institution_info.name": 1,
                    "institution_info.subtype": 1
                }
            }
        ]

        if religion:
            pipeline.insert(1, {"$match": {"institution_info.subtype": religion}})

        results = list(self.worship.aggregate(pipeline))

        heat_map = folium.Map(location=[37, -96], zoom_start=4)

        locs = []
        for point in results:
            coors = point['location_info']['coordinates']
            locs.append([coors[1], coors[0]])

        HeatMap(locs, radius=12).add_to(heat_map)
        if html:
            heat_map.save('religious_heatmap.html')

        return results

    def make_map(self, html=True):
        """ create a map where user can click on religion"""
        pipeline = [
            {
                '$group': {
                    '_id': "$location_info.address.state",
                    'count': {'$sum': 1},
                    'state_pop': {'$first': "$location_info.state_pop"}
                }
            },
            {
                '$project': {
                    'state': '$_id',
                    'ratio': {'$multiply': [{'$divide': ["$count", "$state_pop"]}, 10000]}
                }
            },
            {
                '$sort': {'ratio': -1}
            }
        ]

        results = list(self.worship.aggregate(pipeline))

        # create dataframe
        df = pd.DataFrame(results)
        df = df.drop(columns='_id')

        # make map
        fig = px.choropleth(
            df,
            locations='state',
            locationmode='USA-states',
            color='ratio',
            scope='usa',
            color_continuous_scale="Reds",
            labels={'ratio': 'Density of Places of Worship'}
        )

        fig.update_layout(
            title_text='Density of Places of Worship by State',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)')
        )

        if html:
            fig.write_html('density_map.html')

        return fig.show()









