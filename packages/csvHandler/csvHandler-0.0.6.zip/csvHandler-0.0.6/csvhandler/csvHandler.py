import pandas as pd

NEW_VALUE_COLUMN_SUFFIX = '_new'
RECORD_TYPE_STR = 'recordType'
ID_COLUMN_STR = 'Id'
CHANGED_STR = 'changed'
ADDED_STR = 'added'
DELETED_STR = 'deleted'

def combine(result_path, added_path='', deleted_path='', changed_original_path='', changed_new_path=''):
    if ((changed_original_path != '' and not changed_new_path) or (not changed_original_path and changed_new_path != '')):
        raise ValueError('changed_original_path and change_new_path both must have values')
    
    concanation_arr = []
    if added_path != '':
        added = pd.read_csv(added_path)
        added[RECORD_TYPE_STR] = ADDED_STR
        concanation_arr.append(added)

    if deleted_path != '':
        deleted = pd.read_csv(deleted_path)
        deleted[RECORD_TYPE_STR] = DELETED_STR
        concanation_arr.append(deleted)

    if changed_original_path != '' and changed_new_path != '':
        changed_original = pd.read_csv(changed_original_path)
        changed = pd.read_csv(changed_new_path)
        changed_merge = changed_original.merge(changed, on=ID_COLUMN_STR, suffixes=('', NEW_VALUE_COLUMN_SUFFIX))
        changed_merge[RECORD_TYPE_STR] = CHANGED_STR
        concanation_arr.append(changed_merge)

    result = pd.concat(concanation_arr)
    result.to_csv(result_path, index=False)

class CsvHandler():
    def __init__(self, path):
        self.file_path = path

        data_frame = pd.read_csv(self.file_path)
        self.metadata = {'rows': {'total': data_frame.shape[0],
                                ADDED_STR: len(data_frame[data_frame[RECORD_TYPE_STR] == ADDED_STR]),
                                DELETED_STR: len(data_frame[data_frame[RECORD_TYPE_STR] == DELETED_STR]),
                                CHANGED_STR: len(data_frame[data_frame[RECORD_TYPE_STR] == CHANGED_STR])},
                        'filePath': self.file_path,
                        'columns': data_frame.columns.tolist()}

    def get_metadata(self):
        return self.metadata

    def get_page(self, page_number, page_size):
        if page_number <= 0:
            raise ValueError('page_number cannot be less or equal to zero')
        
        if page_size < 0:
            raise ValueError('page_size cannot be less than zero')

        data_frame = pd.read_csv(self.file_path, skiprows=range(1, (page_number-1)*page_size+1), nrows=page_size)
        return self.__page_format(data_frame)

    def __page_format(self, data_frame):
        records = data_frame.to_dict('records')
        page = []
        for record_dict in records:
            record = {}
            record['id'] = record_dict[ID_COLUMN_STR]
            record[RECORD_TYPE_STR] = record_dict[RECORD_TYPE_STR]
            data = []
            for column_name, value in record_dict.iteritems():
                if (column_name.find(NEW_VALUE_COLUMN_SUFFIX, len(column_name)-len(NEW_VALUE_COLUMN_SUFFIX), len(column_name)) > -1 or
                    column_name == RECORD_TYPE_STR or
                        column_name == ID_COLUMN_STR):
                    continue

                item = {}
                item['columnName'] = column_name
                item['columnType'] = type(value).__name__
                item['value'] = value
                if record[RECORD_TYPE_STR] == CHANGED_STR and value != record_dict[column_name + NEW_VALUE_COLUMN_SUFFIX]:
                    item['newValue'] = record_dict[column_name +
                                                   NEW_VALUE_COLUMN_SUFFIX]

                data.append(item)

            record['data'] = data
            page.append(record)
        return page
