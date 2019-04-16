from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField, SelectField
import sys
import time
import serial.tools.list_ports
from serial import Serial
from flask_bootstrap import Bootstrap

# App config.
DEBUG = True
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    angulo = IntegerField('Angulo:')
    name = IntegerField('name:')
    passo = IntegerField('Passo:')
    # listaPortas = serial.tools.list_ports.comports()
    # conectadas = []
    # for p in listaPortas:
    #     conectadas.append((p.device, p.device))
    # print(conectadas)
    # portas = SelectField('Portas:', choices=conectadas)
    # portas = SelectField('Portas:', choices=[('thais', 'Thais'), ('leonardo', 'Leonardo')])

@app.route('/', methods=['GET'])
def principal():
    form = ReusableForm(request.form)
    listaPortas = serial.tools.list_ports.comports()
    conectadas = []
    for p in listaPortas:
        conectadas.append((p.device, p.device))
    # print(conectadas)
    return render_template('interface.html', form=form, portas=conectadas)

@app.route('/', methods=['POST'])
def principalPost():
    result = request.form
    
    for key, value in result.items():
        if(key == 'portas'):
            porta = value
        if(key == 'submit'):
            botao = value
        if(key == 'valor'):
            valor = value

    if(botao == 'calibrar'):
        serialConect = Serial(porta)
        serialConect.write(b'c\n')
        print("\nCalibrando\n")
    if(botao == 'home'):
        serialConect = Serial(porta)
        serialConect.write(b'h\n')
        print("\nHome\n")
    if(botao == 'left'):
        serialConect = Serial(porta)
        serialConect.write(u'x-{}\n'.format(valor).encode())
        print("\nAndando "+valor+" para tras\n")
    if(botao == 'right'):
        serialConect = Serial(porta)
        serialConect.write(u'x{}\n'.format(valor).encode())
        print("\nAndando "+valor+" para frente")

    form = ReusableForm(request.form)
    listaPortas = serial.tools.list_ports.comports()
    conectadas = []
    for p in listaPortas:
        conectadas.append((p.device, p.device))
    # print(conectadas)
    return render_template('interface.html', form=form, portas=conectadas, passos=valor)

 
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)