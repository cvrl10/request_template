import xlsxwriter
from configparser import ConfigParser
import re
from datetime import date
from database import query_database
import sys

file = open('stdout_err.log', mode='w')
#sys.stdout = file
#sys.stderr = file

EMPTY_CELL = '#FFFFCC'
WEIGHT_COLUMN = 6
VOLUME_COLUMN = WEIGHT_COLUMN + 1
DILUTION_COLUMN = VOLUME_COLUMN + 1

parser = ConfigParser()


class Template:
    def __init__(self, wb, request, replicate, tag, loi, font_color):
        self.close()#need to clear the dictionary in case some exception was thrown leading miscount of analyte tags
        self.__config()
        self.loi = loi
        self.tag = tag
        self.workbook = wb
        self.request_id = request
        self.replicate = replicate
        self.row = 0
        self.digestion_sheet = wb.add_worksheet('digestion_page')

        self.info_format = wb.add_format({'bold': True, 'align': 'right'})
        self.date_format = wb.add_format({'align': 'left', 'num_format': 'yyyy-mm-dd'})
        self.italic_bold_format = wb.add_format({'italic': True, 'bold': True})
        self.italic_format = wb.add_format({'italic': True, 'align': 'right'})
        self.header_format = wb.add_format({'border': 1, 'bold': True, 'align': 'center'})
        self.label_cell_format = wb.add_format({'border': 1, 'bold': True})
        self.empty_cell_format = wb.add_format({'border': 1})
        self.weight_cell = wb.add_format({'border': 1, 'num_format': Template.__rounding_places(self.WEIGHT_DECIMAL)})
        self.conc_cell = wb.add_format({'border': 1, 'num_format': Template.__rounding_places(self.CONC_DECIMAL)})
        self.titrant_cell = wb.add_format({'border': 1, 'num_format': Template.__rounding_places(self.TITRANT_VOL)})
        self.titrant_result_cell = wb.add_format({'border': 1, 'num_format': Template.__rounding_places(self.TITRANT_RESULT)})
        self.lims_format = wb.add_format({'border': 1, 'num_format': Template.__rounding_places(self.LIMS)})
        self.empty_cell_format_left = wb.add_format({'border': 1, 'align': 'left'})
        self.result_cell_format = wb.add_format({'border': 1, 'num_format': '0.00'})
        self.result_string_format = wb.add_format({'align': 'right'})
        self.text_format = wb.add_format({'align': 'left',
                                          'valign': 'top',
                                          'text_wrap': True,
                                          'italic': True})
        self.reported_ppm_format = wb.add_format({'align': 'left', 'num_format': f'{Template.__rounding_places(self.LIMS)}" ppm"'})
        self.reported_percent_format = wb.add_format({'align': 'left', 'num_format': f'{Template.__rounding_places(self.LIMS)}" %"'})

        self.white_font_format = wb.add_format({'font_color': font_color})
        self.__create_header(self.digestion_sheet)
        self.sample_to_elements = {}
        self.element_to_digestion = {}

        self.format = {'white_font': self.white_font_format, 'result': self.lims_format}

        self.append = ' [dried]' if loi else ''
        self._note = ''

        self.element_set = set()
        self.samples = []

    def add_note(self, note: str):
        self._note = note

    @staticmethod
    def __rounding_places(rounding_places):
        return f'0.{"0"*rounding_places}'

    def __config(self):
        parser.optionxform = str
        parser.read('config.ini')
        self.ANALYSIS = {}
        self.COMPOUND = {}

        for key, value in parser.items('Analysis'):
            for element in re.split(r'[,\s]+', value):
                self.ANALYSIS.update({element.lower(): f'{key} analysis'})

        TITRATION_ANALYSIS = parser.get('Analysis', 'titration')
        TITRATION_ANALYSIS = map(lambda s: s.lower(), re.split(r'[,\s]+', TITRATION_ANALYSIS))
        self.TITRATION_ANALYSIS = list(TITRATION_ANALYSIS)
        self.BASE_LOAD = parser.get('Microwave Program', 'base_load')

        self.DEFAULT_ANALYSIS = parser.get('Analysis', 'default')

        for compound, analyte in parser.items('Compound'):
            for analyte in re.split(r'[,\s]+', analyte):
                if analyte.lower() not in self.COMPOUND:
                    self.COMPOUND[analyte.lower()] = []
                    self.COMPOUND[analyte.lower()].append(compound)
                else:
                    self.COMPOUND[analyte.lower()].append(compound)

        self.STEP = parser.getint('Microwave Program', 'steps')
        self.WEIGHT_DECIMAL = parser.getint('Decimal', 'weight')
        self.CONC_DECIMAL = parser.getint('Decimal', 'concentration')
        self.TITRANT_VOL = parser.getint('Decimal', 'titrant_volume')
        self.TITRANT_RESULT = parser.getint('Decimal', 'titrant_result')
        self.LIMS = parser.getint('Decimal', 'LIMS')
        self.SPACING = 2

    def __create_analysis_table(self, worksheet, analyte, sample, index):
        untagged = sample.get_analyte(analyte)
        analysis = self.ANALYSIS.get(untagged.lower(), f'{self.DEFAULT_ANALYSIS} analysis')
        analyte =  analyte if self.tag else untagged
        analysis = f'{analyte} {analysis}'
        worksheet.merge_range(self.row, 0, self.row, 1, analysis, self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{analyte}_ppm{self.append}', self.label_cell_format)
        worksheet.set_column(self.row, 3, len('#DIV/0!'))
        worksheet.write(self.row, 4, f'%{analyte}{self.append}', self.label_cell_format)
        self.__move_cursor()

        start_row = self.row
        start = 1 + index * self.replicate
        end = 1 + (index + 1) * self.replicate
        for i in range(start, end):
            worksheet.write(self.row, 0, f'{sample.id}_{i}', self.label_cell_format)
            worksheet.write(self.row, 1, '''="1/1"''', self.empty_cell_format)
            worksheet.write(self.row, 2, '', self.conc_cell)
            worksheet.write(self.row, 3, '', self.empty_cell_format)
            worksheet.write(self.row, 4, '', self.empty_cell_format)
            self.__move_cursor()
        end_row = self.row-1
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{analyte.lower()} result:', self.result_string_format)
        ppm_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 3)
        ppm_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 3)
        ppm_average = f'=AVERAGE({ppm_start}:{ppm_end})'
        worksheet.write_formula(self.row, 2, ppm_average, self.reported_ppm_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{analyte.lower()} result:', self.result_string_format)
        percent_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 4)
        percent_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 4)
        percent_average = f'=AVERAGE({percent_start}:{percent_end})'
        worksheet.write_formula(self.row, 2, percent_average, self.reported_percent_format)

        compounds = self.COMPOUND.get(analyte.lower(), False)
        if compounds:
            for compound in sorted(compounds):
                self.__move_cursor()
                worksheet.merge_range(self.row, 0, self.row, 1, f'{analyte.lower()} {compound} factor:', self.result_string_format)
                worksheet.write(self.row, 2, '', self.workbook.add_format({'align': 'left'}))
                compound_factor = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
                compound_average = f'=AVERAGE({percent_start}:{percent_end})*({compound_factor})'
                self.__move_cursor()
                worksheet.merge_range(self.row, 0, self.row, 1, f'{analyte.lower()} {compound} result:', self.result_string_format)
                worksheet.write_formula(self.row, 2, compound_average, self.reported_percent_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{analyte.lower()} lot:', self.result_string_format)
        worksheet.merge_range(self.row, 2, self.row, 5, '', self.workbook.add_format({'italic': True}))
        merge_start = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        merge_finish = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 5)
        worksheet.conditional_format(f'{merge_start}:{merge_finish}',
                                     {'type': 'blanks',
                                      'format': self.workbook.add_format({'bg_color': EMPTY_CELL})
                                      })
        lot_address = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        self.__move_cursor(self.SPACING)

        #sample = self.Sample.get(sample)
        #analyte = sample.get_analyte(analyte)
        return {'element': untagged.lower(), 'destination_address': lot_address}


    def create_analysis_worksheet(self, include_expired=False):
        print('Here before calling the class method\n\n\n\n')
        all_analytes = self.Sample.analyte_set()
        print()
        print('Here                                                     getting lot information haha')
        lot_info = query_database(list(all_analytes), include_expired)
        print(f'sample_to_elements: {self.sample_to_elements}')
        print(self.sample_to_elements)

        for sample in sorted(self.Sample.samples):
            print(type(sample))
            sample = self.Sample.get(sample)
            lots = []
            worksheet = self.workbook.add_worksheet(str(sample.id))
            self.__create_header(worksheet)
            correction_factor = 1
            if self.loi:
                correction_factor = self.__create_loi_table(sample.id, worksheet)

            #sample_obj = self.sample_to_elements[sample]
            print(f'analytes: {sample.analytes}')
            if self.__contains_chrome_3(sample.analytes):
                #s = self.sample_to_elements[sample]
                cr2o3, cr6 = self.__edit_list(sample.analytes)
            print(type(sample))
            print(f'is this correct: {sample}')
            print(f'{sample} contains: {sample.analytes}')

            for element in sample:
                index = sample.get_index(element)
                print(f'analytes: {element}')
                if element.upper() == 'LOI':
                    worksheet.autofit()
                    continue
                #print(f'and iterating through element: in self.element_to_digestion {self.element_to_digestion}')
                print(f'analytes in {sample}: {sample.analytes}')
                print(f'{sample} looking for {element}')
                #digestion_object = self.element_to_digestion[element]
                digestion_object = sample[element]
                if self.__is_chrome_3(sample.get_analyte(element).lower()):
                    self.__create_titration_table_cr3(worksheet, element, sample, cr2o3, cr6, correction_factor)
                    worksheet.autofit()
                    continue
                #if element.lower() in self.TITRATION_ANALYSIS:
                if sample.get_analyte(element).lower() in self.TITRATION_ANALYSIS:
                    move_to = self.row + 2
                    self.__create_titration_table(worksheet, element, sample, correction_factor)
                    for sample_id in [f'{sample}_{i}' for i in range(1, self.replicate + 1)]:
                        digestion_object.write_titration(move_to, sample_id, worksheet)
                        move_to += 1
                    worksheet.autofit()
                    continue
                move_to = self.row + 2
                lot = self.__create_analysis_table(worksheet, element, sample, index)
                worksheet.autofit()
                lots.append(lot)

                #remeber keys/elements should be unique if not throw exception
                for sample_id in [f'{sample.id}_{i}'for i in range(1+index*self.replicate, 1 + (index+1)*self.replicate)]:
                    digestion_object.write(move_to, sample_id, worksheet, correction_factor)
                    move_to += 1

            for lot in lots:
                data = lot_info.get(lot['element'], '')
                cell = lot['destination_address']
                worksheet.write(cell, data, self.workbook.add_format({'italic': True}))

            worksheet.write(self.row, 1, 'Note(s):', self.result_string_format)
            worksheet.merge_range(self.row, 2, self.row+2, 5, f'{self._note}', self.text_format)
            #worksheet.autofit()
            print()
        self.__create_formula_sheet()
        self.Digestion.instance = {}

    def __create_header(self, worksheet):
        self.row = 0
        worksheet.write(self.row, 0, 'Date:', self.info_format)
        worksheet.write(self.row, 1, date.today(), self.date_format)
        self.__move_cursor()
        worksheet.write(self.row, 0, 'Request ID:', self.info_format)
        worksheet.write(self.row, 1, self.request_id, self.workbook.add_format({'align': 'left'}))

        self.__move_cursor()
        self.__move_cursor(self.SPACING)

    def __contains_chrome_3(self, element_list):
        return list(filter(self.__is_chrome_3, element_list))

    def __is_chrome_3(self, element):
        return element.lower() in ['criii', 'cr3', 'cr3+', 'crthree']

    def __edit_list(self, sample_to_elements_list):
        skip_list = []
        check_list = list(map(lambda e: e.lower(), self.TITRATION_ANALYSIS))
        for e in sample_to_elements_list:
            if e.lower() in check_list:
                skip_list.append(e)
        for e in skip_list:
            sample_to_elements_list.remove(e)
        '''ensuring that sort order always put cr2o3 first in the list'''
        skip_list.sort(key=lambda e: 'o3' not in e.lower())
        return skip_list

    def __create_titration_table_cr3(self, worksheet, element, sample, cr2O3, cr6, correction_factor):
        #digestion_object = self.element_to_digestion[cr2O3]
        digestion_object = sample[cr2O3]
        move_to = self.row + 2
        total_cell = self.__create_titration_table(worksheet, cr2O3, sample, correction_factor)
        for sample_id in [f'{sample}_{i}' for i in range(1, self.replicate + 1)]:
            digestion_object.write_titration(move_to, sample_id, worksheet)
            move_to += 1

        #digestion_object = self.element_to_digestion[cr6]
        digestion_object = sample[cr6]
        move_to = self.row + 2
        cr6_cell = self.__create_titration_table(worksheet, cr6, sample, correction_factor)
        for sample_id in [f'{sample}_{i}' for i in range(1, self.replicate + 1)]:
            digestion_object.write_titration(move_to, sample_id, worksheet)
            move_to += 1

        worksheet.merge_range(self.row, 0, self.row, 1, f'{element} titration analysis', self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, f'%{cr2O3}{self.append}', self.label_cell_format)
        worksheet.write(self.row, 2, f'%{cr6}{self.append}', self.label_cell_format)
        self.__move_cursor()
        worksheet.write(self.row, 0, f'{sample}', self.label_cell_format)
        worksheet.write_formula(self.row, 1, total_cell, self.titrant_result_cell)
        worksheet.write_formula(self.row, 2, cr6_cell, self.titrant_result_cell)
        self.__move_cursor(self.SPACING)
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        worksheet.write_formula(self.row, 2, f'=({total_cell}-{cr6_cell})*({10_000})', self.reported_ppm_format)
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        worksheet.write_formula(self.row, 2, f'=({total_cell}-{cr6_cell})', self.reported_percent_format)

        compounds = self.COMPOUND.get(element.lower(), False)
        if compounds:
            percent_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
            for compound in sorted(compounds):
                self.__move_cursor()
                worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} {compound} factor:', self.result_string_format)
                worksheet.write(self.row, 2, '', self.workbook.add_format({'align': 'left'}))
                compound_factor = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
                compound_result = f'={percent_cell}*({compound_factor})'
                self.__move_cursor()
                worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} {compound} result:', self.result_string_format)
                worksheet.write_formula(self.row, 2, compound_result, self.reported_percent_format)
        self.__move_cursor(self.SPACING)

    def __create_titration_table(self, worksheet, element, sample, correction_factor):
        untagged = sample.get_analyte(element)
        element =  element if self.tag else untagged
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element} titration analysis', self.workbook.add_format({'align': 'left'}))
        self.__move_cursor()
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        worksheet.write(self.row, 2, 'titrant_volume (mL)', self.label_cell_format)
        worksheet.write(self.row, 3, f'%{element}{self.append}', self.label_cell_format)
        self.__move_cursor()
        start_row = self.row
        for sample_id in [f'{sample}_{i}' for i in range(1, self.replicate + 1)]:
            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, WEIGHT_COLUMN)
            worksheet.write(self.row, 0, f'{sample_id}', self.label_cell_format)
            worksheet.write_formula(self.row, 1, weight_cell, self.weight_cell)
            worksheet.write(self.row, 2, '', self.titrant_cell)
            worksheet.write(self.row, 3, '', self.titrant_result_cell)
            self.__move_cursor()

        end_row = self.row-1
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, 'FAS:', self.result_string_format)
        worksheet.write(self.row, 2, '', self.workbook.add_format({'align': 'left'}))
        fas_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        worksheet.conditional_format(f'{fas_cell}',
                                     {'type': 'blanks',
                                      'format': self.workbook.add_format({'bg_color': EMPTY_CELL})
                                      })
        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        ppm_start = xlsxwriter.utility.xl_rowcol_to_cell(start_row, 3)
        ppm_end = xlsxwriter.utility.xl_rowcol_to_cell(end_row, 3)
        ppm_average = f'=AVERAGE({ppm_start}:{ppm_end})*({10_000})*(1/{correction_factor})'
        worksheet.write_formula(self.row, 2, ppm_average, self.reported_ppm_format)

        self.__move_cursor()
        worksheet.merge_range(self.row, 0, self.row, 1, f'{element.lower()} result:', self.result_string_format)
        percent_average = f'=AVERAGE({ppm_start}:{ppm_end})*(1/{correction_factor})'
        worksheet.write_formula(self.row, 2, percent_average, self.reported_percent_format)
        percent_row = self.row
        self.__move_cursor(self.SPACING)
        #worksheet.autofit()

        return xlsxwriter.utility.xl_rowcol_to_cell(percent_row, 2)

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
        worksheet.write(self.row, 1, '', self.weight_cell)
        worksheet.write(self.row, 2, '', self.weight_cell)
        worksheet.write(self.row, 3, '', self.weight_cell)

        A = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 1)
        B = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 2)
        C = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 3)
        loi_formula = f'=((({B}-{A})-({C}-{A}))/({B}-{A}))*100'
        worksheet.write_formula(self.row, 4, loi_formula, self.result_cell_format)

        loi_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 4)
        worksheet.write_formula(self.row, 5, f'1-({loi_cell}/100)', self.workbook.add_format({'border': 1, 'num_format': '0.0000'}))

        correction_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row, 5, True, True)
        self.__move_cursor(self.SPACING)

        return correction_cell

    def __create_formula_sheet(self):
        self.row = 0
        formula_page = self.workbook.add_worksheet('formula_page')
        analyte_set = set(map(lambda analyte: analyte.lower(), self.element_set))
        titration_set = set(self.TITRATION_ANALYSIS)

        if analyte_set - titration_set:
            self.__write_calculation(formula_page)

        if self.loi:
            self.__write_loi(formula_page)

        if analyte_set & titration_set:
            self.__write_titration(formula_page)

        formula_page.autofit()
        self.workbook.set_properties(
            {
                'author': 'Carl Archemetre',
                'company': 'Clariant',
                'comments': 'Created with Python, XlsxWriter'
            }
        )

    def __write_loi(self, formula_page):
        formula_page.write(self.row, 0, 'A = crucible', self.italic_bold_format)
        self.__move_cursor()
        formula_page.write(self.row, 0, 'B = crucible + sample', self.italic_bold_format)
        self.__move_cursor()
        formula_page.write(self.row, 0, 'C = crucible + sample after drying', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%LOI = ([B-A]-[C-A])/(B-A)*100%', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, 'ppm M+  [dried] = ppm M+/([1-(%LOI)/100])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%M+  [dried] = %M+/([1-(%LOI)/100])', self.italic_bold_format)
        self.__move_cursor(2)
        compounds = set()
        for analyte in self.element_set:
            compounds.update(self.COMPOUND.get(analyte.lower(), []))
        compounds = list(compounds)
        compounds.sort()
        if compounds:
            for compound in compounds:
                formula_page.write(self.row, 0, f'%M{compound[0:1].upper()} [dried] = %M{compound[0:1].upper()}/([1-(%LOI)/100])', self.italic_bold_format)
                self.__move_cursor(2)

    def __write_calculation(self, formula_page):
        formula_page.write(self.row, 0, 'ppm M+ = [conc.][volume][dilution]/[weight]', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%M+ = [conc.][volume][dilution]/([weight]*10,000)', self.italic_bold_format)
        self.__move_cursor(2)
        compounds = set()
        for analyte in self.element_set:
            compounds.update(self.COMPOUND.get(analyte.lower(), []))
        compounds = list(compounds)
        compounds.sort()
        if compounds:
            for compound in compounds:
                formula_page.write(self.row, 0, f'%M{compound[0:1].upper()} = [{compound} factor]*%M+', self.italic_bold_format)
                self.__move_cursor(2)

    def __write_titration(self, formula_page):
        formula_page.write(self.row, 0, '%Cr(VI) = (1.733[mL FAS][N FAS])/([weight])', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%Cr2O3 = 1.462*[%Cr(VI)]', self.italic_bold_format)
        self.__move_cursor(2)
        formula_page.write(self.row, 0, '%Cr(III) = total_Cr - Cr(VI)', self.italic_bold_format)

    def add_microwave(self, elements: list, samples: list):
        self.element_set.update(elements)

        def create_microwave_program():
            def write(data):
                for i in range(len(data)):
                    self.digestion_sheet.write(self.row, i, data[i], self.empty_cell_format)
                self.__move_cursor()

            preset = 0
            for key in parser['Microwave Program'].keys():
                match = re.match(r'step \d+', key)
                if match:
                    data = parser.get('Microwave Program', match.group())
                    data = list(map(int, data.split(',')))
                    write(data=data)
                    preset += 1

            for _ in range(self.STEP-preset):
                write(data=['', '', '', '', ''])

        self.digestion_sheet.merge_range(self.row, 0, self.row, 4, 'Microwave', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Analyte(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Acid Cocktail', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        if self.BASE_LOAD:
            self.digestion_sheet.write(self.row, 0, 'Base Load', self.label_cell_format)
            self.digestion_sheet.merge_range(self.row, 1, self.row, 4, f'{self.BASE_LOAD}', self.empty_cell_format)
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
        analyte_set = set()
        i = []
        for sample in samples:
            if not self.Sample.get(sample):
                s = self.Sample(_id=sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)
            else:
                s = self.Sample.get(sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)

        i = max(i)
        analytes = list(analyte_set)
        analytes.sort()

        microwave = self.Digestion(name='microwave', elements=analytes, format=self.format)
        self.Sample.update(samples=samples, analytes=analytes)
        self.Sample.digest(samples=samples, digestion=microwave)

        self.__create_sample_row(samples, i, microwave, volume='')
        self.__move_cursor(self.SPACING)
        self.digestion_sheet.autofit()

    def add_hotplate(self, elements: list, samples: list):
        self.element_set.update(elements)
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Hotplate', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Analyte(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Cocktail', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        analyte_set = set()
        i = []
        for sample in samples:
            if not self.Sample.get(sample):
                s = self.Sample(_id=sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)
            else:
                s = self.Sample.get(sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)

        i = max(i)
        analytes = list(analyte_set)
        analytes.sort()

        hotplate = self.Digestion(name='hotplate', elements=analytes, format=self.format)
        self.Sample.update(samples=samples, analytes=analytes)
        self.Sample.digest(samples=samples, digestion=hotplate)

        self.__create_sample_row(samples, i, hotplate, volume='')
        self.__move_cursor(self.SPACING)
        self.digestion_sheet.autofit()

    def add_katanax(self, elements: list, samples: list):
        self.element_set.update(elements)
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Katanax', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Analyte(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Acid Cocktail', self.label_cell_format)
        self.digestion_sheet.set_column(0, 0, 12)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        analyte_set = set()
        i = []
        for sample in samples:
            if not self.Sample.get(sample):
                s = self.Sample(_id=sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)#not necessary because of the sample in this set have same element
                #print(f'inside if: {s} address: {id(s)}')
                print(f'inside if analyte_set: {analyte_set}')
                print()
            else:
                s = self.Sample.get(sample)
                s.add_analytes(analytes=elements)
                i.append(s.get_replicate_index(elements))
                analyte_set |= s.index_analytes(elements)
                #print(f'{analyte_set} in else:')
                #print(f'inside else: {s} address: {id(s)}')
                print(f'inside else analyte_set: {analyte_set}')
                print()

        i = max(i)
        print(f'\nadding analytes {elements}, with start replicate index = {i}\n')
        for sample in samples:#delete this
            s = self.Sample.get(sample)
            print(f'                                    CURRENT VIEW OF {s}')
            print(s.digestion_count)
        analytes = list(analyte_set)
        analytes.sort()
        print(f'Analytes passed to digestion object                                  : {analytes}')
        katanax = self.Digestion(name='katanax', elements=analytes, format=self.format)
        self.Sample.update(samples=samples, analytes=analytes)#updates all the samples of this set of analytes
        self.Sample.digest(samples=samples, digestion=katanax)#add this digestion object to this set of samples

        self.__create_sample_row(samples, i, katanax, volume=250)
        self.__move_cursor(self.SPACING)
        self.digestion_sheet.autofit()

    def __move_cursor(self, spacing=1):
        self.row += spacing

    def __create_sample_row(self, samples, index, digestion, volume=250):
        self.digestion_sheet.write(self.row, 0, 'sample(s)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 2, 'volume (mL)', self.label_cell_format)
        self.__move_cursor()

        for sample in samples:

            start = 1+index*self.replicate
            end = 1 + (index+1)*self.replicate
            for i in range(start, end):
                sample_id = f'{sample}_{i}'
                self.digestion_sheet.write(self.row, 0, sample_id, self.label_cell_format)
                self.digestion_sheet.write(self.row, 1, '', self.weight_cell)
                self.digestion_sheet.write(self.row, 2, volume, self.empty_cell_format)

                digestion.store_data(sample_id, self.row)
                self.__move_cursor()

    def close(self):
        self.Sample.close()

    class Sample:
        samples = {}

        @classmethod
        def close(cls):
            cls.samples.clear()

        @classmethod
        def get(cls, _id):
            return cls.samples.get(_id, None)

        @classmethod
        def update(cls, samples:list, analytes:list):
            for sample in samples:
                cls.samples.get(sample).analytes = analytes

        @classmethod
        def digest(cls, samples: list, digestion):
            '''
            Class method that add a digestion object to a set samples.
            :param samples:
            :param digestion:
            :return:
            '''
            for sample in samples:
                cls.samples.get(sample).add_digestion(digestion=digestion)

        @classmethod
        def analyte_set(cls):
            analytes = set()
            print(cls.samples)
            for sample in cls.samples.values():
                print(type(sample))
                print(f'adding to lot tracking: {[sample.get_analyte(analyte) for analyte in sample.analytes]}')
                analytes.update([sample.get_analyte(analyte) for analyte in sample.analytes])
            print('\n\n')
            print(f'analyte list: {analytes}')
            print('class varaiable:')
            return analytes

        def get_index(self, analyte: str):
            i = analyte.split('_')[1]
            return int(i)

        def get_analyte(self, analyte: str):
            return analyte.split('_')[0]

        def __init__(self, _id):
            self.id = _id
            self.digestion_count = {}
            self._analytes = []
            self.samples[_id] = self
            self.digestions = {}

        def add_analyte(self, analyte):
            if analyte in self:
                self.digestion_count[analyte] += 1
            else:
                self.digestion_count[analyte] = 0

            print(f'{analyte}: {self.digestion_count[analyte]}')
            print(f'inside add_analyte: {analyte}')
            print(f'list: {self._analytes}')

        def add_analytes(self, analytes):
            for analyte in analytes:
                self.add_analyte(analyte=analyte)

        def index_analytes(self, analytes: list):
            self.__set_replicate_index(analytes=analytes)
            print(f'all the sanples: {self.samples}')
            #print(f'address of {self}:{id(self)}')
            #print(f'inside index_set for {self}: {self.digestion_count}')
            count = map(lambda analyte: self.digestion_count[analyte], analytes)
            print(f'analytes: {analytes}')
            print(f'count: {count}')
            i = max(count)
            indexed = {f'{analyte}_{i}' for analyte in analytes}
            print(f'inside index_set: {self._analytes}')
            return indexed

        def __set_replicate_index(self, analytes):
            '''

            :param analytes:
            :return: None, sets the index for this set of analytes. Corresponds to the analyte in the set with the highest count.
            '''
            i = self.get_replicate_index(analytes=analytes)
            for analyte in analytes:
                self.digestion_count[analyte] = i

        def get_replicate_index(self, analytes: list):
            '''

            :param analytes:
            :return: the start index for this set of analyte replicates. Corresponds to the analyte in the set with the highest count.
            '''
            count = map(lambda analyte: self.digestion_count[analyte], analytes)
            return max(count)

        @property
        def analytes(self):
            return sorted(self._analytes)

        @analytes.setter
        def analytes(self, analytes):
            self._analytes.extend(analytes)

        def __iter__(self):
            return iter(self.analytes)

        def __contains__(self, analyte):
            return analyte in self.digestion_count

        def __lt__(self, sample):
            return self.id < sample.id

        def __eq__(self, sample_id: str):
            return self.id == sample_id

        def __repr__(self):
            return f'Sample({self.id})'

        def __str__(self):
            return str(self.id)

        def add_digestion(self, digestion):
            for analyte in digestion.elements.copy():
                self[analyte] = digestion

        def __getitem__(self, analyte):
            return self.digestions[analyte]

        def __setitem__(self, analyte, digestion):
            self.digestions[analyte] = digestion

    class Digestion:
        '''

        An instance of this object is pass Template.__create_sample_row as tables are created in Digestion sheet to
            collect source rows for weight and volume.

        '''
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
            self.sampleid_to_sourcerow = {}

        def write(self, to_row, sample_id, destination_worksheet, correction_factor):
            weight_ref, volume_ref = self.__read_source_data(sample_id)

            destination_worksheet.write_formula(to_row, WEIGHT_COLUMN, weight_ref, self.format['white_font'])
            destination_worksheet.write_formula(to_row, VOLUME_COLUMN, volume_ref, self.format['white_font'])

            source_dilution_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 1)
            dilution_formula = '''(LEFT({0},FIND("/",{0})-1)/RIGHT({0},LEN({0})-FIND("/", {0})))'''.format(source_dilution_cell)
            destination_worksheet.write_formula(to_row, DILUTION_COLUMN, dilution_formula, self.format['white_font'])

            conc_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 2)
            volume_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, VOLUME_COLUMN)
            dilution_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, DILUTION_COLUMN)
            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, WEIGHT_COLUMN)
            ppm_calculation = f'=(({conc_cell})*({volume_cell})*({dilution_cell}))/({weight_cell}*{correction_factor})'

            destination_worksheet.write_formula(to_row, 3, ppm_calculation, self.format['result'])

            ppm_cell = xlsxwriter.utility.xl_rowcol_to_cell(to_row, 3)
            percent_calculation = f'={ppm_cell}/{10_000}'
            destination_worksheet.write_formula(to_row, 4, percent_calculation, self.format['result'])
            #destination_worksheet.autofit()

        def write_titration(self, to_row, sample_id, destination_worksheet):
            weight_cell, _ = self.__read_source_data(sample_id)
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

            #logger.info(f'referencing {sample_id} weight from {weight_ref }')
            #logger.info(f'referencing {sample_id} volume from {volume_ref}')

            return weight_ref, volume_ref

        def store_data(self, sample_id, source_row_index):
            #logger.info(f'storing: {sample_id} @digestion_page!{source_row_index}')
            self.sampleid_to_sourcerow[sample_id] = source_row_index

        def __str__(self):
            return self.name

        def __repr__(self):
            return str(self)

'''
replicate = 2
loi = True
color = 'red'
workbook = xlsxwriter.Workbook('TEST.xlsx')
template = Template(workbook, request='TEST', replicate=replicate, tag=False, loi=loi, font_color=color)

analytes = ['Ca', 'Cu']
samples = ['200120001', '200120002']

#template.add_microwave(analytes, samples)

template.add_katanax(analytes, samples)
template.add_katanax(['Cu', 'Al'], ['200120002'])
template.add_katanax(['Al'], ['200120002'])
template.add_katanax(['NH3'], ['200120003'])

template.add_microwave(['Cu'], ['200120002'])
#template.add_katanax(['Cu'], ['200120002'])

template.create_analysis_worksheet(include_expired=False)
template.close()
workbook.close()
import os
os.startfile('TEST.xlsx')#'''

