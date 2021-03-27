#!/usr/bin/env bash

# ###############################################################
# SECTION: WCRP CMIP6 VOCABULARY BASH VARS
# ###############################################################

# Activity ID - canonical name
declare -a CMIP6_ACTIVITY_ID=(
	'aerchemmip'
	'c4mip'
	'cdrmip'
	'cfmip'
	'cmip'
	'cordex'
	'damip'
	'dcpp'
	'dynvarmip'
	'fafmip'
	'geomip'
	'gmmip'
	'highresmip'
	'ismip6'
	'ls3mip'
	'lumip'
	'omip'
	'pamip'
	'pmip'
	'rfmip'
	'scenariomip'
	'simip'
	'viacsab'
	'volmip'
)

# Activity ID - raw name
declare -a CMIP6_ACTIVITY_ID_RAW=(
	'AerChemMIP'
	'C4MIP'
	'CDRMIP'
	'CFMIP'
	'CMIP'
	'CORDEX'
	'DAMIP'
	'DCPP'
	'DynVarMIP'
	'FAFMIP'
	'GeoMIP'
	'GMMIP'
	'HighResMIP'
	'ISMIP6'
	'LS3MIP'
	'LUMIP'
	'OMIP'
	'PAMIP'
	'PMIP'
	'RFMIP'
	'ScenarioMIP'
	'SIMIP'
	'VIACSAB'
	'VolMIP'
)

# Institution ID - canonical name
declare -a CMIP6_INSTITUTION_ID=(
	'aer'
	'as-rcec'
	'awi'
	'bcc'
	'bnu'
	'cams'
	'cas'
	'cccma'
	'cccr-iitm'
	'cmcc'
	'cnrm-cerfacs'
	'csir-wits-csiro'
	'csiro'
	'csiro-arccss'
	'csiro-cosima'
	'dkrz'
	'dwd'
	'e3sm-project'
	'ec-earth-consortium'
	'ecmwf'
	'fio-qlnm'
	'hammoz-consortium'
	'inm'
	'inpe'
	'ipsl'
	'kiost'
	'llnl'
	'messy-consortium'
	'miroc'
	'mohc'
	'mpi-m'
	'mri'
	'nasa-giss'
	'nasa-gsfc'
	'ncar'
	'ncc'
	'nerc'
	'nims-kma'
	'niwa'
	'noaa-gfdl'
	'ntu'
	'nuist'
	'pcmdi'
	'pnnl-waccem'
	'rte-rrtmgp-consortium'
	'rubisco'
	'snu'
	'thu'
	'ua'
	'uci'
	'uhh'
	'uoft'
	'utas'
)

# Institution ID - raw name
declare -a CMIP6_INSTITUTION_ID_RAW=(
	'AER'
	'AS-RCEC'
	'AWI'
	'BCC'
	'BNU'
	'CAMS'
	'CAS'
	'CCCma'
	'CCCR-IITM'
	'CMCC'
	'CNRM-CERFACS'
	'CSIR-Wits-CSIRO'
	'CSIRO'
	'CSIRO-ARCCSS'
	'CSIRO-COSIMA'
	'DKRZ'
	'DWD'
	'E3SM-Project'
	'EC-Earth-Consortium'
	'ECMWF'
	'FIO-QLNM'
	'HAMMOZ-Consortium'
	'INM'
	'INPE'
	'IPSL'
	'KIOST'
	'LLNL'
	'MESSy-Consortium'
	'MIROC'
	'MOHC'
	'MPI-M'
	'MRI'
	'NASA-GISS'
	'NASA-GSFC'
	'NCAR'
	'NCC'
	'NERC'
	'NIMS-KMA'
	'NIWA'
	'NOAA-GFDL'
	'NTU'
	'NUIST'
	'PCMDI'
	'PNNL-WACCEM'
	'RTE-RRTMGP-Consortium'
	'RUBISCO'
	'SNU'
	'THU'
	'UA'
	'UCI'
	'UHH'
	'UofT'
	'UTAS'
)

# MIP-era ID - canonical name
declare -a CMIP6_MIP_ERA=(
	'cmip1'
	'cmip2'
	'cmip3'
	'cmip5'
	'cmip6'
)

# MIP-era ID - raw name
declare -a CMIP6_MIP_ERA_RAW=(
	'CMIP1'
	'CMIP2'
	'CMIP3'
	'CMIP5'
	'CMIP6'
)

# Source ID - canonical name
declare -a CMIP6_SOURCE_ID=(
	'4aop-v1-5'
	'access-cm2'
	'access-esm1-5'
	'access-om2'
	'access-om2-025'
	'arts-2-3'
	'awi-cm-1-1-hr'
	'awi-cm-1-1-lr'
	'awi-cm-1-1-mr'
	'awi-esm-1-1-lr'
	'awi-esm-2-1-lr'
	'bcc-csm2-hr'
	'bcc-csm2-mr'
	'bcc-esm1'
	'besm-2-9'
	'bnu-esm-1-1'
	'cam-mpas-hr'
	'cam-mpas-lr'
	'cams-csm1-0'
	'canesm5'
	'canesm5-canoe'
	'cas-esm2-0'
	'cesm1-1-cam5-cmip5'
	'cesm1-cam5-se-hr'
	'cesm1-cam5-se-lr'
	'cesm1-waccm-sc'
	'cesm2'
	'cesm2-fv2'
	'cesm2-se'
	'cesm2-waccm'
	'cesm2-waccm-fv2'
	'ciesm'
	'cmcc-cm2-hr4'
	'cmcc-cm2-sr5'
	'cmcc-cm2-vhr4'
	'cmcc-esm2'
	'cnrm-cm6-1'
	'cnrm-cm6-1-hr'
	'cnrm-esm2-1'
	'cnrm-esm2-1-hr'
	'csiro-mk3l-1-3'
	'e3sm-1-0'
	'e3sm-1-1'
	'e3sm-1-1-eca'
	'ec-earth3'
	'ec-earth3-aerchem'
	'ec-earth3-cc'
	'ec-earth3-gris'
	'ec-earth3-hr'
	'ec-earth3-lr'
	'ec-earth3-veg'
	'ec-earth3-veg-lr'
	'ec-earth3p'
	'ec-earth3p-hr'
	'ec-earth3p-vhr'
	'ecmwf-ifs-hr'
	'ecmwf-ifs-lr'
	'ecmwf-ifs-mr'
	'emac-2-53-vol'
	'emac-2-54-aerchem'
	'fgoals-f3-h'
	'fgoals-f3-l'
	'fgoals-g3'
	'fio-esm-2-0'
	'gfdl-am4'
	'gfdl-cm4'
	'gfdl-cm4c192'
	'gfdl-esm2m'
	'gfdl-esm4'
	'gfdl-global-lbl'
	'gfdl-grtcode'
	'gfdl-om4p5b'
	'gfdl-rfm-disort'
	'giss-e2-1-g'
	'giss-e2-1-g-cc'
	'giss-e2-1-h'
	'giss-e2-2-g'
	'giss-e3-g'
	'hadgem3-gc31-hh'
	'hadgem3-gc31-hm'
	'hadgem3-gc31-ll'
	'hadgem3-gc31-lm'
	'hadgem3-gc31-mh'
	'hadgem3-gc31-mm'
	'hiram-sit-hr'
	'hiram-sit-lr'
	'icon-esm-lr'
	'iitm-esm'
	'inm-cm4-8'
	'inm-cm5-0'
	'inm-cm5-h'
	'ipsl-cm5a2-inca'
	'ipsl-cm6a-atm-hr'
	'ipsl-cm6a-lr'
	'ipsl-cm6a-lr-inca'
	'ipsl-cm7a-atm-hr'
	'ipsl-cm7a-atm-lr'
	'kace-1-0-g'
	'kiost-esm'
	'lblrtm-12-8'
	'mcm-ua-1-0'
	'miroc-es2h'
	'miroc-es2h-nb'
	'miroc-es2l'
	'miroc6'
	'mpi-esm-1-2-ham'
	'mpi-esm1-2-hr'
	'mpi-esm1-2-lr'
	'mpi-esm1-2-xr'
	'mri-agcm3-2-h'
	'mri-agcm3-2-s'
	'mri-esm2-0'
	'nesm3'
	'nicam16-7s'
	'nicam16-8s'
	'nicam16-9d-l78'
	'nicam16-9s'
	'norcpm1'
	'noresm1-f'
	'noresm2-hh'
	'noresm2-lm'
	'noresm2-lme'
	'noresm2-lmec'
	'noresm2-mh'
	'noresm2-mm'
	'pcmdi-test-1-0'
	'rrtmg-lw-4-91'
	'rrtmg-sw-4-02'
	'rte-rrtmgp-181204'
	'sam0-unicon'
	'taiesm1'
	'taiesm1-timcom'
	'ukesm1-0-ll'
	'ukesm1-0-mmh'
	'ukesm1-ice-ll'
	'uoft-ccsm4'
	'vresm-1-0'
)

# Source ID - raw name
declare -a CMIP6_SOURCE_ID_RAW=(
	'4AOP-v1-5'
	'ACCESS-CM2'
	'ACCESS-ESM1-5'
	'ACCESS-OM2'
	'ACCESS-OM2-025'
	'ARTS-2-3'
	'AWI-CM-1-1-HR'
	'AWI-CM-1-1-LR'
	'AWI-CM-1-1-MR'
	'AWI-ESM-1-1-LR'
	'AWI-ESM-2-1-LR'
	'BCC-CSM2-HR'
	'BCC-CSM2-MR'
	'BCC-ESM1'
	'BESM-2-9'
	'BNU-ESM-1-1'
	'CAM-MPAS-HR'
	'CAM-MPAS-LR'
	'CAMS-CSM1-0'
	'CanESM5'
	'CanESM5-CanOE'
	'CAS-ESM2-0'
	'CESM1-1-CAM5-CMIP5'
	'CESM1-CAM5-SE-HR'
	'CESM1-CAM5-SE-LR'
	'CESM1-WACCM-SC'
	'CESM2'
	'CESM2-FV2'
	'CESM2-SE'
	'CESM2-WACCM'
	'CESM2-WACCM-FV2'
	'CIESM'
	'CMCC-CM2-HR4'
	'CMCC-CM2-SR5'
	'CMCC-CM2-VHR4'
	'CMCC-ESM2'
	'CNRM-CM6-1'
	'CNRM-CM6-1-HR'
	'CNRM-ESM2-1'
	'CNRM-ESM2-1-HR'
	'CSIRO-Mk3L-1-3'
	'E3SM-1-0'
	'E3SM-1-1'
	'E3SM-1-1-ECA'
	'EC-Earth3'
	'EC-Earth3-AerChem'
	'EC-Earth3-CC'
	'EC-Earth3-GrIS'
	'EC-Earth3-HR'
	'EC-Earth3-LR'
	'EC-Earth3-Veg'
	'EC-Earth3-Veg-LR'
	'EC-Earth3P'
	'EC-Earth3P-HR'
	'EC-Earth3P-VHR'
	'ECMWF-IFS-HR'
	'ECMWF-IFS-LR'
	'ECMWF-IFS-MR'
	'EMAC-2-53-Vol'
	'EMAC-2-54-AerChem'
	'FGOALS-f3-H'
	'FGOALS-f3-L'
	'FGOALS-g3'
	'FIO-ESM-2-0'
	'GFDL-AM4'
	'GFDL-CM4'
	'GFDL-CM4C192'
	'GFDL-ESM2M'
	'GFDL-ESM4'
	'GFDL-GLOBAL-LBL'
	'GFDL-GRTCODE'
	'GFDL-OM4p5B'
	'GFDL-RFM-DISORT'
	'GISS-E2-1-G'
	'GISS-E2-1-G-CC'
	'GISS-E2-1-H'
	'GISS-E2-2-G'
	'GISS-E3-G'
	'HadGEM3-GC31-HH'
	'HadGEM3-GC31-HM'
	'HadGEM3-GC31-LL'
	'HadGEM3-GC31-LM'
	'HadGEM3-GC31-MH'
	'HadGEM3-GC31-MM'
	'HiRAM-SIT-HR'
	'HiRAM-SIT-LR'
	'ICON-ESM-LR'
	'IITM-ESM'
	'INM-CM4-8'
	'INM-CM5-0'
	'INM-CM5-H'
	'IPSL-CM5A2-INCA'
	'IPSL-CM6A-ATM-HR'
	'IPSL-CM6A-LR'
	'IPSL-CM6A-LR-INCA'
	'IPSL-CM7A-ATM-HR'
	'IPSL-CM7A-ATM-LR'
	'KACE-1-0-G'
	'KIOST-ESM'
	'LBLRTM-12-8'
	'MCM-UA-1-0'
	'MIROC-ES2H'
	'MIROC-ES2H-NB'
	'MIROC-ES2L'
	'MIROC6'
	'MPI-ESM-1-2-HAM'
	'MPI-ESM1-2-HR'
	'MPI-ESM1-2-LR'
	'MPI-ESM1-2-XR'
	'MRI-AGCM3-2-H'
	'MRI-AGCM3-2-S'
	'MRI-ESM2-0'
	'NESM3'
	'NICAM16-7S'
	'NICAM16-8S'
	'NICAM16-9D-L78'
	'NICAM16-9S'
	'NorCPM1'
	'NorESM1-F'
	'NorESM2-HH'
	'NorESM2-LM'
	'NorESM2-LME'
	'NorESM2-LMEC'
	'NorESM2-MH'
	'NorESM2-MM'
	'PCMDI-test-1-0'
	'RRTMG-LW-4-91'
	'RRTMG-SW-4-02'
	'RTE-RRTMGP-181204'
	'SAM0-UNICON'
	'TaiESM1'
	'TaiESM1-TIMCOM'
	'UKESM1-0-LL'
	'UKESM1-0-MMh'
	'UKESM1-ice-LL'
	'UofT-CCSM4'
	'VRESM-1-0'
)

# Experiment ID - canonical name
declare -a CMIP6_EXPERIMENT_ID=(
	'1pctco2'
	'1pctco2-4xext'
	'1pctco2-bgc'
	'1pctco2-cdr'
	'1pctco2-rad'
	'1pctco2ndep'
	'1pctco2ndep-bgc'
	'1pctco2to4x-withism'
	'a4sst'
	'a4sstice'
	'a4sstice-4xco2'
	'abrupt-0p5xco2'
	'abrupt-2xco2'
	'abrupt-4xco2'
	'abrupt-solm4p'
	'abrupt-solp4p'
	'amip'
	'amip-4xco2'
	'amip-a4sst-4xco2'
	'amip-climsic'
	'amip-climsst'
	'amip-future4k'
	'amip-hist'
	'amip-hld'
	'amip-lfmip-pdlc'
	'amip-lfmip-pobs'
	'amip-lfmip-rmlc'
	'amip-lwoff'
	'amip-m4k'
	'amip-p4k'
	'amip-p4k-lwoff'
	'amip-piforcing'
	'amip-tip'
	'amip-tip-nosh'
	'aqua-4xco2'
	'aqua-control'
	'aqua-control-lwoff'
	'aqua-p4k'
	'aqua-p4k-lwoff'
	'control-1950'
	'control-slab'
	'dcppa-assim'
	'dcppa-hindcast'
	'dcppa-hindcast-niff'
	'dcppa-historical-niff'
	'dcppb-forecast'
	'dcppc-amv-extrop-neg'
	'dcppc-amv-extrop-pos'
	'dcppc-amv-neg'
	'dcppc-amv-pos'
	'dcppc-amv-trop-neg'
	'dcppc-amv-trop-pos'
	'dcppc-atl-control'
	'dcppc-atl-pacemaker'
	'dcppc-atl-spg'
	'dcppc-forecast-addagung'
	'dcppc-forecast-addelchichon'
	'dcppc-forecast-addpinatubo'
	'dcppc-hindcast-noagung'
	'dcppc-hindcast-noelchichon'
	'dcppc-hindcast-nopinatubo'
	'dcppc-ipv-neg'
	'dcppc-ipv-nextrop-neg'
	'dcppc-ipv-nextrop-pos'
	'dcppc-ipv-pos'
	'dcppc-pac-control'
	'dcppc-pac-pacemaker'
	'deforest-globe'
	'esm-1pct-brch-1000pgc'
	'esm-1pct-brch-2000pgc'
	'esm-1pct-brch-750pgc'
	'esm-1pctco2'
	'esm-bell-1000pgc'
	'esm-bell-2000pgc'
	'esm-bell-750pgc'
	'esm-hist'
	'esm-hist-ext'
	'esm-past1000'
	'esm-pi-cdr-pulse'
	'esm-pi-co2pulse'
	'esm-picontrol'
	'esm-picontrol-spinup'
	'esm-ssp534-over'
	'esm-ssp585'
	'esm-ssp585-ocn-alk'
	'esm-ssp585-ocn-alk-stop'
	'esm-ssp585-ssp126lu'
	'esm-ssp585-ssp126lu-ext'
	'esm-ssp585ext'
	'esm-yr2010co2-cdr-pulse'
	'esm-yr2010co2-co2pulse'
	'esm-yr2010co2-control'
	'esm-yr2010co2-noemit'
	'faf-all'
	'faf-antwater-stress'
	'faf-heat'
	'faf-heat-na0pct'
	'faf-heat-na50pct'
	'faf-passiveheat'
	'faf-stress'
	'faf-water'
	'futsst-pdsic'
	'futuresst-4xco2-solar'
	'g1'
	'g6solar'
	'g6sst1'
	'g6sst2-solar'
	'g6sst2-sulfur'
	'g6sulfur'
	'g7cirrus'
	'g7sst1-cirrus'
	'g7sst2-cirrus'
	'highres-future'
	'highressst-4xco2'
	'highressst-future'
	'highressst-lai'
	'highressst-p4k'
	'highressst-present'
	'highressst-smoothed'
	'hist-1950'
	'hist-1950hc'
	'hist-aer'
	'hist-aer-cmip5'
	'hist-all-aer2'
	'hist-all-nat2'
	'hist-bgc'
	'hist-co2'
	'hist-ghg'
	'hist-ghg-cmip5'
	'hist-nat'
	'hist-nat-cmip5'
	'hist-nolu'
	'hist-piaer'
	'hist-pintcf'
	'hist-resamo'
	'hist-resipo'
	'hist-sol'
	'hist-spaer-aer'
	'hist-spaer-all'
	'hist-strato3'
	'hist-totalo3'
	'hist-volc'
	'historical'
	'historical-cmip5'
	'historical-ext'
	'historical-withism'
	'histsst'
	'histsst-1950hc'
	'histsst-nolu'
	'histsst-piaer'
	'histsst-pich4'
	'histsst-pin2o'
	'histsst-pintcf'
	'histsst-pio3'
	'ism-1pctco2to4x-self'
	'ism-1pctco2to4x-std'
	'ism-amip-std'
	'ism-asmb-std'
	'ism-bsmb-std'
	'ism-ctrl-std'
	'ism-historical-self'
	'ism-historical-std'
	'ism-lig127k-std'
	'ism-pdcontrol-std'
	'ism-picontrol-self'
	'ism-ssp585-self'
	'ism-ssp585-std'
	'land-cclim'
	'land-cco2'
	'land-crop-grass'
	'land-crop-nofert'
	'land-crop-noirrig'
	'land-crop-noirrigfert'
	'land-hist'
	'land-hist-altlu1'
	'land-hist-altlu2'
	'land-hist-altstartyear'
	'land-hist-cruncep'
	'land-hist-princeton'
	'land-hist-wfdei'
	'land-nofire'
	'land-nolu'
	'land-nopasture'
	'land-noshiftcultivate'
	'land-nowoodharv'
	'land-ssp126'
	'land-ssp434'
	'land-ssp585'
	'lfmip-initlc'
	'lfmip-pdlc'
	'lfmip-pdlc-cruncep'
	'lfmip-pdlc-princeton'
	'lfmip-pdlc-wfdei'
	'lfmip-rmlc'
	'lfmip-rmlc-cruncep'
	'lfmip-rmlc-princeton'
	'lfmip-rmlc-wfdei'
	'lgm'
	'lig127k'
	'midholocene'
	'midpliocene-eoi400'
	'modelsst-futarcsic'
	'modelsst-pdsic'
	'omip1'
	'omip1-spunup'
	'omip2'
	'omip2-spunup'
	'pa-futantsic'
	'pa-futantsic-ext'
	'pa-futarcsic'
	'pa-futarcsic-ext'
	'pa-pdsic'
	'pa-pdsic-ext'
	'pa-piantsic'
	'pa-piarcsic'
	'past1000'
	'past1000-solaronly'
	'past1000-volconly'
	'past2k'
	'pdsst-futantsic'
	'pdsst-futarcsic'
	'pdsst-futarcsicsit'
	'pdsst-futbkseassic'
	'pdsst-futokhotsksic'
	'pdsst-pdsic'
	'pdsst-pdsicsit'
	'pdsst-piantsic'
	'pdsst-piarcsic'
	'piclim-2xdms'
	'piclim-2xdust'
	'piclim-2xfire'
	'piclim-2xnox'
	'piclim-2xss'
	'piclim-2xvoc'
	'piclim-4xco2'
	'piclim-aer'
	'piclim-anthro'
	'piclim-bc'
	'piclim-ch4'
	'piclim-control'
	'piclim-ghg'
	'piclim-hc'
	'piclim-histaer'
	'piclim-histall'
	'piclim-histghg'
	'piclim-histnat'
	'piclim-lu'
	'piclim-n2o'
	'piclim-nh3'
	'piclim-nox'
	'piclim-ntcf'
	'piclim-o3'
	'piclim-oc'
	'piclim-so2'
	'piclim-spaer-aer'
	'piclim-spaer-anthro'
	'piclim-spaer-histaer'
	'piclim-spaer-histall'
	'piclim-voc'
	'picontrol'
	'picontrol-cmip5'
	'picontrol-spinup'
	'picontrol-spinup-cmip5'
	'picontrol-withism'
	'pisst'
	'pisst-4xco2'
	'pisst-4xco2-rad'
	'pisst-4xco2-solar'
	'pisst-pdsic'
	'pisst-pisic'
	'pisst-pxk'
	'rad-irf'
	'rcp26-cmip5'
	'rcp45-cmip5'
	'rcp60-cmip5'
	'rcp85-cmip5'
	'spinup-1950'
	'ssp119'
	'ssp126'
	'ssp126-ssp370lu'
	'ssp245'
	'ssp245-aer'
	'ssp245-cov-aer'
	'ssp245-cov-fossil'
	'ssp245-cov-ghg'
	'ssp245-cov-modgreen'
	'ssp245-cov-strgreen'
	'ssp245-covid'
	'ssp245-ghg'
	'ssp245-nat'
	'ssp245-strato3'
	'ssp370'
	'ssp370-lowntcf'
	'ssp370-lowntcfch4'
	'ssp370-ssp126lu'
	'ssp370pdsst'
	'ssp370sst'
	'ssp370sst-lowaer'
	'ssp370sst-lowbc'
	'ssp370sst-lowch4'
	'ssp370sst-lowntcf'
	'ssp370sst-lowntcfch4'
	'ssp370sst-lowo3'
	'ssp370sst-ssp126lu'
	'ssp434'
	'ssp460'
	'ssp534-over'
	'ssp534-over-bgc'
	'ssp585'
	'ssp585-bgc'
	'ssp585-withism'
	'volc-cluster-21c'
	'volc-cluster-ctrl'
	'volc-cluster-mill'
	'volc-long-eq'
	'volc-long-hln'
	'volc-long-hls'
	'volc-pinatubo-full'
	'volc-pinatubo-slab'
	'volc-pinatubo-strat'
	'volc-pinatubo-surf'
	'yr2010co2'
)

# Experiment ID - raw name
declare -a CMIP6_EXPERIMENT_ID_RAW=(
	'1pctCO2'
	'1pctCO2-4xext'
	'1pctCO2-bgc'
	'1pctCO2-cdr'
	'1pctCO2-rad'
	'1pctCO2Ndep'
	'1pctCO2Ndep-bgc'
	'1pctCO2to4x-withism'
	'a4SST'
	'a4SSTice'
	'a4SSTice-4xCO2'
	'abrupt-0p5xCO2'
	'abrupt-2xCO2'
	'abrupt-4xCO2'
	'abrupt-solm4p'
	'abrupt-solp4p'
	'amip'
	'amip-4xCO2'
	'amip-a4SST-4xCO2'
	'amip-climSIC'
	'amip-climSST'
	'amip-future4K'
	'amip-hist'
	'amip-hld'
	'amip-lfmip-pdLC'
	'amip-lfmip-pObs'
	'amip-lfmip-rmLC'
	'amip-lwoff'
	'amip-m4K'
	'amip-p4K'
	'amip-p4K-lwoff'
	'amip-piForcing'
	'amip-TIP'
	'amip-TIP-nosh'
	'aqua-4xCO2'
	'aqua-control'
	'aqua-control-lwoff'
	'aqua-p4K'
	'aqua-p4K-lwoff'
	'control-1950'
	'control-slab'
	'dcppA-assim'
	'dcppA-hindcast'
	'dcppA-hindcast-niff'
	'dcppA-historical-niff'
	'dcppB-forecast'
	'dcppC-amv-ExTrop-neg'
	'dcppC-amv-ExTrop-pos'
	'dcppC-amv-neg'
	'dcppC-amv-pos'
	'dcppC-amv-Trop-neg'
	'dcppC-amv-Trop-pos'
	'dcppC-atl-control'
	'dcppC-atl-pacemaker'
	'dcppC-atl-spg'
	'dcppC-forecast-addAgung'
	'dcppC-forecast-addElChichon'
	'dcppC-forecast-addPinatubo'
	'dcppC-hindcast-noAgung'
	'dcppC-hindcast-noElChichon'
	'dcppC-hindcast-noPinatubo'
	'dcppC-ipv-neg'
	'dcppC-ipv-NexTrop-neg'
	'dcppC-ipv-NexTrop-pos'
	'dcppC-ipv-pos'
	'dcppC-pac-control'
	'dcppC-pac-pacemaker'
	'deforest-globe'
	'esm-1pct-brch-1000PgC'
	'esm-1pct-brch-2000PgC'
	'esm-1pct-brch-750PgC'
	'esm-1pctCO2'
	'esm-bell-1000PgC'
	'esm-bell-2000PgC'
	'esm-bell-750PgC'
	'esm-hist'
	'esm-hist-ext'
	'esm-past1000'
	'esm-pi-cdr-pulse'
	'esm-pi-CO2pulse'
	'esm-piControl'
	'esm-piControl-spinup'
	'esm-ssp534-over'
	'esm-ssp585'
	'esm-ssp585-ocn-alk'
	'esm-ssp585-ocn-alk-stop'
	'esm-ssp585-ssp126Lu'
	'esm-ssp585-ssp126Lu-ext'
	'esm-ssp585ext'
	'esm-yr2010CO2-cdr-pulse'
	'esm-yr2010CO2-CO2pulse'
	'esm-yr2010CO2-control'
	'esm-yr2010CO2-noemit'
	'faf-all'
	'faf-antwater-stress'
	'faf-heat'
	'faf-heat-NA0pct'
	'faf-heat-NA50pct'
	'faf-passiveheat'
	'faf-stress'
	'faf-water'
	'futSST-pdSIC'
	'futureSST-4xCO2-solar'
	'G1'
	'G6solar'
	'G6SST1'
	'G6SST2-solar'
	'G6SST2-sulfur'
	'G6sulfur'
	'G7cirrus'
	'G7SST1-cirrus'
	'G7SST2-cirrus'
	'highres-future'
	'highresSST-4xCO2'
	'highresSST-future'
	'highresSST-LAI'
	'highresSST-p4K'
	'highresSST-present'
	'highresSST-smoothed'
	'hist-1950'
	'hist-1950HC'
	'hist-aer'
	'hist-aer-cmip5'
	'hist-all-aer2'
	'hist-all-nat2'
	'hist-bgc'
	'hist-CO2'
	'hist-GHG'
	'hist-GHG-cmip5'
	'hist-nat'
	'hist-nat-cmip5'
	'hist-noLu'
	'hist-piAer'
	'hist-piNTCF'
	'hist-resAMO'
	'hist-resIPO'
	'hist-sol'
	'hist-spAer-aer'
	'hist-spAer-all'
	'hist-stratO3'
	'hist-totalO3'
	'hist-volc'
	'historical'
	'historical-cmip5'
	'historical-ext'
	'historical-withism'
	'histSST'
	'histSST-1950HC'
	'histSST-noLu'
	'histSST-piAer'
	'histSST-piCH4'
	'histSST-piN2O'
	'histSST-piNTCF'
	'histSST-piO3'
	'ism-1pctCO2to4x-self'
	'ism-1pctCO2to4x-std'
	'ism-amip-std'
	'ism-asmb-std'
	'ism-bsmb-std'
	'ism-ctrl-std'
	'ism-historical-self'
	'ism-historical-std'
	'ism-lig127k-std'
	'ism-pdControl-std'
	'ism-piControl-self'
	'ism-ssp585-self'
	'ism-ssp585-std'
	'land-cClim'
	'land-cCO2'
	'land-crop-grass'
	'land-crop-noFert'
	'land-crop-noIrrig'
	'land-crop-noIrrigFert'
	'land-hist'
	'land-hist-altLu1'
	'land-hist-altLu2'
	'land-hist-altStartYear'
	'land-hist-cruNcep'
	'land-hist-princeton'
	'land-hist-wfdei'
	'land-noFire'
	'land-noLu'
	'land-noPasture'
	'land-noShiftCultivate'
	'land-noWoodHarv'
	'land-ssp126'
	'land-ssp434'
	'land-ssp585'
	'lfmip-initLC'
	'lfmip-pdLC'
	'lfmip-pdLC-cruNcep'
	'lfmip-pdLC-princeton'
	'lfmip-pdLC-wfdei'
	'lfmip-rmLC'
	'lfmip-rmLC-cruNcep'
	'lfmip-rmLC-princeton'
	'lfmip-rmLC-wfdei'
	'lgm'
	'lig127k'
	'midHolocene'
	'midPliocene-eoi400'
	'modelSST-futArcSIC'
	'modelSST-pdSIC'
	'omip1'
	'omip1-spunup'
	'omip2'
	'omip2-spunup'
	'pa-futAntSIC'
	'pa-futAntSIC-ext'
	'pa-futArcSIC'
	'pa-futArcSIC-ext'
	'pa-pdSIC'
	'pa-pdSIC-ext'
	'pa-piAntSIC'
	'pa-piArcSIC'
	'past1000'
	'past1000-solaronly'
	'past1000-volconly'
	'past2k'
	'pdSST-futAntSIC'
	'pdSST-futArcSIC'
	'pdSST-futArcSICSIT'
	'pdSST-futBKSeasSIC'
	'pdSST-futOkhotskSIC'
	'pdSST-pdSIC'
	'pdSST-pdSICSIT'
	'pdSST-piAntSIC'
	'pdSST-piArcSIC'
	'piClim-2xDMS'
	'piClim-2xdust'
	'piClim-2xfire'
	'piClim-2xNOx'
	'piClim-2xss'
	'piClim-2xVOC'
	'piClim-4xCO2'
	'piClim-aer'
	'piClim-anthro'
	'piClim-BC'
	'piClim-CH4'
	'piClim-control'
	'piClim-ghg'
	'piClim-HC'
	'piClim-histaer'
	'piClim-histall'
	'piClim-histghg'
	'piClim-histnat'
	'piClim-lu'
	'piClim-N2O'
	'piClim-NH3'
	'piClim-NOx'
	'piClim-NTCF'
	'piClim-O3'
	'piClim-OC'
	'piClim-SO2'
	'piClim-spAer-aer'
	'piClim-spAer-anthro'
	'piClim-spAer-histaer'
	'piClim-spAer-histall'
	'piClim-VOC'
	'piControl'
	'piControl-cmip5'
	'piControl-spinup'
	'piControl-spinup-cmip5'
	'piControl-withism'
	'piSST'
	'piSST-4xCO2'
	'piSST-4xCO2-rad'
	'piSST-4xCO2-solar'
	'piSST-pdSIC'
	'piSST-piSIC'
	'piSST-pxK'
	'rad-irf'
	'rcp26-cmip5'
	'rcp45-cmip5'
	'rcp60-cmip5'
	'rcp85-cmip5'
	'spinup-1950'
	'ssp119'
	'ssp126'
	'ssp126-ssp370Lu'
	'ssp245'
	'ssp245-aer'
	'ssp245-cov-aer'
	'ssp245-cov-fossil'
	'ssp245-cov-GHG'
	'ssp245-cov-modgreen'
	'ssp245-cov-strgreen'
	'ssp245-covid'
	'ssp245-GHG'
	'ssp245-nat'
	'ssp245-stratO3'
	'ssp370'
	'ssp370-lowNTCF'
	'ssp370-lowNTCFCH4'
	'ssp370-ssp126Lu'
	'ssp370pdSST'
	'ssp370SST'
	'ssp370SST-lowAer'
	'ssp370SST-lowBC'
	'ssp370SST-lowCH4'
	'ssp370SST-lowNTCF'
	'ssp370SST-lowNTCFCH4'
	'ssp370SST-lowO3'
	'ssp370SST-ssp126Lu'
	'ssp434'
	'ssp460'
	'ssp534-over'
	'ssp534-over-bgc'
	'ssp585'
	'ssp585-bgc'
	'ssp585-withism'
	'volc-cluster-21C'
	'volc-cluster-ctrl'
	'volc-cluster-mill'
	'volc-long-eq'
	'volc-long-hlN'
	'volc-long-hlS'
	'volc-pinatubo-full'
	'volc-pinatubo-slab'
	'volc-pinatubo-strat'
	'volc-pinatubo-surf'
	'yr2010CO2'
)

# ###############################################################
# SECTION: ES-DOC SPECIALZATIONS
# ###############################################################

# Array of specifications.
declare -a CMIP6_SPECIALIZATIONS=(
	'aerosol'
	'atmos'
	'atmoschem'
	'land'
	'landice'
	'ocean'
	'ocnbgchem'
	'seaice'
	'toplevel'
)

# Array of realm specifications.
declare -a CMIP6_REALM_SPECIALIZATIONS=(
	'aerosol'
	'atmos'
	'atmoschem'
	'land'
	'landice'
	'ocean'
	'ocnbgchem'
	'seaice'
)
