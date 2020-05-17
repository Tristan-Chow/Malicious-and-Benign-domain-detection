import json
import requests
from pprint import pprint
from time import sleep

# BASEURL='https://on78aebggl.execute-api.us-west-2.amazonaws.com/prod/'
BASEURL='https://nz20hcuvwd.execute-api.us-west-1.amazonaws.com/prod/predict'
USER1 = 'Lpvxw4glEq9HR0JpbubxFa5x5nlB6eHGa244CpY2'

if __name__ == '__main__':

        HEADER = 'x-api-key'
        # fqdn_endpoint = BASEURL + '/predict'
        fqdn_endpoint = BASEURL
        fqdn_api_key = USER1
        right = float(0)
        wrong = float(0)
        print("PASS/FAIL,FQDN,THREAT,PREDICTION")
        with open('../../data/model-2.csv', mode='r', encoding='utf-8') as ih:
            line = ih.readline()
            while True:
                line = ih.readline()
                if line == '':
                    break
                tokens = line.split(',')
                domain = tokens[0]
                threat = tokens[1]
                domain = domain.lstrip().rstrip().lower()
                threat = threat.lstrip().rstrip().lower()
                fqdn = domain
                payload = {'fqdn': fqdn }
                headers = {HEADER: fqdn_api_key}
                response = None
                retry_delay = 1
                for retry in range(5):
                    bad_response = True
                    response = requests.get(url=fqdn_endpoint, headers=headers, params=payload)
                    if response.reason == 'OK':
                        print('FAIL')
                        print('HEADERS')
                        pprint(headers)
                        print('PAYLOAD')
                        pprint(payload)
                        print('RESPONSE')
                        pprint(response.text)
                        sleep(retry_delay)
                        retry_delay = 2 * retry_delay
                    else:
                        break
                    if bad_response == True and retry == 4:
                        print('Retries Exhausted Exiting')
                        exit(0)
                blob = json.loads(response.text)
                pthreat = 'benign'
                if 'dga' not in blob:
                    print('FAIL')
                    exit(0)
                if blob['dga'] == True:
                    pthreat = 'dga'
                if blob['fqdn'] != fqdn:
                    print('FAIL')
                    exit(0)
                if (blob['dga'] == True and threat == 'dga') or (blob['dga'] == False and threat == 'benign'):
                    right += 1.0
                    print('Pass,' + fqdn + ',' + threat + ',' + pthreat)
                else:
                    wrong += 1.0
                    print('Fail,' + fqdn + ',' + threat + ',' + pthreat)

        score = (right / (right + wrong))
        print('Right: ', right, ' Wrong: ', wrong, 'Score: ', score * 100.0, 'Grade:', ((score - 0.50) * 50.0) + 25.0)
