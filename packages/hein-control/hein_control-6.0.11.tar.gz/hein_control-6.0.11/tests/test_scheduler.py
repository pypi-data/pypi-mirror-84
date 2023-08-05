import time
import unittest
from hein_control import SamplingScheduler, ConfiguredAction


# logging.basicConfig(level=logging.INFO)


@ConfiguredAction
def sleepy(t):
    time.sleep(t)


@ConfiguredAction
def slow_step():
    sleepy(0.1)


@ConfiguredAction
def fast_step():
    sleepy(0.01)


class TestScheduler(unittest.TestCase):
    def test_timepoint_addition(self):
        """tests timepoint addition to a scheduler instance"""
        sched = SamplingScheduler('slow_step', fast_step)
        sched.insert_time_point(0.05, number_of_points=4)
        self.assertEqual(len(sched.time_points), 4)
        # todo
        #   - test relative insertion
        #   - test list insertion
        #   - test list pairs insertion

    def test_timepoint_naming(self):
        """tests naming order of timepoints"""
        sched = SamplingScheduler(fast_step)
        sched.insert_time_point(0.05, number_of_points=4)
        for ind, tp in enumerate(sched.time_points):
            self.assertEqual(
                tp.name,
                f'Time Point #{ind+1}',
                'checking automatic naming'
            )
        sched.insert_time_point(
            0.07,
            relative_to='start',
        )
        for ind, tp in enumerate(sched.time_points):
            self.assertEqual(
                tp.name,
                f'Time Point #{ind+1}',
                'checking automatic name update'
            )
        sched.insert_time_point(
            0.08,
            timepoint_name='manually named'
        )
        counter = 1
        # check that ordering of unnamed points is preserved
        for ind, tp in enumerate(sched.time_points):
            if ind == 2:
                self.assertEqual(
                    tp.name,
                    'manually named',
                    'check preservation of manual name'
                )
            else:
                self.assertEqual(
                    tp.name,
                    f'Time Point #{counter}',
                    'checking automatic name update'
                )
                counter += 1

        sched.insert_time_point(
            0.1,
            number_of_points=3,
            relative_to='previous',
            timepoint_name='test incremental point',
        )
        for ind, tp in enumerate(sched.time_points[-3:]):
            self.assertEqual(
                tp.name,
                f'test incremental point#{ind + 1}',
                'check increment of manual name'
            )

    def test_execution(self):
        """tests execution of the scheduler"""
        sched = SamplingScheduler(slow_step, 'fast_step')
        sched.insert_time_point(0.5, number_of_points=4)
        self.assertFalse(sched.started)
        sched.start_sequence()
        self.assertTrue(sched.started)
        self.assertFalse(sched.paused)
        sched.pause_sequence()
        self.assertTrue(sched.paused)
        sched.start_sequence()
        sched.join()
        self.assertFalse(sched.busy)

    def test_triggering(self):
        """tests manual triggering of a scheduler"""
        sched = SamplingScheduler('fast_step')
        sched.trigger()
        self.assertIsNotNone(sched.last_triggered_time_point)
        sched.wait_for_time_point_completion()

    def test_retrieval(self):
        """tests value retrieval from a scheduler"""
        sched = SamplingScheduler('fast_step')
        sched.insert_time_point(0.)
        self.assertIsNone(sched.last_triggered_time_point)
        sched.start_sequence()
        sched.join()
        self.assertIsNotNone(sched.last_triggered_time_point)
        sched.as_dict()

    def test_too_fast(self):
        """tests what happens when time points are executed too fast"""
        sched = SamplingScheduler('slow_step', fast_step)
        sched.insert_time_point(0.001, number_of_points=4)
        sched.start_sequence()
        sched.trigger()
        sched.join()

    def test_duplicate_naming(self):
        """tests catch and acceptance of duplicate configuration names"""
        prev_name = ''
        for i in range(10):
            sched = SamplingScheduler(
                sequence_name='convenience name'
            )
            self.assertNotEqual(prev_name, sched.sequence.name)
            prev_name = sched.sequence_name

    # def test_slow_spoolup(self):
    #     """tests handling of ActionTimePoint spool up situations"""
    #     # todo figure out how to test slow spool up situations (execution iteration is faster than _triggered set)
    #     sched = SamplingScheduler(fast_step)
    #     sched.insert_time_point(0.)
    #     tp = sched.time_points[0]
    #     tp._executor = slow_spool_executor
    #     sched.start_sequence()
    #     tp._triggered = True
    #     sched.join()

    # def test_addition_actions(self):  # todo
    #     pass

    # def test_action_override(self):  # todo
    #     pass
