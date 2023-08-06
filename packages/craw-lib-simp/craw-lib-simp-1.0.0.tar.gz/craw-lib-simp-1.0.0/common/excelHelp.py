#!/usr/bin/python
# coding:utf-8
import xlwt, xlrd
from xlutils.copy import copy

'''
pattern_fore_colour
  0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 
  17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 
  23 = Dark Gray, the list goes on...
horz
    HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, 
    HORZ_DISTRIBUTED
vert
    VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
'''


class ExcelHelp:
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        self.titleStyle = xlwt.XFStyle()
        titleFont = xlwt.Font()
        titleFont.bold = True
        titleFont._weight = 18
        self.titleStyle.font = titleFont

        al = xlwt.Alignment()
        al.horz = xlwt.Alignment.HORZ_CENTER
        al.vert = xlwt.Alignment.VERT_CENTER
        self.titleStyle.alignment = al

        pattern = xlwt.Pattern()  # Create the Pattern
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
        pattern.pattern_fore_colour = 4
        # self.titleStyle.pattern = pattern  # Add Pattern to Style

        self.contentStyle = xlwt.XFStyle()
        contentFont = xlwt.Font()
        contentFont._weight = 15
        self.contentStyle.font = contentFont

    def excelCreate(self, titles, allValues, filepath):
        col = 0
        for title in titles:
            self.sheet.write(0, col, title, self.titleStyle)
            col = col + 1
        rows = 1

        for values in allValues:
            valueCol = 0
            for value in values:
                self.sheet.write(rows, valueCol, value, self.contentStyle)
                valueCol = valueCol + 1
            rows = rows + 1
        self.workbook.save(filepath)

    def excel_header_create(self, titles, filepath):
        if not titles:
            return
        col = 0
        for title in titles:
            self.sheet.write(0, col, title, self.titleStyle)
            col = col + 1
        self.workbook.save(filepath)

    def excel_data_write(self, data, filepath):
        if not data:
            return
        work_book = xlrd.open_workbook(filepath)
        sheet = work_book.sheet_by_index(0)
        rows_old = sheet.nrows
        print('表中已有行数', rows_old)
        for i in range(0, len(data)):
            for j in range(0, len(data[i])):
                self.sheet.write(i + rows_old, j, str(data[i][j]), self.titleStyle)
        self.workbook.save(filepath)
