txt = '''  INSERT INTO DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B (
                                        CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY
                                        ,CUS_DO_OMS_ID, DSC_TYP_ID, DAY_DT,
      MIN_ID, ITM_ID, CUS_ORD_OMS_ID, LOC_ID, CUS_ID
                                        ,COUPON_KEY, DSC_KEY, CUS_ORD_HDR_KEY, CUS_ORD_LN_ID, RTRN_FLG, CAN_FLG, LOC_KEY, CUS_KEY, CUS_HIST_KEY, LCL_CNCY_CDE
                                        ,F_DSC_AMT_LCL, F_DSC_AMT
                                        )
                SELECT          DO_HDR.CUS_DO_HDR_KEY
                                ,SRC.CUS_DO_LN_ID
                                ,DSC_TYP.DSC_TYP_KEY
                                ,SRC.COUPON_NUM
                                ,SRC.COUPON_REF_NUM
                                ,SRC.DSC_ID
                                ,SRC.EXT_DSC_ID
                                ,SRC.DAY_DT DAY_KEY
                                ,TIM_MIN.MIN_KEY
                                ,COALESCE(ITM.ITM_KEY,-1)
                                ,MAX(SRC.CUS_DO_OMS_ID)
                                ,MAX(SRC.DSC_TYP_ID)
                                ,MAX(SRC.DAY_DT)
                                ,MAX(SRC.MIN_ID)
                                ,MAX(SRC.ITM_ID)
                                ,MAX(SRC.CUS_ORD_OMS_ID)
                                ,MAX(SRC.LOC_ID)
                                ,MAX(SRC.CUS_ID)
                                ,MAX(COALESCE(CPN.COUPON_KEY,-1))
                                ,MAX(COALESCE(DSC.DSC_KEY,-1))
                                ,MAX(COALESCE(CO_HDR.CUS_ORD_HDR_KEY,-1))
                                ,MAX(COALESCE(SRC.CUS_ORD_LN_ID,'-1'))
                                ,MAX(SRC.RTRN_FLG)
                                ,MAX(SRC.CAN_FLG)
                                ,MAX(LOC.LOC_KEY)
                                ,MAX(COALESCE(DO_HDR.CUS_KEY,-1))    AS CUS_KEY
                                ,-1 AS CUS_HIST_KEY
                                ,MAX(SRC.LCL_CNCY_CDE)
                                ,SUM(SRC.F_DSC_AMT_LCL)
                                ,SUM(CASE WHEN LOC.CNCY_CDE = 'USD'
                                THEN SRC.F_DSC_AMT_LCL
                                ELSE SRC.F_DSC_AMT_LCL * EXCRT.EXCH_RATE
                                END) AS F_DSC_AMT
                FROM "DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B" SRC
                INNER JOIN DW_PRD_DWH_V.V_DWH_F_CUS_DO_HDR_B DO_HDR ON SRC.CUS_DO_OMS_ID = DO_HDR.DO_OMS_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_TIM_MIN_OF_DAY_LU TIM_MIN ON SRC.MIN_ID = TIM_MIN.MIN_24HR_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_CUS_DSC_TYP_LU DSC_TYP ON SRC.DSC_TYP_ID = DSC_TYP.DSC_TYP_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_ORG_LOC_LU LOC ON LTRIM(SRC.LOC_ID,'0') = LOC.LOC_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_F_CUS_ORD_HDR_B CO_HDR ON SRC.CUS_ORD_OMS_ID = CO_HDR.CUS_ORD_OMS_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_D_PRD_ITM_LU ITM ON SRC.ITM_ID = ITM.BELK_ITM_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_D_CUS_DSC_LU DSC ON SRC.DSC_ID = DSC.DSC_ID
                LEFT OUTER JOIN (SELECT SRC1.CUS_DO_OMS_ID,CAST(SRC1.COUPON_NUM AS DECIMAL(18,0)) COUPON_NUM, CPN1.BEG_DT BEG_DT, CPN1.END_DT END_DT,COALESCE(CPN1.COUPON_KEY,-1)  COUPON_KEY
                                ,ROW_NUMBER() OVER (PARTITION BY SRC1.CUS_DO_OMS_ID, SRC1.COUPON_NUM ORDER BY BEG_DT DESC) RNK
                                FROM   DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B SRC1
                                INNER JOIN DW_PRD_DWH_V.V_DWH_D_COUPON_LU CPN1
                                ON CAST(SRC1.COUPON_NUM AS DECIMAL(18,0))=CAST(CPN1.COUPON_NUM AS DECIMAL(18,0))
                                AND SRC1.DAY_DT>=CPN1.BEG_DT
                                AND SRC1.DAY_DT<= CPN1.END_DT
                ) CPN
                ON CPN.CUS_DO_OMS_ID=SRC.CUS_DO_OMS_ID AND CPN.COUPON_NUM = CAST(SRC.COUPON_NUM AS DECIMAL(18,0))
                AND SRC.DAY_DT>=CPN.BEG_DT
                AND SRC.DAY_DT<=CPN.END_DT
                AND RNK=1
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_F_EXCH_RATE_LU EXCRT ON (EXCRT.FROM_CNCY_CDE = LOC.CNCY_CDE AND EXCRT.TO_CNCY_CDE = 'USD' AND SRC.DAY_DT BETWEEN EXCRT.EFF_FROM_DT AND EXCRT.EFF_TO_DT)
                GROUP BY DO_HDR.CUS_DO_HDR_KEY
                    ,DSC_TYP.DSC_TYP_KEY
                    ,SRC.COUPON_NUM
                    ,SRC.COUPON_REF_NUM
                    ,SRC.DSC_ID
                    ,SRC.EXT_DSC_ID
                    ,SRC.DAY_DT
                    ,TIM_MIN.MIN_KEY
                    ,ITM.ITM_KEY
                    ,SRC.CUS_DO_LN_ID

                '''
txt2 = '''  DELETE FROM DW_PRD_DWH.DWH_F_CUS_DO_DSC_LN_B
                WHERE CUS_DO_HDR_KEY in (SELECT CUS_DO_HDR_KEY FROM  DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B)
                AND (CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY) not in (SELECT CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY FROM  DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B)
              '''

txt3 = '''  UPDATE DW_PRD_DWH.DWH_F_CUS_DO_DSC_LN_B tgt
                     SET COUPON_KEY = src.COUPON_KEY, DSC_KEY = src.DSC_KEY, CUS_ORD_HDR_KEY = src.CUS_ORD_HDR_KEY, CUS_ORD_LN_ID = src.CUS_ORD_LN_ID, RTRN_FLG = src.RTRN_FLG, CAN_FLG = src.CAN_FLG, LOC_KEY = src.LOC_KEY, CUS_KEY = src.CUS_KEY, CUS_HIST_KEY = src.CUS_HIST_KEY, LCL_CNCY_CDE = src.LCL_CNCY_CDE,
                     F_DSC_AMT_LCL = src.F_DSC_AMT_LCL, F_DSC_AMT = src.F_DSC_AMT
                     , RCD_UPD_TS=CURRENT_TIMESTAMP
                    FROM DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B src
                  WHERE src.CUS_DO_HDR_KEY = tgt.CUS_DO_HDR_KEY AND src.CUS_DO_LN_ID = tgt.CUS_DO_LN_ID AND src.DSC_TYP_KEY = tgt.DSC_TYP_KEY AND src.COUPON_NUM = tgt.COUPON_NUM AND src.COUPON_REF_NUM = tgt.COUPON_REF_NUM AND src.DSC_ID = tgt.DSC_ID AND src.EXT_DSC_ID = tgt.EXT_DSC_ID AND src.DAY_KEY = tgt.DAY_KEY AND src.MIN_KEY = tgt.MIN_KEY AND src.ITM_KEY = tgt.ITM_KEY
                    AND (coalesce(to_char(src.COUPON_KEY),'0') <> coalesce(to_char(tgt.COUPON_KEY),'0') OR coalesce(to_char(src.DSC_KEY),'0') <> coalesce(to_char(tgt.DSC_KEY),'0') OR coalesce(to_char(src.CUS_ORD_HDR_KEY),'0') <> coalesce(to_char(tgt.CUS_ORD_HDR_KEY),'0') OR coalesce(to_char(src.CUS_ORD_LN_ID),'0') <> coalesce(to_char(tgt.CUS_ORD_LN_ID),'0') OR coalesce(to_char(src.RTRN_FLG),'0') <> coalesce(to_char(tgt.RTRN_FLG),'0') OR coalesce(to_char(src.CAN_FLG),'0') <> coalesce(to_char(tgt.CAN_FLG),'0') OR coalesce(to_char(src.LOC_KEY),'0') <> coalesce(to_char(tgt.LOC_KEY),'0') OR coalesce(to_char(src.CUS_KEY),'0') <> coalesce(to_char(tgt.CUS_KEY),'0') OR coalesce(to_char(src.CUS_HIST_KEY),'0') <> coalesce(to_char(tgt.CUS_HIST_KEY),'0') OR coalesce(to_char(src.LCL_CNCY_CDE),'0') <> coalesce(to_char(tgt.LCL_CNCY_CDE),'0')OR coalesce(to_char(tgt.F_DSC_AMT_LCL),'0') <> coalesce(to_char(src.F_DSC_AMT_LCL),'0')OR coalesce(to_char(tgt.F_DSC_AMT),'0') <> coalesce(to_char(src.F_DSC_AMT),'0'))
              
 '''


def validity_check(list_elements):
	list_of_acceptables = ['DW_','DWH','STG','TMP']
	
	x = [True for i in list_of_acceptables if i in list_elements]
	
	return x 

# validity_checker = validity_check('_DW_asdaSTGDWH')


def replacer(txt):
	txt = txt.replace('\n',' ')
	txt = txt.replace('"','')

	txt = txt.split(' ')
	# txt = txt.remove('')
	txt = [x for x in txt if x]			#bcoz empty string is interpreted as False in Python
	return txt

# txt = replacer(txt3)
# print(txt)

def source_table_finder(txt):
	DELETE_FLG  = False
	UPDATE_FLG  = False
    

	txt_list = replacer(txt)

	possible_target_list = []
	# print(txt_list)
###Checking for DELETE FROM Statement
	for index,value in enumerate(txt_list):
		if value == 'DELETE' and txt_list[index+1] == 'FROM':
			DELETE_FLG = True 
			print('Its a DELETE FROM type query')
		if value == 'UPDATE':
			UPDATE_FLG = True

	source_table_list = []

	if UPDATE_FLG == False and DELETE_FLG==False :
		print('Its a  normal insert-select query')


	target_table = [txt_list[i+1] for i,x in enumerate(txt_list) if x == 'INTO']

	possible_target_list += target_table

	if UPDATE_FLG is True:
		print('Its an update Statement query ')
		# target_table.clear()
		target_table = [txt_list[i+1] for i,x in enumerate(txt_list) if x == 'UPDATE']
        possible_target_list += target_table
        # possible_target_list += target_table

	# if DELETE_FLG is False:
	source_candidate  = [txt_list[i+1] for i,x in enumerate(txt_list) if x == 'FROM']
	source_table_list += source_candidate
	# print(source_table_list)

	source_candidate.clear()
	# print(source_candidate)
	source_candidate  = [txt_list[i+1] for i,x in enumerate(txt_list) if x == 'JOIN']


	filtered_candidate = [i for i in source_candidate if validity_check(i)]

	if(len(source_candidate)!= len(filtered_candidate)):
		print('Certain list_elements has been removed')

	source_table_list += filtered_candidate

	if DELETE_FLG is True:
		target_table = source_table_list[0]
		source_table_list = source_table_list[1:]
        # possible_target_list += target_table



	# print('Before removing duplicate list_elements :')
	# print(len(source_table_list))
	# print(source_table_list)

	# print('after removing duplicate list_elements :')
	source_table_list = [i for i in set(source_table_list)]
	print('Source table count : ' + str(len(source_table_list)))
	print('Source Tables : ')
	print(source_table_list)
	print('Target Table  : ')
	print(target_table)



txtx = ''' 2020-03-07 03:40:29.688945: #################### Get MODULE_TYPE and JOB_ID ####################
2020-03-07 03:40:29.689377: 
            SELECT MODULE_TYP, JOB_ID FROM DW_PRD_DWH_V.V_DWH_C_BATCH_SCRIPTS WHERE LOWER(SCRIPT_NAME)=LOWER('f_cus_do_dsc_ln_ld')
            
2020-03-07 03:40:30.004992: Snowflake Query ID :0192b908-00df-7b17-0000-02c5786bf2fa
2020-03-07 03:40:30.005168: Number of rows:1
2020-03-07 03:40:30.005311: MODULE_TYPE: NTLY
2020-03-07 03:40:30.005554: JOB_ID: 148
2020-03-07 03:40:30.005689: #################### Get LAST_RUN_BOOKMARK ####################
2020-03-07 03:40:30.005934: 
                SELECT MAX(PARAM_VALUE) FROM DW_PRD_DWH_V.V_DWH_C_PARAM
                WHERE PARAM_NAME = 'CURR_DAY'
2020-03-07 03:40:30.252689: Snowflake Query ID :0192b908-0043-9f36-0000-02c5786be642
2020-03-07 03:40:30.252913: Number of rows:1
2020-03-07 03:40:30.253062: CURR_DAY : 2020-03-06
2020-03-07 03:40:30.253343: #################### Script Started ####################
2020-03-07 03:40:30.253508: #################### Get Last Run State ####################
2020-03-07 03:40:30.253925: 
            SELECT coalesce(max(BATCH_ID),0) BATCH_ID
                , coalesce(max(CASE WHEN STATUS = 'COMPLETE' THEN -1
                       WHEN STATUS = 'RESTART' THEN 1
                       ELSE 2 END), 0) STATUS
                , coalesce(max(BOOKMARK), '') BOOKMARK
            FROM DW_PRD_DWH_V.V_DWH_C_BATCH_LOG
            WHERE JOB_ID = '148'
                AND BATCH_ID = (SELECT COALESCE(MAX(BATCH_ID),0) FROM DW_PRD_DWH_V.V_DWH_C_BATCH_LOG WHERE JOB_ID = '148')
                AND BUSINESS_DATE = '2020-03-06'
                
2020-03-07 03:40:31.784604: Snowflake Query ID :0192b908-0010-3a2f-0000-02c5786be64a
2020-03-07 03:40:31.784895: Number of rows:1
2020-03-07 03:40:31.785059: LAST_BATCH_ID: 0
2020-03-07 03:40:31.785191: LAST_RUN_STATUS: 0
2020-03-07 03:40:31.785326: LAST_RUN_BOOKMARK: 
2020-03-07 03:40:31.785437: #################### Get Script Parameter ####################
2020-03-07 03:40:31.785598: 
            SELECT TRIM(PARAM_NAME), TRIM(PARAM_VALUE)
            FROM DW_PRD_DWH_V.V_DWH_C_SCRIPTS_PARAM
            WHERE LOWER(SCRIPT_NAME)=LOWER('f_cus_do_dsc_ln_ld')
2020-03-07 03:40:32.376777: Snowflake Query ID :0192b908-0052-a0d3-0000-02c5786be682
2020-03-07 03:40:32.376991: Number of rows:2
2020-03-07 03:40:32.377169: #################### Get BATCH_ID ####################
2020-03-07 03:40:32.377368: 
            SELECT COALESCE(MAX(BATCH_ID),0) FROM DW_PRD_DWH_V.V_DWH_C_BATCH_LOG WHERE MODULE_NAME='NTLY'
            
2020-03-07 03:40:33.157932: Snowflake Query ID :0192b908-00d4-32fc-0000-02c5786be696
2020-03-07 03:40:33.158117: Number of rows:1
2020-03-07 03:40:33.158261: BATCH_ID: 147
2020-03-07 03:40:33.158356: BATCH_ID: 147
2020-03-07 03:40:33.158479: BOOKMARK: NONE
2020-03-07 03:40:33.158607: #################### Starting Script ####################
2020-03-07 03:40:33.158820: 
                INSERT INTO DW_PRD_DWH.DWH_C_BATCH_LOG  (
                        BATCH_ID
                       ,JOB_ID
                       ,MODULE_NAME
                       ,JOB_NAME
                       ,BUSINESS_DATE
                       ,START_TIMESTAMP
                       ,END_TIMESTAMP
                       ,STATUS
                       ,ERROR_DETAIL
                       ,BOOKMARK
                       ,LOGFILE)
                   SELECT 147
                         ,148
                         ,'NTLY'
                        ,'f_cus_do_dsc_ln_ld'
                         ,'2020-03-06'
                         ,CURRENT_TIMESTAMP
                         ,NULL
                         ,'RUNNING'
                         ,''
                         ,'NONE'
                         ,'/apps/cdwrootprd/loading/log/f_cus_do_dsc_ln_ld_20200307034028.log'
                 
2020-03-07 03:40:34.469695: Snowflake Query ID :0192b908-002b-be5c-0000-02c5786be6b2
2020-03-07 03:40:34.469855: Number of rows:1
2020-03-07 03:40:34.470032: SELECT TRIM(PARAM_VALUE) FROM DW_PRD_DWH_V.V_DWH_C_PARAM where UPPER(PARAM_NAME) = UPPER('CUS_ORD_LOAD')
2020-03-07 03:40:34.972248: Snowflake Query ID :0192b908-0000-91ec-0000-02c5786be6ce
2020-03-07 03:40:34.972448: Number of rows:1
2020-03-07 03:40:34.972739: SELECT TRIM(PARAM_VALUE) FROM DW_PRD_DWH_V.V_DWH_C_PARAM where UPPER(PARAM_NAME) = UPPER('CUS_ORD_DELTA_DURATION')
2020-03-07 03:40:35.849927: Snowflake Query ID :0192b908-001d-c574-0000-02c5786bf35a
2020-03-07 03:40:35.850128: Number of rows:1
2020-03-07 03:40:35.850400: TRUNCATE TABLE DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B
2020-03-07 03:40:36.793578: Snowflake Query ID :0192b908-00a4-0be0-0000-02c5786be6da
2020-03-07 03:40:36.793906: Number of rows:1
2020-03-07 03:40:36.794071: Staging Table Truncated
2020-03-07 03:40:36.794224: #################### Stage table loading from TABLE STARTED ####################
2020-03-07 03:40:36.794494: 
                    SELECT
                        listagg(COLUMN_NAME,',')
                    FROM (
                        SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = 'STG_F_CUS_DO_DSC_LN_B' AND TABLE_SCHEMA = 'DW_PRD_STG'
                      ) TBL
                    
2020-03-07 03:40:39.898401: Snowflake Query ID :0192b908-00f8-7992-0000-02c5786be6e6
2020-03-07 03:40:39.898650: Number of rows:1
2020-03-07 03:40:39.898959: INSERT INTO DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B
            (COUPON_REF_NUM,CUS_ORD_OMS_ID,CUS_DO_LN_ID,EXT_DSC_ID,DSC_TYP_ID,DAY_DT,DSC_ID,CUS_ORD_LN_ID,ITM_ID,LOC_ID,CUS_DO_OMS_ID,CUS_ID,LCL_CNCY_CDE,CAN_FLG,F_DSC_AMT_LCL,MIN_ID,COUPON_NUM,RTRN_FLG)
            SELECT COUPON_REF_NUM,CUS_ORD_OMS_ID,CUS_DO_LN_ID,EXT_DSC_ID,DSC_TYP_ID,DAY_DT,DSC_ID,CUS_ORD_LN_ID,ITM_ID,LOC_ID,CUS_DO_OMS_ID,CUS_ID,LCL_CNCY_CDE,CAN_FLG,F_DSC_AMT_LCL,MIN_ID,COUPON_NUM,RTRN_FLG 
            FROM DW_PRD_STG0.STG_F_CUS_DO_DSC_LN_B 
            WHERE STG_BUSINESS_DT =to_date('20200306','yyyymmdd')
2020-03-07 03:40:46.852701: Snowflake Query ID :0192b908-005c-c039-0000-02c5786bf37a
2020-03-07 03:40:46.852899: Number of rows:362743
2020-03-07 03:40:46.853110: #################### Checking PK constraint count integrity ####################
2020-03-07 03:40:46.853298: describe table DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B
2020-03-07 03:40:46.975891: Snowflake Query ID :0192b908-0078-34c5-0000-02c5786be72e
2020-03-07 03:40:46.976092: Number of rows:18
2020-03-07 03:40:46.976302: #################### No PK found ####################
2020-03-07 03:40:46.976444: #################### Stage table loaded!!! ####################
2020-03-07 03:40:46.976580: STG_F_CUS_DO_DSC_LN_B loaded successfully
2020-03-07 03:40:46.976689: #################### Set BOOKMARK ####################
2020-03-07 03:40:46.976854:                    AFTER_STG_LOAD
2020-03-07 03:40:46.976981: ######################################################
2020-03-07 03:40:46.977077: Load into Temp Table Started
2020-03-07 03:40:46.977252: Truncate Temp Table
2020-03-07 03:40:46.977465: TRUNCATE TABLE DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B
2020-03-07 03:40:47.687519: Snowflake Query ID :0192b908-00cb-dcdd-0000-02c5786be736
2020-03-07 03:40:47.687717: Number of rows:1
2020-03-07 03:40:47.687877: TMP_F_CUS_DO_DSC_LN_B truncated successfully
2020-03-07 03:40:47.687969: Loading TMP_F_CUS_DO_DSC_LN_B
2020-03-07 03:40:47.688509: 
              INSERT INTO DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B (
                                        CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY
                                        ,CUS_DO_OMS_ID, DSC_TYP_ID, DAY_DT,
      MIN_ID, ITM_ID, CUS_ORD_OMS_ID, LOC_ID, CUS_ID
                                        ,COUPON_KEY, DSC_KEY, CUS_ORD_HDR_KEY, CUS_ORD_LN_ID, RTRN_FLG, CAN_FLG, LOC_KEY, CUS_KEY, CUS_HIST_KEY, LCL_CNCY_CDE
                                        ,F_DSC_AMT_LCL, F_DSC_AMT
                                        )
                SELECT          DO_HDR.CUS_DO_HDR_KEY
                                ,SRC.CUS_DO_LN_ID
                                ,DSC_TYP.DSC_TYP_KEY
                                ,SRC.COUPON_NUM
                                ,SRC.COUPON_REF_NUM
                                ,SRC.DSC_ID
                                ,SRC.EXT_DSC_ID
                                ,SRC.DAY_DT DAY_KEY
                                ,TIM_MIN.MIN_KEY
                                ,COALESCE(ITM.ITM_KEY,-1)
                                ,MAX(SRC.CUS_DO_OMS_ID)
                                ,MAX(SRC.DSC_TYP_ID)
                                ,MAX(SRC.DAY_DT)
                                ,MAX(SRC.MIN_ID)
                                ,MAX(SRC.ITM_ID)
                                ,MAX(SRC.CUS_ORD_OMS_ID)
                                ,MAX(SRC.LOC_ID)
                                ,MAX(SRC.CUS_ID)
                                ,MAX(COALESCE(CPN.COUPON_KEY,-1))
                                ,MAX(COALESCE(DSC.DSC_KEY,-1))
                                ,MAX(COALESCE(CO_HDR.CUS_ORD_HDR_KEY,-1))
                                ,MAX(COALESCE(SRC.CUS_ORD_LN_ID,'-1'))
                                ,MAX(SRC.RTRN_FLG)
                                ,MAX(SRC.CAN_FLG)
                                ,MAX(LOC.LOC_KEY)
                                ,MAX(COALESCE(DO_HDR.CUS_KEY,-1))    AS CUS_KEY
                                ,-1 AS CUS_HIST_KEY
                                ,MAX(SRC.LCL_CNCY_CDE)
                                ,SUM(SRC.F_DSC_AMT_LCL)
                                ,SUM(CASE WHEN LOC.CNCY_CDE = 'USD'
                                THEN SRC.F_DSC_AMT_LCL
                                ELSE SRC.F_DSC_AMT_LCL * EXCRT.EXCH_RATE
                                END) AS F_DSC_AMT
                FROM "DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B" SRC
                INNER JOIN DW_PRD_DWH_V.V_DWH_F_CUS_DO_HDR_B DO_HDR ON SRC.CUS_DO_OMS_ID = DO_HDR.DO_OMS_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_TIM_MIN_OF_DAY_LU TIM_MIN ON SRC.MIN_ID = TIM_MIN.MIN_24HR_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_CUS_DSC_TYP_LU DSC_TYP ON SRC.DSC_TYP_ID = DSC_TYP.DSC_TYP_ID
                INNER JOIN DW_PRD_DWH_V.V_DWH_D_ORG_LOC_LU LOC ON LTRIM(SRC.LOC_ID,'0') = LOC.LOC_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_F_CUS_ORD_HDR_B CO_HDR ON SRC.CUS_ORD_OMS_ID = CO_HDR.CUS_ORD_OMS_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_D_PRD_ITM_LU ITM ON SRC.ITM_ID = ITM.BELK_ITM_ID
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_D_CUS_DSC_LU DSC ON SRC.DSC_ID = DSC.DSC_ID
                LEFT OUTER JOIN (SELECT SRC1.CUS_DO_OMS_ID,CAST(SRC1.COUPON_NUM AS DECIMAL(18,0)) COUPON_NUM, CPN1.BEG_DT BEG_DT, CPN1.END_DT END_DT,COALESCE(CPN1.COUPON_KEY,-1)  COUPON_KEY
                                ,ROW_NUMBER() OVER (PARTITION BY SRC1.CUS_DO_OMS_ID, SRC1.COUPON_NUM ORDER BY BEG_DT DESC) RNK
                                FROM   DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B SRC1
                                INNER JOIN DW_PRD_DWH_V.V_DWH_D_COUPON_LU CPN1
                                ON CAST(SRC1.COUPON_NUM AS DECIMAL(18,0))=CAST(CPN1.COUPON_NUM AS DECIMAL(18,0))
                                AND SRC1.DAY_DT>=CPN1.BEG_DT
                                AND SRC1.DAY_DT<= CPN1.END_DT
                ) CPN
                ON CPN.CUS_DO_OMS_ID=SRC.CUS_DO_OMS_ID AND CPN.COUPON_NUM = CAST(SRC.COUPON_NUM AS DECIMAL(18,0))
                AND SRC.DAY_DT>=CPN.BEG_DT
                AND SRC.DAY_DT<=CPN.END_DT
                AND RNK=1
                LEFT OUTER JOIN DW_PRD_DWH_V.V_DWH_F_EXCH_RATE_LU EXCRT ON (EXCRT.FROM_CNCY_CDE = LOC.CNCY_CDE AND EXCRT.TO_CNCY_CDE = 'USD' AND SRC.DAY_DT BETWEEN EXCRT.EFF_FROM_DT AND EXCRT.EFF_TO_DT)
                GROUP BY DO_HDR.CUS_DO_HDR_KEY
                    ,DSC_TYP.DSC_TYP_KEY
                    ,SRC.COUPON_NUM
                    ,SRC.COUPON_REF_NUM
                    ,SRC.DSC_ID
                    ,SRC.EXT_DSC_ID
                    ,SRC.DAY_DT
                    ,TIM_MIN.MIN_KEY
                    ,ITM.ITM_KEY
                    ,SRC.CUS_DO_LN_ID
               
2020-03-07 03:40:57.748953: Snowflake Query ID :0192b908-009b-c930-0000-02c5786bf3be
2020-03-07 03:40:57.749113: Number of rows:362509
2020-03-07 03:40:57.749248: Checking temp reject records
2020-03-07 03:40:57.749419: 
                    SELECT count(*) FROM (SELECT DISTINCT CUS_DO_OMS_ID, DSC_TYP_ID, EXT_DSC_ID, DAY_DT FROM DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B)TMP
                    
2020-03-07 03:40:58.838478: Snowflake Query ID :0192b908-007c-9da8-0000-02c5786be7ba
2020-03-07 03:40:58.838621: Number of rows:1
2020-03-07 03:40:58.838791: 
                    SELECT count(*) FROM (SELECT DISTINCT CUS_DO_OMS_ID, DSC_TYP_ID, EXT_DSC_ID, DAY_DT FROM DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B)TMP
                    
2020-03-07 03:40:59.728276: Snowflake Query ID :0192b908-00f4-03b4-0000-02c5786be7c2
2020-03-07 03:40:59.728423: Number of rows:1
2020-03-07 03:40:59.728595: 
                    SELECT COUNT(*) FROM  INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'REJ_F_CUS_DO_DSC_LN_B' AND TABLE_SCHEMA = 'DW_PRD_STG'
                    
2020-03-07 03:41:02.920102: Snowflake Query ID :0192b908-0079-2827-0000-02c5786be7ca
2020-03-07 03:41:02.920259: Number of rows:1
2020-03-07 03:41:02.920376: Checking feasibility for truncating Reject table REJ_F_CUS_DO_DSC_LN_B
2020-03-07 03:41:02.920565: 
                        SELECT PROCESS_READY_STATUS
                        FROM
                        (
                        SELECT F.*, ROW_NUMBER() OVER (PARTITION BY REJECT_TABLE_NAME ORDER BY BATCH_ID DESC ,JOB_ID DESC,REJ_TIMESTAMP DESC) RNK from  DW_PRD_DWH_V.V_DWH_C_REJ_TBL_PROCESS f
                        WHERE REJECT_TABLE_NAME= 'REJ_F_CUS_DO_DSC_LN_B'
                        ) AA
                        WHERE RNK=1
                        
2020-03-07 03:41:03.569916: Snowflake Query ID :0192b909-00d6-4347-0000-02c5786bf40e
2020-03-07 03:41:03.570066: Number of rows:1
2020-03-07 03:41:03.570257: 
                    SELECT
                        listagg(COLUMN_NAME,',')
                    FROM (
                        SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = 'STG_F_CUS_DO_DSC_LN_B' AND TABLE_SCHEMA = 'DW_PRD_STG'
                      ) TBL
                    
2020-03-07 03:41:05.373466: Snowflake Query ID :0192b909-0004-e668-0000-02c5786bf412
2020-03-07 03:41:05.373625: Number of rows:1
2020-03-07 03:41:05.373725: Loading reject data in reject table : DW_PRD_STG.REJ_F_CUS_DO_DSC_LN_B
2020-03-07 03:41:05.373982: 
                    INSERT INTO DW_PRD_STG.REJ_F_CUS_DO_DSC_LN_B (CUS_DO_OMS_ID,CUS_ID,LCL_CNCY_CDE,CAN_FLG,F_DSC_AMT_LCL,ITM_ID,LOC_ID,COUPON_REF_NUM,CUS_ORD_OMS_ID,DAY_DT,DSC_ID,CUS_ORD_LN_ID,MIN_ID,CUS_DO_LN_ID,EXT_DSC_ID,DSC_TYP_ID,COUPON_NUM,RTRN_FLG, BUSINESS_DT,REJ_TIMESTAMP,BATCH_ID,JOB_ID)
                        SELECT
                            CUS_DO_OMS_ID,CUS_ID,LCL_CNCY_CDE,CAN_FLG,F_DSC_AMT_LCL,ITM_ID,LOC_ID,COUPON_REF_NUM,CUS_ORD_OMS_ID,DAY_DT,DSC_ID,CUS_ORD_LN_ID,MIN_ID,CUS_DO_LN_ID,EXT_DSC_ID,DSC_TYP_ID,COUPON_NUM,RTRN_FLG
                            ,'2020-03-06' BUSINESS_DT
                            ,CURRENT_TIMESTAMP::timestamp_ntz REJ_TIMESTAMP
                            ,147        BATCH_ID
                            ,148          JOB_ID
                        FROM
                            DW_PRD_STG.STG_F_CUS_DO_DSC_LN_B src
                        WHERE (NVL(CUS_DO_OMS_ID,'0'),NVL(DSC_TYP_ID,'0'),NVL(EXT_DSC_ID,'0'),NVL(DAY_DT,'0')) NOT IN
                            ( SELECT
                            NVL(CUS_DO_OMS_ID,'0'),NVL(DSC_TYP_ID,'0'),NVL(EXT_DSC_ID,'0'),NVL(DAY_DT,'0')
                            FROM
                                DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B
                            )
                    
2020-03-07 03:41:07.132952: Snowflake Query ID :0192b909-0032-20a5-0000-02c5786bf41e
2020-03-07 03:41:07.133107: Number of rows:9
2020-03-07 03:41:07.133251: Recording log of reject data in DWH_C_REJ_TBL_PROCESS table
2020-03-07 03:41:07.133452: 
                    INSERT INTO DW_PRD_DWH.DWH_C_REJ_TBL_PROCESS
                    (
                        BATCH_ID
                        ,JOB_ID
                        ,REJECT_TABLE_NAME
                        ,PROCESS_READY_STATUS
                        ,REJ_TIMESTAMP
                    )
                    values
                    (
                        147
                        ,148
                        ,'REJ_F_CUS_DO_DSC_LN_B'
                        ,'N'
                        ,CURRENT_TIMESTAMP
                    )
                    
2020-03-07 03:41:08.445532: Snowflake Query ID :0192b909-0001-5bdf-0000-02c5786be802
2020-03-07 03:41:08.445693: Number of rows:1
2020-03-07 03:41:08.445899: 
                        SELECT TRIM(COUNT(*)) FROM DW_PRD_STG.REJ_F_CUS_DO_DSC_LN_B WHERE JOB_ID=148 AND BUSINESS_DT = DATE '2020-03-06'
                        
2020-03-07 03:41:08.909627: Snowflake Query ID :0192b909-0043-8ccf-0000-02c5786bf42e
2020-03-07 03:41:08.909774: Number of rows:1
2020-03-07 03:41:08.909909: REJ_COUNT = 1
2020-03-07 03:41:08.910005: TMP_F_CUS_DO_DSC_LN_B loaded successfully
2020-03-07 03:41:08.910097: #################### Set BOOKMARK ####################
2020-03-07 03:41:08.910183:                    AFTER_LOAD_TEMP_TABLE
2020-03-07 03:41:08.910270: ######################################################
2020-03-07 03:41:08.910363: Loading DWH_F_CUS_DO_DSC_LN_B
2020-03-07 03:41:08.910454: Truncate Temp Table TMP_F_CUS_DO_TXN_LN_B
2020-03-07 03:41:08.910609: TRUNCATE TABLE DW_PRD_TMP.TMP_F_CUS_DO_TXN_LN_B
2020-03-07 03:41:09.573673: Snowflake Query ID :0192b909-00f3-cbdd-0000-02c5786bf432
2020-03-07 03:41:09.573888: Number of rows:1
2020-03-07 03:41:09.573988: TMP_F_CUS_DO_TXN_LN_B truncated successfully
2020-03-07 03:41:09.574091: Loading TMP_F_CUS_DO_TXN_LN_B
2020-03-07 03:41:09.574289: 
              DELETE FROM DW_PRD_DWH.DWH_F_CUS_DO_DSC_LN_B
                WHERE CUS_DO_HDR_KEY in (SELECT CUS_DO_HDR_KEY FROM  DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B)
                AND (CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY) not in (SELECT CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY FROM  DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B)
               
2020-03-07 03:41:19.539928: Snowflake Query ID :0192b909-00f3-5e4c-0000-02c5786be812
2020-03-07 03:41:19.540070: Number of rows:14
2020-03-07 03:41:19.540214: #################### Update Standard Fact Using Temp ####################
2020-03-07 03:41:19.540428: 
              UPDATE DW_PRD_DWH.DWH_F_CUS_DO_DSC_LN_B tgt
                     SET COUPON_KEY = src.COUPON_KEY, DSC_KEY = src.DSC_KEY, CUS_ORD_HDR_KEY = src.CUS_ORD_HDR_KEY, CUS_ORD_LN_ID = src.CUS_ORD_LN_ID, RTRN_FLG = src.RTRN_FLG, CAN_FLG = src.CAN_FLG, LOC_KEY = src.LOC_KEY, CUS_KEY = src.CUS_KEY, CUS_HIST_KEY = src.CUS_HIST_KEY, LCL_CNCY_CDE = src.LCL_CNCY_CDE,
                     F_DSC_AMT_LCL = src.F_DSC_AMT_LCL, F_DSC_AMT = src.F_DSC_AMT
                     , RCD_UPD_TS=CURRENT_TIMESTAMP
                    FROM DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B src
                  WHERE src.CUS_DO_HDR_KEY = tgt.CUS_DO_HDR_KEY AND src.CUS_DO_LN_ID = tgt.CUS_DO_LN_ID AND src.DSC_TYP_KEY = tgt.DSC_TYP_KEY AND src.COUPON_NUM = tgt.COUPON_NUM AND src.COUPON_REF_NUM = tgt.COUPON_REF_NUM AND src.DSC_ID = tgt.DSC_ID AND src.EXT_DSC_ID = tgt.EXT_DSC_ID AND src.DAY_KEY = tgt.DAY_KEY AND src.MIN_KEY = tgt.MIN_KEY AND src.ITM_KEY = tgt.ITM_KEY
                    AND (coalesce(to_char(src.COUPON_KEY),'0') <> coalesce(to_char(tgt.COUPON_KEY),'0') OR coalesce(to_char(src.DSC_KEY),'0') <> coalesce(to_char(tgt.DSC_KEY),'0') OR coalesce(to_char(src.CUS_ORD_HDR_KEY),'0') <> coalesce(to_char(tgt.CUS_ORD_HDR_KEY),'0') OR coalesce(to_char(src.CUS_ORD_LN_ID),'0') <> coalesce(to_char(tgt.CUS_ORD_LN_ID),'0') OR coalesce(to_char(src.RTRN_FLG),'0') <> coalesce(to_char(tgt.RTRN_FLG),'0') OR coalesce(to_char(src.CAN_FLG),'0') <> coalesce(to_char(tgt.CAN_FLG),'0') OR coalesce(to_char(src.LOC_KEY),'0') <> coalesce(to_char(tgt.LOC_KEY),'0') OR coalesce(to_char(src.CUS_KEY),'0') <> coalesce(to_char(tgt.CUS_KEY),'0') OR coalesce(to_char(src.CUS_HIST_KEY),'0') <> coalesce(to_char(tgt.CUS_HIST_KEY),'0') OR coalesce(to_char(src.LCL_CNCY_CDE),'0') <> coalesce(to_char(tgt.LCL_CNCY_CDE),'0')OR coalesce(to_char(tgt.F_DSC_AMT_LCL),'0') <> coalesce(to_char(src.F_DSC_AMT_LCL),'0')OR coalesce(to_char(tgt.F_DSC_AMT),'0') <> coalesce(to_char(src.F_DSC_AMT),'0'))
              
2020-03-07 03:41:39.803229: Snowflake Query ID :0192b909-007b-bde6-0000-02c5786be882
2020-03-07 03:41:39.803385: Number of rows:2789
2020-03-07 03:41:39.803525: #################### Set BOOKMARK ####################
2020-03-07 03:41:39.803616:                    AFTER_UPDATE_FACT_FROM_TEMP
2020-03-07 03:41:39.803706: ######################################################
2020-03-07 03:41:39.803798: #################### Inserts into Standard Fact Using Temp ####################
2020-03-07 03:41:39.804049: 
              INSERT INTO DW_PRD_DWH.DWH_F_CUS_DO_DSC_LN_B
                  (       CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY
                          ,COUPON_KEY, DSC_KEY, CUS_ORD_HDR_KEY, CUS_ORD_LN_ID, RTRN_FLG, CAN_FLG, LOC_KEY, CUS_KEY, CUS_HIST_KEY, LCL_CNCY_CDE
                        , F_DSC_AMT_LCL, F_DSC_AMT
                        , RCD_INS_TS
                        , RCD_UPD_TS
                   )
                    SELECT CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY
                           ,COUPON_KEY, DSC_KEY, CUS_ORD_HDR_KEY, CUS_ORD_LN_ID, RTRN_FLG, CAN_FLG, LOC_KEY, CUS_KEY, CUS_HIST_KEY, LCL_CNCY_CDE
                         , F_DSC_AMT_LCL, F_DSC_AMT
                         , CURRENT_TIMESTAMP RCD_INS_TS
                         , CURRENT_TIMESTAMP RCD_UPD_TS
                    FROM DW_PRD_TMP.TMP_F_CUS_DO_DSC_LN_B src
                    WHERE ( CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY ) NOT IN ( SELECT CUS_DO_HDR_KEY, CUS_DO_LN_ID, DSC_TYP_KEY, COUPON_NUM, COUPON_REF_NUM, DSC_ID, EXT_DSC_ID, DAY_KEY, MIN_KEY, ITM_KEY FROM DW_PRD_DWH_V.V_DWH_F_CUS_DO_DSC_LN_B)
                    
              
2020-03-07 03:41:46.447424: Snowflake Query ID :0192b909-0086-63e5-0000-02c5786be926
2020-03-07 03:41:46.447579: Number of rows:126149
2020-03-07 03:41:46.447717: #################### Set BOOKMARK ####################
2020-03-07 03:41:46.447808:                    AFTER_INSERT_FACT_FROM_TEMP
2020-03-07 03:41:46.447942: ######################################################
2020-03-07 03:41:46.448058: DWH_F_CUS_DO_DSC_LN_B Load Complete
2020-03-07 03:41:46.448165: #################### End Script: Successful ####################
2020-03-07 03:41:46.448371: 
            UPDATE DW_PRD_DWH.DWH_C_BATCH_LOG
            SET END_TIMESTAMP = CURRENT_TIMESTAMP
                , STATUS = 'COMPLETE'
                , BOOKMARK = 'COMPLETE'
            WHERE BATCH_ID = 147 AND JOB_ID = 148
2020-03-07 03:41:48.130171: Snowflake Query ID :0192b909-008c-18bd-0000-02c5786bf572
2020-03-07 03:41:48.130319: Number of rows:1
2020-03-07 03:41:48.130575: 
                INSERT INTO DW_PRD_DWH.DWH_C_LOAD_AUDIT_LOG
                ( AUDIT_TIMESTAMP, SCRIPT_NAME, BATCH_ID, SOURCE, TARGET, ACTIVITY_TYPE, ACTIVITY_COUNT, COUNT_IN_SOURCE )
                VALUES 
(TO_TIMESTAMP('2020-03-07 03:40:46.853052'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', 'STG_F_CUS_DO_DSC_LN_B', 'INSERT', 362743, null),
(TO_TIMESTAMP('2020-03-07 03:40:57.749211'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', 'TMP_F_CUS_DO_DSC_LN_B', 'INSERT', 362509, null),
(TO_TIMESTAMP('2020-03-07 03:41:07.133207'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', 'REJ_F_CUS_DO_DSC_LN_B', 'INSERT', 9, null),
(TO_TIMESTAMP('2020-03-07 03:41:19.540170'), 'f_cus_do_dsc_ln_ld', 147, 'DWH_F_CUS_DO_DSC_LN_B', 'DWH_F_CUS_DO_DSC_LN_B', 'DELETE', 14, null),
(TO_TIMESTAMP('2020-03-07 03:41:39.803487'), 'f_cus_do_dsc_ln_ld', 147, 'TMP_F_CUS_DO_DSC_LN_B', 'DWH_F_CUS_DO_DSC_LN_B', 'UPDATE', 2789, null),
(TO_TIMESTAMP('2020-03-07 03:41:46.447682'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', 'DWH_F_CUS_DO_DSC_LN_B', 'INSERT', 126149, null)
2020-03-07 03:41:49.463506: Snowflake Query ID :0192b909-008b-0506-0000-02c5786bf57e
2020-03-07 03:41:49.463688: Number of rows:6
2020-03-07 03:41:49.463794: ################ Archiving Stage data to Archive #########
2020-03-07 03:41:49.464001: INSERT INTO DW_PRD_ARC.ARC_STG_F_CUS_DO_DSC_LN_B SELECT * FROM DW_PRD_STG0.STG_F_CUS_DO_DSC_LN_B 
                           WHERE STG_BUSINESS_DT = TO_DATE('20200306','yyyymmdd')
2020-03-07 03:41:51.221403: Snowflake Query ID :0192b909-0074-b1f7-0000-02c5786bf592
2020-03-07 03:41:51.221562: Number of rows:362743
2020-03-07 03:41:51.221778: DELETE FROM DW_PRD_STG0.STG_F_CUS_DO_DSC_LN_B 
                        WHERE STG_BUSINESS_DT = TO_DATE('20200306','yyyymmdd')
2020-03-07 03:41:52.147908: Snowflake Query ID :0192b909-00f1-4bce-0000-02c5786bf5a6
2020-03-07 03:41:52.148073: Number of rows:362743
2020-03-07 03:41:52.148197: Script Completed
2020-03-07 03:41:52.148381: 
                INSERT INTO DW_PRD_DWH.DWH_C_LOAD_AUDIT_LOG
                ( AUDIT_TIMESTAMP, SCRIPT_NAME, BATCH_ID, SOURCE, TARGET, ACTIVITY_TYPE, ACTIVITY_COUNT, COUNT_IN_SOURCE )
                VALUES 
(TO_TIMESTAMP('2020-03-07 03:41:51.221666'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', 'ARC_STG_F_CUS_DO_DSC_LN_B', 'INSERT', 362743, null),
(TO_TIMESTAMP('2020-03-07 03:41:52.148164'), 'f_cus_do_dsc_ln_ld', 147, 'STG_F_CUS_DO_DSC_LN_B', null, 'DELETE', 362743, null)
2020-03-07 03:41:53.586969: Snowflake Query ID :0192b909-00ba-7662-0000-02c5786be9aa
2020-03-07 03:41:53.587128: Number of rows:2
2020-03-07 03:41:53.718040: Database Session Closed

'''
source_table_finder(txtx)
# source_table_finder(txt2)
# source_table_finder(txt)