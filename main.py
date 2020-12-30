# save a local file, then compare both on latest and local on
# Share difference, weight difference,
import pandas as pd


def get_data():
    # use request.get to get the file from ark fund website
    # check see is same as local or not before carrying following steps
    pass

def handle_data()
    original_data = data = pd.read_csv('.\ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv',parse_dates=[0],dayfirst=True)
    new_data = pd.read_csv(".\LATEST_ARK_FOR_TESTING.csv",parse_dates=[0],dayfirst=True)
    new_data.fillna(0,inplace=True)
    original_data.fillna(0,inplace=True)
    process_add_remove(new_data,original_data)

def process_add_remove(new_data,original_data)
    final_data = {"added":[],"removed":[]}
    added_list = []
    removed_list = []
    for company_name in new_data.company:
        if not any(original_data.company.values==company_name):
            added_list.append(company_name)
            added_list.append(new_data.loc[new_data.company==company_name]['ticker'].values[0])
            added_list.append(new_data.loc[new_data.company==company_name]['shares'].values[0])
            added_list.append(new_data.loc[new_data.company==company_name]['weight(%)'].values[0])
            final_data['added'].append(added_list)
            added_list = []
            new_data = new_data[new_data.company != company_name]
    for company_name in original_data.company:
        if not any(new_data.company.values==company_name):
            removed_list.append(company_name)
            removed_list.append(original_data.loc[original_data.company==company_name]['ticker'].values[0])
            removed_list.append(original_data.loc[original_data.company==company_name]['shares'].values[0])
            removed_list.append(original_data.loc[original_data.company==company_name]['weight(%)'].values[0])
            final_data['removed'].append(removed_list)
            removed_list = []
            original_data = original_data[original_data.company != company_name]