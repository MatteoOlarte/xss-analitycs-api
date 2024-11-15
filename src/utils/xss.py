import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification

from ..shemas.security_prediction import SecurityPredictionSchema
from ..shemas.security_prediction import SecurityAnalysis


def __load_model(model_path):
    tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base")
    model = RobertaForSequenceClassification.from_pretrained(model_path)
    return tokenizer, model


def __preprocess_code_line(code_line, tokenizer):
    inputs = tokenizer(code_line, return_tensors="pt",
                       padding="max_length", truncation=True, max_length=512)
    return inputs


def analyze_code(file_path, model, tokenizer):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    max_score = float('-inf')
    most_vulnerable_line = None

    for i, line in enumerate(lines):
        inputs = __preprocess_code_line(line, tokenizer)
        outputs = model(**inputs)
        # Obtener la puntuación para la clase "vulnerable"
        score = outputs.logits[0, 1].item()

        if score > max_score:
            max_score = score
            most_vulnerable_line = (i + 1, line.strip())

    return [most_vulnerable_line] if most_vulnerable_line else []


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
        schema.model = 'Modelo 150 épocas'
        return schema


def run_1600epochs(file_path: str) -> SecurityPredictionSchema:
    model_path = "./security_models/epochs_1600/my_codebert_security_model.ckpt"
    tokenizer, model = __load_model(model_path)

    with open(file_path, 'r') as file:
        code = file.read()
        schema = predict_security(tokenizer, model, code)
        schema.model = 'Modelo 1600 épocas'
        return schema


def vulnerable_lines(file_path: str) -> SecurityAnalysis | None:
    model_path = "./security_models/epochs_1600/my_codebert_security_model.ckpt"
    tokenizer, model = __load_model(model_path)
    vulnerable_lines = analyze_code(file_path, model, tokenizer)

    if vulnerable_lines:
        return SecurityAnalysis(
            model='Modelo 1600 épocas',
            error=vulnerable_lines
        )
    else: 
        return None
