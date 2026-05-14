<<<<<<< HEAD
# framingham-app-cardiac-risk-predictor
 Predicción de riesgo coronario a 10 años
=======
# Framingham Risk Predictor

Sistema de predicción de riesgo coronario a 10 años basado en el **Framingham Heart Study**.

## Descripción

Predice si un paciente tiene riesgo de desarrollar enfermedad coronaria en los próximos 10 años usando dos modelos de Machine Learning entrenados sobre 3,656 registros clínicos reales.

## Modelos

| Modelo | Accuracy |
|--------|----------|
| Regresión Logística | ~85% |
| Red Neuronal (MLP) | ~85% |

## Variables del dataset

| Variable | Descripción |
|----------|-------------|
| male | Sexo (1=masculino, 0=femenino) |
| age | Edad |
| education | Nivel educativo (1-4) |
| currentSmoker | Fumador actual (0/1) |
| cigsPerDay | Cigarrillos por día |
| BPMeds | Medicación para presión (0/1) |
| prevalentStroke | ACV previo (0/1) |
| prevalentHyp | Hipertensión (0/1) |
| diabetes | Diabetes (0/1) |
| totChol | Colesterol total (mg/dL) |
| sysBP | Presión sistólica (mmHg) |
| diaBP | Presión diastólica (mmHg) |
| BMI | Índice de masa corporal |
| heartRate | Frecuencia cardíaca |
| glucose | Glucosa (mg/dL) |

## Ejecución local

```bash
pip install -r requirements.txt
python app.py
```

## Despliegue en Render

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

## Endpoints

- `GET /` — Interfaz web
- `POST /predict` — Predicción individual
- `POST /batch` — Predicción por lotes (CSV)
>>>>>>> 8926328 (Initial commit - Framingham Risk Predictor)
