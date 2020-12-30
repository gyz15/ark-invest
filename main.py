# save a local file, then compare both on latest and local on
# Share difference, weight difference,
import pandas as pd


def get_data():
    # use request.get to get the file from ark fund website
    # todo check see is same as local or not before carrying following steps
    pass

def handle_data()
    original_data = data = pd.read_csv('.\ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv',parse_dates=[0],dayfirst=True)
    new_data = pd.read_csv(".\LATEST_ARK_FOR_TESTING.csv",parse_dates=[0],dayfirst=True)
    new_data.fillna(0,inplace=True)
    original_data.fillna(0,inplace=True)
    processed_data = process_add_remove(new_data,original_data)
    return processed_data

def process_add_remove(new_data,original_data)
    sending_data = {"added":[],"removed":[],"buying":[],"selling":[]}
    added_list = []
    removed_list = []
    for company_name in new_data.company:
        if not any(original_data.company.values==company_name):
            added_list.append(company_name)
            # todo use another function to perform add data to list
            added_list.append(new_data.loc[new_data.company==company_name]['ticker'].values[0])
            added_list.append(new_data.loc[new_data.company==company_name]['shares'].values[0])
            added_list.append(new_data.loc[new_data.company==company_name]['weight(%)'].values[0])
            sending_data['added'].append(added_list)
            added_list = []
            new_data = new_data[new_data.company != company_name]
    for company_name in original_data.company:
        if not any(new_data.company.values==company_name):
            removed_list.append(company_name)
            removed_list.append(original_data.loc[original_data.company==company_name]['ticker'].values[0])
            removed_list.append(original_data.loc[original_data.company==company_name]['shares'].values[0])
            removed_list.append(original_data.loc[original_data.company==company_name]['weight(%)'].values[0])
            sending_data['removed'].append(removed_list)
            removed_list = []
            original_data = original_data[original_data.company != company_name]

    final_data = check_buy_sell(sending_data,new_data,original_data)
    return final_data

def check_buy_sell(sending_data,new_data,original):
    buying_list = []
    selling_list = []
    for company_name in new_data.company:
        new_shares = new_data.loc[new_data.company==company_name]['shares'].values[0]
        old_shares = original_data.loc[original_data.company==company_name]['shares'].values[0]
        if new_shares > old_shares:
            buying_list.append(new_data.loc[new_data.company==company_name]['company'].values[0])
            buying_list.append(new_data.loc[new_data.company==company_name]['shares'].values[0])
            # increase how much on shares
            difference = (new_data.loc[new_data.company==company_name]['shares'].values[0]) - (original_data.loc[original_data.company==company_name]['shares'].values[0])
            buying_list.append(difference)
            buying_list.append(abs(difference)/(original_data.loc[original_data.company==company_name]['shares'].values[0]))
            buying_list.append(new_data.loc[new_data.company==company_name]['weight(%)'].values[0])
            percent_difference = (new_data.loc[new_data.company==company_name]['weight(%)'].values[0]) - (original_data.loc[original_data.company==company_name]['weight(%)'].values[0])
            buying_list.append(percent_difference)
            sending_data['buying'].append(buying_list)
            buying_list = []
        elif new_shares < old_shares:
            selling_list.append(new_data.loc[new_data.company==company_name]['company'].values[0])
            selling_list.append(new_data.loc[new_data.company==company_name]['shares'].values[0])
            # increase how much on shares
            difference = (new_data.loc[new_data.company==company_name]['shares'].values[0]) - (original_data.loc[original_data.company==company_name]['shares'].values[0])
            selling_list.append(difference)
            selling_list.append(abs(difference)/(original_data.loc[original_data.company==company_name]['shares'].values[0]))
            selling_list.append(new_data.loc[new_data.company==company_name]['weight(%)'].values[0])
            percent_difference = (new_data.loc[new_data.company==company_name]['weight(%)'].values[0]) - (original_data.loc[original_data.company==company_name]['weight(%)'].values[0])
            selling_list.append(percent_difference)
            sending_data['selling'].append(selling_list)
            selling_list = []
        return sending_data