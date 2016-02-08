
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
    lg.info("We are loading the eddy npz files.")
    # eddy_ctrl=np.load('/home/chris/mount_win/tracking/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_ERAI01/eddy_track_cb_NEMO.npz')
    # eddy_flat=np.load('/home/chris/mount_win/tracking/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_FLATFCNG_ERAI01/eddy_track_cb_NEMO.npz')

    #home machine
    #eddy_ctrl=np.load('/home/chris/mount_win/eddy_track/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_ERAI01/eddy_track_cb_NEMO.npz')
    #eddy_flat=np.load('/home/chris/mount_win/eddy_track/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_FLATFCNG_ERAI01/eddy_track_cb_NEMO.npz')

    #storm
    eddy_ctrl=np.load('/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_ERAI01/eddy_track_cb_NEMO.npz')
    eddy_flat=np.load('/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/eddy_tracking_katana/nemo_cordex24_FLATFCNG_ERAI01/eddy_track_cb_NEMO.npz')

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

def make_eddy_stats(eddy_list,output_path):
    """function to create pandas HDFStore of eddy stats
    
    :eddy_list: list of eddies to do some stats on
    :output_path: output path for HDFStore (don't put in .h5)
    :returns: @todo
    """
    lg.info("We are calculating eddy stats: ")
    stats={}
    stats['count']=len(eddy_list)
    property=['age','amp','area','scale']

    #init lists
    for prop in property:
        stats[prop]=[]

    #work out mean for each eddy
    for ed in np.arange(len(eddy_list)):
        for prop in property:
            stats[prop].append(np.mean(eddy_list[ed][prop]))


    #take mean across all eddies!
    for prop in property:
        stats[prop]=np.mean(stats[prop])

    df=pd.Series(stats)
    efile = output_path+'_table'+ '.h5'

    #a clobber check here
    try:
        os.remove(efile)
        lg.info("File: " +os.path.basename(efile) + " already exists, clobbering!")
    except OSError:
        pass 

    store = pd.HDFStore(efile,complevel=9, complib='blosc')
    store.append('df',df) #querable columns or dc take more space and are slower
    store.close()
    return

def plot_variable(ed1,ed2,eddy_variable_name,lb1,lb2,output_path_name,seaborn=False):
    """function to plot eddy variable in a historgram
    
    :ed1: @todo
    :ed2: @todo
    :eddy_variable_name: @todo
    :seaborn (optional): if True will use seaborn KDE otherwise just matplotlib histograms
    :returns: @todo
    """
    lg.info("We are plotting :" + eddy_variable_name)
    ed1_cnt=np.arange(len(ed1))
    ed2_cnt=np.arange(len(ed2))
    pone=pd.Series([np.mean(ed1[ed][eddy_variable_name]) for ed in ed1_cnt])
    ptwo=pd.Series([np.mean(ed2[ed][eddy_variable_name]) for ed in ed2_cnt])

    if not seaborn:
        plt.close('all')
        fig=plt.figure()
        ax=fig.add_subplot(1, 1,1)

        a_heights, a_bins = np.histogram(pone,bins=15)
        b_heights, b_bins = np.histogram(ptwo, bins=a_bins)

        width = (a_bins[1] - a_bins[0])/3
        rects1=ax.bar(a_bins[:-1], a_heights, width=width, facecolor='cornflowerblue',label=lb1)
        rects2=ax.bar(b_bins[:-1]+width, b_heights, width=width, facecolor='seagreen',label=lb2)
        ax.set_title(eddy_variable_name)
        ax.legend((rects1[0], rects2[0]), (lb1, lb2))
        #plt.show()

        #ax.set_title('msg')
        #ax.set_xlabel('msg')
        ax.set_ylabel('count')
        #plt.show()
        plt.savefig(output_path_name,dpi=300)
    else:
        plt.close('all')

        ax = sns.distplot(pone, rug=True, rug_kws={"color": "g","alpha":.7},
                   kde_kws={"color": "g", "lw": 3, "label": lb1},
                   hist_kws={"histtype": "step", "linewidth": 3,
                                 "alpha": .7, "color": "g"})

        ax = sns.distplot(ptwo, rug=True, rug_kws={"color": "b","alpha":.7},
                   kde_kws={"color": "b", "lw": 3, "label": lb2},
                   hist_kws={"histtype": "step", "linewidth": 3,
                                 "alpha": .7, "color": "b"})

        ax.set_title(eddy_variable_name)
        plt.savefig(output_path_name,dpi=300)
        # plt.show()
    return

def plot_allvariables(ed1,ed2,eddyvariables,lb1,lb2,output_path_name):
    """function to plot all eddy variables on one plot with matplotlib histograms
    
    :ed1: @todo
    :ed2: @todo
    :eddy_variable_name: @todo
    :returns: @todo
    """
    plt.close('all')
    #fig=plt.figure()
    #width then height
    fig=plt.figure(figsize=(15.0,15.0))

    for edidx,eddy_variable_name in enumerate(eddyvariables):
        lg.info("We are plotting :" + eddy_variable_name)
        ax=fig.add_subplot(2, 2,edidx+1)
        ed1_cnt=np.arange(len(ed1))
        ed2_cnt=np.arange(len(ed2))
        pone=pd.Series([np.mean(ed1[ed][eddy_variable_name]) for ed in ed1_cnt])
        ptwo=pd.Series([np.mean(ed2[ed][eddy_variable_name]) for ed in ed2_cnt])

        a_heights, a_bins = np.histogram(pone,bins=15)
        b_heights, b_bins = np.histogram(ptwo, bins=a_bins)

        width = (a_bins[1] - a_bins[0])/3

        rects1=ax.bar(a_bins[:-1], a_heights, width=width, facecolor='cornflowerblue',label=lb1)
        rects2=ax.bar(b_bins[:-1]+width, b_heights, width=width, facecolor='seagreen',label=lb2)

        ax.set_title(eddy_variable_name)

        ax.legend((rects1[0], rects2[0]), (lb1, lb2))
        #plt.show()

        #ax.set_title('msg')
        #ax.set_xlabel('msg')
        ax.set_ylabel('count')
    #plt.show()
    plt.savefig(output_path_name,dpi=300)
    return


if __name__ == "__main__": 
    LogStart('',fout=False)


    #plot_output_folder='/home/chris/mount_win/plots/'
    plot_output_folder='/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/plots/'
    plot_output_folder='/srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/plots/eddies/'
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

    make_eddy_stats(ctrl_filt,plot_output_folder+'ctrl_anticyclonic_eddy_tracks_stats')
    make_eddy_stats(flat_filt,plot_output_folder+'flat_anticyclonic_eddy_tracks_stats')

    #lg.info("Plotting anticyclonic")
    #plot_variable(ctrl_filt,flat_filt,'amp','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_amp.png')
    #plot_variable(ctrl_filt,flat_filt,'age','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_age.png')
    #plot_variable(ctrl_filt,flat_filt,'scale','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_scale.png')
    #plot_variable(ctrl_filt,flat_filt,'area','ctrl','const',plot_output_folder+'anti_ctrl_v_flat_area.png')

    #variables=['amp','age','scale','area']
    #plot_allvariables(ctrl_filt,flat_filt,variables,'ctrl','const',plot_output_folder+'anti_ctrl_v_flat_allvar.png')

    ##############
    #  cyclonic  #
    ##############
    
    ctrl_filt=filter_eddy_tracks_age(eddy_ctrl,30)
    flat_filt=filter_eddy_tracks_age(eddy_flat,30)

    ctrl_filt=filter_eddy_tracks_space(ctrl_filt,150,160,-40,-30)
    flat_filt=filter_eddy_tracks_space(flat_filt,150,160,-40,-30)

    ctrl_filt=filter_eddy_tracks_type(ctrl_filt,'cyclonic')
    flat_filt=filter_eddy_tracks_type(flat_filt,'cyclonic')

    make_eddy_stats(ctrl_filt,plot_output_folder+'ctrl_cyclonic_eddy_tracks_stats')
    make_eddy_stats(flat_filt,plot_output_folder+'flat_cyclonic_eddy_tracks_stats')

    #lg.info("Plotting cyclonic")
    #plot_variable(ctrl_filt,flat_filt,'amp','ctrl','const',plot_output_folder+'ctrl_v_flat_amp.png')
    #plot_variable(ctrl_filt,flat_filt,'age','ctrl','const',plot_output_folder+'ctrl_v_flat_age.png')
    #plot_variable(ctrl_filt,flat_filt,'scale','ctrl','const',plot_output_folder+'ctrl_v_flat_scale.png')
    #plot_variable(ctrl_filt,flat_filt,'area','ctrl','const',plot_output_folder+'ctrl_v_flat_area.png')

    #variables=['amp','age','scale','area']
    #plot_allvariables(ctrl_filt,flat_filt,variables,'ctrl','const',plot_output_folder+'ctrl_v_flat_allvar.png')

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
