import re
import sys
import os
from collections import defaultdict
import collections


direct = "data/python-exercises/babynames/"


class Babies:
    def __init__(self, direct):
        self.direct = direct
        self.files = []
        for filename in os.listdir(self.direct):
            if ".html" in filename:
                self.files.append(direct + filename)
        self.babies = self.baby_dict()

    def baby_dict(self):
        year_names = {}
        for each_file in self.files:
            html = open(each_file, 'rU')
            names90 = html.read()
            year = int(re.search("(.*)</h", re.search("Popularity in (.*)", names90).group(1)).group(1))

            matches = re.findall("<tr align=\"right\"><td>(.*)</td><td>", names90)
            popular = [match.replace("</td><td>", " ") for match in matches]

            names = {}

            for name in popular:
                names[name.rsplit(' ', 1)[1]] = int(name.rsplit(' ', 1)[0])

            year_names[year] = names

        ordered = collections.OrderedDict(sorted(year_names.items(), key=lambda t: t[0]))

        return ordered

    def all_names(self):
        a_names = []
        for key, value in self.babies.items():
            for k, v in value.items():
                a_names.append({k: v})
        no_dups = defaultdict(list)

        for d in a_names:
            for key, value in d.items():
                no_dups[key].append(value)
        return no_dups

    def sorted(self):
        averages = defaultdict(list)
        for key, value in self.all_names().items():
            averages[key] = sum(value)/len(value)
        sorted_names = sorted(averages.items(), key=lambda x: x[1])
        return sorted_names

    def top_ten(self):
        k = 1
        for name in self.sorted()[:10]:
            print(k, name[0])
            k += 1

    def recent_names(self):
        names2008 = []
        for key, value in self.babies.items():
            if key == 2008:
                for k, v in value.items():
                    names2008.append(k)
        return names2008
        print(recent_names())

    def repeating_names(self):
        repeating = []
        for key, value in self.all_names().items():
            if len(value) == 10:
                repeating.append(key)
        print(repeating)


    def trending(self):
        growth_rates = {}
        for key, value in self.all_names().items():
            if key in self.all_names():
                growth_rates[key] = (value[0]/value[-1])**(1/len(value))

        growth_rates = sorted(growth_rates.items(), key = lambda t: t[1], reverse=True)

        ranks = []
        for key, value in growth_rates:
            ranks.append(key)

        print(ranks[:11])





Babies(direct).trending()

