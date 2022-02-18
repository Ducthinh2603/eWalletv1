import os
import sqlite3

DBPATH = "/Users/thdg/PycharmProjects/eWalletv1/ewallet.db"

with sqlite3.connect(DBPATH) as conn:
    account = '''
        CREATE TABLE IF NOT EXISTS Account (
        account_id CHAR(200),
        account_type TEXT,
        balance FLOAT DEFAULT 0,
        PRIMARY KEY (account_id)
        );
        '''
    merchant = '''
        CREATE TABLE IF NOT EXISTS Merchant (
        merchant_id CHAR(200),
        merchant_name CHAR(200),
        merchant_url TEXT, 
        account_id TEXT,
        api_key TEXT,
        PRIMARY KEY (merchant_id),
        FOREIGN KEY (account_id) REFERENCES Account (account_id)
        );
        '''
    transaction = '''
        CREATE TABLE IF NOT EXISTS Playbook (
        transaction_id CHAR(200), 
        merchant_id CHAR(200),
        income_account TEXT, 
        outcome_account TEXT, 
        amount REAL NOT NULL,
        extraData TEXT,
        status INT,
        PRIMARY KEY (transaction_id),
        FOREIGN KEY (income_account) REFERENCES Account (account_id),
        FOREIGN KEY (outcome_account) REFERENCES Account (account_id),
        FOREIGN KEY (merchant_id) REFERENCES Merchant (merchant_id)
        );
        '''
    c = conn.cursor()
    c.execute(account)
    c.execute(merchant)
    c.execute(transaction)
