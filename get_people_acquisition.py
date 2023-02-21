import pandas as pd
import numpy as np

def get_people(cons_file, email_file, sub_file):
    # read in data
    cons = pd.read_csv(cons_file)
    cons_email = pd.read_csv(email_file)
    cons_sub = pd.read_csv(sub_file)

    # join tables
    cons_temp = cons.merge(cons_email, on = 'cons_id', suffixes = ('_cons', '_email'))
    cons_all = cons_temp.merge(cons_sub, on = 'cons_email_id', suffixes = (None, '_sub'))

    # filter for chapter_id of 1
    cons_one = cons_all[(cons_all['chapter_id'] == 1) | (cons_all['chapter_id'] == None)]

    # filter for primary emails
    cons_one_prim = cons_one[cons_one['is_primary'] == 1]

    # create final df
    final = pd.DataFrame()
    final['email'] = cons_one_prim.email
    final['code'] = cons_one_prim.subsource 
    final['is_unsub'] = np.where(cons_one_prim.isunsub == 1.0, True, False) # convert to boolean
    final['created_dt'] = pd.to_datetime(cons_one_prim.create_dt_cons)
    final['updated_dt'] = pd.to_datetime(cons_one_prim.modified_dt_cons)

    # write people.csv
    final.to_csv('people.csv', index = False)

    return final

def get_acquisitions():
    pass

def main():
    cons_filename = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv'
    email_filename = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv'
    cons_filename = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv'
    people = get_people(cons_filename, email_filename, cons_filename)
    get_acquisitions(people)

if __name__ == '__main__':
    main()