# -*- coding: utf-8 -*-
# !/usr/bin/env python
# coding=utf-8

"""This module implements the basic Mondrian algorithm.
"""

from .models.numrange import NumRange


class Partition(object):

    """Class for Group, which is used to keep records
    Store tree node in instances.
    self.member: records in group
    self.width: width of this partition on each domain. For categoric attribute, it equal
    the number of leaf node, for numeric attribute, it equal to number range
    self.middle: save the generalization result of this partition
    self.allow: 0 donate that not allow to split, 1 donate can be split
    """

    def __init__(self, data, width, middle, qi_len):
        """
        initialize with data, width and middle
        """
        self.member = list(data)
        self.width = list(width)
        self.middle = list(middle)
        self.allow = [1] * qi_len

    def __len__(self):
        """
        return the number of records in partition
        """
        return len(self.member)


class BasicMondrian:
    """Basic Mondrian for k-anonymity.

    This function supports both numeric values and categoric values.

    For numeric values, each iterator is a mean split.
    For categoric values, each iterator is a split on GH.

    Args:
        att_trees (): the taxonomic tree.
        data (): the data to anonymise.
        k (int): the k-value.
        QI_num (int): the number of quasi-identifiers.
    """

    def __init__(self, att_trees, data, k, qi_num=-1):
        self.working = []
        self.qi_range = []
        self.is_cat = []
        self.att_trees = att_trees
        self.data = data
        self.k = k
        self.results = None

        for t in self.att_trees:
            if isinstance(t, NumRange):
                self.is_cat.append(False)
            else:
                self.is_cat.append(True)

        if qi_num <= 0:
            self.qi_len = len(data[0]) - 1
        else:
            self.qi_len = qi_num

    def get_normalized_width(self, partition, index):
        """Returns the normalized width of partition, similar to NCP.
        """
        if self.is_cat[index] is False:
            low = partition.width[index][0]
            high = partition.width[index][1]
            width = (float(self.att_trees[index].sort_value[high]) -
                     float(self.att_trees[index].sort_value[low]))
        else:
            width = partition.width[index]

        divisor = self.qi_range[index]
        if divisor == 0:
            return 0

        return width * 1.0 / self.qi_range[index]

    def choose_dimension(self, partition):
        """Choose the dim with the largest normalized width.

        Returns:
            int: the dim index.
        """
        max_width = -1
        max_dim = -1

        for i in range(self.qi_len):
            if partition.allow[i] == 0:
                continue
            norm_width = self.get_normalized_width(partition, i)
            if norm_width > max_width:
                max_width = norm_width
                max_dim = i

        assert max_width <= 1, 'Error: max_width > 1'
        assert max_dim != -1, 'cannot find the max dim'

        return max_dim

    def frequency_set(self, partition, dim):
        """Get the frequency_set of partition on dim.

        Returns:
            dict{key: str values, values: count}
        """
        frequency = {}

        for record in partition.member:
            try:
                frequency[record[dim]] += 1
            except KeyError:
                frequency[record[dim]] = 1

        return frequency

    def find_median(self, partition, dim):
        """Find the middle of the partition.

        Returns:
            split_val
        """
        frequency = self.frequency_set(partition, dim)
        split_val = ''
        value_list = sorted(frequency.keys(), key=int)

        total = sum(frequency.values())
        middle = total / 2

        if middle < self.k or len(value_list) <= 1:
            return ('', '', value_list[0], value_list[-1])

        index = 0
        split_index = 0

        for i, t in enumerate(value_list):
            index += frequency[t]
            if index >= middle:
                split_val = t
                split_index = i
                break
        else:
            raise Exception('Error: cannot find split_val')

        try:
            next_val = value_list[split_index + 1]
        except IndexError:
            next_val = split_val

        return (split_val, next_val, value_list[0], value_list[-1])

    def split_numerical_value(self, numeric_value, split_val):
        """Split numeric value on split_val.

        Returns:
            sub ranges
        """
        split_num = numeric_value.split(',')
        if len(split_num) <= 1:
            return split_num[0], split_num[0]
        else:
            low = split_num[0]
            high = split_num[1]
            # Fix 2,2 problem
            if low == split_val:
                lvalue = low
            else:
                lvalue = low + ',' + split_val
            if high == split_val:
                rvalue = high
            else:
                rvalue = split_val + ',' + high
            return lvalue, rvalue

    def split_numerical(self, partition, dim, pwidth, pmiddle):
        """Strict split numeric attribute by finding a median.

        lhs = [low, means], rhs = (mean, high]
        """
        sub_partitions = []

        # numeric attributes
        (split_val, next_val, low, high) = self.find_median(partition, dim)
        p_low = self.att_trees[dim].dict[low]
        p_high = self.att_trees[dim].dict[high]

        # update middle
        if low == high:
            pmiddle[dim] = low
        else:
            pmiddle[dim] = low + ',' + high
        pwidth[dim] = (p_low, p_high)

        if split_val == '' or split_val == next_val:
            # update middle
            return []

        middle_pos = self.att_trees[dim].dict[split_val]
        lmiddle = pmiddle[:]
        rmiddle = pmiddle[:]
        lmiddle[dim], rmiddle[dim] = self.split_numerical_value(pmiddle[dim], split_val)
        lhs = []
        rhs = []

        for temp in partition.member:
            pos = self.att_trees[dim].dict[temp[dim]]
            if pos <= middle_pos:
                # lhs = [low, means]
                lhs.append(temp)
            else:
                # rhs = (mean, high]
                rhs.append(temp)
        lwidth = pwidth[:]
        rwidth = pwidth[:]
        lwidth[dim] = (pwidth[dim][0], middle_pos)
        rwidth[dim] = (self.att_trees[dim].dict[next_val], pwidth[dim][1])
        sub_partitions.append(Partition(lhs, lwidth, lmiddle, self.qi_len))
        sub_partitions.append(Partition(rhs, rwidth, rmiddle, self.qi_len))
        return sub_partitions

    def split_categorical(self, partition, dim, pwidth, pmiddle):
        """Split categorical attribute using generalization hierarchy.
        """
        sub_partitions = []

        # categoric attributes
        split_val = self.att_trees[dim][partition.middle[dim]]
        sub_node = [t for t in split_val.child]
        sub_groups = []

        for i in range(len(sub_node)):
            sub_groups.append([])
        if len(sub_groups) == 0:
            # split is not necessary
            return []

        for temp in partition.member:
            qid_value = temp[dim]
            for i, node in enumerate(sub_node):
                try:
                    node.cover[qid_value]
                    sub_groups[i].append(temp)
                    break
                except KeyError:
                    continue
            else:
                raise Exception('Category "%s" unknown.' % qid_value)

        flag = True
        for index, sub_group in enumerate(sub_groups):
            if len(sub_group) == 0:
                continue
            if len(sub_group) < self.k:
                flag = False
                break

        if flag:
            for i, sub_group in enumerate(sub_groups):
                if len(sub_group) == 0:
                    continue
                wtemp = pwidth[:]
                mtemp = pmiddle[:]
                wtemp[dim] = len(sub_node[i])
                mtemp[dim] = sub_node[i].value
                sub_partitions.append(Partition(sub_group, wtemp, mtemp, self.qi_len))

        return sub_partitions

    def split_partition(self, partition, dim):
        """Split partition and distribute records to different sub-partitions.
        """
        pwidth = partition.width
        pmiddle = partition.middle

        if self.is_cat[dim] is False:
            return self.split_numerical(partition, dim, pwidth, pmiddle)
        else:
            return self.split_categorical(partition, dim, pwidth, pmiddle)

    def anonymize(self, partition):
        """Main procedure of Half_Partition.

        Recursively partition groups until not allowable.
        """
        if self.check_splitable(partition) is False:
            self.working.append(partition)
            return

        # Choose dim
        dim = self.choose_dimension(partition)

        assert dim != -1, 'Error: dim=-1'

        sub_partitions = self.split_partition(partition, dim)

        if len(sub_partitions) == 0:
            partition.allow[dim] = 0
            self.anonymize(partition)
        else:
            for sub_p in sub_partitions:
                self.anonymize(sub_p)

    def check_splitable(self, partition):
        """Check if the partition can be further split while satisfying k-anonymity.
        """
        temp = sum(partition.allow)
        if temp == 0:
            return False
        return True

    def mondrian(self):
        """Runs the Basic Mondrian routine.

        Returns:
            (result, ncp): Returns the results in a 2-dimensional list and the normalized certainty
            penalty.
        """

        if self.results is not None:
            return self.results

        result = []
        middle = []
        wtemp = []

        for i in range(self.qi_len):
            if self.is_cat[i] is False:
                self.qi_range.append(self.att_trees[i].range)
                wtemp.append((0, len(self.att_trees[i].sort_value) - 1))
                middle.append(self.att_trees[i].value)
            else:
                self.qi_range.append(len(self.att_trees[i]['*']))
                wtemp.append(len(self.att_trees[i]['*']))
                middle.append('*')

        whole_partition = Partition(self.data, wtemp, middle, self.qi_len)
        self.anonymize(whole_partition)
        ncp = 0.0

        for partition in self.working:
            r_ncp = 0.0
            for i in range(self.qi_len):
                r_ncp += self.get_normalized_width(partition, i)
            temp = partition.middle
            for i in range(len(partition)):
                result.append(temp + partition.member[i][self.qi_len:])
            r_ncp *= len(partition)
            ncp += r_ncp

        # Make NCP a percentage
        ncp /= self.qi_len
        ncp /= len(self.data)
        ncp *= 100

        assert len(result) == len(self.data), 'Records were lost during anonymization.'
        self.results = (result, ncp)

        return self.results
