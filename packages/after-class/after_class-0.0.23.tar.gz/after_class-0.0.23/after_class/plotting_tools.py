
from matplotlib import pyplot as plt
import numpy as np

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
    ax1.set_title('Worst samples distribution by classes')
    return fig1

def plot_joint_barchart(series1, series2,
                        series1_label='False positive',
                        series2_label='False negative(prediction classes)',
                        title='Title'
                        ):
    if len(series1)==0 and len(series2)==0:
           return None
                              
    #reorganizing data for it to be handy
    #to use for histograms
    all_labels = []
    extended_series_1_counts = []
    extended_series_2_counts = []
    
    all_classes = list((set(series1.index)).union(set(series2.index)))
    series_1_dict = {i:c for i,c in series1.iteritems()}
    series_2_dict = {i:c for i,c in series2.iteritems()}
    
    for class_id in all_classes:
        all_labels.append(class_id)
        if class_id in series_1_dict:
            extended_series_1_counts.append(series_1_dict[class_id])
        else:
            extended_series_1_counts.append(0)
        
        if class_id in series_2_dict:
            extended_series_2_counts.append(series_2_dict[class_id])
        else:
            extended_series_2_counts.append(0)
    fig, ax = plt.subplots()
    #fix for extreme one-bar case
    if len(all_classes) == 1:
        width = 2.5
        bar_cords = np.array([0, 5, 10])
        if len(extended_series_1_counts)>0:
            extended_series_1_counts = [0,extended_series_1_counts[0],0]
        if len(extended_series_2_counts)>0:
            extended_series_2_counts = [0,extended_series_2_counts[0],0]
        all_classes = [-1, all_classes[0], -1]
    else:
        width = 10./(2*(len(all_labels)+1))
        bar_cords = np.linspace(0, 10, num=len(all_labels))
    ax.set_ylabel('Number of samples')
    ax.set_xlabel('Class id')
    ax.set_title(title)
    if len(extended_series_2_counts)>0:
        rects1 = ax.bar(bar_cords-(width/2.),
                        extended_series_1_counts,
                        align='center',
                        width=width,
                        label=series1_label)
        
    if len(extended_series_2_counts)>0:
        rects2 = ax.bar(bar_cords+(width/2.),
                        extended_series_2_counts,
                        align='center',
                        width=width,
                        label=series2_label)
    #add some more space from top to add numbers on top of bars.
    max_top = max(np.amax(extended_series_1_counts),
                  np.amax(extended_series_2_counts))
    ax.set_ylim(0, max_top*1.1)
    
    plt.gca().set_xticks(bar_cords)
    plt.gca().set_xticklabels(all_classes)
    #numbers on top of the bars
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    ax.legend()
    fig.tight_layout()
    return fig


def make_fpfn_hists(data):
    '''Applies plot_joint_barchart for every class in data
    to build class_wise bar_chart of fp and fn for a given class to other classes.
    '''
    classes_ids = data['label'].unique()
    class_plot_dict = {}
    for cls_id in classes_ids:
        class_fp_count = data[(data['label']!=cls_id) & (data['pred']==cls_id)]['label'].value_counts()
        class_fn_count = data[(data['label']==cls_id) & (data['pred']!=cls_id)]['pred'].value_counts()
        
        chart_title = 'FP,FN distribution of samples of %s class over other classes.'%(str(cls_id))
        bar_chart = plot_joint_barchart(class_fp_count, class_fn_count, title=chart_title)
        class_plot_dict[cls_id] = bar_chart
    return class_plot_dict