#!/usr/bin/env Python
# -*- coding: utf-8 -*-

import json
# import xmltodict

"""
Abstract Factory Design Pattern

Requirements:
  有两个出票供应商，分别叫做HYLott和JoyLott
  其中HYLott只能出双色球的票，JoyLott只能出福彩3D的票
  以后我们还可能加更多的出票商来出其他彩种的票
  并且我们知道不同出票商有各自定义彩票的数据结构、存储方式（如json串或xml格式）

"""

def order(supplier, lottery, number_list):
    lottery_order = supplier.make_order(lottery, number_list)
    print supplier.order(lottery_order)


class AbstractTicketSupplier(object):
    def make_order(self, lottery, number_list):
        raise NotImplementedError

    def order(self, lottery_order):
        raise NotImplementedError

class HYLott(AbstractTicketSupplier):
    """暂时只能出shuangseqiu"""
    def make_order(self, lottery, number_list):
        """把不同group的分开，放在不同的list中"""
        return [number_list[:5], [number_list[-1]]]

    def order(self, lottery_order):
        return json.dumps(lottery_order)

class JoyLott(AbstractTicketSupplier):
    """暂时只能出fucai3d"""
    def make_order(self, lottery, number_list):
        return {
            'g1': number_list[0],
            'g2': number_list[1],
            'g3': number_list[2]
        }

    def order(self, lottery_order):
        # return xmltodict.parse(lottery_order)
        return lottery_order


def main():
    # shuangseqiu order
    order(HYLott(), 'shuangseqiu', [1, 2, 3, 4, 5, 6, 7])
    # fucai3d order
    order(JoyLott(), 'fucai3d', [1, 1, 1])

if __name__ == '__main__':
    main()
