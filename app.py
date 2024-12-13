# app.py
from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase
from werkzeug.utils import secure_filename
import pandas as pd
import os

app = Flask(__name__)


driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "123456789"))

@app.route('/')
def index():
    with driver.session() as session:
        transactions = session.run("MATCH (t:Transaction) RETURN t").data()
    return render_template('index.html', transactions=transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        vendor_number = request.form['vendor_number']
        transaction_amount = request.form['transaction_amount']
        transaction_type = request.form['transaction_type']

      
        with driver.session() as session:
            session.run(
                "CREATE (t:Transaction {transaction_id: $transaction_id, vendor_number: $vendor_number, transaction_amount: $transaction_amount, transaction_type: $transaction_type})",
                transaction_id=int(transaction_id),
                vendor_number=int(vendor_number),
                transaction_amount=int(transaction_amount),
                transaction_type=transaction_type
            )
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    
    with driver.session() as session:
        session.run(
            """
            MATCH (t:Transaction {transaction_id: $transaction_id})
            DELETE t
            """,
            transaction_id=transaction_id  
        )
    return redirect(url_for('index'))



@app.route('/modify_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def modify_transaction(transaction_id):
    
    with driver.session() as session:
        transaction_result = session.run(
            """
            MATCH (t:Transaction {transaction_id: $transaction_id})
            RETURN t
            """,
            transaction_id=transaction_id  
        ).single()

    if not transaction_result:
        return redirect(url_for('index'))

    transaction = transaction_result['t']

    if request.method == 'POST':
        vendor_number = request.form['vendor_number']
        transaction_amount = request.form['transaction_amount']
        transaction_type = request.form['transaction_type']

        with driver.session() as session:
            session.run(
                """
                MATCH (t:Transaction {transaction_id: $transaction_id})
                SET t.vendor_number = $vendor_number,
                    t.transaction_amount = $transaction_amount,
                    t.transaction_type = $transaction_type
                """,
                transaction_id=transaction_id,  
                vendor_number=int(vendor_number),
                transaction_amount=int(transaction_amount),
                transaction_type=transaction_type
            )
        return redirect(url_for('index'))

    return render_template('modify_transaction.html', transaction=transaction)



if __name__ == '__main__':
    app.run(debug=True, port=5001)