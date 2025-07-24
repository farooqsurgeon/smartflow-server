import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

print("Working dir:", os.getcwd())
print("Before:", os.listdir("."))

# Sample data
X = np.array([[0,8,0],[1,17,1],[2,9,0],[1,18,1]])
y = np.array([0,2,1,2])

model = RandomForestClassifier()
model.fit(X, y)

out_path = "traffic_model.pkl"
with open(out_path, "wb") as f:
    pickle.dump(model, f)

print("Saved model to:", os.path.abspath(out_path))
print("After:", os.listdir("."))
