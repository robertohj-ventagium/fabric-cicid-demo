# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "event_stream": {
# META       "known_event_streams": []
# META     }
# META   }
# META }

# CELL ********************

! python --version
! pip install azure-eventhub==5.11.5 --upgrade --force --quiet
! pip install semantic-link-labs --quiet

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": true
# META }

# MARKDOWN ********************

# # Banking Loan Clickstream Fraud Analytics
# ## Synthetic Data Generator for Real-time Streaming

# CELL ********************

import json
from azure.eventhub import EventHubProducerClient, EventData
import os
import socket
import uuid
import datetime
import random
from random import randrange
import time
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List
import sempy_labs as labs
import sempy_labs.variable_library as sempy_variable_library
import sempy_labs.eventstream as sempy_eventstream

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

eventstream = "BankingLoanFraudStream"
eventstream_source_name = "CustomEndpoint-Source"

es_topology = sempy_eventstream.get_eventstream_topology(eventstream=eventstream)
es_source = es_topology[es_topology["Eventstream Source Name"] == eventstream_source_name]
es_source_id = es_source["Eventstream Source Id"].iloc[0]

es_source_connection = sempy_eventstream.get_eventstream_source_connection(eventstream=eventstream,source_id=es_source_id)
es_eventhub_name = es_source_connection["EventHub Name"].iloc[0]
es_eventhub_connstring = es_source_connection["Primary Connection String"].iloc[0]

producer = EventHubProducerClient.from_connection_string(conn_str=es_eventhub_connstring, eventhub_name=es_eventhub_name)

hostname = socket.gethostname()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Fraud detection parameters
FRAUD_INDICATORS = {
    'VERY_LOW_CREDIT_SCORE': 500,
    'VERY_HIGH_LOAN_AMOUNT': 500000,
    'RAPID_TRANSACTION_THRESHOLD': 2,  # seconds
    'SUSPICIOUS_CREDIT_SCORE_RANGE': (400, 550)
}

STATUSES = ['Document verification', 'Eligibility check', 'Confirmed']
COUNTRIES = ['USA', 'UK', 'Canada', 'Australia', 'Germany']
DEVICES = ['Mobile', 'Desktop', 'Tablet']

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

class BankingLoanDataGenerator:
    def __init__(self):
        self.customer_sessions = {}  # Track customer sessions for fraud detection
        self.last_timestamp = datetime.now()
    
    def generate_customer_id(self) -> str:
        """Generate unique customer ID"""
        return f"CUST_{uuid.uuid4().hex[:8].upper()}"
    
    def determine_fraud_flags(self, data: Dict) -> Dict:
        """Determine fraud indicators for a transaction"""
        fraud_flags = {
            'is_fraud_suspected': False,
            'fraud_reasons': []
        }
        
        # Very low credit score
        if data['credit_score'] < FRAUD_INDICATORS['VERY_LOW_CREDIT_SCORE']:
            fraud_flags['is_fraud_suspected'] = True
            fraud_flags['fraud_reasons'].append('VeryLowCreditScore')
        
        # Suspicious credit score range with high loan amount
        if FRAUD_INDICATORS['SUSPICIOUS_CREDIT_SCORE_RANGE'][0] <= data['credit_score'] <= FRAUD_INDICATORS['SUSPICIOUS_CREDIT_SCORE_RANGE'][1]:
            if data['loan_amount'] > 100000:
                fraud_flags['is_fraud_suspected'] = True
                fraud_flags['fraud_reasons'].append('SuspiciousScoreLoanMismatch')
        
        # Very high loan amount
        if data['loan_amount'] > FRAUD_INDICATORS['VERY_HIGH_LOAN_AMOUNT']:
            fraud_flags['is_fraud_suspected'] = True
            fraud_flags['fraud_reasons'].append('ExcessivelyHighLoanAmount')
        
        # Status sequence validation (should follow order)
        customer_id = data['customer_id']
        if customer_id in self.customer_sessions:
            last_status = self.customer_sessions[customer_id]['last_status']
            current_status = data['status']
            
            # Check if going backwards in workflow
            if STATUSES.index(current_status) < STATUSES.index(last_status):
                fraud_flags['is_fraud_suspected'] = True
                fraud_flags['fraud_reasons'].append('InvalidStatusSequence')
            
            # Check for rapid consecutive transactions
            last_timestamp = self.customer_sessions[customer_id]['last_timestamp']
            time_diff = (data['timestamp'] - last_timestamp).total_seconds()
            if time_diff < FRAUD_INDICATORS['RAPID_TRANSACTION_THRESHOLD']:
                fraud_flags['is_fraud_suspected'] = True
                fraud_flags['fraud_reasons'].append('RapidTransactions')
        
        # Update session
        self.customer_sessions[customer_id] = {
            'last_status': data['status'],
            'last_timestamp': data['timestamp']
        }
        
        return fraud_flags
    
    def generate_event(self, customer_id: str = None, force_fraud: bool = False) -> Dict:
        """Generate a single banking loan clickstream event"""
        if customer_id is None:
            customer_id = self.generate_customer_id()
        
        # Add random time gap
        self.last_timestamp += timedelta(seconds=random.randint(1, 30))
        
        credit_score = random.randint(300, 800)
        
        # If forcing fraud, generate suspicious data
        if force_fraud:
            if random.random() > 0.5:
                credit_score = random.randint(300, 550)  # Low score
            loan_amount = random.randint(450000, 1000000)  # Very high
        else:
            loan_amount = random.randint(10000, 300000)
        
        data = {
            'customer_id': customer_id,
            'transaction_id': str(uuid.uuid4()),
            'loan_amount': loan_amount,
            'status': random.choice(STATUSES),
            'credit_score': credit_score,
            'timestamp': datetime.now(), # self.last_timestamp, # self.last_timestamp is the original generator; for live demo, changed to actual 'now'
            'country': random.choice(COUNTRIES),
            'device_type': random.choice(DEVICES),
            'ip_address': f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge'])
        }
        
        # Add fraud flags
        fraud_info = self.determine_fraud_flags(data)
        data.update(fraud_info)
        
        return data
    
    def generate_batch(self, count: int = 10, fraud_percentage: float = 0.1) -> List[Dict]:
        """Generate a batch of events"""
        events = []
        fraud_count = int(count * fraud_percentage)
        
        for i in range(count):
            force_fraud = i < fraud_count
            events.append(self.generate_event(force_fraud=force_fraud))
        
        return events

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Polished version (more realistic with configurable variables)

import random
import time
import json
import pandas as pd
from datetime import datetime
from azure.eventhub import EventData

# ============================================================
# CONFIGURATION
# ============================================================

MAX_TRANSACTIONS_PER_BURST = 2500   # Maximum transactions generated per burst
BURST_INTERVAL_SECONDS = 1         # Wait time between bursts
FRAUD_RATE = 0.23                   # x% forced-fraud probability

MAX_BURSTS = None                   # None = run indefinitely
# MAX_BURSTS = 10                   # Example: stop after 10 bursts

KEEP_LAST_EVENTS = 5000             # Number of events retained in DataFrame

# ============================================================
# INITIALIZE
# ============================================================

generator = BankingLoanDataGenerator()

events = []
event_count = 0
burst_count = 0

print("Connecting to EventHub...")
print("Streaming banking transactions...")
print(f"Max transactions per burst : {MAX_TRANSACTIONS_PER_BURST}")
print(f"Burst interval             : {BURST_INTERVAL_SECONDS} seconds")
print(f"Fraud rate                 : {FRAUD_RATE:.1%}")
print("Press Stop/Interrupt to end.\n")


# ============================================================
# MAIN STREAMING LOOP
# ============================================================

while MAX_BURSTS is None or burst_count < MAX_BURSTS:

    burst_count += 1

    burst_start = time.time()

    # --------------------------------------------------------
    # Determine number of transactions for this burst
    # --------------------------------------------------------

    transactions_this_burst = random.randint(
        int(MAX_TRANSACTIONS_PER_BURST * 0.5),
        MAX_TRANSACTIONS_PER_BURST
    )

    print(
        f"\n{'=' * 70}\n"
        f"Burst #{burst_count} | "
        f"Generating {transactions_this_burst:,} transactions..."
    )

    burst_events = []

    # --------------------------------------------------------
    # Generate transactions
    # --------------------------------------------------------

    for _ in range(transactions_this_burst):

        event = generator.generate_event(
            force_fraud=(random.random() < FRAUD_RATE)
        )

        # Use actual generation time
        event["generated_at"] = datetime.now()

        burst_events.append(event)

    # --------------------------------------------------------
    # Send generated events to Event Hub
    #
    # Event Hub automatically handles the maximum message
    # size of each EventData batch. If a batch fills up,
    # send it and create a new one.
    # --------------------------------------------------------

    event_batch = producer.create_batch()

    burst_fraud_count = 0
    sent_this_burst = 0

    for event in burst_events:

        if event.get("is_fraud_suspected"):
            burst_fraud_count += 1

        event_json = json.dumps(event, default=str)

        try:
            event_batch.add(EventData(event_json))

        except ValueError:
            # Current Event Hub batch is full.
            producer.send_batch(event_batch)

            sent_this_burst += len(event_batch)

            event_batch = producer.create_batch()
            event_batch.add(EventData(event_json))

    # Send remaining events in the batch
    if len(event_batch) > 0:

        producer.send_batch(event_batch)

        sent_this_burst += len(event_batch)

    # --------------------------------------------------------
    # Store events locally for DataFrame
    # --------------------------------------------------------

    events.extend(burst_events)

    if len(events) > KEEP_LAST_EVENTS:
        events = events[-KEEP_LAST_EVENTS:]

    event_count += transactions_this_burst

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    burst_elapsed = time.time() - burst_start

    throughput = (
        transactions_this_burst / burst_elapsed
        if burst_elapsed > 0
        else 0
    )

    print(
        f"✓ Burst #{burst_count} sent\n"
        f"  Transactions : {transactions_this_burst:,}\n"
        f"  Fraud        : {burst_fraud_count:,} "
        f"({burst_fraud_count / transactions_this_burst:.1%})\n"
        f"  Generation + ingestion time : {burst_elapsed:.2f} sec\n"
        f"  Throughput   : {throughput:,.0f} events/sec\n"
        f"  Total events : {event_count:,}"
    )

    # --------------------------------------------------------
    # Wait before next burst
    # --------------------------------------------------------

    print(
        f"Waiting {BURST_INTERVAL_SECONDS} seconds "
        f"before next burst..."
    )

    time.sleep(BURST_INTERVAL_SECONDS)


# ============================================================
# FINAL DATAFRAME
# ============================================================

print("\nStreaming stopped.")

df = pd.DataFrame(events)

print(f"Events retained locally: {len(df):,}")

df

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

