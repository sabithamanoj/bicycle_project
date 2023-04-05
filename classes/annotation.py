#######################################################################
#           Class definition for annotation crowd
#######################################################################

# Import numpy
import numpy as np


class AnnotationCrowd:

    def __init__(self, data):
        self.data = data

    def get_num_of_annotators(self):
        annotators = self.data['user.vendor_user_id'].unique()
        number = len(annotators)
        return number

    def get_duration_statistics_summary(self):
        statistics = {}
        mean = np.round(np.mean(self.data['task_output.duration_ms']), 2)
        median = np.round(np.median(self.data['task_output.duration_ms']), 2)
        min_value = np.round(self.data['task_output.duration_ms'].min(), 2)
        max_value = np.round(self.data['task_output.duration_ms'].max(), 2)
        Q1 = np.round(self.data['task_output.duration_ms'].quantile(0.25), 2)
        Q3 = np.round(self.data['task_output.duration_ms'].quantile(0.75), 2)
        # Interquartile range
        iqr = np.round(Q3 - Q1, 2)

        # store results in dictionary
        statistics['min'] = min_value
        statistics['mean'] = mean
        statistics['median'] = median
        statistics['max'] = max_value
        statistics['Q1'] = Q1
        statistics['Q3'] = Q3
        statistics['IQR'] = iqr
        return statistics

    def get_amount_of_results(self):
        amount_of_results = self.data['user.vendor_user_id'].value_counts()
        return amount_of_results

    def get_highly_disagree_ids (self):
        # get project_input_ids
        project_input_ids = list(self.data['project_root_node_input_id'].unique())

        # Define empty list to store project ids where annotators have high disagreement
        highly_disagree_id_list = []
        # Check for high disagreement
        response_diff = 1
        # set a counter
        highly_disagree_count = 0

        for id in project_input_ids:
            tmp = self.data[self.data['project_root_node_input_id'] == id]
            # if there is a disagreement between annotators
            if (len(tmp['task_output.answer'].value_counts()) == 2) :
                if (abs(tmp['task_output.answer'].value_counts()[0] - tmp['task_output.answer'].value_counts()[1]) <= response_diff):
                    highly_disagree_id_list.append(id)

        return highly_disagree_id_list

    def get_cant_solve_instances(self):
        return self.data[self.data['task_output.cant_solve'] == True]

    def get_corrupt_data_instances(self):
        return self.data[self.data['task_output.corrupt_data'] == True]

