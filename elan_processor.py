# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:02:02 2022

@author: SNT
"""

from utils import (detect_elan_files, parse_elan_files, align_annotations,
                   merge_modalities, extracting_visual_features_v1,
                   extracting_visual_features_v2, extracting_visual_features_v3)
import argparse, os

#%% ARGUMENT PARSING
def parse_args():
    parser=argparse.ArgumentParser(description='SignON ELAN file processor.'
                                   'Transform ELAN files in handy data to research on SLT and SLR.')
    parser.add_argument('-i', type=str, help='Specify the folder containing ELAN and video files', required=True)
    parser.add_argument('-o', type=str, help='Specify the folder to store the ouput data',required=True)
    parser.add_argument('--video_mode', type=str, nargs='?', default = None,
                        choices=['1', '2', '3', '4'], 
                        help='Video processing mode:\n'
                        '\t (1) This mode is slow and unstable. It tries to match videonnames and participant ids in ELAN files\n'
                        '\t (2) This mode is fast and safer. However, the participant ids in elan files must match video names\n'
                        '\t (3) This mode is fast and safer. However, the videonames must match the session and participant names.'
                        '\t (4) I do not want to process videos.')
    
    # PODEMOS AÑADIR variable skip parsing y skip alignment
    parser.add_argument('--leading_modality', type=str, nargs='?', default = None,
                        help='The leading modality to use when aligning different annotations.\n'
                        'If you do not specify any, you can choose one between the detected during the processing'
                        )    
    args=parser.parse_args()
    return args


#%% MAIN FUNCTION
def main(output_folder = None, input_folder = None, leading_modality = None, video_processing_mode = None):
    
    args= parse_args() if output_folder is None else None
    
    output_folder = args.o if args is not None else output_folder
    input_folder = args.i if args is not None else input_folder
    leading_modality = args.leading_modality if args is not None else leading_modality
    video_processing_mode = args.leading_modality if args is not None else video_processing_mode
    video_processing_mode = int(video_processing_mode)
    
    # CHECK IF INPUT AND OUPUT FOLDERS ARE VALID
    if not os.path.exists(input_folder):
        print('The provided input folder ({}) does not exist'.format(input_folder))
        return -1

    if os.path.exists(output_folder):
        print('The provided output folder ({}) already exists. Remove or provide another output folder name'.format(output_folder))
        return -1
    
    print('[*] Starting to parse ELAN files')
    elan_file_list = detect_elan_files(input_folder)      # DETECTING ELAN FILES
    detected_modalities = parse_elan_files(input_folder,  # PARSING ELAN FILES
                                            elan_file_list, 
                                            output_folder)        
    print()
    print('[*] Starting annotation aligment')
    # IF NO MODALITY IS SPECIFIED OR THE SPECIFIED IS NOT VALID,
    # WE ASK THE USER TO SELECT ONE FROM THE DETECTED
    if leading_modality is None or leading_modality not in detected_modalities:
        sel_mod = None
        choices = list(map(str, range(1, len(detected_modalities)+1)))
        while sel_mod not in choices:
            print('[-] No leading modelity was not specified to align the annotations or the specified is not valid.\nPlease select a valid one:')
            for i,m in enumerate(detected_modalities):
                print('\t ({}) {}'.format(i+1, detected_modalities[i]))
            sel_mod = input()
        leading_modality = detected_modalities[int(sel_mod)-1]    
    print('[-] The aligment is going to peformed using {} as leading modality'.format(leading_modality))
    
    
    align_annotations(output_folder, leading_modality) # ALINGING ANNOTATIONS USING TIMESTAMPS
    merge_modalities(output_folder,  # MERGING MODALITIES IN PARALLEL TEXT FILES
                      detected_modalities,
                      elan_file_list)  
    print('[-] Parallel text files were generated in {}'.format(output_folder))
    print()
    # IF NO VIDEO PROCESSING MODE IS SPECIFIED, WE ASK THE USER TO SELECT ONE FROM THE DETECTED
    if video_processing_mode is None:
        sel_mod = None
        choices = ['1','2','3', '4']
        while sel_mod not in choices:
            print('This framework allows two modes to process videos.\n'
                  'Select the one that most suits your case:\n'
                  '\t (1) This mode is slow and unstable. It tries to match videonnames and participant ids in ELAN files\n'
                  '\t (2) This mode is fast and safer. However, the participant ids in elan files must match video names\n'
                  '\t (3) This mode is fast and safer. However, the videonames must match the session and participant names.'
                  '\t (4) I do not want to process videos.'
                  )
            sel_mod = input()
        video_processing_mode = int(sel_mod)
        
    
    if video_processing_mode == 1: # MATCHING USING ELAN MEDIA INFORMATION, PARTICIPANTS AND SESSION NAMES
        print('[*] Starting video processing') 
        extracting_visual_features_v1(input_folder, output_folder)
        print('[-] Video processing finished')
    elif video_processing_mode == 2: # MATCHING USING ELAN MEDIA INFORMATION, PARTICIPANTS AND SESSION NAMES 
        print('[*] Starting video processing')
        extracting_visual_features_v2(input_folder, output_folder)
        print('[-] Video processing finished')
    elif video_processing_mode == 3: # MATCHING USING ELAN MEDIA INFORMATION, PARTICIPANTS AND SESSION NAMES 
        print('[*] Starting video processing')
        extracting_visual_features_v3(input_folder, output_folder)
        print('[-] Video processing finished')        
        
    print()
    print('[*] Processing completed')


if __name__ == '__main__':
    main(output_folder = 'DGS_ALL', input_folder = 'DGS', leading_modality = None, video_processing_mode = 3)
