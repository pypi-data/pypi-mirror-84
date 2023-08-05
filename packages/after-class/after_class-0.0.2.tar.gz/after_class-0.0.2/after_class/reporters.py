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
        self._add_figures(metrics['Figures'], report_path)
        
        self._add_images(metrics['Worst_samples'], report_path)
        #saving report
        html = self.template_soup.prettify("utf-8")
        report_dst = join(report_path, 'report.html')
        with open(report_dst, "wb") as file:
            file.write(html)
    def _add_figures(self, figures, report_path):
        for fig_name in figures:
            fig = figures[fig_name].get_figure()
            fig.suptitle(fig_name)
            #print(fig_name, type(fig[0][0]))
            fig_path = join(report_path, fig_name+'.png')
            fig.savefig(fig_path)
            
            newtag = self.template_soup.new_tag('img', src=fig_name+'.png')

            figures_div = self.template_soup.find("div", id="figures")
            figures_div.append(newtag)
    def _add_images(self, samples, report_path):
        '''
        supposing id field is a path
        '''
        for index, row in samples.iterrows():
            src_path = row['id']
            name = src_path.split('/')[-1]
            dst_path = join(report_path, name)
            copyfile(src_path, dst_path)
            caption = self._make_sample_caption(row)
            self._make_html_figure(name, caption)
    def _make_html_figure(self, img_name, caption):
        new_figure = self.template_soup.new_tag('figure')
        new_caption = self.template_soup.new_tag('figcaption')
        new_caption.string=caption
        new_img = self.template_soup.new_tag('img', src=img_name)
        
        new_figure.append(new_img)
        new_figure.append(new_caption)
        self.template_soup.body.append(new_figure)
    def _make_sample_caption(self, sample):
        caption = ''
        for key in sample.keys():
            if key!='id':
                caption+=key+' : ' + str(sample[key])+'\n'
        return caption