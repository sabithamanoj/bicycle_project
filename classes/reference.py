######################################################################
#           Class definition for reference class
#####################################################################

class ReferenceClass:
    def __init__(self, data, object_to_identify):
        self.data = data
        self.object_to_identify = object_to_identify

    def get_value_counts(self):
        counts = self.data[self.object_to_identify].value_counts()
        return counts

    def get_bool2int(self):
        # convert bool to int for seaborn countplot
        convert2int = self.data[self.object_to_identify].astype(int)
        return convert2int




