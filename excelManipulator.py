import xlrd
import common_module as cm

def write():
    fileObj = xlrd.open_workbook('Final.xlsx')

    sheet = fileObj.sheet_by_index(0)

    headers = ['lead_id', 'title', 'description', 'skillset', 'bid', 'daysleft', 'verified', 'country',
               'state', 'projectID', 'Continent']
    cm.write_file(cm.os.getcwd(), '/manipulated_data.tsv', '\t'.join(headers)+'\n')

    lead = sheet.col_values(0)[1:]
    title = sheet.col_values(1)[1:]
    des = sheet.col_values(2)[1:]
    bid = sheet.col_values(8)[1:]
    daysleft = sheet.col_values(9)[1:]
    verified = sheet.col_values(10)[1:]
    country = sheet.col_values(11)[1:]
    state = sheet.col_values(12)[1:]
    pr_id = sheet.col_values(13)[1:]
    continent = sheet.col_values(14)[1:]
    skills = [sheet.row_values(i)[3:8] for i in range(sheet.nrows)][1:]

    for i, skill_set in enumerate(skills):
        for skill in skill_set:
            data_list = [str(int(lead[i])), str(title[i]), str(des[i]), str(skill), str(bid[i]), str(daysleft[i]),
                         str(verified[i]), str(country[i]), str(state[i]), str(pr_id[i]), str(continent[i])]
            cm.write_file(cm.os.getcwd(), '/manipulated_data.tsv', '\t'.join(data_list)+'\n')

if __name__ == '__main__':
    write()