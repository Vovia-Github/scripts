import csv
import subprocess

def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def create_project(project_id, project_name):
    print(f"Creating project: {project_name} with ID: {project_id}")
    run_command(["gcloud", "projects", "create", project_id, "--name", project_name])
    run_command(["gcloud", "config", "set", "project", project_id])

def create_dataset(project_id, dataset):
    if dataset:
        print(f"Creating dataset: {dataset} in project: {project_id}")
        run_command(["bq", "mk", "--dataset", f"{project_id}:{dataset}"])

def create_table(project_id, dataset, table):
    if table:
        print(f"Creating schema-less table: {table} in dataset: {dataset}")
        # Creating an empty table without a schema
        run_command(["bq", "mk", "--table", f"{project_id}:{dataset}.{table}"])

csv_file = 'projects.csv'  # Update with your CSV file path

with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        create_project(row['project_id'], row['project_name'])
        for dataset in [row['dataset1'], row['dataset2'], row['dataset3']]:
            create_dataset(row['project_id'], dataset)
        for table in [row['table1'], row['table2']]:
            # Assuming the table belongs to the first dataset, modify as needed
            create_table(row['project_id'], row['dataset1'], table)

print("Script execution completed.")
