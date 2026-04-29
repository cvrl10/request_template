import xlsxwriter
from configparser import ConfigParser
import re
from datetime import date
from pathlib import Path
import sys
import logging
import subprocess

EMPTY_CELL = '#FFFFCC'
WEIGHT_COLUMN = 6
VOLUME_COLUMN = 7
DIGESTION_COLUMN = VOLUME_COLUMN + 1
log_file = 'create_template.log'
logging.basicConfig(filename=log_file, level=logging.INFO, filemode='w')
logger = logging.getLogger(log_file)



base = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
config_path = base/'config.ini'
print(config_path)
ANALYSIS = {}
parser = ConfigParser()
parser.read(config_path)


ic_analysis = parser.get('Analysis', 'ic')
for element in re.split(r'[,\s]+', ic_analysis):
    ANALYSIS.update({element.lower(): 'IC analysis'})

titration_analysis = parser.get('Analysis', 'titration')
titration_analysis = map(lambda s: s.lower(), re.split(r'[,\s]+', titration_analysis))

titration_analysis_list = list(titration_analysis)
print(titration_analysis_list)

STEP = parser.getint('Microwave Program', 'step')
WEIGHT_DECIMAL = parser.getint('Decimal', 'weight')
CONC_DECIMAL = parser.getint('Decimal', 'conc.')
SPACING = 2 #spacing between digestion tables

url = 'master_template.xlsx'

workbook = xlsxwriter.Workbook(url)


class Template:
    def __init__(self, wb, request_id, sample_copy, loi=True):
        self.loi = loi
        self.workbook = wb
        self.request_id = request_id
        self.COPY = sample_copy
        self.row = 0
        self.digestion_sheet = wb.add_worksheet('digestion_page')

        self.info_format = wb.add_format({'bold': True, 'align': 'right'})
        self.date_format = wb.add_format({'num_format': 'yyyy-mm-dd'})
        self.bold_italic_format = wb.add_format({'border': 1, 'italic': True, 'bold': True})
        self.italic_bold_format = wb.add_format({'italic': True, 'bold': True})
        self.italic_format = wb.add_format({'italic': True, 'align': 'right'})
        self.header_format = wb.add_format({'border': 1, 'bold': True, 'align': 'center'})
        self.label_cell_format = wb.add_format({'border': 1, 'bold': True})
        self.empty_cell_format = wb.add_format({'border': 1})
        num_format = '0'*WEIGHT_DECIMAL
        num_format = f'0.{num_format}'
        self.weight_cell = wb.add_format({'border': 1, 'num_format': num_format})
        num_format = '0'*CONC_DECIMAL
        num_format = f'0.{num_format}'
        self.conc_cell = wb.add_format({'border': 1, 'num_format': num_format})
        self.empty_cell_format_left = wb.add_format({'border': 1, 'align': 'left'})
        self.result_cell_format = wb.add_format({'border': 1, 'num_format': '0.00'})
        self.result_string_format = wb.add_format({'align': 'right'})
        self.text_format = wb.add_format({'align': 'left',
                                          'valign': 'top',
                                          'text_wrap': True,
                                          'italic': True})
        self.reported_ppm_format = wb.add_format({'align': 'left', 'num_format': '0.00" ppm"'})
        self.reported_percent_format = wb.add_format({'align': 'left', 'num_format': '0.00" %"'})
        color = '#000000'
        color = '#FFFFFF'
        self.white_font_format = wb.add_format({'font_color': color})
        self.__create_header(self.digestion_sheet)
        self.sample_to_elements = {}
        self.element_to_digestion = {}

        self.format = {'white_font': self.white_font_format, 'result': self.result_cell_format}

        self.append = ' [dried]' if loi else ''

    def __analysis_header(self, worksheet, element):
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{element}_ppm', self.bold_italic_format)
        worksheet.write(self.row, 4, f'%{element}', self.bold_italic_format)
        self.__move_cursor()

    def __create_analysis_table(self, worksheet, element, sample):
        analysis = ANALYSIS.get(element.lower(), f'{element} ICP analysis')
        worksheet.merge_range(self.row, 0, self.row, 1, analysis, self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{element}_ppm{self.append}', self.label_cell_format)
        worksheet.write(self.row, 4, f'%{element}{self.append}', self.label_cell_format)
        self.__move_cursor()

        print(f'inside private method: {sample}')
        start_row = self.row
        for i in range(1, self.COPY+1):
            worksheet.write(self.row, 0, f'{sample}_{i}', self.label_cell_format)
            #worksheet.set_column(0, 0, len(f'{sample}_{i}'))
            worksheet.write(self.row, 1, '''="1/1"''', self.empty_cell_format)
            worksheet.write(self.row, 2, '', self.conc_cell)
            worksheet.write(self.row, 3, '', self.empty_cell_format)
            worksheet.write(self.row, 4, '', self.empty_cell_format)
            self.__move_cursor()
        end_row = self.row-1
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        ppm_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 3)
        ppm_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 3)
        ppm_average = f'=AVERAGE({ppm_start}:{ppm_end})'
        worksheet.write_formula(self.row, 2, ppm_average, self.reported_ppm_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        percent_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 4)
        percent_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 4)
        percent_average = f'=AVERAGE({percent_start}:{percent_end})'
        worksheet.write_formula(self.row, 2, percent_average, self.reported_percent_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} oxide factor:', self.result_string_format)
        worksheet.write(self.row, 2, '', self.workbook.add_format({'align': 'left'}))
        oxide_factor = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        oxide_average = f'=AVERAGE({percent_start}:{percent_end})*({oxide_factor})'
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} oxide result:', self.result_string_format)
        worksheet.write_formula(self.row, 2, oxide_average, self.reported_percent_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} lot:', self.result_string_format)
        worksheet.merge_range(self.row, 2, self.row, 5, '', self.workbook.add_format({'italic': True}))
        merge_start = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        merge_finish = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 5)
        worksheet.conditional_format(f'{merge_start}:{merge_finish}',
                                     {'type': 'blanks',
                                      'format': self.workbook.add_format({'bg_color': EMPTY_CELL})
                                      })
        self.__move_cursor(SPACING)

    def create_analysis_table(self):
        for sample in self.sample_to_elements:
            worksheet = self.workbook.add_worksheet(str(sample))
            self.__create_header(worksheet)
            correction_factor = 1
            if self.loi:
                correction_factor = self.__create_loi_table(sample, worksheet)

            for element in self.sample_to_elements[sample]:
            #for element in self.element_to_digestion:
                print(f'inside for_loop')
                print(f'and iterating through element: in self.element_to_digestion {self.element_to_digestion}')
                digestion_object = self.element_to_digestion[element]
                #if element.lower() in titration_analysis_list and 'other' in digestion_object.name:
                if element.lower() in titration_analysis_list:
                    move_to = self.row + 2
                    self.__create_titration_table(worksheet, element, sample, correction_factor)
                    for sample_id in [f'{sample}_{i}' for i in range(1, self.COPY + 1)]:
                        digestion_object.write_titration(move_to, sample_id, worksheet)
                        move_to += 1
                    continue
                move_to = self.row + 2
                self.__create_analysis_table(worksheet, element, sample)##########
                #move_to = self.row+2
                #remeber keys/elements should be unique if not throw exception
                print(f'this is sample: {sample}')
                #digestion_object = self.element_to_digestion[element]
                print(digestion_object.name)
                for sample_id in [f'{sample}_{i}'for i in range(1, self.COPY + 1)]:
                    digestion_object.write(move_to, sample_id, worksheet, correction_factor)
                    move_to += 1

            worksheet.write(self.row, 1, 'Note(s):', self.result_string_format)
            worksheet.merge_range(self.row, 2, self.row+2, 5, '', self.text_format)
            worksheet.autofit()
            print()
        self.__create_formula_sheet()
        self.Digestion.instance = {}

    def __create_header(self, worksheet):
        self.row = 0
        worksheet.write(self.row, 0, 'Date:', self.info_format)
        worksheet.write(self.row, 1, date.today(), self.date_format)
        self.__move_cursor()
        worksheet.write(self.row, 0, 'Request ID:', self.info_format)
        worksheet.write(self.row, 1, self.request_id)

        self.__move_cursor()
        self.__move_cursor(SPACING)

    def __create_titration_table(self, worksheet, element, sample, correction_factor):
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element} titration analysis', self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        worksheet.write(self.row, 2, 'titrant_volume (mL)', self.label_cell_format)
        worksheet.write(self.row, 3, f'%{element}{self.append}', self.label_cell_format)
        self.__move_cursor()
        start_row = self.row
        for sample_id in [f'{sample}_{i}' for i in range(1, self.COPY + 1)]:
            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, WEIGHT_COLUMN)
            worksheet.write(self.row, 0, f'{sample_id}', self.label_cell_format)
            worksheet.write_formula(self.row, 1, weight_cell, self.empty_cell_format)
            worksheet.write(self.row, 2, '', self.empty_cell_format)
            worksheet.write(self.row, 3, '', self.empty_cell_format)
            self.__move_cursor()

        end_row = self.row-1
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, 'FAS:', self.result_string_format)
        worksheet.write(self.row, 2, '', self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, 'reported result:', self.result_string_format)
        ppm_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 3)
        ppm_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 3)
        ppm_average = f'=AVERAGE({ppm_start}:{ppm_end})*({10_000})*(1/{correction_factor})'
        worksheet.write_formula(self.row, 2, ppm_average, self.reported_ppm_format)
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, 'reported result:', self.result_string_format)
        percent_average = f'=AVERAGE({ppm_start}:{ppm_end})*(1/{correction_factor})'
        worksheet.write_formula(self.row, 2, percent_average, self.reported_percent_format)
        self.__move_cursor(SPACING)
        worksheet.autofit()

    def __create_loi_table(self, sample_id, worksheet):
        worksheet.write(self.row, 0, 'LOI temp:', self.result_string_format)
        format = self.workbook.add_format({'num_format': f'######" {chr(176)}C"'})
        worksheet.write(self.row, 1, '', format)
        temp_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 1)
        worksheet.conditional_format(temp_cell,
                                     {'type': 'blanks',
                                      'format': self.workbook.add_format({'bg_color': EMPTY_CELL})
                                      })
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'crucible (g)', self.label_cell_format)
        worksheet.write(self.row, 2, 'crucible + sample (g)', self.label_cell_format)
        worksheet.write(self.row, 3, f'''="after "&{temp_cell}&" {chr(176)}C"''', self.label_cell_format)
        worksheet.write(self.row, 4, 'LOI (%)', self.label_cell_format)
        worksheet.write(self.row, 5, 'correction', self.label_cell_format)
        self.__move_cursor()

        worksheet.write(self.row, 0, f'{sample_id}', self.label_cell_format)
        worksheet.write(self.row, 1, '', self.empty_cell_format)
        worksheet.write(self.row, 2, '', self.empty_cell_format)
        worksheet.write(self.row, 3, '', self.empty_cell_format)

        A = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 1)
        B = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        C = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 3)
        loi_formula = f'=((({B}-{A})-({C}-{A}))/({B}-{A}))*100'
        worksheet.write_formula(self.row, 4, loi_formula, self.result_cell_format)

        loi_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 4)
        worksheet.write_formula(self.row, 5, f'1-({loi_cell}/100)', self.workbook.add_format({'border': 1, 'num_format': '0.0000'}))

        correction_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 5, True, True)
        self.__move_cursor(SPACING)

        return correction_cell

    def __create_formula_sheet(self):
        self.row = 0
        formula_page = self.workbook.add_worksheet('formula_page')
        formula_page.write(self.row, 0, 'A = crucible', self.italic_bold_format)
        self.__move_cursor()
        formula_page.write(self.row, 0, 'B = crucible + sample', self.italic_bold_format)
        self.__move_cursor()
        formula_page.write(self.row, 0, 'C = crucible + sample after drying', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%LOI = ([B-A]-[C-A])/(B-A)*100%', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, 'ppm M+ = [conc.][volume][dilution]/[weight]', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%M+ = [conc.][volume][dilution]/([weight]*10,000)', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%MO = [oxide factor]*%M+', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, 'ppm M+  [dried] = ppm M+/([1-(%LOI)/100])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%M+  [dried] = %M+/([1-(%LOI)/100])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%MO [dried] = %MO/([1-(%LOI)/100])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%Cr(VI) = (1.733[mL FAS][N FAS])/([weight])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%Cr2O3 = 1.462*[%Cr(VI)]', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%Cr(III) = total_Cr - Cr(VI)', self.italic_bold_format)
        formula_page.autofit()



    def add_microwave(self, elements: list, samples: list):
        def create_microwave_program():
            def write(data):
                for i in range(5):
                    self.digestion_sheet.write(self.row, i, data[i], self.empty_cell_format)
                self.__move_cursor()
            write(data=[15, 1200, 180, 65, 110])
            write(data=[15, 1500, 240, 65, 110])
            for _ in range(STEP-2):
                write(data=['', '', '', '', ''])

        self.digestion_sheet.merge_range(self.row, 0, self.row, 4, 'Microwave', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Element(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Acid Cocktail', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Rack', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format_left)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Vessel', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Stir', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format_left)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Time (min)', self.label_cell_format)
        self.digestion_sheet.set_column(0, 0, len('Time (min)'))
        self.digestion_sheet.write(self.row, 1, 'Power (W)', self.label_cell_format)
        self.digestion_sheet.set_column(1, 1, len('Power (W)')+1)
        self.digestion_sheet.write(self.row, 2, f'T1 ({chr(176)}C)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 3, f'T2 ({chr(176)}C)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 4, 'P (bar)', self.label_cell_format)
        self.__move_cursor()

        create_microwave_program()
        microwave = self.Digestion(name='microwave', elements=elements, format=self.format)
        logger.info(f'{microwave.name} with sample(s)={samples} digesting element(s)={elements}')
        self.__create_sample_row(samples, microwave, volume='')
        self.__move_cursor(SPACING)
        self.digestion_sheet.autofit()

    def add_hotplate(self, elements: list, samples: list):
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Hotplate', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Element(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Cocktail', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        hotplate = self.Digestion(name='hotplate', elements=elements, format=self.format)
        logger.info(f'{hotplate.name} with sample(s)={samples} digesting element(s)={elements}')
        self.__create_sample_row(samples, hotplate, volume='')
        self.__move_cursor(SPACING)
        self.digestion_sheet.autofit()

    def add_katanax(self, elements: list, samples: list):
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Katanax', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Element(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Acid Cocktail', self.label_cell_format)
        self.digestion_sheet.set_column(0, 0, 12)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        katanax = self.Digestion(name='katanax', elements=elements, format=self.format)
        logger.info(f'{katanax.name} with sample(s)={samples} digesting element(s)={elements}')
        self.__create_sample_row(samples, katanax, volume=250)
        self.__move_cursor(SPACING)
        self.digestion_sheet.autofit()

    def add_other(self, elements: list, samples: list):
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'other', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Element(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Cocktail', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        other = self.Digestion(name='other', elements=elements, format=self.format)
        self.__create_sample_row(samples, other, volume='')
        self.__move_cursor(SPACING)
        self.digestion_sheet.autofit()

    def __move_cursor(self, spacing=1):
        self.row += spacing

    def __create_sample_row(self, samples, digestion, volume=250):
        self.digestion_sheet.write(self.row, 0, 'sample(s)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 2, 'volume (mL)', self.label_cell_format)
        self.__move_cursor()
        print(f'{digestion.name}')
        for sample in samples:
            if sample not in self.sample_to_elements:
                self.sample_to_elements[sample] = digestion.elements.copy()  # this is fine because I've taken the consideration that there won't be any empty list
                print(self.sample_to_elements)
                for element in digestion.elements:
                    logger.info(f'adding {element} to {sample}')
                    '''mapping each element to its Digestion object, haven't tested what happen if same element from different digestion will map'''
                    self.element_to_digestion[element] = digestion
            else:
                self.sample_to_elements[sample].extend(digestion.elements.copy())
                for element in digestion.elements:
                    logger.info(f'adding {element} to {sample}')
                    self.element_to_digestion[element] = digestion

            for i in range(1, self.COPY+1):
                sample_id = f'{sample}_{i}'
                self.digestion_sheet.write(self.row, 0, sample_id, self.label_cell_format)
                self.digestion_sheet.write(self.row, 1, '', self.weight_cell)
                self.digestion_sheet.write(self.row, 2, volume, self.empty_cell_format)

                print(f'storing: {sample_id}')
                digestion.store_data(sample_id, self.row)
                self.__move_cursor()

    class Digestion:
        '''

        An instance of this object is pass Template.__create_sample_row as tables are created in Digestion sheet to
            collect source rows for weight and volume.

        '''
        instance = 0
        instance = {}

        @classmethod
        def increment(cls, name):
            if name not in cls.instance:
                cls.instance[name] = 0
                return f'{name}_{0}'
            else:
                cls.instance[name] += 1
                return f'{name}_{cls.instance[name]}'

        def __init__(self, name, elements, format):
            self.format = format
            self.elements = elements
            self.name = self.increment(name)
            #self.increment(name)
            self.sampleid_to_sourcerow = {}

        def write(self, to_row, sample_id, destination_worksheet, correction_factor):
            weight_ref, volume_ref = self.__read_source_data(sample_id)

            destination_worksheet.write_formula(to_row, WEIGHT_COLUMN, weight_ref, self.format['white_font'])
            destination_worksheet.write_formula(to_row, VOLUME_COLUMN, volume_ref, self.format['white_font'])

            source_dilution_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 1)
            dilution_formula = '''(LEFT({0},FIND("/",{0})-1)/RIGHT({0},LEN({0})-FIND("/", {0})))'''.format(source_dilution_cell)
            destination_worksheet.write_formula(to_row, DIGESTION_COLUMN, dilution_formula, self.format['white_font'])

            conc_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 2)
            volume_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, VOLUME_COLUMN)
            dilution_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, DIGESTION_COLUMN)
            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, WEIGHT_COLUMN)
            print(f'corection={correction_factor}')
            ppm_calculation = f'=(({conc_cell})*({volume_cell})*({dilution_cell}))/({weight_cell}*{correction_factor})'

            destination_worksheet.write_formula(to_row, 3, ppm_calculation, self.format['result'])

            ppm_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 3)
            #percent_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 4)
            percent_calculation = f'={ppm_cell}/{10_000}'
            destination_worksheet.write_formula(to_row, 4, percent_calculation, self.format['result'])
            destination_worksheet.autofit()

        def write_titration(self, to_row, sample_id, destination_worksheet):
            weight_cell, _ = self.__read_source_data(sample_id)
            #weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, WEIGHT_COLUMN)
            destination_worksheet.write_formula(to_row, WEIGHT_COLUMN, weight_cell, self.format['white_font'])

        def __read_source_data(self, sample_id):
            '''

            :param sample_id: takes a sample tied to a digestion
            :return: the cells from digestion_page that references the weight and volume for calculations
            '''

            source_row = self.sampleid_to_sourcerow[sample_id]

            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(source_row, 1)
            volume_cell = xlsxwriter.utility.xl_rowcol_to_cell(source_row, 2)
            weight_ref = f'digestion_page!{weight_cell}'
            volume_ref = f'digestion_page!{volume_cell}'

            logger.info(f'referencing {sample_id} weight from {weight_ref }')
            logger.info(f'referencing {sample_id} volume from {volume_ref}')

            return weight_ref, volume_ref

        def store_data(self, sample_id, source_row_index):
            logger.info(f'storing: {sample_id} @digestion_page!{source_row_index}')
            self.sampleid_to_sourcerow[sample_id] = source_row_index

        def __str__(self):
            return self.name
        def __repr__(self):
            return str(self)


copy = 1
start = 0

LOI = True
#LOI = False

template = Template(workbook, 100482511, 2, loi=LOI)
s = ['200127586', '200127587']

#for i in range(copy):
    #template.add_other(['Cr6'], ['200127586'])

for i in range(copy):
    template.add_microwave(['Ca', 'Cu'], s)

for i in range(copy):
    template.add_katanax(['Ti', 'Si'], ['200127587', '200127588'])

for i in range(copy):
    template.add_hotplate(['Ag', 'Pd'], ['200127586'])

template.create_analysis_table()
workbook.close()

subprocess.Popen(['start', 'master_template.xlsx'], shell=True)


