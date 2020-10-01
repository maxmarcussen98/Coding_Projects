from mrjob.job import MRJob
from mrjob.step import MRStep
import numpy as np
import re
import csv


class MRExtract(MRJob):

    def mapper(self, _, line):
        ## Extract date and product id from csv of individual reviews
        prod_id = re.findall(r'(?<=")[A-Z0-9]{10}', line)[1]
        date = re.findall(r'(?<=")[0-9]{2}\s[0-9]{1,2},\s[0-9]{4}', line)[0]
        m = int(date[:2])
        yyyy = int(date[-4:])
        arr = (19 * 12) * [0]
        i = (yyyy - 1996) * 12 + (m - 1)
        arr[i] += 1
        yield prod_id, arr

    def combiner(self, prod_id, date_lists):
        ## Increment all frequency lists for the same mmyyyy
        yield prod_id, [sum(x) for x in (zip(*date_lists))]

    def reducer(self, prod_id, date_lists):
        ## Increment all frequency lists for the same mmyyyy
        yield prod_id, [sum(x) for x in (zip(*date_lists))]

if __name__ == '__main__':
    MRExtract.run()