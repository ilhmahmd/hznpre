from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

class RecommendationModel:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.cv = CountVectorizer()
        self.cosine_sim_matrix = None
        self._prepare_data()

    def _prepare_data(self):
        self.data['features'] = self.data[['Tema', 'Tipe']].fillna('').astype(str).agg(' '.join, axis=1)
        count_matrix = self.cv.fit_transform(self.data['features'])
        self.cosine_sim_matrix = cosine_similarity(count_matrix, count_matrix)

    def get_recommendations(self, location_name, top_n=5, threshold=0):
        if location_name not in self.data['Tempat'].values:
            return []
        indices = pd.Series(self.data.index, index=self.data['Tempat']).drop_duplicates()
        idx = indices[location_name]
        sim_scores = list(enumerate(self.cosine_sim_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [score for score in sim_scores if score[1] > threshold and score[0] != idx]
        sim_scores = sim_scores[:top_n]
        location_indices = [i[0] for i in sim_scores]
        return self.data.iloc[location_indices].to_dict('records')

model = RecommendationModel(data_path='data/locations.csv')

@app.route('/')
def index():
    sort_by_type = request.args.get('sortByType', None)
    sort_by_tema = request.args.get('sortByTema', None)
    sort_by_harga = request.args.get('sortByHarga', None)
    
    filtered_df = model.data.copy()
    
    if sort_by_type:
        filtered_df = filtered_df[filtered_df['Tipe'] == sort_by_type]
    
    if sort_by_tema:
        filtered_df = filtered_df[filtered_df['Tema'] == sort_by_tema]
    
    if sort_by_harga:
        filtered_df = filtered_df.sort_values(by='Harga', ascending=(sort_by_harga == 'asc'))
    
    locations = filtered_df.to_dict('records')
    unique_tipes = model.data['Tipe'].unique()
    unique_temas = model.data['Tema'].unique()
    
    return render_template('index.html', locations=locations, unique_tipes=unique_tipes, unique_temas=unique_temas)

@app.route('/detail/<location_name>')
def detail(location_name):
    if location_name not in model.data['Tempat'].values:
        return "Location not found", 404
    location = model.data[model.data['Tempat'] == location_name].iloc[0].to_dict()
    recommendations = model.get_recommendations(location_name)
    return render_template('detail.html', location=location, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
