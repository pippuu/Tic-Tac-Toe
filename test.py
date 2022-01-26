from tqdm import trange 
import time 

def line_messages(messages):
    for i, m in enumerate(messages, 1):
        trange(1, desc=str(m), position=i, bar_format='{desc}')

n_messages = 2
for i in trange(3):
    line_messages(['iter: %s' % i, 'half: %s' % (i/2)])
    time.sleep(1)

for _ in range(n_messages): print()