import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationModel:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        self.cv = CountVectorizer(stop_words='english')
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


# Inisialisasi model
model = RecommendationModel(data_path='data/locations.csv')
