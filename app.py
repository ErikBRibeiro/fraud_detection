from flask import Flask, request, render_template
from tensorflow.keras.models import load_model
import numpy as np
import joblib
import pandas as pd

app = Flask(__name__)

# Carrega seu modelo
modelo = load_model('my_model.keras')

# Carrega os objetos de pré-processamento
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extrai os dados do formulário
        dados = [
            int(request.form['live']),
            float(request.form['valor']),
            float(request.form['odd']),
            int(request.form['cashouted']),
        ]

        # Configuração inicial do DataFrame
        client_bet = {
            'cliente': [508684, 288933, 541360], 
            'live': [dados[0],dados[0],dados[0]], 
            'valor': [dados[1],dados[1],dados[1]], 
            'odd': [dados[2],dados[2],dados[2]],
            'saldo': [0,0,0], 
            'status': [1,1,1], 
            'cashouted': [dados[3],dados[3],dados[3]], 
            'avg_bet_amount': [1816.366016,1620.77389,227.39495],
            'median_bet_amount': [1375.0,1387.5,62.5],
            'win_rate': [0.568421,0.465116,0.637975]
        }

        for i in range(len(client_bet['cliente'])):
            client_bet['saldo'][i] = client_bet['valor'][i] * client_bet['odd'][i]

        df = pd.DataFrame(data=client_bet)
        df = df.drop('cliente', axis=1)
        numerical_cols = ['valor', 'odd', 'saldo', 'avg_bet_amount', 'median_bet_amount']
        # Aplica a normalização e o PCA
        df[numerical_cols] = scaler.transform(df[numerical_cols])
        X_pca = pca.transform(df)

        # Realiza a predição
        predictions = modelo.predict(X_pca)
        
        print("Dataframe before transformations:", df)
        print("Dataframe after PCA:", X_pca)
        print("Predictions:", predictions)
        
        resultados = {}
        clientes = ['Fred', 'Pedro', 'Lera']
        for i, cliente in enumerate(clientes):
            if predictions[i] > 0.5:  # Ajuste conforme a lógica do seu modelo
                resultados[cliente] = f"If client {cliente} does that bet, it would be flagged as fraud."
            else:
                resultados[cliente] = f"If client {cliente} does that bet, it would not be flagged as fraud."
        print("Resultados:", resultados)
        # Retorna os resultados
        return render_template('resultado.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
