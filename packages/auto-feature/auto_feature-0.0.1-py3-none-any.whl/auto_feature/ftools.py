import re
from featuretools.primitives import make_agg_primitive,make_trans_primitive
from featuretools.variable_types import DateOfBirth,Text,Numeric,Categorical,Boolean,Index,DatetimeTimeIndex,Datetime,TimeIndex,Discrete,Ordinal
from scipy.stats import mode
from featuretools.primitives import TimeSinceLast,TimeSinceFirst,AvgTimeBetween,TimeSince,TimeSincePrevious
import numpy as np
from v_ft.custom_primitives import *
from v_ft import time_unit as tu
import time
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
from functools import reduce
import featuretools as ft


# # featuretools class

class ft_agg(object):
    def __init__(self,config):
        self.config = config
        self.datasets=[[config['names'][i],config['datas'][i],config['keys'][i]] for i in range(len(config['names']))]
        self.frn_keys = config['frn_keys']
        self.relations = config['relations']


        self.time_idx = config['time_index']

        self.agg_kpt = config['pmt_agg_kpt'].replace(' ','').split(',') if config['pmt_agg_kpt'] else []
        self.tfm_kpt = config['pmt_tfm_kpt'].replace(' ','').split(',') if config['pmt_tfm_kpt'] else []

        self.k_n_drp=config['keys_not_drp']
        self.time_unit = config['t_unit'] #year,month,day, with year as default

        ### get intr config###
        self.if_intr = config['if_intr_value']
        self.if_prod_itr = config['if_prod_itr']
        if self.if_intr:
            self.whr_pmt = config['where_primitives'].split(',')
            self.itr_fts = config['itr_fts']
            self.itr_vals = config['itr_vals']
        if self.if_prod_itr:
            self.prod_itr_fts=config['prod_itr_fts']
            self.prod_itr_vals =config['prod_itr_vals']

        if (not self.if_intr) and (not self.if_prod_itr):
            self.whr_pmt = []
            self.itr_val = None


        # cutoff config
        self.if_cut = config['has_cutoff']
        self.cutoff = config['cutoff_date']
        # check if use cutoff dataset
        if config['use_cutoff_df']:
            self.cutoff = config['cut_df'].get_dataframe()
            self.cutoff_idx = config['cut_df_idx']

        # primitive options
        self.options = config['options']
        self.ig_vars = config['ig_vars']

    def get_prmts(self):
        # 1 define customized primitives
        #### already done by import v_ft

        # 2 change the time units of time-related primitives

        t = tu.time_unit(self.time_unit) #from time_unit in v_ft
        time_since_last = t.time_since_last
        time_since_first = t.time_since_first
        avg_time_between = t.avg_time_between
        time_since = t.time_since
        time_since_previous = t.time_since_previous
        #avg_age = AvgAge(time=self.cutoff)
        # 3 get used primitives'count,if_exist,time_since_first,time_since_last'
        whr_dic = {'count':'count','if_exist':enco,'time_since_first':time_since_first,'time_since_last':time_since_last}
        whr_pmts = [whr_dic[n] for n in self.whr_pmt]
        time_agg = {'max_age':max_age,'min_age':min_age,'max_bol':max_bol,'sum_bol':sum_bol,'time_since_first':time_since_first,'time_since_last':time_since_last,'avg_time_between':avg_time_between,'min_time':min_d,'max_time':max_d}
        time_tfm = {'time_since':time_since,'time_since_previous':time_since_previous,'seasons':seasons,'partofday':PartDay,'week_day':week_day}

        agg_used = list(set([time_agg[p] if p in time_agg else p for p in self.agg_kpt]  + whr_pmts))
        if self.tfm_kpt:
            tfm_used = list(set([time_tfm[p] if p in time_tfm else p for p in self.tfm_kpt]))
        else:
            tfm_used = []
        return agg_used,tfm_used,whr_pmts

    def get_ignore_vars(self):

        # get ignore variables
        if self.ign_var_all:
            ig_var = self.ign_var_all.replace(',','|')
            ig_vars = r'[\w\W]*('+ig_var+')'
            patterns = re.compile(ig_vars)
            ignore_vars = {self.base_name:[fe for fe in self.all_feas if patterns.match(fe)]}
        else:
            ignore_vars = {}
        return ignore_vars


    def add_r(self,es,one_df,one_col,many_df,many_col):
        es = es.add_relationship(ft.Relationship(es[one_df][one_col],es[many_df][many_col]))
        return es
    def gen_idx(self,df,cols_k=None,name_key=None,cols_f=None,name_foreign=None, keep_cols=[]):
        # concat keys and drop related cols but keep those also used to do calculation (like c_loss_typ in IP)
        col_drp = []
        if not name_key in df.columns and name_key and cols_k:
            df[name_key]=df[cols_k].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
            col_drp+=cols_k
        if not name_foreign in df.columns and name_foreign and cols_f:
            df[name_foreign] = df[cols_f].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
            col_drp+=cols_f
        #print(col_drp)
        col_drp = list(set(col_drp)-set(keep_cols))
        df = df.drop(columns=list(set(col_drp)))
        return df

    def dup_chk(self,datasets):
        # use the key subset
        for data in datasets:
            data[2].drop_duplicates(subset=data[1], keep='first', inplace=True)

    def get_entityset(self):
        # get product features
        ###############################################
        #### self.datasets [[name,data,key],....]######
        ###############################################



        ######################################################
        # concat idx and get new datasets [[name,key,data,frn],...] #
        # frn_keys can be sub-sub list [[[claimID,enityid],[claimID]]....]
        # so ustilize names to differentiate frn keys
        ## self.datasets [[name,data,key],....]
        ######################################################
        new_datasets=[]
        for i,f_keys in enumerate(self.frn_keys):
            new_frn = []
            df = self.datasets[i][1].copy()
            new_key = self.datasets[i][0]+'_key'
            if f_keys and isinstance(f_keys[0],list):
                for j,f in enumerate(f_keys):
                   # [[],[],[],[],[['ClaimID'],[]],[]]
                    #print('drp',self.k_n_drp)
                    #print('i and j',(i,j))
                    feature_not_drp = self.k_n_drp[i][j]
                    new_frn.append(self.datasets[i][0]+'_frn'+'_'+str(j))
                    #print('before gen',df.columns)
                    df=self.gen_idx(df,self.datasets[i][2],new_key,f,new_frn[j],feature_not_drp)
            else:
                feature_not_drp = self.k_n_drp[i]
                new_frn.append(self.datasets[i][0]+'_frn')
                #print('before gen',df.columns)
                df=self.gen_idx(df,self.datasets[i][2],new_key,f_keys,new_frn[0],feature_not_drp)
            new_datasets.append([self.datasets[i][0],new_key,df,new_frn])
            df=None
        #new_key = self.datasets[-1][0]+'_key'
        #df =  self.gen_idx(self.datasets[-1][1],self.datasets[-1][2],new_key,keep_cols=self.k_n_drp[-1])
        #new_datasets.append((self.datasets[-1][0],new_key,df))
        #df=None



        es = ft.EntitySet() #id='itli'
        # add entity
        ## check duplicate keys (should be avoided in the future)
        self.dup_chk(new_datasets)


        ##################################
        # get cutoff date for processing#
        ##################################
        if self.if_cut:
            df_4_cutoff = new_datasets[-1][2]
            if not self.cutoff:
                self.cutoff = 'cutoff'
                df_4_cutoff[self.cutoff] =  pd.to_datetime('today')

            if self.config['use_cutoff_df']:
                print('i am in use cutoff dataset')
                cut_off_df=self.gen_idx(self.cutoff,self.cutoff_idx,new_datasets[-1][1])
                #cols_k=None,name_key=None,c
                # if use_cutoff_df, then set up cut_df and cut_df index keys
                #config['cut_df'] = None
                #config['cut_df_idx']=None
                #self.cutoff.rename(columns={self.cutoff_idx:'CaseNo'},inplace=True)
                #cut_off_df = self.cutoff[['CaseNo',self.cutoff]]
            else:
                if is_numeric_dtype(df_4_cutoff[self.cutoff]) or is_string_dtype(df_4_cutoff[self.cutoff]):
                    df_4_cutoff[self.cutoff]=pd.to_datetime(df_4_cutoff[self.cutoff],errors='coerce')
                cut_off_df = df_4_cutoff[[new_datasets[-1][1],self.cutoff]].drop_duplicates()

               #make cotoff time at target entity level and no duplicates
        else:
            cut_off_df=None


        ##################################
          # add entities and relations
          #  frn names is list right now, so new_datasets[i][3][0]
          # #
        ##################################
        '''
        itr_data = [new_datasets[i][2].copy() for i in range(len(new_datasets))]
        if self.config['process']=='dev' or self.config['prod_sample']:
            print('get sample')
            n_sample =int(config['prod_sample'] or 1000)
            if self.if_cut:
                #print('check cut0')
                cut_off_df = cut_off_df.iloc[:n_sample,:]
                #print('check cut',cut_off_df.head())

            print('type is',type(new_datasets[-1][2]))
            new_datasets[-1][2] = new_datasets[-1][2].iloc[:n_sample,:]

        '''
        for i,data in enumerate(new_datasets):
            es.entity_from_dataframe(entity_id = data[0],
                                     dataframe=data[2],
                                     index=data[1],
                                     time_index=self.time_idx[i])#,
                                    #variable_types=self.vtype[i])
            #ents.append([data[0],])
        # add relations (one to many: one_df, one_key, many_df,many_frn)
        for r in self.relations:
            if isinstance(r[0],int):
                i,j = r
                es = self.add_r(es,new_datasets[j][0],new_datasets[j][1],new_datasets[i][0],new_datasets[i][3][0])
            else:
                for n,(i,j) in enumerate(r):
                    es = self.add_r(es,new_datasets[j][0],new_datasets[j][1],new_datasets[i][0],new_datasets[i][3][n])

            #es = self.add_r(es,new_datasets[1][0],new_datasets[1][1],new_datasets[0][0],new_datasets[0][3])
            #es = self.add_r(es,new_datasets[1][0],new_datasets[1][1],new_datasets[0][0],new_datasets[0][3])

        #es = add_r('ip_clms','ip_clm','claim_data','claims_frn')



        ##################################
          # get interesting values #
        ##################################
        self.if_prod_itr = self.config['if_prod_itr']

        if self.if_intr:
            for i,fts in enumerate(self.itr_fts):
                if fts:
                    for j,f in enumerate(fts):
                        es[new_datasets[i][0]][f].interesting_values = self.itr_vals[i][j]
            # get interesting product values
            #print("prod_itr is",(self.if_prod_itr,prod_cols))
            if self.if_prod_itr:
                for i,fe_cols in enumerate(self.prod_itr_fts):
                    if fe_cols:
                        for j,fe in enumerate(fe_cols):
                            es[new_datasets[i][0]][fe].interesting_values = self.prod_itr_vals[i][j]
        print('interesting vals finished')
        #print('check cutoff in get_entityset(): ',cutoff.info())
        '''
        if self.config['process']=='dev' or self.config['prod_sample']:
            print('get sample')
            n_sample =int(config['prod_sample'] or 1000)
            if self.if_cut:
                #print('check cut0')
                cut_off_df = cut_off_df.iloc[:n_sample,:]
                #print('check cut',cut_off_df.head())
                #print('check cut2',new_datasets[-1][1])
                used_idx = cut_off_df[new_datasets[-1][1]]
                #print('check cut3',used_idx)
                used_target = es[new_datasets[-1][0]].df.loc[used_idx,:]

            else:
                used_target = es[new_datasets[-1][0]].df.iloc[:n_sample,:]

            print('check target',new_datasets[-1][0])
            es.entity_from_dataframe(entity_id = new_datasets[-1][0],
                                             dataframe=used_target,
                                             index=new_datasets[-1][1],
                                             time_index=self.time_idx[-1],
                                            variable_types=self.vtype[-1])
        '''
        print('get entityset done')
        return es,cut_off_df


        # get dfs result
    def run_dfs(self,es=None,cutoff = None,saved_feature = None, featureonly = False, mat_name = 'all_fm', fet_name ='Whole_schema'):
        # save_res decides whether to save dfs resutls to config
        # mat_name is the key name of the saved matrix result from dfs; fet_name is the kay name of the saved features
        #start = time.time()
        #print('time window values',time_window)
        if not es:
            es,cut_off = self.get_entityset()
        #ignore_vars = self.get_ignore_vars()
        agg_used,tfm_used,whr_pmts = self.get_prmts()
        #print('get primitives over')
        #print('trans is: ',tfm_used)
        #start2 = time.time()
        dfs_res =  ft.dfs(target_entity=self.datasets[-1][0],
                                entityset=es,
                                #cutoff_time=self.config['cutoff'],
                                agg_primitives=agg_used,
                                #agg_primitives=[],
                                trans_primitives=tfm_used,
                                #ignore_entities=['matched_clm'],
                                where_primitives=whr_pmts,
                                primitive_options=self.options,
                                ignore_variables=self.ig_vars,
                                cutoff_time = cutoff,
                                features_only = featureonly
                               )
        #end2 = time.time()
        #print('get dfs over with time: ',end2-start2)

        if not featureonly:
            self.config[fet_name] = dfs_res[1]
            self.config[mat_name] = dfs_res[0]
            self.config['index_save']=dfs_res[0].index

        else:
            self.config[fet_name] = dfs_res
            print('featureonly')

        return dfs_res

    def calculate_matrix(self,es,features,cutoff):
        mtrx = ft.calculate_feature_matrix(features=features, entityset=es,cutoff_time=cutoff)
        return mtrx

    def recover_col(self,df,cols,key):
        df = df.reset_index()
        df[cols] = df[key].str.split("_",n=len(cols)-1,expand=True)
        df.drop(columns=key,inplace=True)
        return df

    def deal_colName(self,df):
        rep_names=[]
        for i in df.columns:
            rep_names.append(i.replace('(','<').replace(')','>').replace('=','@').replace('.','/').replace(',','/').replace(' ',''))
        df.columns=rep_names
        return df
