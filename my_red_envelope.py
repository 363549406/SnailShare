#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc


class RedEnvelopeFactory(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, activate_id):
        self.red_envelop = self._create_red_envelope(activate_id)

    @abc.abstractmethod
    def _create_red_envelope(self, activate_id):
        pass

    def receive(self, user_id):
        self.red_envelop.receive(user_id)


class CircleRedEnvelopeFactory(RedEnvelopeFactory):
    """生成周期性发放红包的活动"""

    def _create_red_envelope(self, activate_id):
        return CircleRedEnvelope(activate_id)


class NormalRedEnvelopeFactory(RedEnvelopeFactory):
    """能生成有过期时间的红包 的活动"""

    def _create_red_envelope(self, activate_id):
        pass


class RedEnvelope(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, activate_id):
        self._activate_id = activate_id

    @abc.abstractmethod
    def receive(self, user_id):
        pass


class CircleRedEnvelope(RedEnvelope):
    """周期性发放红包"""

    def __init__(self, activate_id):
        super(CircleRedEnvelope, self).__init__(activate_id)
        print 'create a {0} for activate {1}'.format(self.__class__.__name__, self._activate_id)

    def receive(self, user_id):
        print '{0} receive a {1}'.format(user_id, self.__class__.__name__)


class NormalRedEnvelope(RedEnvelope):
    """有过期时间的红包"""

    def receive(self, user_id):
        pass


def receive(user_id, activate_id):
    # 从数据库中查到activate_id的活动是：每周给用户发放一个双色球满200减2元红包
    factory = CircleRedEnvelopeFactory(activate_id)
    factory.receive(user_id)


if __name__ == '__main__':
    # 有用户领取额一个周期性红包
    receive(101, 202)