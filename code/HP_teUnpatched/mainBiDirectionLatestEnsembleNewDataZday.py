# This is a Python framework to compliment "Peek-a-Boo, I Still See You: Why Efficient Traffic Analysis Countermeasures Fail".
# Copyright (C) 2012  Kevin P. Dyer (kpdyer.com)
# See LICENSE for more details.
# Extended by Khaled M. Alnaami

import sys
import config
import time
import os
import random
import getopt
import string
import itertools
import shutil # to remove folders

# custom
from Datastore import Datastore
from Webpage import Webpage
from Utils import Utils

# countermeasures
from PadToMTU import PadToMTU
from PadRFCFixed import PadRFCFixed
from PadRFCRand import PadRFCRand
from PadRand import PadRand
from PadRoundExponential import PadRoundExponential
from PadRoundLinear import PadRoundLinear
from MiceElephants import MiceElephants
from DirectTargetSampling import DirectTargetSampling
from Folklore import Folklore
from WrightStyleMorphing import WrightStyleMorphing

# classifiers
from LiberatoreClassifier import LiberatoreClassifier
from WrightClassifier import WrightClassifier
from BandwidthClassifier import BandwidthClassifier
from HerrmannClassifier import HerrmannClassifier
from TimeClassifier import TimeClassifier
from PanchenkoClassifier import PanchenkoClassifier
from VNGPlusPlusClassifier import VNGPlusPlusClassifier
from VNGClassifier import VNGClassifier
from JaccardClassifier import JaccardClassifier
from ESORICSClassifier import ESORICSClassifier
from AdversialClassifier import AdversialClassifier
from AdversarialClassifierOnPanchenko import AdversarialClassifierOnPanchenko
from AdversarialClassifierBiDirectionFeaturesOnly import AdversarialClassifierBiDirectionFeaturesOnly
#from AdversialClassifierTor import AdversialClassifierTor
#from AdversialClassifierBloomFilter import AdversialClassifierBloomFilter
#from AdversarialClassifierOnPanchenkoBloomFilter import AdversarialClassifierOnPanchenkoBloomFilter
from ToWangFilesClosedWorld import ToWangFilesClosedWorld
from ToWangFilesOpenWorld import ToWangFilesOpenWorld
from HP_KNN_LCS import HP_KNN_LCS
from HpNGram import HpNGram

def intToCountermeasure(n):
    countermeasure = None
    if n == config.PAD_TO_MTU:
        countermeasure = PadToMTU
    elif n == config.RFC_COMPLIANT_FIXED_PAD:
        countermeasure = PadRFCFixed
    elif n == config.RFC_COMPLIANT_RANDOM_PAD:
        countermeasure = PadRFCRand
    elif n == config.RANDOM_PAD:
        countermeasure = PadRand
    elif n == config.PAD_ROUND_EXPONENTIAL:
        countermeasure = PadRoundExponential
    elif n == config.PAD_ROUND_LINEAR:
        countermeasure = PadRoundLinear
    elif n == config.MICE_ELEPHANTS:
        countermeasure = MiceElephants
    elif n == config.DIRECT_TARGET_SAMPLING:
        countermeasure = DirectTargetSampling
    elif n == config.WRIGHT_STYLE_MORPHING:
        countermeasure = WrightStyleMorphing
    elif n > 10:
        countermeasure = Folklore

        # FIXED_PACKET_LEN: 1000,1250,1500
        if n in [11,12,13,14]:
            Folklore.FIXED_PACKET_LEN    = 1000
        elif n in [15,16,17,18]:
            Folklore.FIXED_PACKET_LEN    = 1250
        elif n in [19,20,21,22]:
            Folklore.FIXED_PACKET_LEN    = 1500

        if n in [11,12,13,17,18,19]:
            Folklore.TIMER_CLOCK_SPEED   = 20
        elif n in [14,15,16,20,21,22]:
            Folklore.TIMER_CLOCK_SPEED   = 40

        if n in [11,14,17,20]:
            Folklore.MILLISECONDS_TO_RUN = 0
        elif n in [12,15,18,21]:
            Folklore.MILLISECONDS_TO_RUN = 5000
        elif n in [13,16,19,22]:
            Folklore.MILLISECONDS_TO_RUN = 10000

        if n==23:
            Folklore.MILLISECONDS_TO_RUN = 0
            Folklore.FIXED_PACKET_LEN    = 1250
            Folklore.TIMER_CLOCK_SPEED   = 40
        elif n==24:
            Folklore.MILLISECONDS_TO_RUN = 0
            Folklore.FIXED_PACKET_LEN    = 1500
            Folklore.TIMER_CLOCK_SPEED   = 20
        elif n==25:
            Folklore.MILLISECONDS_TO_RUN = 5000
            Folklore.FIXED_PACKET_LEN    = 1000
            Folklore.TIMER_CLOCK_SPEED   = 40
        elif n==26:
            Folklore.MILLISECONDS_TO_RUN = 5000
            Folklore.FIXED_PACKET_LEN    = 1500
            Folklore.TIMER_CLOCK_SPEED   = 20
        elif n==27:
            Folklore.MILLISECONDS_TO_RUN = 10000
            Folklore.FIXED_PACKET_LEN    = 1000
            Folklore.TIMER_CLOCK_SPEED   = 40
        elif n==28:
            Folklore.MILLISECONDS_TO_RUN = 10000
            Folklore.FIXED_PACKET_LEN    = 1250
            Folklore.TIMER_CLOCK_SPEED   = 20


    return countermeasure

def intToClassifier(n):
    classifier = None
    if n == config.LIBERATORE_CLASSIFIER:
        classifier = LiberatoreClassifier
    elif n == config.WRIGHT_CLASSIFIER:
        classifier = WrightClassifier
    elif n == config.BANDWIDTH_CLASSIFIER:
        classifier = BandwidthClassifier
    elif n == config.HERRMANN_CLASSIFIER:
        classifier = HerrmannClassifier
    elif n == config.TIME_CLASSIFIER:
        classifier = TimeClassifier
    elif n == config.PANCHENKO_CLASSIFIER:
        classifier = PanchenkoClassifier
    elif n == config.VNG_PLUS_PLUS_CLASSIFIER:
        classifier = VNGPlusPlusClassifier
    elif n == config.VNG_CLASSIFIER:
        classifier = VNGClassifier
    elif n == config.JACCARD_CLASSIFIER:
        classifier = JaccardClassifier
    elif n == config.ESORICS_CLASSIFIER:
        classifier = ESORICSClassifier
    elif n == config.ADVERSIAL_CLASSIFIER:
        classifier = AdversialClassifier
    elif n == config.ADVERSARIAL_CLASSIFIER_ON_PANCHENKO:
        classifier = AdversarialClassifierOnPanchenko
    elif n == config.ADVERSARIAL_CLASSIFIER_BiDirection_Only:
        classifier = AdversarialClassifierBiDirectionFeaturesOnly
    elif n == config.TO_WANG_FILES_CLOSED_WORLD:
        classifier = ToWangFilesClosedWorld
    elif n == config.TO_WANG_FILES_OPEN_WORLD:
        classifier = ToWangFilesOpenWorld
    elif n == config.HP_KNN_LCS:
        classifier = HP_KNN_LCS
    elif n == config.HP_NGRAM:
        classifier = HpNGram

    '''
    elif n == config.ADVERSIAL_CLASSIFIER_TOR:
        classifier = AdversialClassifierTor
    elif n == config.ADVERSIAL_CLASSIFIER_BLOOM_FILTER:
        classifier = AdversialClassifierBloomFilter
    elif n == config.ADVERSARIAL_CLASSIFIER_ON_PANCHENKO_BLOOM_FILTER:
        classifier = AdversarialClassifierOnPanchenkoBloomFilter
    '''

    return classifier

def usage():
    print """
    -N [int] : use [int] websites from the dataset
               from which we will use to sample a privacy
               set k in each experiment (default 775)

    -k [int] : the size of the privacy set (default 2)

    -d [int]: dataset to use
        0:  Liberatore and Levine Dataset (OpenSSH)
        1:  Herrmann et al. Dataset (OpenSSH)
        2:  Herrmann et al. Dataset (Tor)
        3:  Android Tor dataset
        4:  Android Apps dataset
        5:  Wang et al. dataset (Tor - cell traces). Has to go with option -u
        41: Android Apps dataset (open world only) finance for monitored, and android Apps dataset communication for unmonitored
        42: Android Apps dataset (open world only) finance for monitored, and android Apps dataset social for unmonitored
        6:  Honeypatch dataset (binary). It consists of two class only; attack and benign.
        61: Honeypatch dataset (multiclass). It consists of multiple attack classes and one benign class.
        62: Honeypatch dataset (multiclass). It consists of multiple attack classes and multiple benign classes.
        63: Honeypatch dataset (multiclass). It consists of multiple attack classes and multiple benign classes. "benattack" dataset: attacks are embedded inside benign traffic
        64: Honeypatch dataset (multiclass). Same as -d=63, with cofing.NUM_TRACE_PACKETS used. It consists of multiple attack classes and multiple benign classes. "benattack" dataset: attacks are embedded inside benign traffic.
        65: Honeypatch sysdig dataset
        (default 1)

    -C [int] : classifier to run, if multiple classifiers, then separate by a comma (example: -C 23,3,15)
        0: Liberatore Classifer
        1: Wright et al. Classifier
        2: Jaccard Classifier
        3: Panchenko et al. Classifier
        5: Lu et al. Edit Distance Classifier
        6: Herrmann et al. Classifier
        4: Dyer et al. Bandwidth (BW) Classifier
        10: Dyer et al. Time Classifier
        14: Dyer et al. Variable n-gram (VNG) Classifier
        15: Dyer et al. VNG++ Classifier
        21: Adversarial Classifier
        22: Adversarial Classifier On Panchenko
        31: Adversarial Classifier Tor
        41: Adversarial Classifier using Bloom Filter
        42: Adversarial Classifier On Panchenko using Bloom Filter
        23: Adversarial Classifier Using BiDirection features only (no panch features)
        101:To Wang Files - Closed World Classifier. (Not any more: Should be with option -x 1.)"
        102:To Wang Files - Open World Classifier. (Not any more: Should be with option -x 1.)"
        33: HoneyPatch Sysdig Classifier (kNN-LCS), kNN with Longest Common Subsequence distance metric.
        43: HoneyPatch Sysdig Classifier (NGram)
        (default 0)

    -c [int]: countermeasure to use
        0: None
        1: Pad to MTU
        2: Session Random 255
        3: Packet Random 255
        4: Pad Random MTU
        5: Exponential Pad
        6: Linear Pad
        7: Mice-Elephants Pad
        8: Direct Target Sampling
        9: Traffic Morphing
        (default 0)

    -n [int]: number of trials to run per experiment (default 1)

    -t [int]: number of training traces to use per experiment (default 16)

    -T [int]: number of testing traces to use per experiment (default 4)

    -D [0 or 1]: Packet Size as a word (default 0)
    -E [0 or 1]: UniBurst Size as a word (default 0)
    -F [0 or 1]: UniBurst Time as a word (default 0)
    -G [0 or 1]: UniBurst Number as a word (default 0)
    -H [0 or 1]: BiBurst Size as a word (default 0)
    -I [0 or 1]: BiBurst Time as a word (default 0)

    -A [0 or 1]: Ignore ACK packets (default 0, ACK packets NOT ignored (ACK included)

    -V [0 or 1]: Five number summary, for the Adversarial Classifier (Default is 0)

    -m : Number of Monitored Websites for Open World (m < k). (default -1: Not An Open World Scenario)

    -u : Number of nonMonitored Websites for Open World (used in Wang Tor dataset (dataset number 5)). -k = -m = NumMonitored. (default -1)

    -x [0 or 1]: 0: no Extra,   1: Extra.    (default 0)   with -C 101: To Wang Files - Closed World Classifier (for generating OSAD files) and - Open World.

                    This has been overridden.

    -P : Number of Principal Component Analysis (PCA) components (default 0: No PCA required.) It has to be <= number of sum of instances in both training and testing files

    -g : Linear Discriminant Analysis. Number of Principal Components (default 0: No LDA required.) It has to be < number of classes. g for generalized eigenvalue problem

    -b: bucket size (default: 600)

    -l: lasso (default: 0, no lasso)

    -s: Span Time. For covariate Shift experiments. Training traces are collected at time t and testing traces are collected at time t+s. (Default is 0, no time constraint on training and testing instances)

    -X [0 or #folds]: Apply cross validation. (default 0, no cross validation)

    -i: Number of benign classes for the honeypatch dataset

    -p: Number of packets to be used from testing traces. Mainly used for the Honeypatch datasets.

    -Q: Number of total attacks (collected between Honeypatch and Decoy) (default -1, no HP_DCOY Attacks). Honeypatch datasets.
    -w: Number of attacks (collected between Honeypatch and Decoy) to be used in training (default -1, use all). Honeypatch datasets. (If -1 or not set, then include all. If 0, then don't include any. If x, then include x HP-DCOY attack classes only).
    -W: Number of attacks (collected between Honeypatch and Decoy) to be used in testing  (default -1, use all). Honeypatch datasets. (If -1 or not set, then include all. If 0, then don't include any. If x, then include x HP-DCOY attack classes only).

    -y: Number of neighbors for kNN (default: 3).

    -f: Number of the most important features (Tree-based Random Forest Feature Selection)

    -e: Ensemble

    -a: List of ordered attacks (mainly for IDS zero-day experiments)

    -o: HP_dataset name (see config.HP_DATA_SETS)
    """

def run():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:T:N:k:c:C:d:n:r:B:D:E:F:G:H:I:J:K:L:M:A:m:V:P:g:q:x:b:l:u:s:X:i:p:w:W:Q:y:f:e:a:o:h")
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    char_set = string.ascii_lowercase + string.digits
    runID = ''.join(random.sample(char_set,8))

    webpageIndex = 1; # Global variable to write the Wang OSAD file names. For Wang OSAD files numbering X-Y.txt (Closed World) // -C 101.  Oct 14, 2015

    HP_DATASET_KEY = -1

    for o, a in opts:
        if o in ("-k"):
            config.BUCKET_SIZE = int(a)
        elif o in ("-C"):
            config.CLASSIFIER_LIST = a.split(",")
        elif o in ("-d"):
            config.DATA_SOURCE = int(a)
        elif o in ("-c"):
            config.COUNTERMEASURE = int(a)
        elif o in ("-N"):
            config.TOP_N = int(a)
        elif o in ("-t"):
            config.NUM_TRAINING_TRACES = int(a)
        elif o in ("-T"):
            config.NUM_TESTING_TRACES = int(a)
        elif o in ("-n"):
            config.NUM_TRIALS = int(a)
        elif o in ("-r"):
            runID = str(a)
        elif o in ("-D"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['packetSize'] = 1
        elif o in ("-E"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['burstSize'] = 1
        elif o in ("-F"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['burstTime'] = 1
        elif o in ("-G"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['burstNumber'] = 1
        elif o in ("-H"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['biBurstSize'] = 1
        elif o in ("-I"):
            if int(a) == 1:
                config.GLOVE_OPTIONS['biBurstTime'] = 1
        elif o in ("-B"):
            config.GLOVE_OPTIONS['ModelTraceNum'] = int(a)
        elif o in ("-J"):
            config.GLOVE_PARAMETERS['window'] = int(a)
        elif o in ("-K"):
            config.GLOVE_PARAMETERS['no_components'] = int(a)
        elif o in ("-L"):
            config.GLOVE_PARAMETERS['learning_rate'] = float(a)
        elif o in ("-M"):
            config.GLOVE_PARAMETERS['epochs'] = int(a)
        elif o in ("-A"):
            config.IGNORE_ACK = bool(int(a))
        elif o in ("-m"):
            config.NUM_MONITORED_SITES = int(a)
        elif o in ("-V"):
            config.FIVE_NUM_SUM = int(a)
        elif o in ("-x"):
            config.EXTRA = int(a)
        elif o in ("-P"):
            config.n_components_PCA = int(a)
        elif o in ("-g"):
            config.n_components_LDA = int(a)
        elif o in ("-q"):
            config.n_components_QDA = int(a)
        elif o in ("-b"):
            config.bucket_Size = int(a)
        elif o in ("-l"):
            config.lasso = float(a) # Float for threshold
        elif o in ("-u"):
            config.NUM_NON_MONITORED_SITES = int(a)
        elif o in ("-s"):
            config.COVARIATE_SHIFT = int(a)
        elif o in ("-X"):
            config.CROSS_VALIDATION = int(a)
        elif o in ("-i"):
            config.NUM_BENIGN_CLASSES = int(a)
        elif o in ("-p"):
            config.NUM_TRACE_PACKETS = int(a)
        elif o in ("-Q"):
            config.NUM_HP_DCOY_ATTACKS_TOTAL = int(a)
        elif o in ("-w"):
            config.NUM_HP_DCOY_ATTACKS_TRAIN = int(a)
        elif o in ("-W"):
            config.NUM_HP_DCOY_ATTACKS_TEST = int(a)
        elif o in ("-y"):
            config.NUM_NEIGHBORS = int(a)
        elif o in ("-f"):
            config.NUM_FEATURES_RF = int(a)
        elif o in ("-e"):
            config.ENSEMBLE = int(a)
        elif o in ("-a"):
            config.ATTACK_LIST = a.split(",")
            config.ATTACK_LIST = map(int, config.ATTACK_LIST) # casting string elements to in
        elif o in ("-o"):
            HP_DATASET_KEY = int(a)
        else:
            usage()
            sys.exit(2)

    config.RUN_ID = runID

    if not os.path.exists(config.OUTPUT_DIR):
        os.mkdir(config.OUTPUT_DIR)

    if not os.path.exists(config.WANG):
        os.mkdir(config.WANG)

    if not os.path.exists(config.CACHE_DIR):
        os.mkdir(config.CACHE_DIR)

    if not os.path.exists(config.SYSDIG):
        os.mkdir(config.SYSDIG)

    # Check
    if config.NUM_HP_DCOY_ATTACKS_TRAIN != -1 or config.NUM_HP_DCOY_ATTACKS_TEST != -1:
        if config.NUM_HP_DCOY_ATTACKS_TOTAL == -1:
            print 'Please indicate NUM_HP_DCOY_ATTACKS_TOTAL, Option -Q.'
            sys.exit(2)

    if config.DATA_SOURCE == 0:
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = len(config.DATA_SET)-config.NUM_TESTING_TRACES
    elif config.DATA_SOURCE == 1:
        maxTracesPerWebsiteH = 160
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = maxTracesPerWebsiteH-config.NUM_TESTING_TRACES
    elif config.DATA_SOURCE == 2:
        maxTracesPerWebsiteH = 18
        #29May2015 maxTracesPerWebsiteH = 160 # Changed from 18 to 160 on 28May2015
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = maxTracesPerWebsiteH-config.NUM_TESTING_TRACES
    elif config.DATA_SOURCE == 3:
        config.DATA_SET = config.DATA_SET_ANDROID_TOR
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = len(config.DATA_SET)-config.NUM_TESTING_TRACES
        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'pcap-logs-Android-Tor-Grouping')
    elif config.DATA_SOURCE == 4 or config.DATA_SOURCE == 41 or config.DATA_SOURCE == 42:
        config.DATA_SET = config.DATA_SET_ANDROID_APPS
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = len(config.DATA_SET)-config.NUM_TESTING_TRACES
        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'pcap-logs-android-apps')
    elif config.DATA_SOURCE == 5:
        config.DATA_SET = config.DATA_SET_WANG_TOR
        startIndex = config.NUM_TRAINING_TRACES
        endIndex   = len(config.DATA_SET)-config.NUM_TESTING_TRACES
        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'wang-tor/batch')
    elif config.DATA_SOURCE == 6:
        config.DATA_SET = config.DATA_SET_HONEYPATCH_BENIGN
        startIndexBenign = config.NUM_TRAINING_TRACES
        endIndexBenign   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        config.DATA_SET = config.DATA_SET_HONEYPATCH_ATTACK
        startIndexAttack = config.NUM_TRAINING_TRACES
        endIndexAttack   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatchdata')
    elif config.DATA_SOURCE == 61 or config.DATA_SOURCE == 62:
        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_BENIGN
        startIndexBenign = config.NUM_TRAINING_TRACES
        endIndexBenign   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_ATTACK
        startIndexAttack = config.NUM_TRAINING_TRACES
        endIndexAttack   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        if config.DATA_SOURCE == 61:
            config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatchdataMulticlass')
        elif config.DATA_SOURCE == 62:
            config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatchdataMulticlassAttackBenign')

    elif config.DATA_SOURCE == 63:
        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_BENATTACK_BENIGN
        startIndexBenign = config.NUM_TRAINING_TRACES
        endIndexBenign   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_BENATTACK_ATTACK
        startIndexAttack = config.NUM_TRAINING_TRACES
        endIndexAttack   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackOld')

    elif config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65:
        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_BENATTACK_BENIGN
        startIndexBenign = config.NUM_TRAINING_TRACES * config.NUM_TRAINING_TRACES_BENIGN_FACTOR # * 2 more benign data
        endIndexBenign   = len(config.DATA_SET)-(config.NUM_TESTING_TRACES * config.NUM_TESTING_TRACES_BENIGN_FACTOR) # * 2 more benign data

        config.DATA_SET = config.DATA_SET_HONEYPATCH_MC_BENATTACK_ATTACK
        startIndexAttack = config.NUM_TRAINING_TRACES
        endIndexAttack   = len(config.DATA_SET)-config.NUM_TESTING_TRACES

        if config.DATA_SOURCE == 64:
            if (HP_DATASET_KEY == -1):
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattack')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackTest')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackMerge')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackUnpatched')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewData')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewDataUnpatched')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewData-regularPatched')
                config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewDataZday')
            else:
                config.PCAP_ROOT = os.path.join(config.BASE_DIR, config.HP_DATASETS[HP_DATASET_KEY][0]) # packets

        elif config.DATA_SOURCE == 65:
            if (HP_DATASET_KEY == -1):
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdig')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigTest')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigMerge')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesUnpatched')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesAllEvents')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewData')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewDataUnpatched')
                #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewData-regularPatched')
                config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewDataZday')
            else:
                config.PCAP_ROOT = os.path.join(config.BASE_DIR, config.HP_DATASETS[HP_DATASET_KEY][1]) # syscalls



    for i in range(config.NUM_TRIALS):

        #startStart = time.time()

        webpageIds = range(0, config.TOP_N - 1)
        random.shuffle( webpageIds )
        webpageIds = webpageIds[0:config.BUCKET_SIZE]


        #seed = random.randint( startIndex, endIndex )

        if config.DATA_SOURCE == 6 or config.DATA_SOURCE == 61 or config.DATA_SOURCE == 62 or config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65: # honeypatch
            seedBenign = random.randint( startIndexBenign, endIndexBenign )
            seedAttack = random.randint( startIndexAttack, endIndexAttack )
        else: # all other datsets
            seed = random.randint( startIndex, endIndex )


        # Jan 19, 2016.
        # removing webpages with not-enough-packet traces
        # mainly for open world and d 0
        config.BAD_WEBSITES = []
        if ((config.DATA_SOURCE == 0 or config.DATA_SOURCE == 4 or config.DATA_SOURCE == 41 or config.DATA_SOURCE == 42)): # and config.NUM_MONITORED_SITES != -1):
            badSample = True
            #numLeastPackets = 50
            numLeastPackets = 5
            numAllowedBadTracesPerWebsiteTrain = int(config.NUM_TRAINING_TRACES/2)
            numAllowedBadTracesPerWebsiteTest = int(config.NUM_TESTING_TRACES/2)
            #numAllowedBadTracesPerWebsiteTrain = numAllowedBadTracesPerWebsiteTest = 0
            while badSample:
                if Utils.goodSample(webpageIds, seed-config.NUM_TRAINING_TRACES, seed, numAllowedBadTracesPerWebsiteTrain, numLeastPackets) and \
                   Utils.goodSample(webpageIds, seed, seed+config.NUM_TESTING_TRACES,  numAllowedBadTracesPerWebsiteTest, numLeastPackets):
                    badSample = False
                else:
                    # resample
                    #webpageIds = range(0, config.TOP_N - 1)
                    webpageIds = list(set(range(0, config.TOP_N - 1)) - set(config.BAD_WEBSITES) ) # exclude bad websites so they are not examined again
                    #print 'config.BAD_WEBSITES inside'
                    #print config.BAD_WEBSITES
                    #print
                    random.shuffle( webpageIds )
                    webpageIds = webpageIds[0:config.BUCKET_SIZE]

        #print config.BAD_WEBSITES
        #print webpageIds
        #print 'here'

        monitoredWebpageIdsObj = []
        unMonitoredWebpageIdsObj = []

        # For honeypatch dataset (62)
        benignWebpageIds = []
        attackWebpageIds = []
        if config.DATA_SOURCE == 62 or config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65:
            webpageIds = sorted(webpageIds) # sorted as the first few (depending on -i option) are benign and the rest are attacks
            benignWebpageIds = webpageIds[0:config.NUM_BENIGN_CLASSES] # For the dataset (-d 62 or 63), -i: used in closed-world and open-world to decide number of benign classes
            attackWebpageIds = webpageIds[config.NUM_BENIGN_CLASSES:]

            # for zero day experiments, to be passed in the args
            if (config.ATTACK_LIST): # list not empty
                attackWebpageIds = config.ATTACK_LIST
                webpageIds = benignWebpageIds + attackWebpageIds

        # for Wang's knn open world files (1's and -1's)
        if (config.NUM_MONITORED_SITES != -1 and config.DATA_SOURCE != 5 and config.DATA_SOURCE != 41 and config.DATA_SOURCE != 42): # open world for all datasets except Wang Tor
            monitoredWebpageIdsObj = webpageIds[0:config.NUM_MONITORED_SITES] # Arrays.copyOfRange(webpageIds, 0, config.NUM_MONITORED_SITES);
            unMonitoredWebpageIdsObj = webpageIds[config.NUM_MONITORED_SITES:] # Arrays.copyOfRange(webpageIds, config.NUM_MONITORED_SITES, webpageIds.length);
        elif (config.NUM_NON_MONITORED_SITES != -1 and config.DATA_SOURCE == 5): # Wang Tor dataset
            monitoredWebpageIdsObj = webpageIds[0:config.NUM_MONITORED_SITES] # Arrays.copyOfRange(webpageIds, 0, config.NUM_MONITORED_SITES);
            unMonitoredWebpageIdsObj = [] # will be 100, 101, 102, ... (100+config.NUM_NON_MONITORED_SITES)
            # Wang Tor dataset consists of files with 0 to 99 as monitored with 89 traces each and 0 to 8999 as nonMonitored with one trace each
            # We consider webpage id for monitored as the file numbering (0 to 99) but for nonMonitored, the ids start from 100. When reading the
            # nonMonitored files, we will do (id - 100) to get the correct file number.
            unMonStartId = 100
            for i in range(config.NUM_NON_MONITORED_SITES):
                unMonitoredWebpageIdsObj.append(unMonStartId + i)

            # in case of config.DATA_SOURCE == 5 (Wang Tor), webpageIds represent monitored at first and then
            # then we concatenate the unmonitored starting from id 100
            webpageIds = webpageIds + unMonitoredWebpageIdsObj

        elif (config.NUM_NON_MONITORED_SITES != -1 and (config.DATA_SOURCE == 41 or config.DATA_SOURCE == 42)): # Android communication
            monitoredWebpageIdsObj = webpageIds[0:config.NUM_MONITORED_SITES] # Arrays.copyOfRange(webpageIds, 0, config.NUM_MONITORED_SITES);
            unMonitoredWebpageIdsObj = [] # will be 10000, 10001, 10002, ... (10000+config.NUM_NON_MONITORED_SITES)
            # Android Apps Communication dataset consists of files with 0 to 99 as monitored with 89 traces each and 0 to 8999 as nonMonitored with one trace each
            # We consider webpage id for monitored as usual but for nonMonitored, the ids start from 10000.
            unMonStartId = 10000
            for i in range(config.NUM_NON_MONITORED_SITES):
                unMonitoredWebpageIdsObj.append(unMonStartId + i)

            # in case of config.DATA_SOURCE == 5 (Wang Tor), webpageIds represent monitored at first and then
            # then we concatenate the unmonitored starting from id 100
            webpageIds = webpageIds + unMonitoredWebpageIdsObj


        #seed = random.randint( startIndex, endIndex )

        #preCountermeasureOverhead = 0
        #postCountermeasureOverhead = 0
#
        ##classifier     = intToClassifier(config.CLASSIFIER)
        #countermeasure = intToCountermeasure(config.COUNTERMEASURE)
#
        #trainingSet = []
        #testingSet  = []
#
        #targetWebpage = None
        #extraCtr = 0
###

        debugInfos = {}

        #assign config.CLASSIFIER here
        #loop over each classifier
        for clsfr in config.CLASSIFIER_LIST:
            preCountermeasureOverhead = 0
            postCountermeasureOverhead = 0

            #classifier     = intToClassifier(config.CLASSIFIER)
            countermeasure = intToCountermeasure(config.COUNTERMEASURE)

            trainingSet = []
            testingSet  = []

            targetWebpage = None
            extraCtr = 0
            startStart = time.time()


            #if int(clsfr) == 23: # Bi-Di
            #    config.IGNORE_ACK = False

            config.CLASSIFIER = int(clsfr)

            if config.ENSEMBLE != 0:
                print 'changing datasets sources for -C 23 and -C 43, please comment if necessary'
                if config.CLASSIFIER == 23:
                    config.DATA_SOURCE=64
                    if (HP_DATASET_KEY == -1):
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattack')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackTest')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackMerge')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackUnpatched')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewData')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewDataUnpatched')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewData-regularPatched')
                        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackNewDataZday')
                    else:
                        config.PCAP_ROOT = os.path.join(config.BASE_DIR, config.HP_DATASETS[HP_DATASET_KEY][0]) # packets

                elif config.CLASSIFIER == 33: # lcs-knn
                    config.DATA_SOURCE=65
                    #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackSysdig')
                    #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackSysdigMerge')
                elif config.CLASSIFIER == 43:
                    config.DATA_SOURCE=65
                    if (HP_DATASET_KEY == -1):
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackSysdig')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackSysdigTest')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR,'honeypatckBenattackSysdigMerge')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesUnpatched')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewData')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewDataUnpatched')
                        #config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewData-regularPatched')
                        config.PCAP_ROOT = os.path.join(config.BASE_DIR   ,'honeypatckBenattackSysdigFilesNewDataZday')
                    else:
                        config.PCAP_ROOT = os.path.join(config.BASE_DIR, config.HP_DATASETS[HP_DATASET_KEY][1]) # syscalls

            classifier     = intToClassifier(config.CLASSIFIER)


            outputFilenameArray = [os.path.basename(__file__),
                                   'results',
                                   'k'+str(config.BUCKET_SIZE),
                                   'c'+str(config.COUNTERMEASURE),
                                   'd'+str(config.DATA_SOURCE),
                                   'C'+str(config.CLASSIFIER),
                                   'N'+str(config.TOP_N),
                                   't'+str(config.NUM_TRAINING_TRACES),
                                   'T'+str(config.NUM_TESTING_TRACES),
                                   'D' + str(config.GLOVE_OPTIONS['packetSize']),
                                   'E' + str(config.GLOVE_OPTIONS['burstSize']),
                                   'F' + str(config.GLOVE_OPTIONS['burstTime']),
                                   'G' + str(config.GLOVE_OPTIONS['burstNumber']),
                                   'H' + str(config.GLOVE_OPTIONS['biBurstSize']),
                                   'I' + str(config.GLOVE_OPTIONS['biBurstTime']),
                                   'A' + str(int(config.IGNORE_ACK)),
                                   'V' + str(int(config.FIVE_NUM_SUM)),
                                   'P' + str(int(config.n_components_PCA)),
                                   'g' + str(int(config.n_components_LDA)),
                                   'l' + str(int(config.lasso)),
                                   'b' + str(int(config.bucket_Size))

                                  ]

            if config.COVARIATE_SHIFT != 0:
                outputFilenameArray.append('s' + str(int(config.COVARIATE_SHIFT)))

            if config.NUM_NON_MONITORED_SITES != -1 and (config.DATA_SOURCE == 5 or config.DATA_SOURCE == 41 or config.DATA_SOURCE == 42 \
                                                      or config.DATA_SOURCE == 6 or config.DATA_SOURCE == 61 or config.DATA_SOURCE == 62 \
                                                      or config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65):
                outputFilenameArray.append('u'+str(config.NUM_NON_MONITORED_SITES))

            if config.CROSS_VALIDATION != 0: # cross validation
                outputFilenameArray.append('cv'+str(config.CROSS_VALIDATION))

            # HP datasets
            if config.NUM_TRACE_PACKETS != -1: # num of packets to be used
                outputFilenameArray.append('p'+str(config.NUM_TRACE_PACKETS))

            if config.NUM_BENIGN_CLASSES != -1:
                outputFilenameArray.append('i'+str(config.NUM_BENIGN_CLASSES))

            # HP datasets
            if config.NUM_HP_DCOY_ATTACKS_TRAIN != -1 or config.NUM_HP_DCOY_ATTACKS_TEST != -1:
                outputFilenameArray.append('Q'+str(config.NUM_HP_DCOY_ATTACKS_TOTAL))
                outputFilenameArray.append('w'+str(config.NUM_HP_DCOY_ATTACKS_TRAIN))
                outputFilenameArray.append('W'+str(config.NUM_HP_DCOY_ATTACKS_TEST))

            # Number of neighbors in kNN_LCS
            if config.CLASSIFIER == config.HP_KNN_LCS:
                outputFilenameArray.append('y'+str(config.NUM_NEIGHBORS))

            if config.Num_Features_Selected != 0:
                outputFilenameArray.append('f'+str(config.Num_Features_Selected))

            outputFilename = os.path.join(config.OUTPUT_DIR,'.'.join(outputFilenameArray))

            if not os.path.exists(config.CACHE_DIR):
                os.mkdir(config.CACHE_DIR)

            if not os.path.exists(outputFilename+'.output'):
                banner = ['accuracy','overhead','timeElapsedTotal','timeElapsedClassifier','fileId', 'targetID']
                f = open( outputFilename+'.output', 'w' )
                f.write(','.join(banner))
                f.close()
            if not os.path.exists(outputFilename+'.debug'):
                f = open( outputFilename+'.debug', 'w' )
                f.close()

            # OSAD closed world
            tempRunID = runID
            outputFilenameArrayOSAD = ['OSAD',
                                       tempRunID,
                                   'k'+str(config.BUCKET_SIZE),
                                   'c'+str(config.COUNTERMEASURE),
                                   'd'+str(config.DATA_SOURCE),
                                   'C'+str(config.CLASSIFIER),
                                   'N'+str(config.TOP_N),
                                   't'+str(config.NUM_TRAINING_TRACES),
                                   'T'+str(config.NUM_TESTING_TRACES)
                                  ]
            OSADfolder = os.path.join(config.WANG,'.'.join(outputFilenameArrayOSAD))

            if config.CLASSIFIER == config.TO_WANG_FILES_CLOSED_WORLD:
                    if not os.path.exists(OSADfolder):
                        os.mkdir(OSADfolder)
                    else:
                        shutil.rmtree(OSADfolder) # delete and remake folder
                        os.mkdir(OSADfolder)

            # WangOW open world
            outputFilenameArrayWangOpenWorld = ['KNNW',
                                                'openWorld'+str(config.NUM_MONITORED_SITES),
                                       tempRunID,
                                   'k'+str(config.BUCKET_SIZE),
                                   'c'+str(config.COUNTERMEASURE),
                                   'd'+str(config.DATA_SOURCE),
                                   'C'+str(config.CLASSIFIER),
                                   'N'+str(config.TOP_N),
                                   't'+str(config.NUM_TRAINING_TRACES),
                                   'T'+str(config.NUM_TESTING_TRACES)
                                  ]

            # For Wang Tor dataset
            if config.NUM_NON_MONITORED_SITES != -1:
                outputFilenameArrayWangOpenWorld.append('u'+str(config.NUM_NON_MONITORED_SITES))

            WangOpenWorldKnnfolder = os.path.join(config.WANG,'.'.join(outputFilenameArrayWangOpenWorld))

            if config.CLASSIFIER == config.TO_WANG_FILES_OPEN_WORLD:
                    if not os.path.exists(WangOpenWorldKnnfolder):
                        os.mkdir(WangOpenWorldKnnfolder)
                    else:
                        shutil.rmtree(WangOpenWorldKnnfolder) # delete and remake folder
                        os.mkdir(WangOpenWorldKnnfolder)

                    # batch folder
                    os.mkdir(WangOpenWorldKnnfolder+'/'+'batch')


            for webpageId in webpageIds:
                #if webpageId < config.NUM_BENIGN_CLASSES:
                #    continue
                if config.DATA_SOURCE == 0 or config.DATA_SOURCE == 3 or config.DATA_SOURCE == 4:
                    if config.COVARIATE_SHIFT == 0:
                        # Normal case
                        webpageTrain = Datastore.getWebpagesLL( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                        webpageTest  = Datastore.getWebpagesLL( [webpageId], seed, seed+config.NUM_TESTING_TRACES )
                    else:
                        # span time training/testing
                        webpageTrain = Datastore.getWebpagesLL( [webpageId], 0, config.NUM_TRAINING_TRACES )
                        #webpageTest  = Datastore.getWebpagesLL( [webpageId], len(config.DATA_SET)-config.NUM_TESTING_TRACES, len(config.DATA_SET) )
                        # a span of config.COVARIATE_SHIFT days
                        webpageTest  = Datastore.getWebpagesLL( [webpageId], config.NUM_TRAINING_TRACES+config.COVARIATE_SHIFT, config.NUM_TRAINING_TRACES+config.COVARIATE_SHIFT+config.NUM_TESTING_TRACES)

                elif config.DATA_SOURCE == 1 or config.DATA_SOURCE == 2:
                    webpageTrain = Datastore.getWebpagesHerrmann( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                    webpageTest  = Datastore.getWebpagesHerrmann( [webpageId], seed, seed+config.NUM_TESTING_TRACES )

                elif config.DATA_SOURCE == 5:
                    if not unMonitoredWebpageIdsObj.__contains__(webpageId):
                        # monitored webpage so we take instances for training and testing as we do regularly
                        webpageTrain = Datastore.getWebpagesWangTor( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                        webpageTest  = Datastore.getWebpagesWangTor( [webpageId], seed, seed+config.NUM_TESTING_TRACES )
                    else:
                        # unmonitored so we take just one testing trace
                        #webpageTrain = Datastore.getDummyWebpages(webpageId)
                        webpageTest  = Datastore.getWebpagesWangTor( [webpageId], 1, 2 )
                        webpageTrain = webpageTest # just to overcome assigning targetWebpage for c8 and c9 defenses, but it will not be appended to the training set

                elif config.DATA_SOURCE == 41 or config.DATA_SOURCE == 42:
                    if not unMonitoredWebpageIdsObj.__contains__(webpageId):
                        # monitored webpage so we take instances for training and testing as we do regularly
                        webpageTrain = Datastore.getWebpagesLL( [webpageId], seed-config.NUM_TRAINING_TRACES, seed )
                        webpageTest  = Datastore.getWebpagesLL( [webpageId], seed, seed+config.NUM_TESTING_TRACES )
                    else:
                        # unmonitored so we take just one testing trace
                        #webpageTrain = Datastore.getDummyWebpages(webpageId)
                        webpageTest  = Datastore.getWebpagesLL( [webpageId], 1, 2 )
                        webpageTrain = webpageTest # just to overcome assigning targetWebpage for c8 and c9 defenses, but it will not be appended to the training set

                elif config.DATA_SOURCE == 6:
                    # -u option (config.NUM_NON_MONITORED_SITES) is used for the open world for honeypatch data as the number of instances
                    if config.NUM_NON_MONITORED_SITES == -1: # closed world setting
                        if webpageId == 0: # benign
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign-config.NUM_TRAINING_TRACES, seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign, seedBenign+config.NUM_TESTING_TRACES )
                        elif webpageId == 1: # attack
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                    else: # open world setting. option -u has to be set (config.NUM_NON_MONITORED_SITES)
                        if webpageId == 0: # benign. open world: benign is the nonMonitored
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES/2 )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], config.NUM_NON_MONITORED_SITES/2, config.NUM_NON_MONITORED_SITES )
                        elif webpageId == 1: # attack. open world: attack is the monitored
                            # -t and -T will be for the attack only in case of open world
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )

                elif config.DATA_SOURCE == 61:
                    # -u option (config.NUM_NON_MONITORED_SITES) is used for the open world for honeypatch data as the number of instances
                    if config.NUM_NON_MONITORED_SITES == -1: # closed world setting
                        if webpageId == 0: # benign
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign-config.NUM_TRAINING_TRACES, seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign, seedBenign+config.NUM_TESTING_TRACES )
                        else: # attack1, attack2, ...etc
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                    else: # open world setting. option -u has to be set (config.NUM_NON_MONITORED_SITES)
                        if webpageId == 0: # benign. open world: benign is the nonMonitored
                            # -u is split between training and testing
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES/2 )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], config.NUM_NON_MONITORED_SITES/2, config.NUM_NON_MONITORED_SITES )
                        else: # attack. open world: attack is the monitored
                            # -t and -T will be for the attack only in case of open world
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )

                elif config.DATA_SOURCE == 62 or config.DATA_SOURCE == 63:
                    # -u option (config.NUM_NON_MONITORED_SITES) is used for the open world for honeypatch data as the number of instances
                    if config.NUM_NON_MONITORED_SITES == -1: # closed world setting
                        if webpageId in benignWebpageIds: # benign
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign-config.NUM_TRAINING_TRACES, seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign, seedBenign+config.NUM_TESTING_TRACES )
                        else: # attack2, attack3, ...etc
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                    else: # open world setting. option -u has to be set (config.NUM_NON_MONITORED_SITES)
                        if webpageId in benignWebpageIds: # benign. open world: benign is the nonMonitored
                            # -u is split between training and testing
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES/2 )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], config.NUM_NON_MONITORED_SITES/2, config.NUM_NON_MONITORED_SITES )

                            ########## Temp, to be deleted ########## Mar 02, 2016 ########
                            #if webpageId == 0:
                            #    webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES ) # train with blog, webpage 0
                            #    webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId + 1], 0, config.NUM_NON_MONITORED_SITES ) # testing with wordpress, webpage 1
                            #elif webpageId == 1:
                            #    continue
                            ########## end of 'to be deleted' ###########

                            ########## Temp, to be deleted ########## Mar 02, 2016 ########
                            #if webpageId == 0:
                            #    continue
                            #elif webpageId == 1:
                            #    webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES ) # train with wordpress, webpage 1
                            #    webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId - 1], 0, config.NUM_NON_MONITORED_SITES ) # testing with blog, webpage 0
                            ########## end of 'to be deleted' ###########
                        else: # attack. open world: attack is the monitored
                            # -t and -T will be for the attack only in case of open world
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                elif config.DATA_SOURCE == 64:
                    # -u option (config.NUM_NON_MONITORED_SITES) is used for the open world for honeypatch data as the number of instances
                    if config.NUM_NON_MONITORED_SITES == -1: # closed world setting
                        if webpageId in benignWebpageIds: # benign
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedBenign-config.NUM_TRAINING_TRACES, seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSomePackets( [webpageId], seedBenign, seedBenign+config.NUM_TESTING_TRACES )
                        else: # attack2, attack3, ...etc
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSomePackets( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                    else: # open world setting. option -u has to be set (config.NUM_NON_MONITORED_SITES)
                        if webpageId in benignWebpageIds: # benign. open world: benign is the nonMonitored
                            # -u is split between training and testing
                            #webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], 0, config.NUM_NON_MONITORED_SITES/2 )
                            #webpageTest  = Datastore.getWebpagesHoneyPatchSomePackets( [webpageId], config.NUM_NON_MONITORED_SITES/2, config.NUM_NON_MONITORED_SITES )
                            webpageTrain = Datastore.getWebpagesHoneyPatchSomePackets( [webpageId], seedBenign-(config.NUM_TRAINING_TRACES * config.NUM_TRAINING_TRACES_BENIGN_FACTOR), seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSomePackets( [webpageId], seedBenign, seedBenign+(config.NUM_TESTING_TRACES * config.NUM_TESTING_TRACES_BENIGN_FACTOR) )
                        else: # attack. open world: attack is the monitored
                            # -t and -T will be for the attack only in case of open world
                            webpageTrain = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatch( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                elif config.DATA_SOURCE == 65:
                    # -u option (config.NUM_NON_MONITORED_SITES) is used for the open world for honeypatch data as the number of instances
                    if config.NUM_NON_MONITORED_SITES == -1: # closed world setting
                        if webpageId in benignWebpageIds: # benign
                            webpageTrain = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedBenign-config.NUM_TRAINING_TRACES, seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedBenign, seedBenign+config.NUM_TESTING_TRACES )
                        else: # attack2, attack3, ...etc
                            webpageTrain = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )
                    else: # open world setting. option -u has to be set (config.NUM_NON_MONITORED_SITES)
                        if webpageId in benignWebpageIds: # benign. open world: benign is the nonMonitored
                            # -u is split between training and testing
                            #webpageTrain = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], 0, config.NUM_NON_MONITORED_SITES/2 )
                            #webpageTest  = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], config.NUM_NON_MONITORED_SITES/2, config.NUM_NON_MONITORED_SITES )

                            #continue # temp, no benign
                            #print "not supposed to come here"

                            webpageTrain = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedBenign-(config.NUM_TRAINING_TRACES * config.NUM_TRAINING_TRACES_BENIGN_FACTOR), seedBenign )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedBenign, seedBenign+(config.NUM_TESTING_TRACES * config.NUM_TESTING_TRACES_BENIGN_FACTOR) )
                        else: # attack. open world: attack is the monitored
                            # -t and -T will be for the attack only in case of open world
                            webpageTrain = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedAttack-config.NUM_TRAINING_TRACES, seedAttack )
                            webpageTest  = Datastore.getWebpagesHoneyPatchSysdig( [webpageId], seedAttack, seedAttack+config.NUM_TESTING_TRACES )


                webpageTrain = webpageTrain[0]
                webpageTest = webpageTest[0]

                if targetWebpage == None:
                    targetWebpage = webpageTrain

                # for unmonitored in Wang Tor dataset, webpageTrain is empty
                # so no need to calculate the overhead
                if not (config.DATA_SOURCE == 5 and unMonitoredWebpageIdsObj.__contains__(webpageId)):
                    preCountermeasureOverhead  += webpageTrain.getBandwidth()

                preCountermeasureOverhead  += webpageTest.getBandwidth()
                #preCountermeasureOverhead  += webpageTrain.getBandwidth()
                #preCountermeasureOverhead  += webpageTest.getBandwidth()

                metadata = None
                if config.COUNTERMEASURE in [config.DIRECT_TARGET_SAMPLING, config.WRIGHT_STYLE_MORPHING]:
                    metadata = countermeasure.buildMetadata( webpageTrain,  targetWebpage )


                i = 0

                webpageList = [webpageTrain, webpageTest]

                # For open world and Wang dataset
                if (config.DATA_SOURCE == 5 and unMonitoredWebpageIdsObj.__contains__(webpageId)):
                    webpageList = [webpageTest]
                    i = 1 # so the trace will go to the testing arff file only

                # Number of HP_DCOY attack classes to be included in training/testingmainBiDirectionLatestEnsembleNewData.py
                if ((config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65) and webpageId in attackWebpageIds):
                    # instead of using webpageId for if conditions, we use attkWebpageIndex (mainly for zero-day shuffling, but can be generalized)
                    attkWebpageIndex = config.NUM_BENIGN_CLASSES + attackWebpageIds.index(webpageId) # zero-indexed
                    if config.NUM_HP_DCOY_ATTACKS_TRAIN == -1 and config.NUM_HP_DCOY_ATTACKS_TEST == -1:
                        # Normal case, take all attack classes for training and testing
                        #webpageList = [webpageTrain, webpageTest]
                        pass
                    elif config.NUM_HP_DCOY_ATTACKS_TRAIN != -1 and config.NUM_HP_DCOY_ATTACKS_TEST == -1:
                        # Few of the HP_DCOY attacks
                        if attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TRAIN): #(k - Q) + w:
                            # was if webpageId < (config.BUCKET_SIZE - ...
                            #webpageList = [webpageTrain, webpageTest]
                            pass
                        else:
                            webpageList = [webpageTest]
                            i = 1 # so the trace will go to the testing arff file only
                    elif config.NUM_HP_DCOY_ATTACKS_TRAIN == -1 and config.NUM_HP_DCOY_ATTACKS_TEST != -1:
                        # Few of the HP_DCOY attacks
                        if attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TEST):
                            #webpageList = [webpageTrain, webpageTest]
                            pass
                        else:
                            webpageList = [webpageTrain]
                            i = 0 # so the trace will go to the training arff file only
                    elif config.NUM_HP_DCOY_ATTACKS_TRAIN != -1 and config.NUM_HP_DCOY_ATTACKS_TEST != -1:
                        # Few of the HP_DCOY attacks
                        if attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TRAIN) \
                            and attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TEST):
                            #webpageList = [webpageTrain, webpageTest]
                            pass
                        elif not attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TRAIN) \
                            and attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TEST):
                            webpageList = [webpageTest]
                            i = 1 # so the trace will go to the testing arff file only
                        elif attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TRAIN) \
                            and not attkWebpageIndex < (config.BUCKET_SIZE - config.NUM_HP_DCOY_ATTACKS_TOTAL + config.NUM_HP_DCOY_ATTACKS_TEST):
                            webpageList = [webpageTrain]
                            i = 0 # so the trace will go to the training arff file only
                        else:
                            continue # webpageId won't be added to either training or testing set. Grab next webpageId


                for w in webpageList: # was for w in [webpageTrain, webpageTest]:
                    for trace in w.getTraces():
                        if countermeasure:
                            if config.COUNTERMEASURE in [config.DIRECT_TARGET_SAMPLING, config.WRIGHT_STYLE_MORPHING]:
                                if w.getId()!=targetWebpage.getId():
                                    traceWithCountermeasure = countermeasure.applyCountermeasure( trace,  metadata )
                                else:
                                    traceWithCountermeasure = trace
                            else:
                                traceWithCountermeasure = countermeasure.applyCountermeasure( trace )
                        else:
                            traceWithCountermeasure = trace

                        postCountermeasureOverhead += traceWithCountermeasure.getBandwidth()

                        if config.EXTRA == 0: # Normal classifiers
                            if config.CLASSIFIER != config.TO_WANG_FILES_OPEN_WORLD and config.CLASSIFIER != config.TO_WANG_FILES_CLOSED_WORLD:
                                instance = classifier.traceToInstance( traceWithCountermeasure )

                                if instance:
                                    if i==0:
                                        trainingSet.append( instance )
                                    elif i==1:
                                        testingSet.append( instance )
                            elif config.CLASSIFIER == config.TO_WANG_FILES_CLOSED_WORLD:
                                extraCtr += 1
                                instances = classifier.traceToInstances( traceWithCountermeasure, webpageIndex, extraCtr, OSADfolder )
                            elif config.CLASSIFIER == config.TO_WANG_FILES_OPEN_WORLD:
                                #extraCtr += 1
                                instances = classifier.traceToInstances( traceWithCountermeasure, extraCtr, WangOpenWorldKnnfolder, monitoredWebpageIdsObj, unMonitoredWebpageIdsObj )
                                extraCtr += 1 # 0_0 index starts from zero in Wang's open world dataset

                        else: # OSAD classifier (just to write Wang closed world files
                            extraCtr += 1
                            instances = classifier.traceToInstances( traceWithCountermeasure, webpageIndex, extraCtr, OSADfolder )
                            #no need for the following if we want to generate OSAD files only
                            #in future in sha Allah, if setwise needed, then uncomment the following lines as we need the arff files
                            #if instances:
                            #    if i==0:
                            #        for instance in instances:
                            #            trainingSet.append( instance )
                            #    elif i==1:
                            #        for instance in instances:
                            #            testingSet.append( instance )


                        #instance = classifier.traceToInstance( traceWithCountermeasure )

                        #if instance:
                        #    if i==0:
                        #        trainingSet.append( instance )
                        #    elif i==1:
                        #        testingSet.append( instance )
                    #print "appending to sets done for webpage: " + str(w.getId())

                    i+=1
                if config.CLASSIFIER == config.TO_WANG_FILES_CLOSED_WORLD or config.CLASSIFIER == config.TO_WANG_FILES_OPEN_WORLD:
                    webpageIndex += 1 # OSAD or Open World KNN files
                    extraCtr = 0
            ###################


            #print "main: after trainingSet.append"

            startClass = time.time()

            #[accuracy,debugInfo] = classifier.classify( runID, trainingSet, testingSet )

            if config.CLASSIFIER == config.TO_WANG_FILES_CLOSED_WORLD or config.CLASSIFIER == config.TO_WANG_FILES_OPEN_WORLD:
                [accuracy,debugInfo] = ['NA', []]
            else:
                [accuracy,debugInfo] = classifier.classify( runID, trainingSet, testingSet )

            end = time.time()

            overhead = str(postCountermeasureOverhead)+'/'+str(preCountermeasureOverhead)

            output = [accuracy,overhead]

            output.append( '%.2f' % (end-startStart) )
            output.append( '%.2f' % (end-startClass) )

            output.append(tempRunID)

            summary = ', '.join(itertools.imap(str, output))

            f = open( outputFilename+'.output', 'a' )
            f.write( "\n"+summary )
            f.close()

            f = open( outputFilename+'.debug', 'a' )
            for entry in debugInfo:
                if len(entry) == 2:
                    f.write( entry[0]+','+entry[1]+"\n" )
                else:
                    f.write( entry[0]+','+entry[1]+','+entry[2]+"\n" )

            f.close()

            if config.DATA_SOURCE == 6 or (config.DATA_SOURCE == 61 and config.NUM_NON_MONITORED_SITES != -1): # honeypatch dataset, calculate TPR, FPR, F2, ...etc
                positive = [] # attacks are positive
                for i in webpageIds:
                    if i != 0:
                        positive.append('webpage'+str(i)) # attack

                negative = ['webpage0'] # benign is negative
                Utils.calcTPR_FPR(debugInfo, outputFilename, positive, negative)
                #Utils.drawROC_AUC(debugInfo, positive, negative)

            if config.NUM_NON_MONITORED_SITES != -1 and (config.DATA_SOURCE == 62 or config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65): # honeypatch dataset, calculate TPR, FPR, F2, ...etc
                positive = [] # attacks are positive
                negative = [] # benign is negative
                for i in webpageIds:
                    if i < config.NUM_BENIGN_CLASSES:
                        negative.append('webpage'+str(i)) # benign
                    else:
                        positive.append('webpage'+str(i)) # attack

                Utils.calcTPR_FPR(debugInfo, outputFilename, positive, negative)
                #Utils.drawROC_AUC(debugInfo, positive, negative)

            if config.ENSEMBLE != 0:
                debugInfos[config.CLASSIFIER] = debugInfo # {3: [['webpage170', 'webpage170'],..., ['webpage143', 'webpage143']], 15: [['webpage170', 'webpage170'],..., ['webpage143', 'webpage143']], 23: [['webpage170', 'webpage170'],..., ['webpage143', 'webpage143']]}

        #print debugInfos
        if config.ENSEMBLE != 0:
            #print config.CLASSIFIER_LIST
            classifiersList = map(int, config.CLASSIFIER_LIST)
            [ensembleAccuracy,ensembleDebugInfo] = Utils.getEnsembleAccuracy(debugInfos,classifiersList)

            # write new output file with .e
            #print ensembleAccuracy
            f = open( outputFilename+'.ensemble.debug', 'a' )
            for entry in ensembleDebugInfo:
                f.write( entry[0]+','+entry[1]+"\n" )
            f.close()

            if config.NUM_NON_MONITORED_SITES != -1 and (config.DATA_SOURCE == 62 or config.DATA_SOURCE == 63 or config.DATA_SOURCE == 64 or config.DATA_SOURCE == 65): # honeypatch dataset, calculate TPR, FPR, F2, ...etc
                positive = [] # attacks are positive
                negative = [] # benign is negative
                for i in webpageIds:
                    if i < config.NUM_BENIGN_CLASSES:
                        negative.append('webpage'+str(i)) # benign
                    else:
                        positive.append('webpage'+str(i)) # attack

                outputFilename += '.ensemble.output'
                Utils.calcTPR_FPR(ensembleDebugInfo, outputFilename, positive, negative)
                #Utils.drawROC_AUC(ensembleDebugInfo, positive, negative)



if __name__ == '__main__':
    run()
