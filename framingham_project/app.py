from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import joblib
import os
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

app = Flask(__name__)

MODELS_DIR = 'models'
FEATURE_NAMES = ['male', 'age', 'education', 'currentSmoker', 'cigsPerDay',
                 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes',
                 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose']

def load_model(model_type):
    scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    if model_type == 'mlp':
        model = joblib.load(os.path.join(MODELS_DIR, 'mlp.pkl'))
    else:
        model = joblib.load(os.path.join(MODELS_DIR, 'logreg.pkl'))
    return model, scaler

@app.route('/')
def index():
    tab = request.args.get('tab', 'individual')
    return render_template('index.html', tab=tab)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        modelo_type = request.form.get('modelo', 'logreg')
        values = []
        for f in FEATURE_NAMES:
            values.append(float(request.form.get(f, 0)))

        X = np.array(values).reshape(1, -1)
        model, scaler = load_model(modelo_type)
        X_scaled = scaler.transform(X)
        pred = int(model.predict(X_scaled)[0])
        prob = round(float(model.predict_proba(X_scaled)[0][1]) * 100, 1)

        form_data = {f: request.form.get(f, '') for f in FEATURE_NAMES}
        return render_template('index.html', tab='individual',
                               pred_individual=pred,
                               prob_individual=prob,
                               modelo=modelo_type,
                               **form_data)
    except Exception as e:
        return render_template('index.html', tab='individual',
                               error=f'Error: {str(e)}',
                               modelo=request.form.get('modelo', 'logreg'))

@app.route('/batch', methods=['POST'])
def batch():
    try:
        modelo_type = request.form.get('modelo_batch', 'logreg')
        file = request.files.get('file')
        if not file:
            return render_template('index.html', tab='lotes', error='No se subió ningún archivo.')

        df = pd.read_csv(file)
        has_target = 'TenYearCHD' in df.columns

        missing = [f for f in FEATURE_NAMES if f not in df.columns]
        if missing:
            return render_template('index.html', tab='lotes',
                                   error=f'Columnas faltantes: {missing}')

        df = df.dropna(subset=FEATURE_NAMES)
        X = df[FEATURE_NAMES]
        model, scaler = load_model(modelo_type)
        X_scaled = scaler.transform(X)
        preds = model.predict(X_scaled)

        info = f'<strong>{len(preds)}</strong> predicciones realizadas.'
        matriz = None
        reporte = None

        if has_target:
            y_true = df['TenYearCHD']
            acc = round(accuracy_score(y_true, preds) * 100, 1)
            correctas = int((y_true == preds).sum())
            info = (f'Target: <strong>TenYearCHD</strong> ({len(preds)} valores)<br>'
                    f'✅ Columnas reconocidas.<br>'
                    f'Resultados: <strong>{len(preds)}</strong> predicciones | '
                    f'<strong>{correctas}</strong> correctas | Accuracy: <strong>{acc}%</strong>')
            cm = confusion_matrix(y_true, preds)
            matriz = cm.tolist()
            reporte = classification_report(y_true, preds)

        return render_template('index.html', tab='lotes',
                               info_msg=info,
                               matriz=matriz,
                               reporte=reporte)
    except Exception as e:
        return render_template('index.html', tab='lotes', error=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
