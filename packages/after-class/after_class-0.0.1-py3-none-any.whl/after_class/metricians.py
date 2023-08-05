from sklearn.metrics import classification_report
'''
metricians are objects which take as input DataFrame 
of processed samples(path_to_sample, prediction, label, sample_loss)
and produce dictionary of metrics and other data describing classification results
for a given samples
'''

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
                 sort_classes_by='f1-score',
                 sort_samples_by='loss',
                 topN=5,
                 top_percent_samples=0.1,
                 global_metrics=['accuracy', 'weighted avg', 'macro avg']):
        self.sort_classes_by = sort_classes_by
        self.sort_samples_by = sort_samples_by
        self.topN = topN
        self.top_percent_samples = top_percent_samples
        self.global_metrics = global_metrics
    def __call__(self, test_results):
        report = classification_report(test_results['label'],
                                       test_results['pred'],
                                       output_dict=True)
        global_metrics = {}
        for metric_name in self.global_metrics:
            global_metrics[metric_name] = report.pop(metric_name)
        
        bestNclasses, worstNclasses = self.get_extreme_classes(report)
        worst_samples, worst_samples_classes_hist = \
           self.get_worst_samples(test_results)
        metrics = {'BestNClasses' : bestNclasses,
                   'WorstNClasses' : worstNclasses,
                   'Worst_samples' : worst_samples,
                   'Figures' :
                    {'Worst_samples_labels_hist' : worst_samples_classes_hist},
                   'Samples_threshold' : self.top_percent_samples,
                   'Global_metrics' : global_metrics}
        return metrics
    def get_extreme_classes(self, classes_report):
        key_lambda = lambda item: item[1][self.sort_classes_by]
        sorted_dict = {k: v for k, v in 
                       sorted(classes_report.items(), key=key_lambda)}
        
        dict_len = len(sorted_dict)
        best_N_classes_report = {}
        worst_N_classes_report = {}
        for i,(k,v) in enumerate(sorted_dict.items()):
            if i < self.topN:
                best_N_classes_report[k] = v
            if i > dict_len - self.topN:
                worst_N_classes_report[k] = v
        return best_N_classes_report, worst_N_classes_report
    
    def get_worst_samples(self, test_result):
        sorted_data = test_result.sort_values(self.sort_samples_by,
                                           ascending=False)
        
        take_till = int(len(sorted_data)*self.top_percent_samples)
        if take_till == 0:
            take_till = 1
        worst_samples = sorted_data[:take_till]
        worst_samples_dist = worst_samples.hist('label')[0][0]
        return worst_samples, worst_samples_dist