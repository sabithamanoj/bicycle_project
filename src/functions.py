import numpy as np
import pandas as pd
import re


def get_annotator_task_performance(anonymized_data, reference_data):

    # For comparison with reference-set map 'yes' to True and 'no' to False of task_output.answer of anonymized data
    anonymized_mapped = anonymized_data.copy()
    anonymized_mapped['task_output.answer'] = anonymized_mapped['task_output.answer'].map({'yes': True, 'no': False})

    annotators_list = list(anonymized_mapped['user.vendor_user_id'].unique())
    annotator_task_performance = {}
    for annotator in annotators_list:
        annotator_task_performance[annotator] = {'number_of_correct_responses': 0, 'number_of_wrong_responses': 0, 'total_time': 0}

    for annotator in annotators_list:
        annotator_df = anonymized_mapped[anonymized_mapped['user.vendor_user_id'] == annotator]
        # iterate through rows
        for index, row in annotator_df.iterrows():
            # To get image url
            image_url = row['root_input.image_url']
            # To get only the image name
            image_jpg = re.sub(r'.*/', '', image_url)
            image_name = re.sub(r'.jpg', '', image_jpg)
            annotator_answer = row['task_output.answer']
            reference_answer = reference_data[image_name]['is_bicycle']
            annotator_task_performance[annotator]['total_time'] += row['task_output.duration_ms']

            # Compare the answer of the annotator with reference and if it is a correct response,
            # then increment the 'number_of_correct_responses' counter
            # or else increment the 'number_of_wrong_responses' counter
            if annotator_answer == reference_answer:
                annotator_task_performance[annotator]['number_of_correct_responses'] += 1
            else:
                annotator_task_performance[annotator]['number_of_wrong_responses'] += 1

    # For each annotator compute average_duration and percentage of correct responses
    for x in annotator_task_performance.keys():
        annotator_task_performance[x]['average_duration'] = round(annotator_task_performance[x]['total_time']/(annotator_task_performance[x]['number_of_correct_responses']+annotator_task_performance[x]['number_of_wrong_responses']), 2)
        annotator_task_performance[x]['percentage_correct_response'] = round((annotator_task_performance[x]['number_of_correct_responses']/(annotator_task_performance[x]['number_of_correct_responses']+annotator_task_performance[x]['number_of_wrong_responses'])) * 100, 2)

    df_annotator_task_details = pd.DataFrame.from_dict(annotator_task_performance, orient='index')
    return df_annotator_task_details


