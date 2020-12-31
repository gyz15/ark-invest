# save a local file, then compare both on latest and local on
# Share difference, weight difference,
import pandas as pd
import requests
import os


URL = {
    "ARKK":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv",
    "ARKQ":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv",
    "ARKW":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "ARKG":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv",
    "ARKF":"https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv",
}

def main():
    for key,value in URL.items():
        dict_data = get_data(key,value)
        print(f"Getting data for {key} from {value}. Please wait...")
        print (dict_data)
        # todo replace data here after get all dict_data
        # with open of old, with open of new, write old to new
def get_data(key,url):
    with requests.get(url,stream=True) as r:
        with open (f".\DATA\LATEST_{key}_FOR_TESTING.csv","wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print("Finished saving data to local, preparing to compare data between previous and latest...")
    changed_data = handle_data(key)
    return changed_data

def handle_data(key):
    original_data = data = pd.read_csv(f'.\DATA\PREVIOUS_DAY_{key}.csv',parse_dates=[0],dayfirst=True)
    new_data = pd.read_csv(f".\DATA\LATEST_{key}_FOR_TESTING.csv",parse_dates=[0],dayfirst=True)
    data_to_be_saved = new_data.copy()
    new_data.fillna(0,inplace=True)
    original_data.fillna(0,inplace=True)
    processed_data = process_add_remove(new_data,original_data)
    print("Finish processing data, saving latest file and deleting old file...")
    if os.path.exists(f".\DATA\PREVIOUS_DAY_{key}.csv"):
        print("Previous file found. Deleting it now")
        os.remove(f".\DATA\PREVIOUS_DAY_{key}.csv")
    else:
        pass
        print("Error, can't find previous file")
        # notify admin that something went wrong
    print("Saving current data for tommorow's")
    data_to_be_saved.to_csv(path_or_buf=f'.\DATA\PREVIOUS_DAY_{key}.csv',index=False)
    print("Data saved.")
    return processed_data

def process_add_remove(new_data,original_data):
    sending_data = {"added":[],"removed":[],"buying":[],"selling":[]}
    added_list = []
    removed_list = []
    print("Checking for whether any company has been removed or added.")
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

def check_buy_sell(sending_data,new_data,original_data):
    buying_list = []
    selling_list = []
    print("Checking if fund manager had bought more or sold the shares they're holding")
    for company_name in new_data.company:
        new_shares = new_data.loc[new_data.company==company_name]['shares'].values[0]
        old_shares = original_data.loc[original_data.company==company_name]['shares'].values[0]
        if new_shares > old_shares:
            buying_list.append(new_data.loc[new_data.company==company_name]['company'].values[0])
            buying_list.append(new_data.loc[new_data.company==company_name]['ticker'].values[0])
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
            selling_list.append(new_data.loc[new_data.company==company_name]['ticker'].values[0])
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


if __name__=='__main__':
    main()