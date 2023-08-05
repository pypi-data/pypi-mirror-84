__all__ = ['get']
import random

chrome_versions = ['75.0.3770.8',
                   '75.0.3770.90',
                   '76.0.3809.12',
                   '76.0.3809.126',
                   '76.0.3809.25',
                   '76.0.3809.68',
                   '77.0.3865.10',
                   '77.0.3865.40',
                   '78.0.3904.105',
                   '78.0.3904.11',
                   '78.0.3904.70',
                   '79.0.3945.16',
                   '79.0.3945.36',
                   '80.0.3987.106',
                   '80.0.3987.16',
                   '81.0.4044.138',
                   '81.0.4044.20',
                   '81.0.4044.69',
                   '83.0.4103.14',
                   '83.0.4103.39',
                   '84.0.4147.30',
                   '85.0.4183.38',
                   '85.0.4183.83',
                   '85.0.4183.87',
                   '86.0.4240.22',
                   '87.0.4280.20',
                   ]

chrome_user_agents = []
for chrome_version in chrome_versions:
    chrome_user_agents.append(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version} Safari/537.36'.format(version=chrome_version)
    )


def get():
    return random.choice(chrome_user_agents)


if __name__ == '__main__':
    for i in range(10):
        print(get())





