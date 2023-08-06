from bs4 import BeautifulSoup
from shutil import copyfile

import os
from os.path import join

this_path = os.path.dirname(__file__)
templates_path = join(this_path, 'report_templates')
'''
reporters are the objects which take metrics dict of metricians and 
convert them to visualization of one kind or another - for example HTML-page report.
'''

class ImagesReporter(object):
    '''
    Reporter to create HTML-page report of worst samples - with their
    images, lavels, preditions, losses and distribution by classes.
    '''
    def __init__(self,
                 template_path=join(templates_path,'worst_samples_report.html')):
        
        with open(template_path, "r") as f:
            contents = f.read()
            self.template_soup = BeautifulSoup(contents, 'html')
    def __call__(self, metrics, report_path='/app/data/report'):
        if not os.path.isdir(report_path):
            os.mkdir(report_path)
        images_path = join(report_path, 'images')
        if not os.path.isdir(images_path):
            os.mkdir(images_path)
        self._add_figures(metrics['Figures'], report_path)
        self._add_classes_divs(metrics['Worst_samples'])
        self._add_samples_images(metrics['Worst_samples'], report_path)
        #saving report
        html = self.template_soup.prettify("utf-8")
        report_dst = join(report_path, 'report.html')
        with open(report_dst, "wb") as file:
            file.write(html)
    def _add_figures(self, figures, report_path):
        for fig_name in figures:
            fig = figures[fig_name]
            #print(fig_name, type(fig[0][0]))
            fig_path = join(report_path, 'images', fig_name+'.png')
            rel_fig_path = join('images',fig_name+'.png')
            fig.savefig(fig_path, bbox_inches='tight')
            
            newtag = self.template_soup.new_tag('img', src=rel_fig_path)
            
            if fig_name == "Worst_samples_piechart":
                figures_div = self.template_soup.find("div", id="Worst_samples_piechart")
            else:
                figures_div = self.template_soup.find("div", id="Worst_classes_fpfn")
            figures_div.append(newtag)
    def _add_classes_divs(self, samples):
        class_ids = samples['label'].unique()
        samples_div = self.template_soup.find("div", id="Worst_samples")
        
        for cls_id in class_ids:
            newtag = self.template_soup.new_tag('div', id=str(cls_id))
            new_tag_name = self.template_soup.new_tag('h2')
            new_tag_name.string = 'Worst samples of class: %s'%(str(cls_id))
            newtag.append(new_tag_name)
            samples_div.append(newtag)
            
    def _add_samples_images(self, samples, report_path):
        '''
        supposing id field is a path
        '''
        images_path = join(report_path, 'images')

        for _, row in samples.iterrows():
            src_path = row['id']
            sample_class = row['label']
            class_div = self.template_soup.find("div", id=str(sample_class))
            name = src_path.split('/')[-1]
            dst_path = join(images_path, name)
            copyfile(src_path, dst_path)
            rel_path = join('images', name)
            caption = self._make_sample_caption(row)
            self._make_html_figure(rel_path, caption, append_to=class_div)
    def _make_html_figure(self, img_name, caption, append_to=None):
        new_figure = self.template_soup.new_tag('figure')
        new_caption = self.template_soup.new_tag('figcaption')
        new_caption.string=caption
        new_img = self.template_soup.new_tag('img', src=img_name)
        
        new_figure.append(new_img)
        new_figure.append(new_caption)
        if append_to is None:
           self.template_soup.body.append(new_figure)
        else:
            append_to.append(new_figure)
    def _make_sample_caption(self, sample):
        caption = ''
        for key in sample.keys():
            if key!='id':
                caption+=key+' : ' + str(sample[key])
        return caption