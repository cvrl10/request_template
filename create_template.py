import xlsxwriter

STEP = 3 #config_file
SPACING = 2 #spacing between digestion tables
COPY = 2    #duplicates or triplicates

url = 'template.xlsx'

workbook = xlsxwriter.Workbook(url)

class Digestion:
    def __init__(self, wb):
        self.row = 0
        self.digestion_sheet = wb.add_worksheet('Digestion')
        self.header_format = wb.add_format({'border': 1, 'bold': True, 'align': 'center'})

        self.label_cell_format = wb.add_format({'border': 1, 'bold': True})
        self.empty_cell_format = wb.add_format({'border': 1})

    def microwave(self, elements: list, samples: list):
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

        self.__create_sample_row(*samples)
        self.__move_cursor(SPACING)


    def hotplate(self, elements: list, samples: list):
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

        self.__create_sample_row(*samples)
        self.__move_cursor(SPACING)

    def katanax(self, elements: list, samples: list):
        self.digestion_sheet.merge_range(self.row, 0, self.row, 2, 'Katanax', self.header_format)
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

        self.__create_sample_row(*samples)
        self.__move_cursor(SPACING)

    def __move_cursor(self, spacing=1):
        self.row += spacing


    def __create_sample_row(self, *samples):
        self.digestion_sheet.write(self.row, 0, 'sample(s)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 1, 'weight (g)', self.label_cell_format)
        self.digestion_sheet.write(self.row, 2, 'volume (mL)', self.label_cell_format)
        self.digestion_sheet.set_column(2, 2, len('volume (mL)'))
        self.__move_cursor()

        for sample in samples:
            for i in range(1, COPY+1):
                self.digestion_sheet.write(self.row, 0, f'{sample}_{i}', self.label_cell_format)
                self.digestion_sheet.write(self.row, 1, '', self.empty_cell_format)
                self.digestion_sheet.write(self.row, 2, f'', self.empty_cell_format)
                self.__move_cursor()


        pass



copy = 1
start = 0

digestion = Digestion(workbook)

for i in range(copy):
    digestion.microwave(['Ca, Cu'], [200127586])

for i in range(copy):
    digestion.katanax(['Ti, Si'], [200127586, 200127587])

for i in range(copy):
    digestion.hotplate(['Ag, Pd'], [200127586])


workbook.close()

