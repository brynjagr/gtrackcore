import os
import unittest
import itertools

from gtrackcore.core.LogSetup import logMessage
from gtrackcore.preprocess.PreProcessTracksJob import PreProcessAllTracksJob
from gtrackcore.tools.TrackOperations import coverage, overlap, overlap_iter, count_elements, \
    count_elements_in_all_bounding_regions, sum_of_values, sum_of_weights, sum_of_weights_iter
from gtrackcore.track.core.GenomeRegion import GenomeRegion
from gtrackcore.util.CommonFunctions import createOrigPath


class TestTrackTools(unittest.TestCase):
    def setUp(self):
        for track_data in all_test_track_data.values():
            self._write_original_file(track_data)
            try:
                PreProcessAllTracksJob(track_data['genome'], track_data['track_name']).process()
            except Exception:
                logMessage('Could not preprocess %s (%s)' % (':'.join(track_data['track_name']), track_data['genome']))

    def tearDown(self):
        pass

    @staticmethod
    def _write_original_file(track_data):
        dir_path = createOrigPath(track_data['genome'], track_data['track_name'])
        filename = dir_path + os.sep + 'file.gtrack'
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(filename, mode='w') as f:
            for line in itertools.chain(track_data['headers'], track_data['data']):
                f.write(line + '\n')

    def test_overlap(self):
        track_data1 = all_test_track_data['segment1']
        track_data2 = all_test_track_data['segment2']
        result = overlap(track_data1['track_name'], False,
                         track_data2['track_name'], False, track_data1['genome_regions'])
        result_should_be = 200

        self.assertEqual(result, result_should_be, msg='overlap result was %d, but should be %d for track %s and %s' %
                                                       (result, result_should_be, ':'.join(track_data1['track_name']),
                                                        ':'.join(track_data2['track_name'])))

    def test_overlap_with_iterator(self):
        track_data1 = all_test_track_data['segment1']
        track_data2 = all_test_track_data['segment2']
        result = overlap_iter(track_data1['track_name'], False,
                              track_data2['track_name'], False, track_data1['genome_regions'])
        result_should_be = 200

        self.assertEqual(result, result_should_be, msg='overlap iter result was %d, but should be %d for track %s and %s'
                                                       % (result, result_should_be, ':'.join(track_data1['track_name']),
                                                          ':'.join(track_data2['track_name'])))

    def test_coverage(self):
        track_data = all_test_track_data['segment1']
        result = coverage(track_data['track_name'], False, track_data['genome_regions'])
        result_should_be = 250

        self.assertEqual(result, result_should_be, msg='coverage result was %d, but should be %d for track %s' %
                                                       (result, result_should_be, ':'.join(track_data['track_name'])))

    def test_count_elements(self):
        track_data = all_test_track_data['genome_partition1']
        result = count_elements(track_data['track_name'], False, track_data['genome_regions'])
        result_should_be = 5

        self.assertEqual(result, result_should_be, msg='element count result was %d, but should be %d for track %s' %
                                                       (result, result_should_be, ':'.join(track_data['track_name'])))

    def test_count_elements_in_all_bounding_regions(self):
        track_data = all_test_track_data['genome_partition1']
        result = count_elements_in_all_bounding_regions(track_data['genome'], track_data['track_name'], False)
        result_should_be = 5

        self.assertEqual(result, result_should_be, msg='element count in all bounding regions result was %d, but should'
                                                       ' be %d for track %s' % (result, result_should_be,
                                                                                ':'.join(track_data['track_name'])))

    def test_sum_of_values(self):
        track_data = all_test_track_data['function1']
        result = sum_of_values(track_data['track_name'], False, track_data['genome_regions'])
        result_should_be = 18.0

        self.assertAlmostEqual(result, result_should_be, msg='sum of values result was %f, but should be %f for track'
                                                             ' %s' % (result, result_should_be,
                                                                      ':'.join(track_data['track_name'])), places=2)

        track_data = all_test_track_data['valued_segment1']
        result = sum_of_values(track_data['track_name'], True, track_data['genome_regions'])
        result_should_be = 400.4

        self.assertAlmostEqual(result, result_should_be, msg='sum of values result was %f, but should be %f for track '
                                                             '%s' % (result, result_should_be,
                                                                     ':'.join(track_data['track_name'])), places=2)

    def test_sum_of_weights(self):
        track_data = all_test_track_data['linked_segments1']
        result = sum_of_weights(track_data['track_name'], True, track_data['genome_regions'])
        result_should_be = 23.1

        self.assertAlmostEqual(result, result_should_be, msg='sum of values result was %f, but should be %f for track '
                                                             '%s' % (result, result_should_be,
                                                                     ':'.join(track_data['track_name'])), places=2)

    def test_sum_of_weights_with_iterator(self):
        track_data = all_test_track_data['linked_segments1']
        result = sum_of_weights_iter(track_data['track_name'], True, track_data['genome_regions'])
        result_should_be = 23.1

        self.assertAlmostEqual(result, result_should_be, msg='sum of values result was %f, but should be %f for track '
                                                             '%s' % (result, result_should_be,
                                                                     ':'.join(track_data['track_name'])), places=2)

all_test_track_data = {
    'segment1': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'segment1'],
        'headers': [
            '##track type: segments',
            '\t'.join(['###seqid', 'start', 'end']),
        ],
        'data': [
            '\t'.join(map(str, ['chr21', 100, 200])),
            '\t'.join(map(str, ['chr21', 150, 250])),
            '\t'.join(map(str, ['chr21', 200, 250])),
            '\t'.join(map(str, ['chrM', 100, 200])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 46944323),
            GenomeRegion('testgenome', 'chrM', 0, 16571),
        ]
    },
    'segment2': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'segment2'],
        'headers': [
            '##track type: segments',
            '\t'.join(['###seqid', 'start', 'end']),
        ],
        'data': [
            '\t'.join(map(str, ['chr21', 150, 250])),
            '\t'.join(map(str, ['chrM', 0, 200])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 46944323),
            GenomeRegion('testgenome', 'chrM', 0, 16571),
        ]
    },
    'valued_segment1': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'valued_segment1'],
        'headers': [
            '##track type: valued segments',
            '\t'.join(['###seqid', 'start', 'end', 'value']),
        ],
        'data': [
            '\t'.join(map(str, ['chr21', 100, 200, 100.1])),
            '\t'.join(map(str, ['chr21', 110, 200, 100.1])),
            '\t'.join(map(str, ['chr21', 120, 200, 100.1])),
            '\t'.join(map(str, ['chrM', 100, 200, 100.1])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 46944323),
            GenomeRegion('testgenome', 'chrM', 0, 16571),
        ]
    },
    'linked_segments1': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'linked_segments1'],
        'headers': [
            '##track type: linked segments',
            '##edge weight type: number',
            '##edge weight dimension: scalar',
            '##edge weights: true',
            '\t'.join(['###seqid', 'start', 'end', 'id', 'edges']),
        ],
        'data': [
            '\t'.join(map(str, ['chr21', 100, 200, 'a', 'b=1.1'])),
            '\t'.join(map(str, ['chr21', 150, 250, 'b', 'a=2.2;c=3.3'])),
            '\t'.join(map(str, ['chr21', 200, 250, 'c', 'a=4.4;d=5.5'])),
            '\t'.join(map(str, ['chrM', 100, 200, 'd', 'c=6.6'])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 46944323),
            GenomeRegion('testgenome', 'chrM', 0, 16571),
        ]
    },
    'genome_partition1': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'genome_partition1'],
        'headers': [
            '##track type: genome partition',
            '\t'.join(['###end']),
        ],
        'data': [
            '####seqid=chr21; start=0;  end=1000',
            '\t'.join(map(str, [250])),
            '\t'.join(map(str, [500])),
            '\t'.join(map(str, [750])),
            '\t'.join(map(str, [1000])),
            '####seqid=chrM; start=0;  end=200',
            '\t'.join(map(str, [200])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 1000),
            GenomeRegion('testgenome', 'chrM', 0, 200),
        ]
    },
    'function1': {
        'genome': 'testgenome',
        'track_name': ['integration_test_data', 'tools', 'function1'],
        'headers': [
            '##track type: function',
            '\t'.join(['###value']),
        ],
        'data': [
            '####genome=testgenome; seqid=chr21; start=0; end=5',
            '\t'.join(map(str, [1.0])),
            '\t'.join(map(str, [2.0])),
            '\t'.join(map(str, [3.0])),
            '\t'.join(map(str, [4.0])),
            '\t'.join(map(str, [5.0])),
            '####genome=testgenome; seqid=chrM; start=0; end=2',
            '\t'.join(map(str, [1.0])),
            '\t'.join(map(str, [2.0])),
        ],
        'genome_regions': [
            GenomeRegion('testgenome', 'chr21', 0, 5),
            GenomeRegion('testgenome', 'chrM', 0, 2),
        ]
    },
}


if __name__ == "__main__":
    unittest.main()
