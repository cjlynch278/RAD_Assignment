class VectorStore:
    def __init__(self, storage_backend):
        self.storage_backend = storage_backend
        self.vectors = {}

    def add_vector(self, key, vector):
        self.vectors[key] = vector
        self.storage_backend.store(key, vector)

    def retrieve_vector(self, key):
        if key in self.vectors:
            return self.vectors[key]
        return self.storage_backend.retrieve(key)

    def query(self, query_vector, top_k=5):
        return self.storage_backend.query(query_vector, top_k)

    def delete_vector(self, key):
        if key in self.vectors:
            del self.vectors[key]
        self.storage_backend.delete(key)