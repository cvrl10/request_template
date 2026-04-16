import xlsxwriter

STEP = 3 #config_file
SPACING = 2
url = 'template.xlsx'

workbook = xlsxwriter.Workbook(url)
digestion = workbook.add_worksheet('Digestion')
row = 0
column = 0

def microwave(row, elements):
    def step(wb, start):
        format = workbook.add_format({'border': 1})
        wb.write(start, 0, '', format)
        wb.write(start, 1, '', format)
        wb.write(start, 2, '', format)
        wb.write(start, 3, '', format)
        wb.write(start, 4, '', format)
        return start+1


    format = workbook.add_format({'border': 1, 'bold': True})
    digestion.merge_range(row, 0, row, 4, 'Microwave', workbook.add_format({'border': 1,
                                                                            'bold': True,
                                                                            'align': 'center'}))
    border_format = workbook.add_format({'border': 1})
    row += 1

    digestion.write(row, column, 'Element(s)', format)
    digestion.merge_range(row, 1, row, 4, ', '.join(elements), border_format)
    row += 1

    digestion.write(row, column, 'Rack', format)
    digestion.merge_range(row, 1, row, 4, '', border_format)
    row += 1

    digestion.write(row, column, 'Cocktail', format)
    digestion.merge_range(row, 1, row, 4, '', border_format)
    row += 1

    digestion.write(row, column, 'Vessel', format)
    digestion.merge_range(row, 1, row, 4, '', border_format)
    row += 1

    digestion.write(row, column, 'Stir', format)
    digestion.merge_range(row, 1, row, 4, '', border_format)
    row += 1

    digestion.write(row, 0, 'Time (min)', format)
    digestion.set_column(0, 0, len('Time (min)'))
    digestion.write(row, 1, 'Power (W)', format)
    digestion.set_column(1, 1, len('Power (W)'))
    digestion.write(row, 2, 'T1 (C)', format)
    digestion.write(row, 3, 'T2 (C)', format)
    digestion.write(row, 4, 'P (bar)', format)
    row += 1
    for i in range(STEP):
        row = step(digestion, row)

    return row


def katanax(row, elements):
    digestion.merge_range(row, 0, row, 2, 'Katanax', workbook.add_format({'border': 1,
                                                                            'bold': True,
                                                                            'align': 'center'}))


    border_format = workbook.add_format({'border': 1})
    row += 1

    format = workbook.add_format({'border': 1, 'bold': True})

    digestion.write(row, column, 'Element(s)', format)
    #digestion.write(row, 1, ', '.join(elements), border_format)
    digestion.merge_range(row, 1, row, 2, ', '.join(elements), border_format)
    row += 1

    digestion.write(row, column, 'SOP#', format)
    #digestion.write(row, 1, '', border_format)
    digestion.merge_range(row, 1, row, 2, '', border_format)
    row += 1

    return row

#microwave(0)
#workbook.close()

copy = 2
start = 0

for i in range(copy):
    start = microwave(start, ['Ca, Cu'])
    start += SPACING

for i in range(copy):
    start = katanax(start, ['Ti, Si'])
    start += SPACING

workbook.close()

