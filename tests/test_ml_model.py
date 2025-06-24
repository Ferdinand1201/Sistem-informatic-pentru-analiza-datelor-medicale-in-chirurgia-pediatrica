import pytest
from app.ml_model import predict_risk, train_model
import os

def test_predict_risk_binary_output():
    result = predict_risk(190, 88.0, 39.0)
    assert result in [0, 1]

def test_model_training_creates_file():
    from app.ml_model import MODEL_PATH
    if os.path.exists(MODEL_PATH):
        os.remove(MODEL_PATH)
    train_model(force=True)
    assert os.path.exists(MODEL_PATH)
