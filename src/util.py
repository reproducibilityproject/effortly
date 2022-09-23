# This Source Code Form is subject to the terms of the MIT
# License. If a copy of the same was not distributed with this
# file, You can obtain one at
# https://github.com/reproducibilityproject/effortly/blob/main/LICENSE

import os
import json
import filetype
import numpy as np
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from science_parse_api.api import parse_pdf
from collections import defaultdict, Counter

# function for obtaining the html from the URI
def obtain_content(url):
    """
    Gather the html result from a given url
    Parameters
    ----------
    arg1 | url: str
        The url string
    Returns
    -------
    HTML response
        urllib3.response
    """
    try:
        # create the urllib3 object
        http = urllib3.PoolManager()

        # make a request
        r = http.request('GET', url)

        # return the urllib3 response object
        return r
    except:
        # return urllib3 error object
        return urllib3.response.HTTPErrors

# function for downloading the PDF
def download_pdf(dataframe_name):
    """
    Download the PDF output of a given article
    and save to disk
    Parameters
    ----------
    arg1 | dataframe_name: str
        The name of the CSV file
    Returns
    -------
    Boolean
        urllib3.response
    """
    try:
        # read the dataframe
        dataframe = pd.read_csv(dataframe_name, low_memory=False)

        # iterate over every URL and save pdf output to disk
        for doi, url in tqdm(zip(dataframe.doi, dataframe.pdf_url)):
            # download the pdf
            content = obtain_content(url)

            # open a file
            with open(doi.replace('.', '_').replace('/', '-') + ".pdf", "wb") as fout:
                # write the contents
                fout.write(content.data)

            # close the connections
            content.close()

        # return true
        return True
    except:
        # return urllib3 error object
        return False


# function for generating single science-parse output
def gen_sci_parse_op(dir_name, host, port, file):
    """
    Generate science Parse output for a given PDF
    Parameters
    ----------
    arg1 | dir_name: str
        The directory where the PDF is located
    arg2 | host: str
        The hostname for the Science Parse docker server
    arg3 | port: str
        The port number of the Science Parse docker server
    arg4 | file: str
        The file name fo the PDF
    Returns
    -------
    Science Parse Output Dictionary
        dict
    """
    try:
        # init bool flag to generate output_dict
        generate = False

        # obtain the current directory
        owd = os.getcwd()

        # change the directory to where HTMLS are located
        os.chdir(dir_name)

        # check if given file is in the directory
        if file in os.listdir() and filetype.guess(path_to_file).mime == 'application/pdf':
            generate = True

        # change the directory back to the current working directory
        os.chdir(owd)

        if generate:
            # parse the sections of the paper
            pdf_paper = Path(dir_name, file).resolve()

            # parse the PDF
            output_dict = parse_pdf(host, pdf_paper, port=port)

        # return the output dict of the PDF
        return output_dict
    except:
        # return dict with error message
        return {'msg': 'Error generating Science Parse output'}
