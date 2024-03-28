from datetime import datetime
from os.path import join as join_path
from os.path import exists
from os import makedirs

class Logger:
    LOW_LEVEL = 'LOW_LEVEL_ERROR'
    MEDIUM_LEVEL = 'MEDIUM_LEVEL_ERROR'
    HIGH_LEVEL = 'HIGH_LEVEL_ERROR'
    
    def __init__(self):
        self.log_dir = './logs'
        self.create_dir(self.log_dir)
        
    def create_dir(self, dir_path):
        if not exists(dir_path):
            makedirs(dir_path)
            
    def get_log_file(self, level):
        now = datetime.now()
        date_str = now.strftime('%Y%m%d')
        hour_str = now.strftime('%H')
        log_dir = join_path(self.log_dir, date_str)
        self.create_dir(log_dir)
        file_name = f'{level.lower()}_{hour_str}h.log'
        return join_path(log_dir, file_name)
    
    def log(self, level, message):
        log_file = self.get_log_file(level)
        now = datetime.now()
        date_str = now.strftime('%d-%m-%Y %H:%M:%S')
        log_message = f'[{date_str}] [{level}] {message}\n'
        with open(log_file, 'a') as f:
            f.write(log_message)
