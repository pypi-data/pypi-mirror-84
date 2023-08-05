import glob
from astropy.io import fits
import pandas as pd
class HeaderSummary:
    '''
    HeaderSummary does retrieving information from fits files' headers. path_list provides the search paths applied by glob.glob(). For each file, fits.open() is used to open the file. Header info is retrieved as specified in keywords.
    + Output:
      - self.table is pandas.DataFrame table.
    + Inputs:
      - path_list = a list of path to be searched for files with glob.glob
        > Ex. path_list = ['/Users/kb/15347/HST/*/*flt.fits','/Users/kb/15664/HST/*/*flt.fits']
      - keywords = a dict of (key:value) = extension number : header keyword to be searched for.
        > if None, keywords will set to {0:['ROOTNAME','DATE-OBS','FILTER','EXPSTART','EXPTIME','SUBARRAY'],}
      - sort_by = a list of keywords to be sorted using pandas.DataFrame.sort_values(by=sort_by)
        > if None, this will set to ['EXPSTART']
        > ascending and reseting indices
      - do_sort = True to sort self.table
      - colname = a list of column names, running parallel to keywords
        > pandas.DataFrame(df,columns=colname)
      - add_filepath = True to append the filepaths to the last column
    + Compute:
      - self.compute() to prepare the output self.table
    + Save:
      - self.table.to_csv() from pandas.DataFrame method.
    '''
    def __init__(self,path_list,keywords=None,sort_by=None,do_sort=True,colname=None,add_filepath=True):
        self.path_list = path_list
        self.keywords = keywords
        self.sort_by = sort_by
        self.do_sort = do_sort
        self.colname = colname
        self.add_filepath = add_filepath
        if self.keywords is None:
            self.keywords = self._keywords()
        if self.sort_by is None:
            self.sort_by = ['EXPSTART']
        if self.colname is None:
            self.colname = self._colname()
    def compute(self):
        out = []
        for jj,j in enumerate(self.path_list):
            t = glob.glob(j)
            for ii,i in enumerate(t):
                filepath = i
                tt = fits.open(filepath)
                ttt = []
                for extnum in self.keywords.keys():
                    for keyword in self.keywords[extnum]:
                        ttt.append(tt[extnum].header[keyword])
                if self.add_filepath:
                    ttt.append(filepath)
                out.append(ttt)
        if self.add_filepath:
            self.colname.append('FILEPATH')
        self.table = pd.DataFrame(out,columns=self.colname,)
        if self.do_sort:
            self._do_sort()
    def _do_sort(self):
        self.table.sort_values(by=self.sort_by,inplace=True,ignore_index=True)
    def _colname(self):
        return ['ROOTNAME','DATE-OBS','FILTER','EXPSTART','EXPTIME','SUBARRAY']
    def _keywords(self):
        return {0:['ROOTNAME','DATE-OBS','FILTER','EXPSTART','EXPTIME','SUBARRAY'],}    
    