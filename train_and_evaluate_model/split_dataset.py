import pandas as pd


if __name__ == '__main__':
    
    # Load the full CSV file
    df = pd.read_csv('../data/cx_logd.csv.gz', delimiter='\t')

    # Split the data into training and validation sets
    validation_set = df.sample(n=100000, random_state=898124)   # 100,000 records for validation
    training_set = df.drop(validation_set.index)                # Remaining records for training

    # Save the sets to new CSV files
    validation_set.to_csv('validation_set.csv.gz', index=False, sep='\t')
    training_set.to_csv('training_set.csv.gz', index=False, sep='\t')
    