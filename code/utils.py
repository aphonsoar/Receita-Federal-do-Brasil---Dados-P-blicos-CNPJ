from codec import codec
import bs4 as bs
import os
import re
import subprocess
import sys
import urllib.request

bar = [
  '░', '░', '░', '░', '░',
  '░', '░', '░', '░', '░',
  '░', '░', '░', '░', '░',
  '░', '░', '░', '░', '░'
]

#%%
def replace_console(content):
  sys.stdout.write("\r" + content)
  sys.stdout.flush()

current_bar = bar.copy()

#%%
# Create this bar_progress method which is invoked automatically from wget:
def bar_progress(current, total, width=80):
  global current_bar
  bar_length = len(current_bar)
  total_done = round(current / total * bar_length)
  bar_position = total_done - 1

  if(bar_position >= 0):
    for index in range(total_done):
      current_bar[index] = '█'

  bar_layout = ''.join(current_bar)
  progress_message = "Downloading: %s [%d / %d] bytes" % (bar_layout, current, total)
  
  replace_console(progress_message)
  
  if(total_done >= bar_length):
    current_bar = bar.copy()

def get_env(env):
    return os.getenv(env)

def get_formated_pages(url):
    raw_html = urllib.request.urlopen(url)
    raw_html = raw_html.read()

    # Formatar página e converter em string
    page_items = bs.BeautifulSoup(raw_html, 'lxml')
    html_str = str(page_items)
    return html_str

def get_encoding_codec(escaped_extracted_file_path = None):
  if(os.name == 'posix'):
    commandOutput = subprocess.check_output(f'file -bi {escaped_extracted_file_path}', shell=True)
    charset = re.search('charset=(.*)', commandOutput.decode("utf-8")).group(1)
    charset = codec[charset]
    return charset
  else:
    return None