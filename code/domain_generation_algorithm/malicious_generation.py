import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor





def generate_domain(year: int, month: int, day: int) -> str:
    """Generate a domain name for the given date."""
    domain = ""

    for i in range(16):
        year = ((year ^ 8 * year) >> 11) ^ ((year & 0xFFFFFFF0) << 17)
        month = ((month ^ 4 * month) >> 25) ^ 16 * (month & 0xFFFFFFF8)
        day = ((day ^ (day << 13)) >> 19) ^ ((day & 0xFFFFFFFE) << 12)
        domain += chr(((year ^ month ^ day) % 25) + 97)

    return domain + ".com"

def map_to_lowercase_letter(s):
    return ord('a') + ((s - ord('a')) % 26)

def next_domain(domain):
    pre, tail = domain.split(".")[0], domain.split(".")[1]
    dl = [ord(x) for x in list(pre)]
    dl[0] = map_to_lowercase_letter(dl[0] + dl[3])
    dl[1] = map_to_lowercase_letter(dl[0] + 2*dl[1])
    dl[2] = map_to_lowercase_letter(dl[0] + dl[2] - 1)
    dl[3] = map_to_lowercase_letter(dl[1] + dl[2] + dl[3])
    return ''.join([chr(x) for x in dl])


def wiki_ban_chinad(date):
    year, month, day = date.year, date.month, date.day
    TLDS = ['.com', '.org', '.net', '.biz', '.info', '.ru', '.cn']
    domain = generate_domain(year, month, day)
    count = 0
    date_list = []
    for i in range(10000):
        domain = next_domain(domain)
        tail_name = TLDS[count % len(TLDS)]
        domain = domain + tail_name
        count += 1
        date_list.append(domain)
    return date_list

df_dict = {'domain_name':[]}
pool = ThreadPoolExecutor(max_workers=4)
start = '2020-01-01'
end = '2020-04-07'
date_pool = []
datestart = datetime.datetime.strptime(start, '%Y-%m-%d')
dateend = datetime.datetime.strptime(end, '%Y-%m-%d')
while datestart < dateend:
    date_pool.append(datestart)
    datestart += datetime.timedelta(days=2)
for date_list in pool.map(wiki_ban_chinad, date_pool):
    df_dict['domain_name'].extend(date_list)

df = pd.DataFrame(df_dict)
print(len(df['domain_name'].unique()))
df.to_csv('../data/malicious_domain.csv', index=False)