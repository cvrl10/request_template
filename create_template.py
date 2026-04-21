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
        self.request_id = request_id
        self.COPY = sample_copy
        self.row = 0
        self.digestion_sheet = wb.add_worksheet('Digestion')

        self.info_format = wb.add_format({'bold': True, 'align': 'right'})
        self.date_format = wb.add_format({'num_format': 'yyyy-mm-dd'})
        self.bold_italic_format = wb.add_format({'border': 1, 'italic': True, 'bold': True})
        self.header_format = wb.add_format({'border': 1, 'bold': True, 'align': 'center'})
        self.label_cell_format = wb.add_format({'border': 1, 'bold': True})
        self.empty_cell_format = wb.add_format({'border': 1})

        self.__create_header(self.digestion_sheet)
        self.sample_to_elements = {}
        self.element_to_digestion = {}

    def __analysis_header(self, worksheet, element):
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{element}_ppm', self.bold_italic_format)
        worksheet.write(self.row, 4, f'%{element}', self.bold_italic_format)
        self.__move_cursor()

    def __create_analysis_table(self, worksheet, element, sample):
        worksheet.write(self.row, 0, 'sample', self.label_cell_format)
        worksheet.write(self.row, 1, 'Dilution', self.label_cell_format)
        worksheet.write(self.row, 2, 'conc. [mg/L]', self.label_cell_format)
        worksheet.set_column(2, 2, len('conc. [mg/L]'))
        worksheet.write(self.row, 3, f'{element}_ppm', self.bold_italic_format)
        worksheet.write(self.row, 4, f'%{element}', self.bold_italic_format)
        self.__move_cursor()

        print(f'inside private method: {sample}')
        for i in range(1, self.COPY+1):
            worksheet.write(self.row, 0, f'{sample}_{i}', self.label_cell_format)
            worksheet.set_column(0, 0, len(f'{sample}_{i}'))
            worksheet.write(self.row, 1, '''="1/1"''', self.empty_cell_format)
            worksheet.write(self.row, 2, '', self.empty_cell_format)
            worksheet.write(self.row, 3, '', self.empty_cell_format)
            worksheet.write(self.row, 4, '', self.empty_cell_format)
            self.__move_cursor()

        self.__move_cursor(SPACING)

    def create_analysis_table(self):
        for sample in self.sample_to_elements:
            #self.row = 0
            #worksheet = self.workbook.add_worksheet(sample)
            worksheet = self.workbook.add_worksheet(str(sample))
            self.__create_header(worksheet)
            for element in self.sample_to_elements[sample]:
            #for element in self.element_to_digestion:
                print(f'inside for_loop')
                print(f'and iterating through element: in self.element_to_digestion {self.element_to_digestion}')
                move_to = self.row+1
                self.__create_analysis_table(worksheet, element, sample)
                #remeber keys/elements should be unique if not throw exception
                print(f'this is sample: {sample}')
                digestion_object = self.element_to_digestion[element]
                print(digestion_object.name)
                for sample_id in [f'{sample}_{i}'for i in range(1, self.COPY + 1)]:
                    digestion_object.write(move_to, sample_id, worksheet)
                    move_to += 1
                #print('here')
                print(element, ' ', end='')
                #print(type(element))
            print()
            #worksheet = self.workbook.add_worksheet('200126511')
            #self.__create_analysis_table(worksheet, 'Ni', [200126511, 200126512])

        #self.__create_analysis_table(worksheet, 'Ti', [200126512, 200126513])

    def __create_header(self, worksheet):
        self.row = 0
        worksheet.write(self.row, 0, 'Date:', self.info_format)
        worksheet.write(self.row, 1, date.today(), self.date_format)
        self.__move_cursor()
        worksheet.write(self.row, 0, 'Request ID:', self.info_format)
        worksheet.write(self.row, 1, self.request_id)

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
        self.__create_sample_row(samples, microwave, volume='')
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

        hotplate = self.Digestion(name='hotplate', elements=elements)
        self.__create_sample_row(samples, hotplate, volume='')
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

        katanax = self.Digestion(name='katanax', elements=elements)
        self.__create_sample_row(samples, katanax, volume=250)
        self.__move_cursor(SPACING)

    def __move_cursor(self, spacing=1):
        self.row += spacing

    def __reset_cursor(self, move_to):
        self.row = move_to


    def __create_sample_row(self, samples, digestion, volume=250):
        self.digestion_sheet.write(self.row, 0, 'sample(s)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 2, 'volume (mL)', self.label_cell_format)
        self.digestion_sheet.set_column(2, 2, len('volume (mL)'))
        self.__move_cursor()
        print(f'{digestion.name}')
        for sample in samples:#fix here
            print(f'staring with: {sample}')
            if sample not in self.sample_to_elements:
                self.sample_to_elements[sample] = digestion.elements.copy()  # this is fine because I've taken the consideration that there won't be any empty list
                print(self.sample_to_elements)
                for element in digestion.elements:
                    print(f'from for loop: {element}')
                    print(f'from for loop: {type(element)}')
                    '''mapping each element to its Digestion object'''
                    self.element_to_digestion[element] = digestion
            else:
                # self.sample_to_elements[sample].extend(digestion.elements)
                print(f'here: {digestion.elements}')
                self.sample_to_elements[sample].extend(digestion.elements.copy())
            for i in range(1, self.COPY+1):
                sample_id = f'{sample}_{i}'
                self.digestion_sheet.write(self.row, 0, sample_id, self.label_cell_format)
                self.digestion_sheet.write(self.row, 1, '', self.empty_cell_format)
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
        WEIGHT_COLUMN = 6
        VOLUME_COLUMN = 7

        @classmethod
        def increment(cls):
            cls.instance += 1

        def __init__(self, name, elements):
            self.elements = elements
            self.name = f'{name}_{self.instance}'
            self.increment()
            self.sampleid_to_sourcerow = {}

        def write(self, to_row, sample_id, destination_worksheet):
            weight_ref, volume_ref = self.__read_source_data(sample_id)

            destination_worksheet.write_formula(to_row, self.WEIGHT_COLUMN, weight_ref)
            destination_worksheet.write_formula(to_row, self.VOLUME_COLUMN, volume_ref)

        def __read_source_data(self, sample_id):
            #for sample_id in [for i]
            print(f'type of key: {type(sample_id)}')
            print(f'key: {sample_id}')
            print(self.sampleid_to_sourcerow)
            source_row = self.sampleid_to_sourcerow[sample_id]

            weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(source_row, 1)
            volume_cell = xlsxwriter.utility.xl_rowcol_to_cell(source_row, 2)
            weight_ref = f'Digestion!{weight_cell}'
            volume_ref = f'Digestion!{volume_cell}'

            return weight_ref, volume_ref

        def store_data(self, sample_id, source_row_index):
            print(f'storing: {sample_id} @{source_row_index}')
            self.sampleid_to_sourcerow[sample_id] = source_row_index

            #print(f'Im storing this data: {row}')
            #print(f'size of list: {len(self.row)}')





copy = 1
start = 0

template = Template(workbook, 100482511, 3)
s = ['200127586', '200127587']

for i in range(copy):
    microwave_digestion = template.add_microwave(['Ca', 'Cu'], s)
    #print(microwave_digestion)

for i in range(copy):
    d = template.add_katanax(['Ti', 'Si'], ['200127587', '200127588'])
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

