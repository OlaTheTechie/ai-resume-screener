from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_similarity_score(text1: str, text2: str) -> float:
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    cosine_sim = util.pytorch_cos_sim(embeddings1, embeddings2)
    return cosine_sim.item()
