# -*- coding: utf-8
'''
Generate the dic of Python from xlsx file.
'''

import os
from openpyxl.reader.excel import load_workbook
from .base_crud import crud_path

xlsx_file = './database/meta/info_tags.xlsx'

if os.path.exists(xlsx_file):
    wb = load_workbook(filename=xlsx_file)
else:
    wb = None

sheet_arr = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4', 'Sheet5']


def build_dir():
    tag_arr = ['add', 'edit', 'view', 'list', 'infolist']
    path_arr = [os.path.join(crud_path, x) for x in tag_arr]
    for wpath in path_arr:
        if os.path.exists(wpath):
            continue
        os.makedirs(wpath)


class_arr = ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

# Save the sig_name( e_name) in array of each sheet. to keep the order.
sig_name_arr = {}
for sheet_name in sheet_arr:
    sig_name_arr[sheet_name] = []


def gen_html_dic():
    if wb:
        pass
    else:
        return False

    fo = open('xxtmp_html_dic.py', 'w')

    for wk_sheet in wb:
        for jj in class_arr:

            row1_val = wk_sheet['{0}1'.format(jj)].value
            row2_val = wk_sheet['{0}2'.format(jj)].value

            if row1_val and row1_val != '':

                c_name, slug_name = row1_val.split(',')
                sig_name_arr[sheet_name].append(slug_name)

                tags1 = row2_val.split(',')
                tags1 = [x.strip() for x in tags1]
                tags_dic = {}

                if len(tags1) == 1:
                    tags_dic[1] = row2_val
                    ctr_type = 'text'
                else:
                    for ii in range(len(tags1)):
                        tags_dic[ii + 1] = tags1[ii].strip()
                    ctr_type = 'select'

                fo.write('''html_{0} = {{
                    'en': 'tag_{0}',
                    'zh': '{1}',
                    'dic': {2},
                    'type': '{3}',
                    }}\n'''.format(slug_name, c_name, tags_dic, ctr_type))
    fo.close()


def gen_array_crud():
    if wb:
        pass
    else:
        return False

    kind_dic = {}
    # 父类索引
    papa_index = 1
    # 子类索引
    c_index = 1
    papa_id = 0
    uid = ''

    p_dic = {}

    with open('xxtmp_array_add_edit_view.py', 'w') as fo_edit:

        # for sheet_ranges in sheet_ranges_arr:
        # for sheet_name in sheet_arr:
        #     try:
        #         sheet_ranges = wb[sheet_name]
        #     except:
        #         return
        for sheet_ranges in wb:
            kind_sig = str(sheet_ranges['A1'].value).strip()
            # 逐行遍历
            for row_num in range(3, 1000):
                # 父类
                p_cell_value = sheet_ranges['A{0}'.format(row_num)].value
                # 子类
                c_cell_val = sheet_ranges['C{0}'.format(row_num)].value

                if p_cell_value or c_cell_val:
                    pass
                else:
                    break
                if p_cell_value and p_cell_value != '':
                    papa_id = p_cell_value.split(',')[0].strip().strip('t')
                    c_index = 1

                    # papa_id = papa_index
                    papa_index += 1
                    u_dic = {}
                    u_dic['uid'] = 'adfd'
                    u_dic['name'] = sheet_ranges['B{0}'.format(row_num)].value
                    u_dic['arr'] = []

                    p_dic = {
                        'uid': '{0}'.format(papa_id),
                        'name': sheet_ranges['B{0}'.format(row_num)].value,
                        'u_arr': [],
                    }
                    for ii, jj in zip(class_arr, sig_name_arr[sheet_name]):
                        cell_val = sheet_ranges['{0}{1}'.format(ii, row_num)].value
                        if cell_val == 1:
                            u_dic['arr'].append('{0}'.format(jj))
                    fo_edit.write('dic_{0}00 = {1}\n'.format(papa_id, u_dic['arr']))
                    fo_edit.write('kind_{0}00 = "{1}"\n'.format(papa_id, kind_sig))

                if c_cell_val and c_cell_val != '':
                    u_dic = {}
                    sun_id = sheet_ranges['B{0}'.format(row_num)].value.split(',')[0].strip().strip('t')

                    app_uid = '{0}{1}'.format(papa_id, sun_id)
                    p_dic['u_arr'].append(app_uid)
                    u_dic['uid'] = app_uid
                    u_dic['name'] = sheet_ranges['C{0}'.format(row_num)].value
                    u_dic['arr'] = []

                    for ii, jj in zip(class_arr, sig_name_arr[sheet_name]):
                        cell_val = sheet_ranges['{0}{1}'.format(ii, row_num)].value
                        if cell_val == 1:
                            u_dic['arr'].append('{0}'.format(jj))
                    fo_edit.write('dic_{0} = {1}\n'.format(app_uid, u_dic['arr']))
                    fo_edit.write('kind_{0} = "{1}"\n'.format(app_uid, kind_sig))


if __name__ == '__main__':
    gen_html_dic()
    gen_array_crud()