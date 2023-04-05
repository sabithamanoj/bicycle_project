################################################################################
#       Home work task from Quality Match GmbH
###############################################################################
import json
import pandas as pd
import logging
from matplotlib import pyplot as plt
import seaborn as sns
import argparse

import os
import sys
sys.path.append(".")
import functions
from classes import annotation
from classes import reference


def main(anonymized_file, reference_file):

    # Log file to be saved in 'results' directory
    path = "../results"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print("The new directory 'results' is created!")
    from datetime import datetime
    now = datetime.now()
    date_time = now.strftime("%m%d%Y_%H%M%S")

    filename='../results/tasks' + date_time +'.log'
    logging.basicConfig(filename=filename, level=logging.INFO, filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)

    logging.info('Log file can be found in {}'.format(filename))

    # Convert anonymized json to pandas data frame
    logging.info('Converting anonymized json to Pandas Dataframe')
    with open(anonymized_file) as data_file:
        data = json.load(data_file)

    anonymized_data = pd.DataFrame()
    for task in data['results']['root_node']['results'].keys():
        tmp_df = pd.json_normalize(data['results']['root_node']['results'][task]['results'])
        anonymized_data = pd.concat([anonymized_data, tmp_df], ignore_index=True )


    logging.info('The shape of anonymized data: {}'.format(anonymized_data.shape))
    logging.info('The columns in anonymized_data: {}'.format(anonymized_data.columns))

    #Define object of class
    obj_annotation_crowd = annotation.AnnotationCrowd(anonymized_data)

    ###################################################################
    #                       Tasks1
    ###################################################################
    # a. How many annotators did contribute to the dataset?
    ##################################################################
    logging.info('How many annotators did contribute to the dataset?')
    num_of_annotators = obj_annotation_crowd.get_num_of_annotators()
    logging.info('Number of annotators : {}'.format(num_of_annotators))


    ####################################################################
    # b. What are the average, min and max annotation times (durations)?
    ###################################################################
    logging.info('What are the average, min and max annotation times (durations)?')
    statistics = obj_annotation_crowd.get_duration_statistics_summary()
    logging.info('Average duration_ms : {}'.format(statistics['mean']))
    logging.info('Minimum duration_ms : {}'.format(statistics['min']))
    logging.info('Maximum duration_ms : {}'.format(statistics['max']))

    # Find outliers in the data
    # lowerbound = Q1- 1.5 * IQR, Upperbound : Q3 + 1.5*IQR
    lower_bound = statistics['Q1'] - (1.5 * statistics['IQR'])
    upper_bound = statistics['Q3'] + (1.5 * statistics['IQR'])
    logging.info('Outlier are those less than lower_bound and upper_bound')
    logging.info('lower_bound : {}'.format(lower_bound))
    logging.info('upper_bound : {}'.format(upper_bound))
    outlier_df = anonymized_data[ (anonymized_data['task_output.duration_ms'] < lower_bound) |
                                  (anonymized_data['task_output.duration_ms'] > upper_bound)]
    logging.debug('Outlier Data frame')
    logging.debug(outlier_df.shape)


    # Check for tasks with annotation duration < lower_bound
    duration_lessthan_lowerbound_data = anonymized_data[anonymized_data['task_output.duration_ms'] < lower_bound]
    logging.debug('The following project_root_node_input_id and vendor_user_id has duration < lower_bound')
    logging.debug('project_root_node_input_id: {}'.format(duration_lessthan_lowerbound_data['project_root_node_input_id'].unique()))
    logging.debug('vendor_user_id: {}'.format(duration_lessthan_lowerbound_data['user.vendor_user_id'].unique()))

    logging.info('Removing instances with duration < lower bound from dataset for further evaluation')
    # Remove rows with duration < lower bound
    anonymized_data_after_removal = anonymized_data[anonymized_data['task_output.duration_ms'] > lower_bound]
    logging.info('The shape of anonymized data after removing the outliers with duration < lower_bound : {}'.format(anonymized_data_after_removal.shape))

    # Creating new object with data after removal of instances with duration < lower bound
    obj2_annotation_crowd = annotation.AnnotationCrowd(anonymized_data_after_removal)
    # check for min value after removal
    statistics = obj2_annotation_crowd.get_duration_statistics_summary()
    logging.info('Minimum duration_ms after removing data with duration_ms < lower_bound: {}'.format(statistics['min']))

    # Plot histogram
    anonymized_data_after_removal.hist(column='task_output.duration_ms', bins=200)
    # Boxplot
    plt.figure()
    plt.boxplot(anonymized_data_after_removal['task_output.duration_ms'], showmeans=True, meanline=True)
    plt.title('Box plot with outliers')

    # Boxplot without outliers
    plt.figure()
    plt.boxplot(anonymized_data_after_removal['task_output.duration_ms'], sym='', showmeans=True, meanline=True)
    plt.title('Box plot without outliers')

    #########################################################################
    # c. Did all annotators produce the same amount of results, or are there differences?
    #######################################################################
    logging.info('Did all annotators produce the same amount of results?')
    logging.info('Number of results from each annotator :')
    amount_of_results = obj2_annotation_crowd.get_amount_of_results()
    logging.info('{}'.format(amount_of_results))

    ########################################################################
    # d. Are there questions for which annotators highly disagree?
    #######################################################################
    logging.info('Are there questions for which annotators highly disagree?')
    highly_disagree_list = obj2_annotation_crowd.get_highly_disagree_ids()
    logging.info('Number of project_ids with high disagreement : {}'.format(len(highly_disagree_list)))
    logging.debug('project_root_node_input_id with high disagreement')
    logging.debug('{}'.format(highly_disagree_list))

    #########################################################################
    #               Task 2
    ########################################################################
    # a. How often does 'cant_solve' and 'corrupt_data' occur in the project
    # and do you see a trend within the annotators that made use of these options?

    # Find cant_solve instances
    cant_solve_df = obj2_annotation_crowd.get_cant_solve_instances()
    logging.info('Number of cant_solve instances: {}'.format(cant_solve_df.shape[0]))
    cant_solve_annotators = cant_solve_df['user.vendor_user_id'].unique()
    logging.info('Annotators with cant_solve: {}'.format(cant_solve_annotators))
    #annotator_18_cant_solve= cant_solve_df[cant_solve_df['user.vendor_user_id'] == 'annotator_18']
    #print(annotator_18_cant_solve.shape)

    # Find corrupt_data instances
    corrupt_data_df = obj2_annotation_crowd.get_corrupt_data_instances()
    logging.info('Number of corrupt_data: {}'.format(corrupt_data_df.shape[0]))
    corrupt_annotators = corrupt_data_df['user.vendor_user_id'].unique()
    logging.info('Annotators with corrupt_data: {}'.format(corrupt_annotators))



    ###############################################################
    #               Task 3
    ###############################################################
    # Is the reference set balanced? Please demonstrate via numbers and visualizations.
    logging.info('Check if reference set is balanced')

    # Read reference json file
    with open(reference_file) as data_file:
        reference_data = json.load(data_file)

    # Define pandas data frame for reference data
    df_reference = pd.DataFrame()
    temp_df = pd.DataFrame()
    for img in reference_data.keys():
        extracted_key = list(reference_data[img].keys())[0]
        temp_df['image'] = [img]
        temp_df[extracted_key] = [reference_data[img][extracted_key]]
        df_reference = pd.concat([df_reference, temp_df])

    obj_reference = reference.ReferenceClass(df_reference, extracted_key)

    # Check the number of instances in True and False classes
    num_of_true_cases = obj_reference.get_value_counts()[0]
    num_of_false_cases = obj_reference.get_value_counts()[1]
    logging.info('Number of bicyle_true cases: {}'.format(num_of_true_cases))
    logging.info('Number of bicyle_false cases: {}'.format(num_of_false_cases))

    bool2int = obj_reference.get_bool2int()
    plt.figure()
    plt.title('Reference set count-plot')
    sns.countplot(x=bool2int)

    ####################################################################
    #           Task 4
    ##################################################################
    # Using the reference set, can you identify good and bad annotators?
    df_annotator_task_performance = functions.get_annotator_task_performance(anonymized_data_after_removal, reference_data)
    logging.info('Task performance of annotators')

    index = df_annotator_task_performance.index.values
    logging.info('{}'.format(df_annotator_task_performance[['percentage_correct_response', 'average_duration']]))
    df_annotator_task_performance.to_excel('../results/annotators_task_performance.xlsx')

    plt.figure()
    graph = sns.scatterplot(data=df_annotator_task_performance,x='average_duration', y='percentage_correct_response')
    graph.axhline(92.5)
    for i in range(df_annotator_task_performance.shape[0]):
        plt.text(x=df_annotator_task_performance.average_duration[i]+0.3, y=df_annotator_task_performance.percentage_correct_response[i]+0.1, s=index[i],
                 fontdict=dict(color='red',size=7), bbox=dict(facecolor='yellow',alpha=0.5))
    plt.xlabel('Average Duration')
    plt.ylabel('Percentage of correct Response')
    plt.show()
    ###############################################################################


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--anonymized_json', type=argparse.FileType('r', encoding='UTF-8'),
                        required=True, help="The json file with anonymized data")
    parser.add_argument('-r', '--reference_json', type=argparse.FileType('r', encoding='UTF-8'),
                        required=True, help="The json file with reference data")
    args = parser.parse_args()

    main(args.anonymized_json.name,args.reference_json.name)