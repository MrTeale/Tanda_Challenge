import pandas as pd
from collections import Counter
from pprint import pprint
import argparse

# Variables
settings_default_path = './Tanda_Settings_Info.csv'
organisation_settings_path = './Tanda_Organisation_Settings.csv'
USERS_CHANGE_X_DEFAULT = 50


def load_csv(filepath):
    '''Loads CSV files containing data

    Args:
        filepath (string): location of file

    Returns:
        df (pandas.DataFrame): dataframe containing the csv files data
    '''
    with open(filepath, 'r') as file:
        return pd.read_csv(file)


def type_switch(setting_type, value):
    types = {
        'Boolean': lambda value: True if 'True' == value or 'true' == value else False,
        'Numeric': lambda value: float(value),
        'Enumerative': lambda value: str(value)
    }
    return types[setting_type](value)


def percent_changed():
    ''' Analysis of the percentage of Users that change each settings
    '''
    default_df = load_csv(settings_default_path)
    organisation_df = load_csv(organisation_settings_path)

    percentage_df = pd.DataFrame(columns=['setting', 'percentage'])

    for column in list(organisation_df.columns.values):
        setting_default = default_df.loc[default_df['setting'] == column]
        data = organisation_df[column].tolist()

        total = 0
        different = 0
        default = type_switch(setting_default['data_type'].tolist()[0],
                              setting_default['default'].tolist()[0])

        for row in data:
            total += 1
            if row != default and row is not default:
                different += 1

        percentage_df = percentage_df.append({
            'setting': column,
            'percentage': round((different / total) * 100, 2)
        }, ignore_index=True)

    percentage_df = percentage_df.set_index('setting')
    percentage_df.to_csv('./part1.csv')


def change_x_percent(x_value):
    default_df = load_csv(settings_default_path)
    organisation_df = load_csv(organisation_settings_path)

    changed_amount = {}
    for column in list(organisation_df.columns.values):
        changed_amount[column] = 0

    for i, row in organisation_df.iterrows():
        cols_changed = {}
        changed = 0
        total = len(list(organisation_df.columns.values))

        for column in list(organisation_df.columns.values):
            setting_default = default_df.loc[default_df['setting'] == column]
            default = type_switch(setting_default['data_type'].tolist()[0],
                                  setting_default['default'].tolist()[0])

            data = type_switch(setting_default['data_type'].tolist()[0], row[column])

            if data != default and data is not default:
                changed += 1
                cols_changed[column] = 1

        if round((changed / total) * 100, 2) > x_value:
            changed_amount = dict(Counter(cols_changed) + Counter(changed_amount))

    distribution_df = pd.DataFrame.from_dict(changed_amount, orient='index')
    distribution_df.columns = ['count']
    distribution_df.index.name = 'setting'
    distribution_df.to_csv('./part2.csv')


def implicit_explicit():

    default_df = load_csv(settings_default_path)
    organisation_df = load_csv(organisation_settings_path)

    percentage_df = pd.DataFrame(columns=['type', 'percentage'])
    implicit_total = 0
    implicit_different = 0
    explicit_total = 0
    explicit_different = 0

    for column in list(organisation_df.columns.values):
        setting_default = default_df.loc[default_df['setting'] == column]
        data = organisation_df[column].tolist()
        setting_type = setting_default['impact'].tolist()[0]
        default = type_switch(setting_default['data_type'].tolist()[0],
                              setting_default['default'].tolist()[0])

        for row in data:
            if 'Implicit' in setting_type:
                implicit_total += 1
                if row != default and row is not default:
                    implicit_different += 1
            else:
                explicit_total += 1
                if row != default and row is not default:
                    explicit_different += 1

    percentage_df = percentage_df.append({
        'type': 'Implicit',
        'percentage': round((implicit_different / implicit_total) * 100, 2)
    }, ignore_index=True)

    percentage_df = percentage_df.append({
        'type': 'Explicit',
        'percentage': round((explicit_different / explicit_total) * 100, 2)
    }, ignore_index=True)

    percentage_df = percentage_df.set_index('type')
    percentage_df.to_csv('./part3.csv')


def affected_users(settings):

    default_df = load_csv(settings_default_path)
    organisation_df = load_csv(organisation_settings_path)

    total = 0
    affected = 0
    changed_affected = {}

    for column in list(organisation_df.columns.values):
        changed_affected[column] = 0

    for i, row in organisation_df.iterrows():
        total += 1
        setting_defaulted = False
        for setting in settings:
            setting_default = default_df.loc[default_df['setting'] == setting]
            
            default = type_switch(setting_default['data_type'].tolist()[0],
                                  setting_default['default'].tolist()[0])

            if row[setting] == default and row[setting] is default:
                setting_defaulted = True
                break

        if setting_defaulted is False:
            affected += 1

    changed_affected['input_settings'] = round((affected / total) * 100, 2)
    
    for i, row in organisation_df.iterrows():
        setting_defaulted = False
        for setting in settings:
            setting_default = default_df.loc[default_df['setting'] == setting]
            default = type_switch(setting_default['data_type'].tolist()[0],
                                  setting_default['default'].tolist()[0])

            value = row[column]
            if value == default or value is default:
                setting_defaulted = True
                break

        if setting_defaulted is False:
            for column in list(organisation_df.columns.values):
                setting_default = default_df.loc[default_df['setting'] == column]
                data = row[column]

                default = type_switch(setting_default['data_type'].tolist()[0],
                                      setting_default['default'].tolist()[0])

                if data != default and data is not default:
                    changed_affected[column] += 1

    for key, value in changed_affected.items():
        changed_affected[key] = round((value / i) * 100, 2)

    distribution_df = pd.DataFrame.from_dict(changed_affected, orient='index')
    distribution_df.columns = ['percentage']
    distribution_df.index.name = 'setting'
    distribution_df.to_csv('./part4.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-1', '--one', action='store_true',
                        help='percent_changed for each setting')
    parser.add_argument('-2', '--two', action='store_true',
                        help='percent_changed for each setting')
    parser.add_argument('-3', '--three', action='store_true',
                        help='percent_changed for each setting')
    parser.add_argument('-4', '--four', action='store_true',
                        help='percent_changed for each setting')

    args, rem_args = parser.parse_known_args()

    if args.one:
        percent_changed()
   
    if args.two:
        parser.add_argument('-p', '--percentage', type=float,
                            help='<Required> above percentage', required=True, default=USERS_CHANGE_X_DEFAULT)
        args = parser.parse_args(rem_args, namespace=args)
        change_x_percent(args.percentage)

    if args.three:
        implicit_explicit()

    if args.four:
        parser.add_argument('-s', '--setting', action='append',
                            help='<Required> Desired Settings', required=True)
        args = parser.parse_args(rem_args, namespace=args)
        affected_users(args.setting)
