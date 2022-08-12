# When import this module, do import in the following form
# from ProcessData import graph
# from ProcessData import preProcess

import matplotlib.pyplot as plt
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_rows = None
pd.options.display.max_info_columns

def preProcess(path, drop_feature = None, partition_by = None, convert_to_timestamp = None, sort_by_value = None):
    # check path
    if isinstance(path, str):
        df = pd.read_csv(path)
    elif isinstance(path, pd.DataFrame):
        df = path
    else: 
        raise TypeError("Wrong path type")
    # check features to drop
    if drop_feature == 'default':
        df.drop(["log_group_name", "log_stream_name", "record_id", "stream_name", "record_arrival_stream_timestamp","record_arrival_stream_epochtime", "log_event_timestamp","log_event_epochtime","kin_shard_id","index_date","metric_ts", "vnf_major_release","vnf_minor_release","year","month","day", "hour","region"], axis = 1, inplace=True)
    elif drop_feature != None:
        df.drop(drop_feature)
    # convert from epochtime to timestamp
    if convert_to_timestamp != None:
        df[convert_to_timestamp] = pd.to_datetime(df[convert_to_timestamp],unit='ms')
    # do partition into dictionary
    data_frames = {}
    if partition_by != None: 
        partition_type = df[partition_by].unique().tolist()
        for part in partition_type:
            data_frames_temp = df[df[partition_by]==part]
            empty_cols = [col for col in data_frames_temp.columns if data_frames_temp[col].isnull().all()]
            data_frames[part] = data_frames_temp.drop(empty_cols, axis=1)
            del data_frames_temp
    # sort the dataframes in the dictionary
    if sort_by_value != None:
        if partition_by != None:
            for part in partition_type:
                data_frames[part] = data_frames[part].sort_values(by=sort_by_value)
        else: df.sort_values(by=sort_by_value)

    if len(data_frames) == 0: return df
    return data_frames


# def graph(dataFrame, byFeature, xval, *args):
#     # graph(dataFrame, byFeature, xval, [[yval1, 'r'], [yval2, 'b'])
#     for yval in kwargs: 
#         pass

def graph(*args):
    # graph(dataFrame, byFeature, xval, yval1, yval2)
    numargs = len(args)
    if numargs < 4 or numargs > 5:
        raise TypeError(f'expected 4 or 5 arguments, dataFrame, byFeature, xval, yval1, yval2(optional). Got {numargs}.')

    data_frames = args[0]
    byFeature = args[1]
    xval = args[2]
    yval1 = args[3]
    if numargs == 5: yval2 = args[4]

    features = data_frames[byFeature].unique()
    # c = 0
    for feature in features:
        # c = c + 1
        # if c > 3: break
        df_features = data_frames.loc[data_frames[byFeature] == feature]
        
        x1 = df_features[xval].tolist()
        y1 = df_features[yval1].tolist()
        
        fig, ax = plt.subplots()
        ax.plot(x1, y1, '.:', label = yval1)
        plt.legend()
        ax.set_title(f'{byFeature}: {feature}')
        ax.set_xlabel(xval)
        ax.set_ylabel(yval1)
        
        if numargs == 5: 
            y2 = df_features[yval2].tolist()
            ax2 = ax.twinx()
            ax2.plot(x1, y2, '.:r', label = yval2)
            plt.legend()
            ax2.set_ylabel(yval2)

        fig.set_size_inches(15, 7)
        fig.autofmt_xdate()

        
    plt.show()