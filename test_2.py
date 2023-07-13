import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Generate sample data
jobs = [
    {'JobID': 'Job1', 'ScheduledDate': datetime.today(), 'Status': 'Completed', 'RecordsProcessed': 1000,
     'ExecutionTime': '00:30:15', 'StartTime': datetime.now() - timedelta(minutes=30), 'EndTime': datetime.now()},
    {'JobID': 'Job2', 'ScheduledDate': datetime.today(), 'Status': 'Failed', 'RecordsProcessed': 500,
     'ExecutionTime': '00:20:45', 'StartTime': datetime.now() - timedelta(minutes=45), 'EndTime': datetime.now()},
    {'JobID': 'Job3', 'ScheduledDate': datetime.today() - timedelta(days=1), 'Status': 'Not Scheduled', 'RecordsProcessed': 0,
     'ExecutionTime': 'N/A', 'StartTime': 'N/A', 'EndTime': 'N/A'},
    {'JobID': 'Job4', 'ScheduledDate': datetime.today(), 'Status': 'Completed', 'RecordsProcessed': 2000,
     'ExecutionTime': '01:15:30', 'StartTime': datetime.now() - timedelta(hours=1), 'EndTime': datetime.now()},
    {'JobID': 'Job5', 'ScheduledDate': datetime.today(), 'Status': 'Completed', 'RecordsProcessed': 1500,
     'ExecutionTime': '00:45:10', 'StartTime': datetime.now() - timedelta(minutes=50), 'EndTime': datetime.now()}
]

# Convert data to DataFrame
df = pd.DataFrame(jobs)

# Calculate summary metrics
total_jobs = len(df)
scheduled_jobs = len(df[df['ScheduledDate'].dt.date == datetime.today().date()])
completed_jobs = len(df[df['Status'] == 'Completed'])
failed_jobs = len(df[df['Status'] == 'Failed'])
not_scheduled_jobs = len(df[df['Status'] == 'Not Scheduled'])
total_records_processed = df['RecordsProcessed'].sum()

selected_date = st.date_input('Select a date', pd.to_datetime('today').date())

# Create graph for job status
status_data = df['Status'].value_counts()
status_labels = status_data.index.tolist()
status_values = status_data.values.tolist()
status_colors = ['green', 'red', 'gray']
status_fig = go.Figure(data=[go.Pie(labels=status_labels, values=status_values, hole=.4)])
status_fig.update_traces(marker=dict(colors=status_colors))
status_fig.update_layout(title='Job Status')

# Create graph for job execution time
execution_data = df[df['Status'] == 'Completed']
execution_times = [datetime.strptime(time, '%H:%M:%S').time() for time in execution_data['ExecutionTime']]
execution_fig = go.Figure(data=[go.Histogram(x=execution_times, nbinsx=10)])
execution_fig.update_layout(title='Job Execution Time')

# Display the report
st.title('Batch Summary Report')

# Display overall metrics as a table with highlighting
st.header('Overall Metrics')
metrics_data = {
    'Metric': ['Total Jobs', 'Scheduled Jobs for Today', 'Completed Jobs', 'Failed Jobs', 'Not Scheduled Jobs', 'Total Records Processed'],
    'Value': [total_jobs, scheduled_jobs, completed_jobs, failed_jobs, not_scheduled_jobs, total_records_processed]
}
metrics_df = pd.DataFrame(metrics_data)

# Create a Styler object to apply highlighting to the table
highlighted_metrics_df = metrics_df.style.applymap(lambda x: 'background-color: red' if x == failed_jobs else '')

# Display the table with highlighting
st.table(highlighted_metrics_df)



# Display graphs
st.header('Job Metrics')
st.plotly_chart(status_fig, use_container_width=True)
st.plotly_chart(execution_fig, use_container_width=True)

# Display job details
st.header('Job Details')
st.dataframe(df, width=800)  # Adjust the width to fit the page

