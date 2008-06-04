#!/usr/bin/env python

# path manuiplation to include the directory above
import sys
sys.path.append('..')

import unittest
import operator
import datetime

import eventCalBase

class testMonthCalendar(unittest.TestCase):
    def setUp(self):
        self.emsg = 'Expect %s, got %s'
        self.now = datetime.datetime.now()
        self.cal = eventCalBase.monthCalendar(1, 'someone', self.now.year, 
                self.now.month)

    def testGetDate(self):
        """Test getDate()"""
        day = 9
        expect = datetime.date(self.now.year, self.now.month, day)
        got = self.cal.getDate(day)
        self.failUnlessEqual(expect, got, self.emsg % (expect, got))
        
    def testAddEvent(self):
        """Test addEvent()"""
        fixdate = datetime.datetime(2007,6,20,12,30,0)
        event = eventCalBase.event(1, 'test', fixdate)
        self.cal.addEvent(event, fixdate.day)

        expectdate = self.cal.getDate(fixdate.day)
        event.setStart(datetime.datetime.combine(expectdate, fixdate.time()))
        expect = [event]
        got = self.cal.getDailyEvents(fixdate.day)
        self.failUnlessEqual(expect, got, self.emsg % (expect, got))

    def testGetEvents_multipleEvents(self):
        """Test getEvents()"""
        now = datetime.datetime.now()
        event = eventCalBase.event(1, 'test', now)
        for c in xrange(3):
            self.cal.addEvent(event, now.day)

        expect = self.cal.events[now.day]
        got = self.cal.getEvents(now.day, now.time().replace(microsecond=0))
        self.failUnlessEqual(expect, got, self.emsg % (expect, got))

    def testDelEvent(self):
        """Test delEvent()"""
        daylist = [1,2,20]
        timelist = [datetime.time(12,30,0),
                    datetime.time(13, 0,0),
                    datetime.time(14,45,0),]
        # add event
        id = 1
        for d in daylist:
            for t in timelist:
                date = datetime.date(self.now.year, self.now.month, d)
                dt = datetime.datetime.combine(date, t)
                event = eventCalBase.event(id, 'test', dt)
                self.cal.addEvent(event, d)
                id += 1
        # get event (before delete)
        before = []
        for d in daylist:
            before.append(self.cal.getDailyEvents(d))
        # del event and compare output
        for d, b in zip(daylist, before):
            b.pop(1)
            self.cal.delEvent(d, timelist[1])
            expect = b
            got = self.cal.getDailyEvents(d)
            self.failUnlessEqual(expect, got, self.emsg % (expect, got))


class testEvent(unittest.TestCase):
    def setUp(self):
        self.eDatetime = datetime.datetime.now()
        self.e = eventCalBase.event(1, 'event', self.eDatetime, 'some event')
    
    def testEqual(self):
        """Test ==operator"""
        _other = eventCalBase.event(1, 'event', self.eDatetime,)
        self.failUnlessEqual(self.e, _other,
                'a1 == a2 failed.  a1=%s, a2=%s' % (self.e, _other))

    def testLessThan(self):
        """Test <operator"""
        _dt = self.eDatetime + datetime.timedelta(1)
        _other = eventCalBase.event(2, 'event', _dt)
        self.failUnless(operator.lt(self.e, _other),
                'a1 < a2 failed.  a1=%s, a2=%s' % (self.e, _other))
        self.failIf(operator.lt(_other, _other),
                'a1 < a2 failed.  a1=%s, a2=%s' % (_other, _other))

    def testLessThanEqual(self):
        """Test <=operator"""
        _dt = self.eDatetime + datetime.timedelta(1)
        _other = eventCalBase.event(2, 'event', _dt)
        self.failUnless(operator.le(self.e, _other),
                'a1 <= a2 failed.  a1=%s, a2=%s' % (self.e, _other))
        self.failUnless(operator.le(_other, _other),
                'a1 <= a2 failed.  a1=%s, a2=%s' % (_other, _other))

    def testGreaterThan(self):
        """Test >operator"""
        _dt = self.eDatetime - datetime.timedelta(1)
        _other = eventCalBase.event(2, 'event', _dt)
        self.failUnless(operator.gt(self.e, _other),
                'a1 > a2 failed.  a1=%s, a2=%s' % (self.e, _other))
        self.failIf(operator.gt(_other, _other),
                'a1 > a2 failed.  a1=%s, a2=%s' % (_other, _other))

    def testGreaterThanEqual(self):
        """Test >=operator"""
        _dt = self.eDatetime - datetime.timedelta(1)
        _other = eventCalBase.event(2, 'event', _dt)
        self.failUnless(operator.ge(self.e, _other),
                'a1 => a2 failed.  a1=%s, a2=%s' % (self.e, _other))
        self.failUnless(operator.ge(_other, _other),
                'a1 => a2 failed.  a1=%s, a2=%s' % (_other, _other))

    def testNotEqual(self):
        """Test !=operator"""
        _dt = self.eDatetime - datetime.timedelta(1)
        _other = eventCalBase.event(2, 'event', _dt)
        self.failUnless(operator.ne(self.e, _other),
                'a1 != a2 failed.  a1=%s, a2=%s' % (self.e, _other))
        self.failIf(operator.ne(_other, _other),
                'a1 != a2 failed.  a1=%s, a2=%s' % (_other, _other))

    def testPassDue(self):
        """Test passDue()"""
        _future = self.eDatetime + datetime.timedelta(1)
        _past = self.eDatetime - datetime.timedelta(1)
        self.failUnless(self.e.passDue(_future),
                'Expect passDue(%s) of %s to be True' % (_future, self.e))
        self.failIf(self.e.passDue(_past),
                'Expect passDue(%s) of %s to be False' % (_past, self.e))
        self.failIf(self.e.passDue(self.eDatetime),
                'Expect passDue(%s) of %s to be False' % (
                self.eDatetime, self.e))

    def testStart(self):
        """test setStart()"""
        emsg = 'Expect %s, got %s'
        f = datetime.datetime
        expect = f.combine(datetime.date(2007,5,26), f.now().time())
        self.e.setStart(expect)
        self.failUnlessEqual(expect, self.e.start, 
                emsg % (expect, self.e.start))

if __name__ == '__main__':
    unittest.main()


