from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Configuração da base de dados
DB_PATH = os.path.join('data', 'pontos.csv')
if not os.path.exists('data'): os.makedirs('data')
if not os.path.exists(DB_PATH):
    pd.DataFrame(columns=['ID', 'Data', 'Hora', 'Tipo']).to_csv(DB_PATH, index=False)

# Credenciais de Teste
USUARIOS = {
    "101": "777",
    "admin": "master123"
}

# --- ROTA DE LOGIN ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')

        # Verificação e Redirecionamento
        if user_id in USUARIOS and USUARIOS[user_id] == password:
            if user_id == "admin":
                return redirect(url_for('admin_page')) # Link para Admin
            else:
                return redirect(url_for('empregado_page', user_id=user_id)) # Link para Empregado
        
    return render_template('login.html')

# --- PÁGINA DO EMPREGADO ---
@app.route('/empregado/<user_id>')
def empregado_page(user_id):
    return render_template('painel.html', user_id=user_id)

# --- PÁGINA DO ADMIN ---
@app.route('/admin')
def admin_page():
    df = pd.read_csv(DB_PATH)
    dados = df.to_dict(orient='records')
    return render_template('admin.html', pontos=dados[::-1])

# --- LÓGICA DE REGISTO ---
@app.route('/registrar/<user_id>/<tipo>')
def registrar(user_id, tipo):
    df = pd.read_csv(DB_PATH)
    novo = {
        'ID': user_id, 
        'Data': datetime.now().strftime("%d/%m/%Y"), 
        'Hora': datetime.now().strftime("%H:%M:%S"), 
        'Tipo': tipo
    }
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
    df.to_csv(DB_PATH, index=False)
    return redirect(url_for('empregado_page', user_id=user_id))

@app.route('/exportar')
def exportar():
    return send_file(DB_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)