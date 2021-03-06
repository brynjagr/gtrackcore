import shutil
import os

from gtrackcore.util.profile.Profiler import Profiler


def importFile(fileName, genome, trackName):
    """ ?!
    Generate gtrackcore data from a textual genomic track.

    The genomic track is converted to SmartMemmaps, which are
    placed in a path created from the track id (genome and
    trackName). The path is prepended by a base directory that
    is specified in the configuration.

    The original track data is also persisted.

    Parameters
    ----------
    fileName : string
        Name of genomic track (input file).
    genome : string
        Genome id.
    trackName : string
       An id that uniquely represents a track. E.g. 'Genes and gene subsets:Genes:Refseq'. Each part of the
        trackName may be separated by ':', '^', or '|'.
    """

    trackName = _convertTrackName(trackName)

    from gtrackcore.util.CommonFunctions import createOrigPath, createPath
    origFn = createOrigPath(genome, trackName, os.path.basename(fileName))
    if os.path.exists(origFn):
        shutil.rmtree(os.path.dirname(origFn))
    createPath(origFn)
    shutil.copy(fileName, origFn)
    os.chmod(origFn, 0664)

    from gtrackcore.preprocess.PreProcessTracksJob import PreProcessAllTracksJob
    PreProcessAllTracksJob(genome, trackName).process()


def preprocessTrack(genome, track_name, force=False):
    track_name = _convertTrackName(track_name)

    if force:
        from gtrackcore.metadata.TrackInfo import TrackInfo
        TrackInfo(genome, track_name).resetTimeOfPreProcessing()

    from gtrackcore.preprocess.PreProcessTracksJob import PreProcessAllTracksJob
    PreProcessAllTracksJob(genome, track_name).process()


#TODO: Confirm docstring
def _convertTrackName(trackName):
    """ ?!
    Convert a trackName string to a list.

    Parameters
    ----------
    trackName : string
       An id that uniquely represents a track. E.g. 'Genes and gene subsets:Genes:Refseq'. Each part of the
        trackName may be separated by ':', '^', or '|'.

    Returns
    -------
    list of strings
        Track id converted to list format.
    """
    from gtrackcore.util.CommonFunctions import convertTNstrToTNListFormat
    return convertTNstrToTNListFormat(trackName, doUnquoting=True)

#TODO: Confirm docstring
def _isValidTrack(genome, trackName):
    """ ?!
    Check if the track exists, and is valid.

    Parameters
    ----------
    genome : string
        Genome id.
    trackName : list of strings
        Track id in list format.

    Returns
    -------
    bool
        Whether the track is valid or not.

    """
    from gtrackcore.track.hierarchy.ProcTrackOptions import ProcTrackOptions
    if not ProcTrackOptions.isValidTrack(genome, trackName):
        print 'Track "%s" of genome "%s" is not valid.' % (':'.join(trackName), genome)
        return False
    return True

#TODO: Confirm docstring
def _getDirPath(genome=''):
    """
    Get directory path for ??

    Paramters
    ---------
    genome : string
        Genome id.

    Returns
    -------
    dirPath : string
        The found directory path.

    """
    from gtrackcore.util.CommonFunctions import get_dir_path, createPath
    dirPath = get_dir_path('', [])
    createPath(dirPath)
    return dirPath

#TODO: Confirm docstring
def listAvailableGenomes():
    """ ?!
    List available genomes found in path.

    """
    print 'List of available genomes:'
    dirPath = _getDirPath()
    for dir in os.listdir(dirPath):
        if dir[0] != '.':
            print '    ' + dir

#TODO: Confirm docstring
def listAvailableTracks(genome):
    """ ?!
    List available tracks for the genome found in the path.

    Prints in the form <...category:trackname>

    Parameters
    ----------
    genome : string
        Genome that one want to list tracks for.

    """
    print 'List of available tracks for genome "%s":' % genome
    _getDirPath(genome)

    from gtrackcore.track.hierarchy.ProcTrackNameSource import ProcTrackNameSource
    for trackName in ProcTrackNameSource(genome):
        print '    ' + ':'.join(trackName)

#TODO: Learn
def getExtractionOptions(genome, trackName):
    """ ??
    Paramters
    ---------
    genome : string
        Genome id.
    trackName : string
       An id that uniquely represents a track. E.g. 'Genes and gene subsets:Genes:Refseq'. Each part of the
        trackName may be separated by ':', '^', or '|'.
    """


    trackName = _convertTrackName(trackName)
    if not _isValidTrack(genome, trackName):
        return

    print
    print 'Available extraction options for track "%s" of genome "%s":' % (':'.join(trackName), genome)
    print
    print '{:<19}'.format('fileFormatName') + '{:<17}'.format('allowOverlaps') + 'Description'
    print '-'*80

    from gtrackcore.extract.TrackExtractor import TrackExtractor
    for text, suffix in TrackExtractor.getTrackExtractionOptions(genome, trackName):
        fileFormatName, asOriginal, allowOverlaps = TrackExtractor.getAttrsFromExtractionFormat(text)
        print '{:<19}'.format(fileFormatName) + '{:<17}'.format(str(allowOverlaps)) + text

def _commonExportFile(outFileName, genome, trackName, fileFormatName, allowOverlaps, bins):
    trackName = _convertTrackName(trackName)
    if not _isValidTrack(genome, trackName):
        return

    outFileName = os.path.abspath(outFileName)

    from gtrackcore.extract.TrackExtractor import TrackExtractor
    TrackExtractor.extractOneTrackManyRegsToOneFile(trackName, bins, outFileName, fileFormatName=fileFormatName, \
                                                    globalCoords=True, asOriginal=False, \
                                                    allowOverlaps=allowOverlaps)

#TODO: Confirm docstring
def exportFile(outFileName, genome, trackName, fileFormatName, allowOverlaps):
    """ ?!
    Generate a textual genomic track from gtrackcore data.

    Paramters
    ---------
    outFileName : string
        Name of output textual genomic track.
    genome : string
        Genome id.
    trackName : string
       An id that uniquely represents a track. E.g. 'Genes and gene subsets:Genes:Refseq'. Each part of the
        trackName may be separated by ':', '^', or '|'.
    fileFormatName : string
        Textual file format of output (genomic track type). E.g. GTrack, GFF, BED, etc.
    allowOverlaps : bool
        ??

    """

    from gtrackcore.input.userbins.UserBinSource import UserBinSource
    bins = UserBinSource('*', '*', genome, includeExtraChrs=True)

    _commonExportFile(outFileName, genome, trackName, fileFormatName, allowOverlaps, bins)

#TODO: Confirm docstring
def exportFileInRegion(outFileName, genome, trackName, fileFormatName, allowOverlaps, region):
    """ ??
    Generate a textual genomic track from gtrackcore data in a specific region.

    Paramters
    ---------
    outFileName : string
        Name of output textual genomic track.
    genome : string
        Genome id.
    trackName : string
       An id that uniquely represents a track. E.g. 'Genes and gene subsets:Genes:Refseq'. Each part of the
        trackName may be separated by ':', '^', or '|'.
    fileFormatName : string
        Textual file format of output (genomic track type). E.g. GTrack, GFF, BED, etc.
    allowOverlaps : bool
        ??
    region : ??

"""

    from gtrackcore.input.userbins.UserBinSource import UserBinSource
    bins = UserBinSource(region, '*', genome, includeExtraChrs=True)

    _commonExportFile(outFileName, genome, trackName, fileFormatName, allowOverlaps, bins)


def getTrackData(genome, trackName, chr, allowOverlaps):
    trackName = _convertTrackName(trackName)
    if not _isValidTrack(genome, trackName):
        print 'There is no track %s for genome %s. Import it by using importFile()' % (trackName, genome)
        sys.exit(0)

    from gtrackcore.track.pytables.TrackSource import TrackSource
    trackSource = TrackSource()
    return trackSource.get_track_data(genome, trackName, allowOverlaps)


def getTrackElementCount(trackData):
    from gtrackcore.track.tools.TrackTools import countElements

    return countElements(trackData)

def getTracksIntersection(trackData1, trackData2):
    raise NotImplementedError


def _usage():
    print 'syntax: '
    print 'to use: [name] [args]'
    print 'available commands: '
    print ', '.join(funcList.keys())
    sys.exit(0)

if __name__ == "__main__":
    from collections import OrderedDict
    import types
    import sys

    profile = True
    thisModule = sys.modules[__name__]

    funcList = OrderedDict((a, thisModule.__dict__.get(a)) for a in sorted(dir(thisModule))
                if isinstance(thisModule.__dict__.get(a), types.FunctionType) and a[0] != '_')

    if len(sys.argv) == 1:
        _usage()
    else:
        assert( len(sys.argv) >= 2)
        if not sys.argv[1] in funcList:
            _usage()
        else:
            try:
                func = funcList[sys.argv[1]]
                func(*sys.argv[2:])
            except:
                print
                print 'usage: python Api.py ' + str(func.__name__) + ' ' + str(func.__doc__)
                print
                raise
