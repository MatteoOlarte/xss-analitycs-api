import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

from ..shemas.security_prediction import SecurityPredictionSchema


def __load_model(model_path):
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    model = RobertaForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model


def predict_security(tokenizer, model, code) -> SecurityPredictionSchema:
    # Tokenizar el contenido del archivo
    inputs = tokenizer(
        code, 
        return_tensors="pt",             
        truncation=True,
        padding=True
    )

    # Pasar el contenido tokenized a través del modelo
    with torch.no_grad():
        outputs = model(**inputs)

    # Obtener las predicciones y las probabilidades
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)
    predictions = torch.argmax(logits, dim=-1)

    # Interpretar las predicciones
    label = predictions.item()
    confidence = probabilities[0][label].item()

    if label == 1:
        return SecurityPredictionSchema(is_secure=False, model='', confidence=confidence)
    else:
        return SecurityPredictionSchema(is_secure=True, model='', confidence=confidence)
    

def run_150epochs(file_path: str) -> SecurityPredictionSchema:
    model_path = "./security_models/epochs_150/my_codebert_security_model.ckpt"
    tokenizer, model = __load_model(model_path)

    with open(file_path, 'r') as file:
        code = file.read()
        schema = predict_security(tokenizer, model, code)
        schema.model = 'model_150e'
        return schema
    

def run_1600epochs(file_path: str) -> SecurityPredictionSchema:
    model_path = "./security_models/epochs_1600/my_codebert_security_model.ckpt"
    tokenizer, model = __load_model(model_path)

    with open(file_path, 'r') as file:
        code = file.read()
        schema = predict_security(tokenizer, model, code)
        schema.model = 'model_1600e'
        return schema