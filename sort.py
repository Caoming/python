#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import sys

sorts = [1, 8, 9, 23, 54, 123, 45, 23, 4, 6]
print(len(sorts))
n = len(sorts)

# 冒泡排序


def bubbleSort(arr):
    for i in range(n):
        for j in range(i, n):
            if(arr[i] > arr[j]):
                temp = arr[j]
                arr[j] = arr[i]
                arr[i] = temp

# 插入排序


def insertionSort(arr):
    for i in range(n):
        index = i
        for j in range(i):
            --index
            if(arr[i] < arr[index]):
                temp = arr[i]
                arr[i] = arr[index]
                arr[index] = temp

# 选择排序


def selectionSort(arr):
    for i in range(n):
        for j in range(n - i - 1):
            if(arr[n - j] > arr[n - j - 1]):
                arr[i] = arr[n - j - 1]

# 归并算法的合并


def merge(arr, p1, r1, p2, r2):
    temp = np.empty(len(arr))
    i=0
    j=0
    z = 0
    while(i <= (r1 - p1) and j <= (r2 - p2)):
        if(arr[i] < arr[j]):
            temp[z] = arr[i]
            i += 1
        else:
            temp[z] = arr[j]
            j += 1

        z += 1

    # 多余的复制过去
    if(i == r1 - p1):
        for k in range(r2 - p2 - j):
            temp[z] = arr[j]
            j += 1
            z += 1
    if(j == r2 - p2):
        for k in range(r1 - p1 - i):
            temp[z] = arr[i]
            i += 1
            z += 1
    for k in range(r2 - p1):
        arr[p1 + k] = temp[k]


# 归并排序
def mergeSort(arr, p, r):
    # 递归终止条件
    if(p >= r):
        return

    q = (p + r) // 2
    mergeSort(arr, p, q)
    mergeSort(arr, q + 1, r)

    # 合并算法
    merge(arr, p, q, q + 1, r)


print("归并排序")
sorts = [1, 8, 9, 23, 54, 123, 45, 23, 4, 6]
print("插入排序后的数据为")
mergeSort(sorts, 0, 10)
for i in range(n):
    print("%d" % sorts[i])

print("冒泡排序后的数据为")

bubbleSort(sorts)
for i in range(n):
    print("%d" % sorts[i])

sorts = [1, 8, 9, 23, 54, 123, 45, 23, 4, 6]
print("插入排序后的数据为")
bubbleSort(sorts)
for i in range(n):
    print("%d" % sorts[i])

sorts = [1, 8, 9, 23, 54, 123, 45, 23, 4, 6]
print("选择排序后的数据为")
bubbleSort(sorts)
for i in range(n):
    print("%d" % sorts[i])
