import sympy as sp
from flask import Flask, render_template, request, jsonify
from sympy import sin, cos
import numpy as np
import math


e = math.e
print(e)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/laplacian", methods=['POST'])
def laplacian():
    lpexp = request.form['lpexp']
    if lpexp:
        wrt = ['x', 'y', 'z'] ##temporary
        result = 0
        for item in wrt:
            print(item)
            lp = (sp.diff(sp.diff(lpexp, sp.symbols(item)), sp.symbols(item))) ## temp
            print(lp)
            result = result + lp
            print(result)
            lp = result
            print(lp)
        lpexp = str(lpexp)
        lp = str(lp)
        lpexp = lpexp.replace('**', '^')
        lp = lp.replace('**', '^')
        return render_template('index.html', lp=lp, lpexp=lpexp)
    else:
        return render_template('index.html', error='N/A')


@app.route('/derivative', methods=['POST'])
def derivative():
    exp = request.form['expression']
    exp = exp.replace('e', 'E')
    wrt = request.form['wrt']
    num = request.form.get('num')

    interval = np.arange(1, (int(num)+1), 1)
    for x in interval:
        newderivative = str(sp.diff(exp, sp.symbols(wrt), x))
        print("Interval:", x, ":", newderivative)

    print('final:', newderivative)

    def numtoword(n):
        if 10 <= n%100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n%10, 'th')
        return str(n) + suffix

    exp = exp.replace('**', '^')
    exp = exp.replace('*', '')
    newderivative = newderivative.replace('**', '^')
    newderivative = newderivative.replace('*', '')

    return render_template('index.html', derivative=str(newderivative), wrt=wrt, expression=exp, numderivatives=numtoword(int(num)))


@app.route('/vectorlaplacian', methods=['POST'])
def vectorlaplacian():
    vector = request.form['vlap']
    initialv = vector
    if vector:        
################################
        vector = vector.replace('e', 'E')
        ##vector = vector.replace('(', '')
        vector = vector.replace(' ', '')
        ##vector = vector.replace(')', '')
        vector = vector.split(',')
#################################
## needs to loop through each component of the vector (loop)
    ## then needs to take a partial derivative with respect to each variable (loop)
    ## take each partial derivative and make a sum of each to be the total partial derivative for each component of vecvtor
## Then needs to arrange each partial derivative into a vector (use append)
        dimension = len(vector)
        wrt = ['x', 'y', 'z']
        count = 0
        laplacian = 0
        resultantvector = []
#################################### Looping through each component of vector
        for item in vector:
            print('First for loop, componeent =', item)
            interval = len(wrt)
            print('Amount of inner loops needed for partial derivates for this component:', interval)
            totalsecondderr = 0
            for item2 in wrt:
                itemwrt = wrt[count]      
                print('COMPONENT:', item)
                print('Taking derivatives with respect to:', item2)
                derr = sp.diff(item, sp.symbols(item2))
                print("First Derivative", derr)
                secondderr = sp.diff(derr, sp.symbols(item2))
                totalsecondderr = totalsecondderr + secondderr
                print('Second Derivative (WRTX)', secondderr)
            resultantvector.append(totalsecondderr)
            count = count + 1
            laplacian = laplacian + secondderr
        print('Final Laplacian:', laplacian)
        print('Laplacian vector:', resultantvector)
        print('Input was a', dimension, 'dimensional vector.')
        return render_template('index.html', laplacian=str(resultantvector), laplacianexpression=initialv)

        
    else: 
        return render_template('index.html', error='N/A')