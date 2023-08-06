from pyrasgo.connection import Connection
from pyrasgo.monitoring import track_usage
from pyrasgo.api import RasgoConnection

class RasgoOrchestration(Connection):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rasgo = RasgoConnection(api_key=self._api_key)

    @track_usage
    def simulate_orchestration(self, source_table: str, func):
        '''
        Run a python function against a source table
        
        param source_table: Snowflake table holding raw data
        param func: function containing feature transformation code (should be named generate_feature)

        return: Success or Failure message
        '''
        df = self.rasgo.get_source_table(table_name=source_table, record_limit=-1)
        dx = func(df)
        return f'Code successfully created dataframe with shape {dx.shape}'

    @track_usage
    def generate_featureset_files(self, features: list, dimensions: list, granularity: str, src_table: str, func=None):
        '''
        return: yml file
        '''
        #call generate_yml_file(features, dimensions, granularity, src_table)
        #call generate_py_file(module)
        #call generate_requirements_file(module)
        raise NotImplementedError

    @track_usage
    def generate_yml_file(self, features: list, dimensions: list, granularity: str, src_table: str):
        '''
        return: yml file
        '''
        raise NotImplementedError

    @track_usage
    def generate_py_file(self, func):
        '''
        return: feature.py file
        '''
        #Wrap generate_feature function and output as file
        raise NotImplementedError

    @track_usage
    def generate_requirements_file(self, func):
        '''
        return: requirements.txt file
        '''
        #Scan generate_feature function for import statements and output as file
        raise NotImplementedError