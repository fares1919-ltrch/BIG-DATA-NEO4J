import numpy as np
import random
import pandas as pd
from neo4j import GraphDatabase


transaction_id = [i for i in range(1, 51)]  
vendor_number = np.random.randint(low=1, high=2500, size=(50,))  
transaction_amount = np.random.randint(low=20, high=1250000, size=(50))  
transaction_types = ['cash_withdrawl', 'cash_deposit', 'transfer_domestic', 'transfer_international']


random_integers = [random.randint(0, 3) for _ in range(50)]
transaction_list = [transaction_types[i] for i in random_integers]

transaction_data = {
    "transaction_ID": transaction_id,
    "vendor_number": list(vendor_number),
    "transaction_amount": list(transaction_amount),
    "transaction_type": transaction_list,
}

transaction_DataFrame = pd.DataFrame(transaction_data)


print(transaction_DataFrame.head(1))


transaction_list = transaction_DataFrame.values.tolist()
transaction_execution_commands = []

for transaction in transaction_list:
    
    neo4j_create_statement = (
        f"CREATE (t:Transaction {{"
        f"transaction_id: {transaction[0]}, "
        f"vendor_number: {transaction[1]}, "
        f"transaction_amount: {transaction[2]}, "
        f"transaction_type: '{transaction[3]}'}})"
    )
    transaction_execution_commands.append(neo4j_create_statement)


def execute_transactions(transaction_execution_commands):
    
    driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "123456789"))
    with driver.session() as session:  
        for command in transaction_execution_commands:
            session.run(command)
    driver.close()  


execute_transactions(transaction_execution_commands)
from neo4j import GraphDatabase
fetch_all_transactions_query = "MATCH (t:Transaction) RETURN t"

def execute_transactions(query, return_result=False):
    database_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "123456789"))
    with database_connection.session() as session:
        transaction_result = session.run(query)
        if return_result:
            return [record["t"] for record in transaction_result]



all_transactions = execute_transactions(fetch_all_transactions_query, True)

print("All Transactions:")
for transaction in all_transactions:
    
    for key, value in transaction.items():
        print(f"{key}: {value}")
    print("-" * 30) 