import csv
import pandas as pd


def get_point(input_file_name, output_file_name):
    with open(output_file_name, 'w+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, dialect='excel')
        # 读要转换的txt文件，文件每行各词间以字符分隔
        with open(input_file_name, 'r', encoding='utf-8') as filein:
            for line in filein:
                line_list = line.strip(r'\n').split('	')
                spamwriter.writerow(line_list)

    # data = pd.read_csv(output_file_name, error_bad_lines=False)
    data = pd.read_csv(output_file_name)
    print(data.head(3))

    data = data[['ID', 'Latitude', 'Longitude', 'Type']]
    print(data.head(3))
    data.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    input_file = 'd07_text_meta_2020_11_16.txt'
    output_file = 'FF_ID3.csv'

    get_point(input_file, output_file)

