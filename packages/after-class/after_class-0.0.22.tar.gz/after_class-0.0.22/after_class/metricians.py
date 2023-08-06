from sklearn.metrics import classification_report
from matplotlib import pyplot as plt
import numpy as np
'''
metricians are objects which take as input DataFrame 
of processed samples(path_to_sample, prediction, label, sample_loss)
and produce dictionary of metrics and other data describing classification results
for a given samples
'''

def make_worst_samples_pie(worst_samples, unite_after=15):
    counts_series = worst_samples.value_counts(['label'])
    labels = []
    sizes = []
    the_rest = 0
    for cnt,(i,c) in enumerate(counts_series.items()):
        if cnt < unite_after:
            labels.append(str(i))
            sizes.append(c)
        else:
            the_rest+=c
    sizes.append(the_rest)
    labels.append('all the rest')
    
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig1


class Metrician(object):
    '''
    Metrician providing following metrics and data from data frame:
     - class-wise f1_score, precision, recall
     - global accuracy of classification
     - avg precision and recall - simple avg(macro) and with respect to classes balance
     - Top N best, worst classes(by one of class-wise metrics)
     - M % of worst samples(from samples rating by loss by default)
     - M % worst samples distribution by classes.        
    '''
    def __init__(self, 
                 sort_classes_by='total_loss',
                 sort_samples_by='loss',
                 topN=5,
                 top_percent_samples=0.1,
                 global_metrics=['accuracy', 'weighted avg', 'macro avg']):
        self.sort_classes_by = sort_classes_by
        self.sort_samples_by = sort_samples_by
        self.topN = topN
        self.top_percent_samples = top_percent_samples
        self.global_metrics = global_metrics
    def __call__(self, test_results, idx_name_dict=None):
        report = classification_report(test_results['label'],
                                       test_results['pred'],
                                       output_dict=True)
        
        if self.sort_classes_by == 'total_loss':
            total_loss_by_class = test_results.groupby('label')['loss'].sum()
            for i,v in total_loss_by_class.iteritems():
                report[str(i)]['total_loss'] = v

        global_metrics = {}
        for metric_name in self.global_metrics:
            global_metrics[metric_name] = report.pop(metric_name)
        
        flat_report = {'class_id' : [],
                        'f1-score' : [],
                        'precision' : [],
                        'recall' : [],
                        'support' : []}
        if self.sort_classes_by == 'total_loss':
            flat_report['total_loss'] = []
        
        #eliminating nesting of dictionaries in report
        for class_id in report:
            if idx_name_dict is not None:
                new_class_id = str(class_id)+' ('+idx_name_dict[class_id]+')'
            else:
                new_class_id = str(class_id)
            flat_report['class_id'].append(new_class_id)
            for metric_name, value in report[class_id].items():
                flat_report[metric_name].append(value)
        #ordering values of lists by selected metric
        sort_metric = flat_report[self.sort_classes_by]
        order = np.argsort(sort_metric)
        if self.sort_classes_by == 'total_loss':
            order = order[::-1]

        for key in flat_report:
            flat_report[key] = np.array(flat_report[key])[order]

        worst_samples, worst_samples_piechart = \
           self.get_worst_samples(test_results, idx_name_dict=idx_name_dict)

        metrics = {'Class-wise_report' : flat_report,
                   'Worst_samples' : worst_samples,
                   'Figures' :
                    {'Worst_samples_piechart' : worst_samples_piechart},
                   'Samples_threshold' : self.top_percent_samples,
                   'Global_metrics' : global_metrics}
        return metrics
    
    def get_worst_samples(self, test_result, idx_name_dict=None):
        sorted_data = test_result.sort_values(self.sort_samples_by,
                                           ascending=False)
        
        take_till = int(len(sorted_data)*self.top_percent_samples)
        if take_till == 0:
            take_till = 1
        worst_samples = sorted_data[:take_till]

        if idx_name_dict is not None:
            get_pred_name = lambda row: str(row['pred'])+' ('+idx_name_dict[str(row['pred'])]+')'
            get_label_name = lambda row: str(row['label'])+' ('+idx_name_dict[str(row['label'])]+')'
            worst_samples['pred'] = worst_samples.apply(get_pred_name, axis=1)
            worst_samples['label'] = worst_samples.apply(get_label_name, axis=1)
        pie_chart = make_worst_samples_pie(worst_samples)
        return worst_samples, pie_chart