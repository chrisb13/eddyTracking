
#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@student.unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Mon, 14 Dec 2015 13:40:24
#   Machine created on: chris-VirtualBox2
#

"""
quick and dirty scripts for looking at tasman sea eddy tracks
"""
from cb2logger import *
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

def load_eddy_tracks():
    """function to load the eddy tracks from Eric Oliver's Eddy Tracking algorithm
    :returns: @todo
    """
    # eddy_ctrl=np.load('/home/chris/mount_win/tracking/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_ERAI01/eddy_track_cb_NEMO.npz')
    # eddy_flat=np.load('/home/chris/mount_win/tracking/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_FLATFCNG_ERAI01/eddy_track_cb_NEMO.npz')

    #home machine
    eddy_ctrl=np.load('/home/chris/mount_win/eddy_track/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_ERAI01/eddy_track_cb_NEMO.npz')
    eddy_flat=np.load('/home/chris/mount_win/eddy_track/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_FLATFCNG_ERAI01/eddy_track_cb_NEMO.npz')
    return eddy_ctrl['eddies'],eddy_flat['eddies']

def filter_eddy_tracks_age(dict_of_eddies_from_npz,eddy_age):
    """function to filter eddy_tracks of some age
    :dict_of_eddies_from_npz:
    :eddy_age:
    :returns: @todo
    """
    eddy_count=len(dict_of_eddies_from_npz)
    filtered_eddy_dict=[]
    for ed in np.arange(eddy_count):
        if dict_of_eddies_from_npz[ed]['age']>eddy_age:
            filtered_eddy_dict.append(dict_of_eddies_from_npz[ed])

    return filtered_eddy_dict


def filter_eddy_tracks_space(dict_of_eddies_from_npz,minlong,maxlong,minlat,maxlat):
    """function to filter eddy_tracks of some age
    :dict_of_eddies_from_npz:
    :minlong:
    :maxlong:
    :minlat:
    :maxlat:
    :returns: @todo
    """
    eddy_count=len(dict_of_eddies_from_npz)
    filtered_eddy_dict=[]
    for ed in np.arange(eddy_count):
        #careful, good for southernhemisphere
        inlatrange=\
        (dict_of_eddies_from_npz[ed]['lat'] > minlat).all()\
                and (dict_of_eddies_from_npz[ed]['lat'] < maxlat).all()

        inlongrange=\
        (dict_of_eddies_from_npz[ed]['lon'] > minlong).all()\
                and (dict_of_eddies_from_npz[ed]['lon'] < maxlong).all()

        if inlatrange and inlongrange:
            filtered_eddy_dict.append(dict_of_eddies_from_npz[ed])

    return filtered_eddy_dict

def filter_eddy_tracks_type(dict_of_eddies_from_npz,eddy_type):
    """function to filter eddy_tracks of some age
    :dict_of_eddies_from_npz:
    :eddy_type:
    :returns: @todo
    """
    eddy_count=len(dict_of_eddies_from_npz)
    filtered_eddy_dict=[]
    for ed in np.arange(eddy_count):
        if dict_of_eddies_from_npz[ed]['type']==eddy_type:
            filtered_eddy_dict.append(dict_of_eddies_from_npz[ed])

    return filtered_eddy_dict

def plot_variable(ed1,ed2,eddy_variable_name,lb1,lb2,output_path_name):
    """function to plot eddy variable in a historgram
    
    :ed1: @todo
    :ed2: @todo
    :eddy_variable_name: @todo
    :returns: @todo
    """
    ed1_cnt=np.arange(len(ed1))
    ed2_cnt=np.arange(len(ed2))
    pone=pd.Series([np.mean(ed1[ed][eddy_variable_name]) for ed in ed1_cnt])
    ptwo=pd.Series([np.mean(ed2[ed][eddy_variable_name]) for ed in ed2_cnt])
    plt.close('all')

    ax = sns.distplot(pone, rug=True, rug_kws={"color": "g","alpha":.7},
               kde_kws={"color": "g", "lw": 3, "label": lb1},
               hist_kws={"histtype": "step", "linewidth": 3,
                             "alpha": .7, "color": "g"})

    ax = sns.distplot(ptwo, rug=True, rug_kws={"color": "b","alpha":.7},
               kde_kws={"color": "b", "lw": 3, "label": lb2},
               hist_kws={"histtype": "step", "linewidth": 3,
                             "alpha": .7, "color": "b"})

    plt.savefig(output_path_name,dpi=300)
    # plt.show()
    return

if __name__ == "__main__": 
    LogStart('',fout=False)


    plot_output_folder='/home/chris/mount_win/plots/'
    mkdir(plot_output_folder)

    eddy_ctrl,eddy_flat=load_eddy_tracks()

    ####################
    #  anticylyclonic  #
    ####################
    
    ctrl_filt=filter_eddy_tracks_age(eddy_ctrl,30)
    flat_filt=filter_eddy_tracks_age(eddy_flat,30)

    ctrl_filt=filter_eddy_tracks_space(ctrl_filt,150,160,-40,-30)
    flat_filt=filter_eddy_tracks_space(flat_filt,150,160,-40,-30)

    ctrl_filt=filter_eddy_tracks_type(ctrl_filt,'anticyclonic')
    flat_filt=filter_eddy_tracks_type(flat_filt,'anticyclonic')

    plot_variable(ctrl_filt,flat_filt,'amp','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_amp.png')
    plot_variable(ctrl_filt,flat_filt,'age','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_age.png')
    plot_variable(ctrl_filt,flat_filt,'scale','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_scale.png')
    plot_variable(ctrl_filt,flat_filt,'area','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_area.png')

    ##############
    #  cyclonic  #
    ##############
    
    ctrl_filt=filter_eddy_tracks_age(eddy_ctrl,30)
    flat_filt=filter_eddy_tracks_age(eddy_flat,30)

    ctrl_filt=filter_eddy_tracks_space(ctrl_filt,150,160,-40,-30)
    flat_filt=filter_eddy_tracks_space(flat_filt,150,160,-40,-30)

    ctrl_filt=filter_eddy_tracks_type(ctrl_filt,'cyclonic')
    flat_filt=filter_eddy_tracks_type(flat_filt,'cyclonic')

    plot_variable(ctrl_filt,flat_filt,'amp','ctrl','const',plot_output_folder+'ctrl_v_flat_amp.png')
    plot_variable(ctrl_filt,flat_filt,'age','ctrl','const',plot_output_folder+'ctrl_v_flat_age.png')
    plot_variable(ctrl_filt,flat_filt,'scale','ctrl','const',plot_output_folder+'ctrl_v_flat_scale.png')
    plot_variable(ctrl_filt,flat_filt,'area','ctrl','const',plot_output_folder+'ctrl_v_flat_area.png')


    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
