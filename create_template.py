import xlsxwriter
from datetime import date

STEP = 3 #config_file
SPACING = 2 #spacing between digestion tables
#COPY = 2    #duplicates or triplicates

url = 'template.xlsx'

workbook = xlsxwriter.Workbook(url)


class Template:
    def __init__(self, wb, request_id, sample_copy):
        self.workbook = wb
        self.COPY = sample_copy
        self.row = 0
        self.digestion_sheet = wb.add_worksheet('Digestion')

        self.info_format = wb.add_format({'bold': True, 'align': 'right'})
        self.date_format = wb.add_format({'num_format': 'yyyy-mm-dd'})
        self.bold_italic_format = wb.add_format({'border': 1, 'italic': True, 'bold': True})
        self.header_format = wb.add_format({'border': 1, 'bold': True, 'align': 'center'})
        self.label_cell_format = wb.add_format({'border': 1, 'bold': True})
        self.empty_cell_format = wb.add_format({'border': 1})

        self.__create_header(request_id)
        self.dictionary = {}

    def __create_analysis_table(self, worksheet, element, samples):
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{element}_ppm', self.bold_italic_format)
        worksheet.write(self.row, 4, f'%{element}', self.bold_italic_format)
        self.__move_cursor()

        for sample in samples:
            for i in range(1, self.COPY+1):
                worksheet.write(self.row, 0, f'{sample}_{i}', self.label_cell_format)
                worksheet.set_column(0, 0, len(f'{sample}_{i}'))
                worksheet.write(self.row, 1, '', self.empty_cell_format)
                worksheet.write(self.row, 2, '', self.empty_cell_format)
                worksheet.write(self.row, 3, '', self.empty_cell_format)
                worksheet.write(self.row, 4, '', self.empty_cell_format)
                self.__move_cursor()

        self.__move_cursor(SPACING)

    def create_analysis_table(self):
        self.row = 0
        worksheet = self.workbook.add_worksheet('200126511')
        self.__create_analysis_table(worksheet, 'Ni', [200126511, 200126512])

        self.__create_analysis_table(worksheet, 'Ti', [200126512, 200126513])

    def __create_header(self, request_id):
        self.digestion_sheet.write(self.row, 0, 'Date:', self.info_format)
        self.digestion_sheet.write(self.row, 1, date.today(), self.date_format)
        self.__move_cursor()
        self.digestion_sheet.write(self.row, 0, 'Request ID:', self.info_format)
        self.digestion_sheet.write(self.row, 1, request_id)

        self.__move_cursor()
        self.__move_cursor(SPACING)

    def add_microwave(self, elements: list, samples: list):
        def step(i):
            self.digestion_sheet.write(i, 0, '', self.empty_cell_format)
            self.digestion_sheet.write(i, 1, '', self.empty_cell_format)
            self.digestion_sheet.write(i, 2, '', self.empty_cell_format)
            self.digestion_sheet.write(i, 3, '', self.empty_cell_format)
            self.digestion_sheet.write(i, 4, '', self.empty_cell_format)
            self.__move_cursor()

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
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Vessel', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Stir', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 4, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Time (min)', self.label_cell_format)
        self.digestion_sheet.set_column(0, 0, len('Time (min)'))
        self.digestion_sheet.write(self.row, 1, 'Power (W)', self.label_cell_format)
        self.digestion_sheet.set_column(1, 1, len('Power (W)')+1)
        self.digestion_sheet.write(self.row, 2, 'T1 (C)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 3, 'T2 (C)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 4, 'P (bar)', self.label_cell_format)
        self.__move_cursor()
        for _ in range(STEP):
            step(self.row)
        microwave = self.Digestion(name='microwave', elements=elements)
        self.__create_sample_row(samples, for_=microwave, volume='')
        self.__move_cursor(SPACING)
        return microwave

    def add_hotplate(self, elements: list, samples: list):
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Hotplate', self.header_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Element(s)', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, ', '.join(elements), self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'SOP#', self.label_cell_format)
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.digestion_sheet.write(self.row, 0, 'Acid Cocktail', self.label_cell_format)
        self.digestion_sheet.set_column(0, 0, len('Acid Cocktail'))
        self.digestion_sheet.merge_range(self.row, 1, self.row, 2, '', self.empty_cell_format)
        self.__move_cursor()

        self.__create_sample_row(samples, volume='')
        self.__move_cursor(SPACING)

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

        self.__create_sample_row(samples, volume=250)
        self.__move_cursor(SPACING)

    def __move_cursor(self, spacing=1):
        self.row += spacing

    def __create_sample_row(self, samples, for_, volume=250):
        self.digestion_sheet.write(self.row, 0, 'sample(s)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 2, 'volume (mL)', self.label_cell_format)
        self.digestion_sheet.set_column(2, 2, len('volume (mL)'))
        self.__move_cursor()
#We are here to solve this
        for sample in samples:
            for i in range(1, self.COPY+1):
                self.digestion_sheet.write(self.row, 0, f'{sample}_{i}', self.label_cell_format)
                self.digestion_sheet.write(self.row, 1, '', self.empty_cell_format)
                self.digestion_sheet.write(self.row, 2, volume, self.empty_cell_format)
                if sample not in self.dictionary:
                    self.dictionary[sample] = for_.elements #this is fine because I've taken the consideration that there won't be any empty list
                else:
                    self.dictionary[sample].extend(for_.elements)
                for_.store_data(self.row)
                self.__move_cursor()

    class Digestion:
        instance = 0
        WEIGHT_COLUMN = 6
        VOLUME_COLUMN = 7

        @classmethod
        def increment(cls):
            cls.instance += 1

        def __init__(self, name, elements):
            self.elements = elements
            self.name = f'{name}_{self.instance}'
            self.increment()
            self.row = []
            self.cursor = 0

        def write(self, row, worksheet):
            weight_ref, volume_ref = self.__read_data()

            worksheet.write_formula(row, self.WEIGHT_COLUMN, weight_ref)
            worksheet.write_formula(row, self.VOLUME_COLUMN, volume_ref)

        def __read_data(self):
            #self.__next()
            #print(f'reading data: {self.row[self.cursor]}')
            print(f'cursor is @: {self.cursor}')
            #print(f'type : {type(self.row)}')
            print(f'size : {len(self.row)}')
            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row[self.cursor], 1)
            volume_cell = xlsxwriter.utility.xl_rowcol_to_cell(self.row[self.cursor], 2)
            weight_ref = f'Digestion!{weight_cell}'
            volume_ref = f'Digestion!{volume_cell}'
            self.__next()
            return weight_ref, volume_ref

        def __next(self):
            print('Im here')
            print(f'cursor is at: {self.cursor}')
            print(f'size of list: {len(self.row)}')
            self.cursor += 1
            #print(f'cursor is at: {self.cursor}')
            print('Im here')
            self.cursor = self.cursor % len(self.row)

        def store_data(self, row):
            self.row.append(row)
            print(f'Im storing this data: {row}')
            print(f'size of list: {len(self.row)}')






copy = 1
start = 0

template = Template(workbook, 100482511, 2)

for i in range(copy):
    microwave_digestion = template.add_microwave(['Ca, Cu'], ['200127586'])
    worksheet = template.workbook.add_worksheet('200126512')
    microwave_digestion.write(1, worksheet)

for i in range(copy):
    #template.add_katanax(['Ti, Si'], [200127586, 200127587])
    pass

for i in range(copy):
    #template.add_hotplate(['Ag, Pd'], [200127586])
    pass

template.create_analysis_table()

#worksheet = template.workbook.add_worksheet('200126512')

#d = template.Digestion(name='microwave')
#d.store_data(0)
#d.write(1, worksheet)



workbook.close()

